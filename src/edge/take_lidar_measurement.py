import board
import busio
import adafruit_vl53l0x
import time
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)
sensor.measurement_timing_budget = 200000

while True:
    print('Range: {}mm'.format(sensor.range))
    time.sleep(0.25)