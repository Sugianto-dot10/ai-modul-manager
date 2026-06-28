import os
import shutil
import re
import threading
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pyngrok import ngrok
from sentence_transformers import SentenceTransformer
import chromadb
from pypdf import PdfReader

# 1. Setup FastAPI & Database
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Load model AI (hanya perlu sekali di awal)
encoder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
db_client = chromadb.Client()
collection = db_client.get_or_create_collection(name="arsip_modul_pintar")

# 2. Fungsi Ekstraksi Metadata yang Tangguh
def parse_identitas(text):
    # Pembersihan karakter sampah hasil OCR
    text_bersih = re.sub(r'[\"\'\r\n]+', ' ', text)
    
    pola = {
        "nama_modul": r"(?:Judul|Modul Ajar)\s*:\s*([^,]+)",
        "kelas": r"(?:Fase/Kelas)\s*:\s*([^,]+)"
    }
    
    meta = {}
    for k, p in pola.items():
        match = re.search(p, text_bersih, re.IGNORECASE)
        meta[k] = match.group(1).strip() if match else "Umum"
        
    # Folder otomatis ringkas & aman (hanya alfanumerik)
    meta['kelas'] = re.sub(r'[^a-zA-Z0-9]', '', meta['kelas'])[:6] 
    return meta

# 3. Endpoint Upload
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
    
    # Ekstraksi Teks
    text = ""
    try:
        reader = PdfReader(temp_path)
        for page in reader.pages: text += page.extract_text() or ""
    except: pass
    
    meta = parse_identitas(text)
    folder = os.path.join("storage", meta['kelas'])
    os.makedirs(folder, exist_ok=True)
    shutil.move(temp_path, os.path.join(folder, file.filename))
    
    # Simpan ke Database Vektor
    collection.add(
        ids=[file.filename], 
        embeddings=[encoder.encode(text).tolist()], 
        metadatas=[meta], 
        documents=[text]
    )
    return {"pesan": f"Tersimpan di folder: {meta['kelas']}"}

# 4. Endpoint Pencarian dengan Logika Fallback
@app.get("/search")
async def search(query: str):
    query_vector = encoder.encode(query).tolist()
    res = collection.query(query_embeddings=[query_vector], n_results=5)
    
    output = []
    if res['metadatas'] and len(res['metadatas'][0]) > 0:
        # KITA TAMBAHKAN 'res['ids'][0]' UNTUK MENARIK NAMA FILE ASLI
        for doc_id, meta, dist in zip(res['ids'][0], res['metadatas'][0], res['distances'][0]):
            
            print(f"DEBUG -> ID File: {doc_id} | Skor Jarak: {dist:.3f}")
            
            output.append({
                "nama_file": doc_id, # <-- MENGAMBIL LANGSUNG DARI ID DATABASE (100% AKURAT)
                "kelas": meta.get("kelas", "Umum")
            })
            
    return {"hasil": output}

# 5. Endpoint View
@app.get("/view")
async def view_file(nama_file: str):
    # Cari metadata berdasarkan nama file
    res = collection.get(ids=[nama_file])
    if not res['metadatas']: raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    
    folder = res['metadatas'][0]['kelas']
    path = os.path.join("storage", folder, nama_file)
    return FileResponse(path) if os.path.exists(path) else HTTPException(404)

# 6. Jalankan server (Ganti token Anda di bawah!)
ngrok.set_auth_token("tokenngrok")
public_url = ngrok.connect(8000).public_url
print(f"URL API: {public_url}")
threading.Thread(target=lambda: uvicorn.run(app, port=8000), daemon=True).start()
