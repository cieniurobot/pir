import RPi.GPIO as GPIO
import time
import urllib

DOMOTICZ_SWITCH_ID = 1
DOMOTICZ_SWITCH_URL = "http://127.0.0.1:8080/json.htm?type=command&param=switchlight&idx={0}&switchcmd=On".format(DOMOTICZ_SWITCH_ID)
PIR_LOG = "/home/pi/pirlog.log"
GPIO.setmode(GPIO.BCM)
PIR_PIN = 23
GPIO.setup(PIR_PIN, GPIO.IN)


class Pir():
    previous_state = False
    current_state = False

    def write_log(self, message):
        with open(PIR_LOG, 'a') as file:
            file.write("{0} - {1}".format(time.strftime("%Y-%m-%d %H:%M"),message))

    def start(self):
        try:
            print("PIR Module Started (CTRL+C to exit)")
            time.sleep(2)
            print("PIR Ready")
            while True:
                time.sleep(0.2)
                self.previous_state = self.current_state
                self.current_state = GPIO.input(PIR_PIN)
                if self.current_state != self.previous_state:
                    print("Motion Detected!")
                    httpresponse = urllib.urlopen (DOMOTICZ_SWITCH_URL)
                    print(httpresponse.read())
                write_log(self.current_state)
        except KeyboardInterrupt:
            print("Quit")
            GPIO.cleanup()


if __name__ == '__main__':
    pir = Pir()
    pir.start()