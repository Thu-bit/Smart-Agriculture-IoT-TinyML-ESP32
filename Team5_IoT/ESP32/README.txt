# ESP32 Firmware

## Giới thiệu

Thư mục này chứa chương trình MicroPython chạy trên ESP32.

ESP32 có nhiệm vụ:

- Đọc dữ liệu cảm biến
- Kết nối WiFi
- Gửi dữ liệu lên Blynk
- Nhận lệnh điều khiển
- Thực hiện suy luận TinyML
- Điều khiển Relay và máy bơm

Toàn bộ quá trình suy luận được thực hiện trực tiếp trên ESP32 mà không cần Cloud AI.

---

## Cấu trúc thư mục

| File | Chức năng |
|------|-----------|
| boot.py | Khởi tạo ESP32 và kết nối WiFi |
| main.py | Chương trình điều khiển chính |
| BlynkLib.py | Thư viện giao tiếp với Blynk |
| tinyml_model.py | Mô hình TinyML chạy trên ESP32 |

---

## Luồng hoạt động

```
ESP32

│

├── Đọc DHT11

├── Đọc độ ẩm đất

├── Đọc ánh sáng

│

▼

tinyml_model.predict()

│

▼

Kết quả

│

├── 1 → Relay ON

└── 0 → Relay OFF

│

▼

Cập nhật trạng thái lên Blynk
```

---

## Chế độ hoạt động

### AUTO

- ESP32 đọc dữ liệu cảm biến
- TinyML tự quyết định bật/tắt máy bơm
- Người dùng chỉ theo dõi trên Blynk

---

### MANUAL

- Người dùng điều khiển Relay bằng Blynk
- TinyML không can thiệp

---

## TinyML

ESP32 sử dụng hàm:

```python
predict(temperature, humidity, soil)
```

Kết quả:

```
1 → Cần tưới

0 → Không cần tưới
```

Mô hình này được huấn luyện trên máy tính và chuyển đổi sang MicroPython trước khi nạp vào ESP32.

---

## Quy trình triển khai

```
Train trên máy tính

↓

Decision Tree

↓

tinyml_model.py

↓

Copy sang ESP32

↓

ESP32 thực hiện Inference
```

---

## Phần cứng sử dụng

- ESP32
- DHT11
- Cảm biến độ ẩm đất
- Cảm biến ánh sáng (LDR)
- Relay 1 kênh
- Máy bơm mini
- Nguồn cấp
- Blynk Cloud

---

## Công nghệ sử dụng

- ESP32
- MicroPython
- Blynk IoT
- TinyML
- Edge AI