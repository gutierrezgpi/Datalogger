"""
Leitura de temperatura, pressão atmosférica e altitude com BMP280.
"""

import time
import board
import adafruit_bmp280
from datetime import datetime

i2c = board.I2C()

bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

SEA_LEVEL_PRESSURE = 1013.25
bmp280.sea_level_pressure = SEA_LEVEL_PRESSURE
bmp280.mode = adafruit_bmp280.MODE_NORMAL
bmp280.standby_period = adafruit_bmp280.STANDBY_TC_500
bmp280.iir_filter = adafruit_bmp280.IIR_FILTER_X16
bmp280.overscan_pressure = adafruit_bmp280.OVERSCAN_X16
bmp280.overscan_temperature = adafruit_bmp280.OVERSCAN_X2

try:
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Iniciado teste do sensor BMP280.")
    
    for i in range(4):
        
        time.sleep(1)

        temperature = bmp280.temperature
        pressure = bmp280.pressure
        altitude = bmp280.altitude

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[{timestamp}] "
            f"BMP280 -> Temperatura: {temperature:.2f} °C | "
            f"Pressão Atmosférica: {pressure:.2f} hPa | "
            f"Altitude: {altitude:.2f} m"
        )
        
except Exception as e:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Erro ao acessar o BMP280: {e}")
finally:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Encerrado teste do sensor BMP280.")
