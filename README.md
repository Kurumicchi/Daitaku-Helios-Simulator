<p align="center">
  <img src="assets/img/Banner.png" alt="Daitaku Helios Banner">
</p>


# Daitaku Helios Simulator

Game latihan pose tangan berbasis webcam yang terinspirasi dari Daitaku Helios.

Pemain ditampilkan gambar pose tangan Helios, kemudian harus menirukan pose tersebut di depan webcam. Program mendeteksi bentuk tangan serta posisi upper body pemain menggunakan MediaPipe Hand Landmarker dan Pose Landmarker, lalu menentukan apakah pose pemain sesuai dengan pose yang diminta.

Proyek tugas mata kuliah Pengolahan Citra dan Video (PCV).

## Demo

<p align="left">
  <img src="demo/2026-09-04.gif" alt="Daitaku Helios Simulator Demo" width="50%">
</p>

## Konten

* `src/main.py` — aplikasi utama: webcam, hand tracking, dan game loop.
* `src/poses.py` — logika deteksi berbagai pose tangan.
* `src/audio.py` — pemutaran efek suara.
* `models/hand_landmarker.task` — model hand tracking dari MediaPipe.
* `models/pose_landmarker.task` — model pose tracking dari MediaPipe.
* `assets/helios/` — gambar referensi pose Daitaku Helios.
* `assets/audio/` — efek suara dan audio game.
* `demo/` — video demo project.

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
| MediaPipe    | Hand & Upper-body pose tracking     |
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
MediaPipe Pose Landmarker
   ↓
33 Pose Landmarks
   ↓
Pose Detection
   ↓
Pose Matching
   ↓
Score / Game Response
```

MediaPipe mendeteksi hingga dua tangan dan menghasilkan 21 landmark untuk masing-masing tangan.

MediaPipe Pose Landmarker mendeteksi 33 landmark tubuh. Pada project ini, landmark yang digunakan untuk pengenalan pose hanya bagian upper body, yaitu:
- Left shoulder
- Right shoulder
- Left elbow
- Right elbow
- Left wrist
- Right wrist

Landmark tersebut kemudian digunakan untuk mengenali bentuk tangan, seperti posisi jari terbuka atau terlipat. Sedangkan landmark shoulder, elbow, dan wrist digunakan untuk mengenali posisi serta bentuk gerakan lengan.

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

### Helios Peace

Pose peace khas Daitaku Helios menggunakan tangan kanan dengan tambahan posisi lengan.

<p align="left">
  <img src="assets/img/Peace.png" alt="Daitaku Helios Banner" width="30%">
</p>

* Tangan kanan harus membentuk Helios Peace (Thumb, index, dan middle finger terbuka, ring dan pinky terlipat)
* Upper arm harus mengarah keluar dari shoulder
* Forearm ditekuk kembali ke arah shoulder
* Hand pose dan arm pose harus terpenuhi secara bersamaan

## Progress

### 2026-09-03

* **Hand tracking berhasil.** Menggunakan MediaPipe Hand Landmarker Tasks API untuk mendeteksi hingga dua tangan dan menampilkan landmark pada webcam.
* **Pose detection.** Membuat `poses.py` untuk mendeteksi peace biasa, upside-down peace, dan Gyaru Peace menggunakan MediaPipe hand landmarks.
* **Audio response.** Menambahkan `weiii.mp3` menggunakan Pygame sebagai respons ketika pose Gyaru Peace berhasil terdeteksi. Ditambahkan cooldown agar suara tidak dimainkan berulang kali setiap frame.
* **Project setup.** Membuat project Python, virtual environment, struktur folder awal, dan memasang OpenCV, MediaPipe, serta Pygame.

### 2026-09-04

* **Upper-body tracking.** Menggunakan landmark shoulder, elbow, dan wrist untuk tracking posisi lengan tanpa menggunakan full-body pose.
* **Handedness detection.** Menambahkan pengecekan tangan kanan menggunakan informasi handedness dari MediaPipe.
* **Arm pose detection.** Menambahkan pengecekan posisi shoulder, elbow, dan wrist untuk memastikan bentuk lengan sesuai dengan pose Helios.