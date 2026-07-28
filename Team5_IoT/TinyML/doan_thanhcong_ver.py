import network
import time
from machine import Pin, ADC
import dht
import BlynkLib
from tinyml_model import predict

# =====================================
# WIFI & BLYNK
# =====================================

WIFI_SSID = "ABC_XYZ"
WIFI_PASS = "a1234567899"
BLYNK_AUTH = "cxNSZG4onVLE8ZWoz1sL4a0zvmlMLbCM"

wifi = network.WLAN(network.STA_IF)
wifi.active(False)
time.sleep(1)
wifi.active(True)

print("Dang ket noi WiFi...")
wifi.connect(WIFI_SSID, WIFI_PASS)

while not wifi.isconnected():
    print(".", end="")
    time.sleep(0.5)

print("\nWiFi Connected!")
print(wifi.ifconfig())

print("Dang ket noi Blynk...")
blynk = BlynkLib.Blynk(BLYNK_AUTH, insecure=True)
print("Blynk Connected!")

# =====================================
# HARDWARE
# =====================================

relay_bom = Pin(5, Pin.OUT)
relay_bom.value(0)

dht_sensor = dht.DHT11(Pin(4))

cam_bien_dat = ADC(Pin(35))
cam_bien_dat.atten(ADC.ATTN_11DB)
cam_bien_dat.width(ADC.WIDTH_12BIT)

# =====================================
# BIEN TOAN CUC
# =====================================

trang_thai_bom = False
auto_mode = False

# =====================================
# CHUYEN MODE (V5)
# =====================================

@blynk.on("V5")
def mode_handler(value):
    global auto_mode

    auto_mode = int(value[0]) == 1

    if auto_mode:
        print("===== TinyML MODE =====")
        blynk.virtual_write(4, "TinyML Mode")
    else:
        print("===== Manual MODE =====")
        blynk.virtual_write(4, "Manual Mode")

# =====================================
# NUT BAT/TAT BOM (V3)
# =====================================

@blynk.on("V3")
def relay_handler(value):

    global trang_thai_bom

    if auto_mode:
        print("Dang TinyML Mode -> Bo qua nut bam")
        return

    if int(value[0]) == 1:

        relay_bom.value(1)
        trang_thai_bom = True

        print("BAT BOM")
        blynk.virtual_write(4, "Dang tuoi thu cong...")

    else:

        relay_bom.value(0)
        trang_thai_bom = False

        print("TAT BOM")
        blynk.virtual_write(4, "He thong dang cho")

# =====================================
# DOC CAM BIEN
# =====================================

def doc_va_gui_du_lieu():

    global trang_thai_bom

    # ---------- DHT11 ----------

    thanh_cong = False

    for _ in range(3):

        try:

            dht_sensor.measure()

            nhiet_do = dht_sensor.temperature()
            do_am_kk = dht_sensor.humidity()

            thanh_cong = True
            break

        except:

            time.sleep_ms(200)

    if not thanh_cong:

        print("Loi DHT11")
        return

    # ---------- Soil ----------

    gia_tri = cam_bien_dat.read()

    do_am_dat = 100 - (gia_tri / 4095 * 100)

    print("---------------------------")
    print("Nhiet do :", nhiet_do)
    print("Am KK    :", do_am_kk)
    print("Am Dat   :", round(do_am_dat,1))

    # ---------- GUI BLYNK ----------

    blynk.virtual_write(0, nhiet_do)
    blynk.virtual_write(1, do_am_kk)
    blynk.virtual_write(2, round(do_am_dat,1))

    # ===========================================
    # TinyML MODE
    # ===========================================

    if auto_mode:

        ai = predict(
            nhiet_do,
            do_am_kk,
            round(do_am_dat)
        )

        print("TinyML =", ai)

        if ai == 1:

            relay_bom.value(1)
            trang_thai_bom = True

            blynk.virtual_write(3,1)
            blynk.virtual_write(
                4,
                "TinyML: BAT BOM"
            )

            print(">>> AI BAT BOM")

        else:

            relay_bom.value(0)
            trang_thai_bom = False

            blynk.virtual_write(3,0)
            blynk.virtual_write(
                4,
                "TinyML: KHONG TUOI"
            )

            print(">>> AI TAT BOM")

    # ===========================================
    # MANUAL MODE
    # ===========================================

    else:

        if trang_thai_bom and do_am_dat >= 50:

            relay_bom.value(0)

            trang_thai_bom = False

            blynk.virtual_write(3,0)

            blynk.virtual_write(
                4,
                "Dat du am -> Da tat bom"
            )

            print("Dat du am -> Tat bom")

        elif do_am_dat < 30:

            blynk.virtual_write(
                4,
                "CANH BAO: Dat qua kho!"
            )

            try:
                blynk.log_event(
                    "dat_kho",
                    "Can tuoi nuoc!"
                )
            except:
                pass

            print("CANH BAO DAT KHO")

        else:

            blynk.virtual_write(
                4,
                "He thong dang cho"
            )

# =====================================
# MAIN
# =====================================

print("------------------------------------")
print("HE THONG TUOI CAY THONG MINH")
print("Manual + TinyML")
print("------------------------------------")

thoi_gian_cu = time.ticks_ms()

while True:

    try:

        blynk.run()

        if time.ticks_diff(
            time.ticks_ms(),
            thoi_gian_cu
        ) >= 3000:

            doc_va_gui_du_lieu()

            thoi_gian_cu = time.ticks_ms()

    except Exception as e:

        print("Loi:", e)

        time.sleep(2)
