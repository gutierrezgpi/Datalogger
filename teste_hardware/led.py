import RPi.GPIO as GPIO
from datetime import datetime
import time

LED_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Iniciado teste do LED.")
    
    for i in range(4):
        
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.HIGH)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Led acesso")
        
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Led apagado")
        
except KeyboardInterrupt:
    print("\nEncerrando o programa.")
finally:
    GPIO.cleanup()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Encerrado teste do LED")