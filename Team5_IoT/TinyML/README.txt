# TinyML Training

## Giới thiệu

Thư mục này chứa toàn bộ quá trình xây dựng và huấn luyện mô hình TinyML sử dụng Decision Tree để hỗ trợ hệ thống IoT giám sát môi trường nông nghiệp.

Quá trình huấn luyện được thực hiện trên máy tính bằng Python và thư viện Scikit-learn. Sau khi huấn luyện, mô hình được chuyển đổi thành mã nguồn MicroPython để triển khai trên ESP32.

---

## Quy trình thực hiện

```
Dataset
    │
    ▼
train_decision_tree.py
    │
    ▼
Decision Tree Model (.pkl)
    │
    ▼
generate_tinyml_model.py
    │
    ▼
tinyml_model.py
    │
    ▼
ESP32
```

---

## Cấu trúc thư mục

| File | Mô tả |
|------|------|
| smart_agriculture_dataset.csv | Bộ dữ liệu huấn luyện |
| smart_agriculture_dataset.xlsx | Phiên bản Excel của bộ dữ liệu |
| train_decision_tree.py | Huấn luyện mô hình Decision Tree |
| train_model.py | Script hỗ trợ huấn luyện |
| smart_agriculture_model.pkl | Mô hình đã huấn luyện |
| decision_tree.pkl | Mô hình Decision Tree |
| tree_rules.txt | Luật quyết định của mô hình |
| generate_tinyml_model.py | Chuyển Decision Tree thành mã MicroPython |
| tinyml_model.py | File được sinh tự động để chạy trên ESP32 |

---

## Bộ dữ liệu

Mỗi mẫu dữ liệu gồm 3 đặc trưng:

| Thuộc tính | Ý nghĩa |
|------------|---------|
| Temperature | Nhiệt độ môi trường (°C) |
| Humidity | Độ ẩm không khí (%) |
| Soil | Độ ẩm đất (%) |

Nhãn đầu ra:

- 0 → Không cần tưới
- 1 → Cần tưới

---

## Huấn luyện mô hình

Mô hình sử dụng:

- Decision Tree Classifier
- Scikit-learn

Các bước:

1. Đọc dữ liệu CSV
2. Chia Train/Test
3. Huấn luyện Decision Tree
4. Đánh giá Accuracy
5. Lưu mô hình (.pkl)
6. Xuất cây quyết định

---

## Chuyển đổi sang MicroPython

Sau khi huấn luyện thành công:

```
Decision Tree
        │
        ▼
generate_tinyml_model.py
        │
        ▼
tinyml_model.py
```

Script `generate_tinyml_model.py` chuyển toàn bộ cây quyết định thành các câu lệnh `if-else`, giúp ESP32 có thể suy luận mà không cần thư viện Machine Learning.

---

## Mục tiêu

ESP32 không thực hiện huấn luyện mô hình.

ESP32 chỉ thực hiện **Inference (suy luận)** thông qua file `tinyml_model.py`, giúp hệ thống đưa ra quyết định tưới nước ngay trên thiết bị (Edge AI).

---

## Công nghệ sử dụng

- Python 3
- Scikit-learn
- Pandas
- NumPy
- Decision Tree
- TinyML