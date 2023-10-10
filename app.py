#import the necessary packages
import time, os
from datetime import datetime
import picamera
import local_settings as l
import telepot
from gpiozero import Button, MotionSensor
from picamera import PiCamera
from time import sleep
from signal import pause
import urllib3

# Set up the Telegram bot
bot = telepot.Bot(l.telegram['token'])

#create objects that refer to a button,
#a motion sensor and the PiCamera
button = Button(2)
pir = MotionSensor(4)
camera = PiCamera()

#start the camera
camera.rotation = 180
camera.start_preview()

#image image names
i = 0

# create http pool manager
http = urllib3.PoolManager()

#stop the camera when the pushbutton is pressed
def stop_camera():
    camera.stop_preview()
    #exit the program
    exit()

#take photo when motion is detected
def take_photo():
    global i
    i = i + 1
    filename = '/home/pi/ratcam/image_%s.jpg' % i
    camera.capture(filename)
    print('A photo has been taken')
    #resp = http.request("POST", "https://ntfy.sh/rat-catcher-pemberley")
    with open(filename,'rb') as f:
        bot.sendPhoto(l.telegram['to_user_id'], f)
    sleep(5)

if __name__ == '__main__':
    #assign a function that runs when the button is pressed
    button.when_pressed = stop_camera
    #assign a function that runs when motion is detected
    pir.when_motion = take_photo

    pause()