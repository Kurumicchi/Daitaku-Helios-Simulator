# Daitaku Helios Simulator

Game latihan pose tangan berbasis webcam yang terinspirasi dari Daitaku Helios.

Pemain ditampilkan gambar pose tangan Helios, kemudian harus menirukan pose tersebut di depan webcam. Program mendeteksi posisi dan bentuk tangan pemain menggunakan MediaPipe Hand Landmarker, lalu menentukan apakah pose pemain sesuai dengan pose yang diminta.

Proyek tugas mata kuliah Pengolahan Citra dan Video (PCV).

## Konten

* `src/main.py` — aplikasi utama: webcam, hand tracking, dan game loop.
* `src/poses.py` — logika deteksi berbagai pose tangan.
* `src/audio.py` — pemutaran efek suara.
* `models/hand_landmarker.task` — model hand tracking dari MediaPipe.
* `assets/helios/` — gambar referensi pose Daitaku Helios.
* `assets/audio/` — efek suara dan audio game.
* `requirements.txt` — daftar library Python yang dibutuhkan.

## Test

```powershell
.\.venv\Scripts\Activate.ps1
```

```powershell
python src/main.py
```

Aplikasi akan membuka webcam dan mendeteksi tangan pemain.

Tekan `q` pada window untuk keluar.

## Teknologi

| Nama         | Fungsi                              |
| ------------ | ----------------------------------- |
| Python 3.13  | Bahasa pemrograman                  |
| OpenCV       | Webcam dan pemrosesan gambar        |
| MediaPipe    | Hand tracking dan 21 hand landmarks |
| Pygame       | Pemutaran audio                     |
| Git / GitHub | Version control                     |

## Cara Kerja

Pipeline utama program:

```text
Webcam
   ↓
OpenCV
   ↓
MediaPipe Hand Landmarker
   ↓
21 Hand Landmarks
   ↓
Pose Detection
   ↓
Pose Matching
   ↓
Score / Game Response
```

MediaPipe mendeteksi hingga dua tangan dan menghasilkan 21 landmark untuk masing-masing tangan.

Landmark tersebut kemudian digunakan untuk mengenali bentuk tangan, seperti posisi jari terbuka atau terlipat.

## Pose yang Sudah Didukung

### Peace

Pose peace biasa dengan:

* Index finger terbuka
* Middle finger terbuka
* Ring finger terlipat
* Pinky terlipat

### Gyaru Peace

Pose khas Daitaku Helios dengan dua tangan membentuk peace terbalik.

* Dua tangan harus terdeteksi
* Kedua tangan harus membentuk upside-down peace
* Jika kondisi terpenuhi, pose dianggap berhasil

## Progress

### 2026-09-03

* **hand tracking berhasil.** Menggunakan MediaPipe Hand Landmarker Tasks API untuk mendeteksi hingga dua tangan dan menampilkan landmark pada webcam.
* **pose detection.** Membuat `poses.py` untuk mendeteksi peace biasa, upside-down peace, dan Gyaru Peace menggunakan MediaPipe hand landmarks.
* **Audio response.** Menambahkan `weiii.mp3` menggunakan Pygame sebagai respons ketika pose Gyaru Peace berhasil terdeteksi. Ditambahkan cooldown agar suara tidak dimainkan berulang kali setiap frame.
* **project setup.** Membuat project Python, virtual environment, struktur folder awal, dan memasang OpenCV, MediaPipe, serta Pygame.