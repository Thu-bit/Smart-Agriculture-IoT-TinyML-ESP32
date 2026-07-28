import network
import time
from machine import Pin, ADC
import dht
import BlynkLib
from tinyml_model import predict

# 1. THÔNG TIN KẾT NỐI
WIFI_SSID = 'ABC_XYZ'
WIFI_PASS = 'a1234567899'
BLYNK_AUTH = 'cxNSZG4onVLE8ZWoz1sL4a0zvmlMLbCM'

# Khởi tạo và reset trạng thái WiFi an toàn để tránh lỗi Internal State Error
wifi = network.WLAN(network.STA_IF)
wifi.active(False)
time.sleep(1)
wifi.active(True)

print("Đang kết nối WiFi...")
wifi.connect(WIFI_SSID, WIFI_PASS)

while not wifi.isconnected():
    time.sleep(0.5)
    print(".", end="")

print("\nĐã kết nối WiFi thành công! IP của ESP32:", wifi.ifconfig()[0])

# Khởi tạo kết nối với máy chủ Blynk
print("Đang kết nối với Blynk...")
blynk = BlynkLib.Blynk(BLYNK_AUTH, insecure=True)
print("Đã kết nối Blynk!")

# 2. KHAI BÁO PHẦN CỨNG
relay_bom = Pin(5, Pin.OUT)     # Chân Relay G5
relay_bom.value(0)              # Tắt bơm ban đầu

dht_sensor = dht.DHT11(Pin(4))  # Chân DHT11 G4

cam_bien_dat = ADC(Pin(35))     # Chân Độ ẩm đất G35
cam_bien_dat.atten(ADC.ATTN_11DB)   # Cho phép đọc điện áp tới 3.3V
cam_bien_dat.width(ADC.WIDTH_12BIT) # Độ phân giải 0 - 4095

# Biến toàn cục trạng thái bơm
trang_thai_bom = False

# 3. NHẬN LỆNH TỪ BLYNK (Nút nhấn trên app bật/tắt bơm - Dùng Virtual Pin V3)
@blynk.on("V3")
def v3_write_handler(value):
    global trang_thai_bom
    if int(value[0]) == 1:
        print("📲 Bạn đã bấm nút BẬT bơm trên Blynk!")
        relay_bom.value(1)
        trang_thai_bom = True
        blynk.virtual_write(4, "Dang tuoi nuoc thu cong...")
    else:
        print("📲 Bạn đã bấm nút TẮT bơm trên Blynk!")
        relay_bom.value(0)
        trang_thai_bom = False
        blynk.virtual_write(4, "He thong dang cho...")

# 4. ĐỌC CẢM BIẾN VÀ GỬI LÊN BLYNK
def doc_va_gui_du_lieu():
    global trang_thai_bom
    
    nhiet_do = 0
    do_am_kk = 0
    
    # Thử đọc cảm biến DHT11 (Thử tối đa 3 lần nếu bị lỗi checksum)
    thanh_cong = False
    for _ in range(3):
        try:
            dht_sensor.measure()
            nhiet_do = dht_sensor.temperature()
            do_am_kk = dht_sensor.humidity()
            thanh_cong = True
            break
        except Exception:
            time.sleep_ms(200) # Đợi một chút rồi thử lại
            
    if not thanh_cong:
        print("❌ Bắt được lỗi DHT11 checksum, tự động bỏ qua lượt này...")
        return  # Bỏ qua vòng đo này, giữ nguyên hệ thống chạy tiếp

    # Đọc Độ ẩm đất
    gia_tri_dat_tho = cam_bien_dat.read()
    do_am_dat = 100 - (gia_tri_dat_tho / 4095.0 * 100) 
    
    print("🌡 Nhiệt độ:", nhiet_do, "C | 💧 Ẩm KK:", do_am_kk, "% | 🌱 Ẩm Đất:", round(do_am_dat, 1), "%")
    
    # Gửi dữ liệu lên Blynk (V0: Nhiệt độ, V1: Ẩm KK, V2: Ẩm đất)
    blynk.virtual_write(0, nhiet_do)
blynk.virtual_write(1, do_am_kk)
    blynk.virtual_write(2, round(do_am_dat, 1))
    
    # TỰ ĐỘNG TẮT BƠM KHI ĐẤT ĐỦ ẨM (Ngưỡng >= 50%)
    if trang_thai_bom and do_am_dat >= 50:
        print("💧 Đất đã đủ ẩm (>= 50%)! Tự động ngắt máy bơm.")
        relay_bom.value(0)
        trang_thai_bom = False
        blynk.virtual_write(3, 0) # Tắt nút Switch trên app
        blynk.virtual_write(4, "Dat da du am (>=50%), da tu dong tat bom!")
        blynk.log_event("dat_kho", "✅ Đất đã đủ ẩm, máy bơm tự động tắt.")

    # CẢNH BÁO ĐẤT KHÔ VÀ ĐẨY THÔNG BÁO LÊN BLYNK (Khi dưới 30%)
    elif do_am_dat < 30:
        print("⚠️ CẢNH BÁO: Đất đang quá khô! Cần bấm nút tưới nước ngay lập tức!")
        blynk.virtual_write(4, "CANH BAO: Dat qua kho (<30%), can tuoi nuoc!")
        blynk.log_event("dat_kho", "⚠️ Cảnh báo: Đất quá khô (<30%), hãy bật máy bơm ngay!")
    
    elif not trang_thai_bom:
        blynk.virtual_write(4, "Trang thai: Dat binh thuong, he thong cho.")

# Vòng lặp chính
print("Hệ thống đã sẵn sàng chạy!")
thoi_gian_cu = time.ticks_ms()

while True:
    blynk.run() # Lắng nghe lệnh từ app Blynk liên tục
    
    # Cứ mỗi 3 giây sẽ đọc cảm biến 1 lần
    if time.ticks_diff(time.ticks_ms(), thoi_gian_cu) > 3000:
        doc_va_gui_du_lieu()
        thoi_gian_cu = time.ticks_ms()
