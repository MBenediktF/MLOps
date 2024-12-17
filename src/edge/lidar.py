import board
import busio
import adafruit_vl53l0x
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)


def take_lidar_measurement():
    try:
        measurement = sensor.range
        return measurement
    except Exception:
        return None


if __name__ == "__main__":
    while True:
        measurement = take_lidar_measurement()
        print(f'Measurement: {measurement} mm')
