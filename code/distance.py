import RPi.GPIO as GPIO
import RPi_I2C_driver
import time

GPIO.setmode(GPIO.BCM)

TRIG = 13  # WPi 0, pin 11
ECHO = 19  # WPi 1, pin 12
RADIUS = 4.72
pi = 3.14159

GPIO.setwarnings(False)

lcd = RPi_I2C_driver.lcd(0X27)
lcd.clear()

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def GetDistance():
    GPIO.output(TRIG, False)
    time.sleep(0.5)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 3)

    return distance

if __name__ == "__main__":
    try:
        while (1):
            now = time.localtime()
            timestamp = ("%04d-%02d-%02d %02d:%02d:%02d" %
                         (now.tm_year, now.tm_mon, now.tm_mday,
                          now.tm_hour, now.tm_min, now.tm_sec))

            distance = GetDistance()*RADIUS*RADIUS*pi
            dist_str = "{:.0f}".format(distance)  # 소수점 이하 0자리까지 출력(반올림)

            print("%s %s ml" % (timestamp, dist_str))
            time.sleep(1)

            lcd.setCursor(0, 0)
            lcd.print("%s" % (timestamp))
            lcd.setCursor(0, 1)

            if distance < 10:
                lcd.print("%s ml" % (dist_str))
            else:
                lcd.print("%s ml" % (dist_str))

    except KeyboardInterrupt:
        print("\nPress Ctrl - C")
    finally:
        print("END")
        GPIO.cleanup()
