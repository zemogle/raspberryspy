#/usr/bin/python
import urllib2, urllib
import time, os
from datetime import datetime
import subprocess
import RPi.GPIO as GPIO
import picamera
import local_settings as l
import telepot

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    bot = telepot.Bot(l.telegram['token'])
    return bot

def action_callback(bot):
    print("Button pressed")
    bot.sendMessage(l.telegram['to_user_id'], "Doorbell!")
    data = l.data
    filename = snap()
    cmds = ['/home/pi/sendimg.sh']
    subprocess.call(cmds)
    img_url = "http://www.zemogle.uk/doorbell/%s" % (filename)
    data['url'] = img_url
    dataenc = urllib.urlencode(data)
    content = urllib2.urlopen(url=l.PUSH_URL, data=dataenc).read()
    print("Button Released")
    return

def snap():
    filename = "image-%s.jpg" % datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S")
    full_file = os.path.join(l.IMAGE_DIR,filename)
    my_file = open(full_file, 'wb')
    with picamera.PiCamera() as camera:
        camera.led = False
        camera.resolution = (400,300)
        camera.rotation = 90
        # Camera warm-up time
        time.sleep(2)
        camera.capture(my_file)
    my_file.close()
    return filename


if __name__ == "__main__":
    bot = init()
    while True:
        GPIO.wait_for_edge(23, GPIO.RISING)
        action_callback(bot)
        GPIO.cleanup()
