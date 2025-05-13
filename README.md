# 🐾 Hệ thống giám sát và nhận diện vật nuôi trong chuồng trại bằng YOLOv5 và YOLOv8

Dự án này xây dựng một hệ thống ứng dụng thị giác máy tính để **giám sát, nhận diện, và kiểm soát số lượng vật nuôi** trong chuồng trại bằng cách sử dụng mô hình **YOLOv5** và **YOLOv8**.

---

## 📌 Mục tiêu

- Giám sát số lượng vật nuôi theo thời gian thực từ camera hoặc video.
- Nhận diện các loài vật cụ thể (gà, vịt, bò, heo, dê, v.v.).
- Phát hiện khi có động vật bị **thiếu hoặc xổng chuồng**.
- Ghi log sự kiện ra file Excel để quản lý.
- Hỗ trợ giao diện người dùng đơn giản dễ sử dụng.

---

## 🛠️ Thư viện sử dụng

| Thư viện | Mục đích |
|----------|----------|
| `torch`, `torchvision`, `torchaudio` | Chạy mô hình học sâu |
| `opencv-python` (`cv2`) | Xử lý ảnh, camera |
| `ultralytics` | Chạy mô hình YOLOv8 |
| `pandas` | Ghi và xử lý dữ liệu log |
| `Pillow` (`PIL`) | Vẽ và hiển thị ảnh |
| `tkinter` | Tạo giao diện người dùng |
| `datetime`, `time` | Xử lý thời gian |
| `threading` | Chạy song song giao diện và camera |

---

## ⚙️ Cài đặt

### 1. Tạo môi trường ảo (tuỳ chọn)
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

### 2. Cài thư viện
---bash
pip install torch torchvision torchaudio
pip install opencv-python
pip install ultralytics
pip install pandas
pip install pillow
hoặc
pip install -r requirements.txt

## Chạy dự án tại Main.py
