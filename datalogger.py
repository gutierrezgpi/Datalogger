from time import sleep
from datetime import datetime
import board
import adafruit_bmp280
import adafruit_dht
import csv
from os import path, mkdir
import RPi.GPIO as GPIO

# Diretórios e constantes
LOG_DIR = "log"
DATA_DIR = "data"
CSV_HEADER = [
    "bmp280_timestamp", "bmp280_temperature", "bmp280_pressure", "bmp280_altitude",
    "dht22_timestamp", "dht22_temperature", "dht22_humidity"
]
BMP280_DEFAULT_SEA_LEVEL = 1013.25
SENSOR_READ_INTERVAL = 2
DHT22_PIN = board.D10
LED_PIN = 26

# Configuração inicial
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def set_led(state):
    GPIO.output(LED_PIN, GPIO.HIGH if state else GPIO.LOW)

def blink_led(times, interval=0.5):
    for _ in range(times):
        set_led(True)
        sleep(interval)
        set_led(False)
        sleep(interval)

class BMP280Sensor:
    def __init__(self):
        i2c = board.I2C()
        self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
        self._configure_sensor()

    def _configure_sensor(self):
        self.bmp280.sea_level_pressure = BMP280_DEFAULT_SEA_LEVEL
        self.bmp280.mode = adafruit_bmp280.MODE_NORMAL
        self.bmp280.standby_period = adafruit_bmp280.STANDBY_TC_500
        self.bmp280.iir_filter = adafruit_bmp280.IIR_FILTER_X16
        self.bmp280.overscan_pressure = adafruit_bmp280.OVERSCAN_X16
        self.bmp280.overscan_temperature = adafruit_bmp280.OVERSCAN_X2

    def read(self):
        try:
            return {
                "timestamp": datetime.now(),
                "temperature": self.bmp280.temperature,
                "pressure": self.bmp280.pressure,
                "altitude": self.bmp280.altitude
            }
        except Exception as e:
            timestamp = datetime.now()
            Log.error(e, "Erro na leitura do BMP280", timestamp)
            blink_led(5)
            return {"error": str(e), "timestamp": timestamp}

class DHT22Sensor:
    def __init__(self, pin):
        self.dht22 = adafruit_dht.DHT22(pin)

    def read(self):
        try:
            return {
                "timestamp": datetime.now(),
                "temperature": self.dht22.temperature,
                "humidity": self.dht22.humidity
            }
        except Exception as e:
            timestamp = datetime.now()
            Log.error(e, "Erro na leitura do DHT22", timestamp)
            blink_led(5)
            return {"error": str(e), "timestamp": timestamp}

class Log:
    _filename = None

    @staticmethod
    def _initialize():
        if not path.exists(LOG_DIR):
            mkdir(LOG_DIR)
        if Log._filename is None:
            date_now = datetime.now().strftime("%Y-%m-%d")
            Log._filename = f"{LOG_DIR}/raw_{date_now}.txt"

    @staticmethod
    def _write_log(level, message, timestamp=None):
        Log._initialize()
        timestamp = timestamp or datetime.now()
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        print(formatted_message)
        try:
            with open(Log._filename, mode="a", encoding="utf-8") as file:
                file.write(formatted_message)
        except Exception as e:
            print(f"Erro ao escrever no log: {e}")

    @staticmethod
    def debug(message):
        Log._write_log("DEBUG", message)

    @staticmethod
    def info(message):
        Log._write_log("INFO", message)

    @staticmethod
    def warning(message):
        Log._write_log("WARNING", message)

    @staticmethod
    def error(error, message="", timestamp=None):
        Log._write_log("ERROR", f"{message} | {type(error).__name__} | {error} | {error.args}", timestamp)

    @staticmethod
    def critical(message):
        Log._write_log("CRITICAL", message)

class CSVHandler:
    @staticmethod
    def save_data(bmp280_data, dht22_data, filename):
        try:
            if not path.exists(DATA_DIR):
                mkdir(DATA_DIR)
            filepath = f"{DATA_DIR}/{filename}"
            if not path.exists(filepath):
                with open(filepath, mode='w', newline="", encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(CSV_HEADER)
                    Log.debug(f"Arquivo CSV {filename} criado.")

            with open(filepath, mode="a", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    bmp280_data.get("timestamp", ""),
                    bmp280_data.get("temperature", ""),
                    bmp280_data.get("pressure", ""),
                    bmp280_data.get("altitude", ""),
                    dht22_data.get("timestamp", ""),
                    dht22_data.get("temperature", ""),
                    dht22_data.get("humidity", "")
                ])
        except Exception as e:
            Log.error(e, "Erro ao salvar dados no CSV")

if __name__ == "__main__":
    try:
        Log.info("Iniciado a captura dos dados.")
        bmp_sensor = BMP280Sensor()
        dht_sensor = DHT22Sensor(DHT22_PIN)

        while True:
            sleep(SENSOR_READ_INTERVAL)
            bmp280_data = bmp_sensor.read()
            dht22_data = dht_sensor.read()
            date_now = datetime.now().strftime("%Y-%m-%d")
            CSVHandler.save_data(bmp280_data, dht22_data, f"raw_{date_now}.csv")
    except KeyboardInterrupt:
        Log.debug("Programa interrompido pelo usuário.")
    except ValueError as e:
        Log.error(e, "Erro de valor durante a inicialização")
        blink_led(10)
    except Exception as e:
        Log.error(e, "Erro inesperado")
    finally:
        GPIO.cleanup()
        if 'dht_sensor' in locals():
            dht_sensor.dht22.exit()
        Log.debug("Encerrado a captura dos dados.")
