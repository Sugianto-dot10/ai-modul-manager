🧠 AI Modul Manager: Semantic Search & Auto-Classification

Proyek ini adalah implementasi terapan dari Natural Language Processing (NLP) dan Computer Vision (CV) untuk memecahkan masalah manajemen arsip di dunia pendidikan (khususnya Modul Ajar Kurikulum Merdeka).

Sistem ini mengubah cara pencarian tradisional yang kaku (lexical search) menjadi pencarian cerdas berbasis makna (semantic search), serta mengotomatisasi klasifikasi dokumen fisik ke dalam folder digital.

✨ Fitur Utama

Ingesti Dokumen Otomatis (Computer Vision / OCR)
Mengekstrak teks dari dokumen PDF atau hasil scan modul ajar secara otomatis.

Information Extraction (RegEx)
Membersihkan "teks kotor" hasil ekstraksi dan menarik metadata kunci (seperti Fase/Kelas dan Mata Pelajaran) untuk membuat ID Folder secara dinamis.

Pencarian Semantik (Semantic Search)
Mencari dokumen tidak berdasarkan kecocokan huruf (seperti Ctrl+F), melainkan berdasarkan kedekatan makna/konteks. (Contoh: Mencari "internet" akan memunculkan modul "Jaringan Komputer").

Dashboard Interaktif
Antarmuka web (SPA) modern berbasis Tailwind CSS yang responsif dan mudah digunakan oleh guru/admin.

🛠️ Arsitektur & Teknologi

Proyek ini menggunakan arsitektur Client-Server yang dipisahkan secara hybrid:

Frontend (Lokal/Web Server): * HTML5, Vanilla JavaScript.

Tailwind CSS (Styling & UI responsif).

Chart.js (Visualisasi edukatif Cosine Similarity).

Backend (Google Colab / Cloud):

Framework API: FastAPI & Uvicorn.

Tunneling: Ngrok (Menjembatani Colab ke Frontend publik).

Database Vektor: ChromaDB (In-memory Vector Database).

AI / NLP Model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (Model embedding multibahasa yang sangat efisien).

Ekstraksi PDF: pypdf / EasyOCR.

⚙️ Alur Kerja Sistem (Workflow)

Upload: User mengunggah file .pdf via Web UI.

Ekstraksi & Regex: Backend membaca teks dan mencari pola metadata (misal: "Kelas: F/11 TKJ"). Sistem memotong dan menormalisasi teks tersebut menjadi nama folder (F11TKJ).

Vectorization: Teks utuh diubah menjadi representasi matematika (384-dimensi Dense Vector) menggunakan model Transformer.

Penyimpanan: Vektor dan metadata disimpan ke dalam collection di ChromaDB.

Penelusuran (Kueri): Saat user mencari kata kunci, kueri diubah menjadi vektor. Sistem menghitung Cosine Similarity antara kueri dan seluruh dokumen di database untuk memunculkan Top-5 hasil terdekat.

🚀 Cara Menjalankan Proyek (Setup)

Karena proyek ini memanfaatkan GPU/RAM besar secara gratis dari Google Colab untuk pemrosesan AI, ikuti langkah berikut:

1. Setup Backend (Google Colab)

Buka file notebook backend_nlp_modul.ipynb di Google Colab.

Pastikan Anda memiliki akun Ngrok untuk mendapatkan Auth Token.

Masukkan Auth Token Ngrok Anda pada variabel NGROK_AUTH_TOKEN di dalam sel kode.

Jalankan semua sel (Run All).

Pada output sel terakhir, Anda akan mendapatkan URL Publik (contoh: https://abcd-1234.ngrok-free.app). Salin URL ini.

2. Setup Frontend (Lokal)

Buka file index.html (atau dashboard_nlp.html) menggunakan code editor (seperti VS Code).

Cari variabel URL_API di dalam tag <script>.

Ganti nilainya dengan URL Ngrok yang baru saja Anda salin:

const URL_API = "[https://abcd-1234.ngrok-free.app](https://abcd-1234.ngrok-free.app)"; 


Simpan file HTML tersebut.

Buka index.html di browser Anda (Chrome/Firefox/Edge). Sistem siap digunakan!

🧠 Konsep Akademik yang Diunggulkan

Repositori ini juga mendemonstrasikan penyelesaian tantangan teknis dalam NLP:

Threshold Tuning (Dilema Ambang Batas): Implementasi logika pencarian dinamis. Jika Cosine Distance diset terlalu ketat, terjadi Data Sparsity (hasil kosong). Kode ini mendemonstrasikan penarikan id langsung dari ChromaDB dengan penyesuaian jarak matematis yang ditoleransi (misal: < 1.8).

Multilingual Context: Penggunaan versi multilingual-MiniLM-L12 membuktikan bahwa model mampu memahami relasi semantik bahasa Indonesia yang tidak kaku.

📝 Catatan Penting

Sesi Colab (Volatile): Karena database (ChromaDB) berjalan di atas RAM sesi Google Colab, seluruh data modul yang diunggah akan hilang saat sesi Colab dihentikan atau timeout. Sistem ini bersifat Proof of Concept (Prototipe). Untuk tahap production, ChromaDB perlu di-host secara permanen.

👥 Kontributor

[Nama Anda] - Peneliti & Pengembang Utama

Dibuat sebagai bagian dari Tugas / Proyek Akhir Mata Kuliah NLP & Computer Vision.
