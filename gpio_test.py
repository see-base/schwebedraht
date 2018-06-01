import RPi.GPIO as GPIO

segmente = {
    "start": [37],
    "bonus": [33, 29, 18],
    "malus": [35, 31, 22, 16],
    "ende": [12]
}

def init_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    for key, value in segmente.items():
        GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print("GPIOs bereit")

def main():
    while True:
        for key, value in segmente.items():
            for pin in value:
                if not GPIO.input(pin):
                    print("Pin {} berührt -> {}".format(pin, key)
