"""
Syntax:
F:Forward
B:Backward
R:Right
L:Left
(Example: FRP: Forward-Right-Picture)
P:Picture
K:Password
-t:Time to do task (in milliseconds)
-s:Start (only to be used if -t isnt in a command)
-e:End
Some Examples:
F -t 5000
B -s
PS ########
"""
try:
    import RPi.GPIO as GPIO
except ImportError:
    import GPIO_MOCK as GPIO
from config import *
import io
import picamera
import socket
import time
import pygame
import threading
GPIO.cleanup()
mode = GPIO.getmode()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(R_Forward,GPIO.OUT)
GPIO.setup(R_Backward,GPIO.OUT)
GPIO.setup(L_Forward,GPIO.OUT)
GPIO.setup(L_Backward,GPIO.OUT)
pygame.init()
camera = picamera.PiCamera()
camera.resolution = (640,480)
pygame.mixer.init()
pygame.mixer.music.load("bootup.mp3")
pygame.mixer.music.play()
camera.start_preview()
forward = pygame.mixer.Sound("forward.ogg")
backward = pygame.mixer.Sound("backward.ogg")
left = pygame.mixer.Sound("left.ogg")
right = pygame.mixer.Sound("right.ogg")
image_send = False
clock = pygame.time.Clock()
images_sent = 0
def is_bigger(time1,time2):
    if time1.tm_year < time2.tm_year:
        return False
    else:
        if time1.tm_mon < time2.tm_mon:
            return False
        else:
            if time1.tm_mday < time2.tm_mday:
                return False
            else:
                if time1.tm_hour < time2.tm_hour:
                    return False
                else:
                    if time1.tm_min < time2.tm_min:
                        return False
                    else:
                        if time1.tm_sec < time2.tm_min:
                            return False
                        else:
                            return True
def send_image(clientsocket):
    global image_send
    image_send = True
    mystream = io.BytesIO()
    camera.capture(mystream,"jpeg")
    image_send = False
    picture_data = mystream.getvalue()
    clientsocket.send(str(len(picture_data)).encode('ascii'))
    clientsocket.send(picture_data)
class Command():
    def __init__(self,Command):
        global music
        self.cmd = Command.split(" ")
        if self.cmd[0] == "M":
            if self.cmd[1] == "0":
                pygame.mixer.music.load("hello.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "1":
                pygame.mixer.music.load("cdzhyderzpfy.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "2":
                pygame.mixer.music.load("air_raid_siren.wav")
                pygame.mixer.music.play()
            elif self.cmd[1] == "3":
                pygame.mixer.music.load("yeet-sound-effect.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "4":
                pygame.mixer.music.load("sanic_hegehog.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "5":
                pygame.mixer.music.load("Soviets.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "6":
                pygame.mixer.music.load("goodbye.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "7":
                pygame.mixer.music.load("yes.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "8":
                pygame.mixer.music.load("no.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "9":
                pygame.mixer.music.load("maybe.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "Q":
                pygame.mixer.music.load("youcant.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "W":
                pygame.mixer.music.load("youcan.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "E":
                pygame.mixer.music.load("bazinga2.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "R":
                pygame.mixer.music.load("ok.mp3")
                pygame.mixer.music.play()
            elif self.cmd[1] == "T":
                pygame.mixer.music.load("good.mp3")
                pygame.mixer.music.play()
            pygame.mixer.music.set_volume(music)
        if self.cmd[1] == "-t":
            Mode = GPIO.HIGH
            Time = int(self.cmd[2])/1000
        elif self.cmd[1] == "-s":
            Mode = GPIO.HIGH
            Time = 0
        else:
            Mode = GPIO.LOW
            Time = 0
        if self.cmd[0] == "F":
            if Mode == GPIO.HIGH:
                forward.play()
            GPIO.output((R_Forward,L_Forward),Mode)
            if Time != 0:
                time.sleep(Time)
                GPIO.output(R_Forward,GPIO.LOW)
                GPIO.output(L_Forward,GPIO.LOW)
        elif self.cmd[0] == "B":
            if Mode == GPIO.HIGH:
                backward.play()
            GPIO.output((R_Backward,L_Backward),Mode)
            if Time != 0:
                time.sleep(Time)
                GPIO.output(R_Backward,GPIO.LOW)
                GPIO.output(L_Backward,GPIO.LOW)
        elif self.cmd[0] == "V":
            if self.cmd[1] == "0":
                music -= .01
            elif self.cmd[1] == "1":
                music += .01
            pygame.mixer.music.set_volume(music)
        elif self.cmd[0] == "R":
            if Mode == GPIO.HIGH:
                right.play()
            GPIO.output(R_Backward,Mode)
            if Time != 0:
                time.sleep(Time)
                GPIO.output(L_Forward,GPIO.LOW)
        elif self.cmd[0] == "L":
            if Mode == GPIO.HIGH:
                left.play()
            GPIO.output(R_Forward,Mode)
            if Time != 0:
                time.sleep(Time)
                GPIO.output(R_Forward,GPIO.LOW)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
music = 1
host = socket.gethostname()
port = 5670
serversocket.bind(("0.0.0.0",port))
serversocket.listen(5)
command = True
alarm = False
alarmon = False
charging = False
atime = 0
FPS = 1
while True:
    clientsocket,addr = serversocket.accept()
    while True:
        if command:
            msg = clientsocket.recv(1024).decode('ascii')
            if msg[0] == "C":
                charging = True
                command = False
                atime = time.localtime(time.time()+60)
            elif msg[0] == "A":
                alarm = True
                command = False
                atime = int(msg.split(" ")[1])
            elif msg[0] == "P":
                if not image_send:
                    thread = threading.Thread(target=send_image,args=(clientsocket,))
                    thread.start()
            else:
                Command(msg)
        elif alarm:
            clock.tick(FPS)
            if is_bigger(time.localtime(time.time()),time.localtime(atime)) and not alarmon:
                pygame.mixer.music.load("sanic_hegehog.mp3")
                pygame.mixer.music.play(loops=-1)
                alarmon = True
        elif charging:
            clock.tick(FPS)
            if is_bigger(time.localtime(time.time()),atime):
                pygame.mixer.music.load("charge2.mp3")
                pygame.mixer.music.play()
                atime = time.localtime(time.time()+60)
GPIO.cleanup()
serversocket.close()
camera.stop_preview()
