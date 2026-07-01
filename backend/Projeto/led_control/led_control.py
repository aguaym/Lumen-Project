import RPi.GPIO as GPIO

LED_PIN = 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED_PIN, GPIO.OUT)


def ligar_led():

    GPIO.output(LED_PIN, GPIO.HIGH)


def desligar_led():

    GPIO.output(LED_PIN, GPIO.LOW)
