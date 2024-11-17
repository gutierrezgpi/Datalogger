"""
Leitura de temperatura e umidade com DHT22.
"""

import board
import adafruit_dht
from time import sleep
from datetime import datetime

dht22 = adafruit_dht.DHT22(board.D10)

try:
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Iniciado teste do sensor DHT22.")
    
    for i in range(4):
        try:
            
            sleep(2)
            
            temperature = dht22.temperature
            humidity = dht22.humidity

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] DHT22 -> Temperatura: {temperature:.2f} °C | Umidade: {humidity:.2f} %")
        
        except RuntimeError as e:
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Erro transitório: {e.args[0]}")
            continue

except Exception as e:
    print(f"Erro inesperado: {e}")

finally:
    dht22.exit()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Encerrado teste do sensor DHT22.")