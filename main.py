#/usr/bin/python
import urllib2, urllib
import time, os
from datetime import datetime
import subprocess
import RPi.GPIO as GPIO
import picamera
import local_settings as l


SNAPSHOT_DIR = os.path.join(CURRENT_PATH,'/images')

def __main__():
    url = 'https://api.pushover.net/1/messages.json'
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(23, GPIO.RISING)
    GPIO.add_event_callback(23, action_callback)

def action_callback(channel):
    print("Button pressed")
    data = l.data
    filename = snap()
    cmds = ['/usr/local/bin/s3cmd', '-c', '/home/pi/.s3cfg', '--no-progress', 'sync','{}/*.jpg'.format(SNAPSHOT_DIR),'s3://www.zemogle.uk/doorbell/']
    subprocess.call(cmds)
    img_url = "http://www.zemogle.uk/doorbell/%s" % (filename)
    data['url'] = img_url
    dataenc = urllib.urlencode(data)
    content = urllib2.urlopen(url=url, data=dataenc).read()
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

def myip():
    url = 'http://ipecho.net/plain'
    f = urllib2.urlopen(url)
    ip = f.read()
    return ip

__main__()
