#/usr/bin/python
import time, os
from datetime import datetime
import RPi.GPIO as GPIO
import picamera
import local_settings as l
import telepot

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    bot = telepot.Bot(l.telegram['token'])
    return bot

def snap(bot):
    filename = "image-%s.jpg" % datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S")
    full_file = os.path.join(l.IMAGE_DIR,filename)
    bot.sendMessage(l.telegram['to_user_id'], "Doorbell!")
    my_file = open(full_file, 'wb')
    with picamera.PiCamera() as camera:
        camera.led = False
        camera.resolution = (400,300)
        camera.rotation = 90
        # Camera warm-up time
        time.sleep(2)
        camera.capture(my_file)
    my_file.close()
    f = open(full_file,'r')
    bot.sendPhoto(l.telegram['to_user_id'], f)
    f.close()
    return


if __name__ == "__main__":
    bot = init()
    while True:
        GPIO.wait_for_edge(23, GPIO.RISING)
        snap(bot)
        GPIO.cleanup()
