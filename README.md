# 🕰️ Time Capsule AI

Prototype aplikasi web berbasis **Streamlit** yang mengubah satu foto potret menjadi video "perjalanan waktu" sinematik, dibangun sebagai proyek untuk mata kuliah **Generative AI** — Program Studi Teknik Informatika, Fakultas Ilmu Komputer, **Universitas Mercu Buana**.

Antarmuka dirancang dengan gaya modern ala aplikasi AI (dark theme, aurora gradient, glassmorphism) agar terlihat seperti produk AI generation profesional, sementara proses rendering video sesungguhnya dilakukan secara terpisah melalui **Google AI Studio**.

---

## ✨ Fitur

- 📤 **Upload Foto** — unggah foto potret (JPG/JPEG/PNG) dengan area drag & drop bergaya modern
- 🖼️ **Preview Gambar** — pratinjau foto yang diunggah secara langsung
- 🤖 **AI Processing Panel** — timeline visual proses (Upload → Analyze → Prompt → Google AI Studio → Render → Complete)
- ✨ **Generate Button** — memicu simulasi proses rendering dengan animasi loading
- 🎬 **Video Player** — menampilkan video hasil pertama yang ditemukan di folder `generated_videos/`
- 📊 **Statistic Cards** — ringkasan AI Engine, Status, Output, dan Resolution
- 🌌 **Dark Theme + Aurora Gradient Background**
- 💎 **Glassmorphism UI** terinspirasi dari RunwayML, Luma AI, dan Pika
- 📱 **Responsive Layout**

---

## 📁 Struktur Proyek

```
TimeCapsulePrototype/
├── app.py                 # Kode utama aplikasi Streamlit
├── requirements.txt        # Daftar dependensi Python
├── generated_videos/       # Folder output video hasil generate (Google AI Studio)
└── README.md
```

---

## 🚀 Cara Menjalankan

1. **Clone repository**
   ```bash
   git clone https://github.com/RHNSPTR/TimeCapsulePrototype.git
   cd TimeCapsulePrototype
   ```

2. **Buat virtual environment (opsional tapi disarankan)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

3. **Install dependensi**
   ```bash
   pip install -r requirements.txt
   ```

4. **Siapkan video hasil generate**
   Masukkan file video hasil proses dari Google AI Studio (`.mp4`, `.mov`, atau `.avi`) ke dalam folder:
   ```
   generated_videos/
   ```

5. **Jalankan aplikasi**
   ```bash
   streamlit run app.py
   ```

6. Buka browser pada alamat yang muncul di terminal (biasanya `http://localhost:8501`).

---

## 🧠 Alur Kerja (Workflow)

1. Pengguna mengunggah foto potret melalui antarmuka web
2. Foto diproses secara eksternal menggunakan pipeline Google AI Studio (di luar aplikasi ini)
3. Video hasil generate ditempatkan ke folder `generated_videos/`
4. Aplikasi Streamlit membaca video pertama pada folder tersebut dan menampilkannya melalui video player

> **Catatan:** Aplikasi ini adalah *front-end prototype*. Proses AI generation video (image-to-video) tidak dijalankan secara langsung di dalam aplikasi, melainkan disiapkan secara manual melalui Google AI Studio sebagai bagian dari alur demonstrasi.

---

## 🛠️ Teknologi yang Digunakan

- [Streamlit](https://streamlit.io/) — framework utama antarmuka web
- Python 3.x
- HTML/CSS custom (untuk styling dark theme, aurora gradient, dan glassmorphism)
- Google AI Studio — proses generation video eksternal

---

## 👤 Kontributor

**Rehan Saputra**
Program Studi Teknik Informatika, Fakultas Ilmu Komputer
Universitas Mercu Buana

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan tugas akademik (mata kuliah Generative AI) dan bersifat prototype non-komersial.
