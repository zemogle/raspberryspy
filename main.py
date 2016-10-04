#/usr/bin/python
import urllib2, urllib
import time, os
from datetime import datetime
import subprocess
import RPi.GPIO as GPIO
import picamera
import local_settings as l


SNAPSHOT_DIR = '/home/pi/images'
PUSH_URL = 'https://api.pushover.net/1/messages.json'

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(23, GPIO.RISING)
    GPIO.add_event_callback(23, action_callback)
    return

def action_callback(channel):
    print("Button pressed")
    data = l.data
    filename = snap()
    cmds = ['/home/pi/sendimg.sh']
    subprocess.call(cmds)
    img_url = "http://www.zemogle.uk/doorbell/%s" % (filename)
    data['url'] = img_url
    dataenc = urllib.urlencode(data)
    content = urllib2.urlopen(url=PUSH_URL, data=dataenc).read()
    print("Button Released")
    return 

def snap():
    filename = "image-%s.jpg" % datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S")
    camera = picamera.PiCamera()
    camera.led = False
    camera.resolution = (800,600)
    #camera.shutter_speed = 20000
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    camera.capture(SNAPSHOT_DIR +filename)
    return filename


if __name__ == "__main__":
    init()
    while True:
        time.sleep(0.01)
