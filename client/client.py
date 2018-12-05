import pygame as pg
from Variables import *
import socket
import time
import threading
WIDTH = 1400
HEIGHT = 670
FPS = 30

pg.init()
pg.mixer.init()

class GameLoop():
    def __init__(self):
        self.WIDTH = 1400
        self.HEIGHT = 670
        self.FPS = 30
        self.VOLUME = 100
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 5670
        self.s.settimeout(20)
        self.s.connect(("172.20.10.4",port))
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Boi Bot Runner")
        self.clock = pg.time.Clock()
        self.picture = False
        self.picture2 = False
        self.Send = False
        self.OF = ['Off','Off','Off','Off']
        self.running = True
        self.Frame = 0
        self.thread_number = 0
        self.take_pictures = True
        self.bmes = [("OOF *LOUD*","M 1"),("Air Raid Siren","M 2"),("Yeet x3","M 3"),
        ("Sanic Theme *LOUD*","M 4"),("Russian National Anthem","M 5"),("Ali-A Intro *Loud*","M Z"),
        ("NFL Theme *Loud*","M X"),("E *LOUD*","M C"),("MOAN *LOUD*","M V"),("Mr Boomtastic *LOUD*","M B"),
        ("Flamingo *LOUD*","M N"),("Universal Theme *LOUD*","M M"),("Minecraft Theme *LOUD*","M q"),
        ("Mickey Mouse *LOUD*","M w"),("Default Dance *LOUD*","M e"),("Yes","M 7"),("No","M 8"),("Maybe","M 9"),("Hello","M 0"),
        ("Goodbye","M 6"), ("You Can't","M Q"),("You Can", "M W"),("Bazinga","M E"),("Ok","M R"),
        ("Good", "M T"),("Charging Mode","C C"),("Volume Up","V 1"),("Volume Down","V 0")]
        self.game_loop()
    def game_loop(self):
        while self.running:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_w and not self.Send:
                        self.s.send("F -s".encode('ascii'))
                        self.Send = True
                        self.OF[0] = 'On'
                    elif event.key == pg.K_a and not self.Send:
                        self.s.send("L -s".encode('ascii'))
                        self.Send = True
                        self.OF[1] = 'On'
                    elif event.key == pg.K_d and not self.Send:
                        self.s.send("R -s".encode('ascii'))
                        self.Send = True
                        self.OF[2] = 'On'
                    elif event.key == pg.K_s and not self.Send:
                        self.s.send("B -s".encode('ascii'))
                        self.Send = True
                        self.OF[3] = 'On'
                    elif event.key == pg.K_p:
                        if not self.take_pictures:
                            self.take_pictures = True
                        else:
                            self.take_pictures = False
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_w and self.Send:
                        self.s.send("F -e".encode('ascii'))
                        self.Send = False
                        time.sleep(.5)
                        self.OF[0] = "Off"
                    elif event.key == pg.K_a and self.Send:
                        self.s.send("L -e".encode('ascii'))
                        self.Send = False
                        time.sleep(.5)
                        self.OF[1] = "Off"
                    elif event.key == pg.K_d and self.Send:
                        self.s.send("R -e".encode('ascii'))
                        self.Send = False
                        time.sleep(.5)
                        self.OF[2] = "Off"
                    elif event.key == pg.K_s and self.Send:
                        self.s.send("B -e".encode('ascii'))
                        self.Send = False
                        time.sleep(.5)
                        self.OF[3] = "Off"
            self.screen.fill(BLUE)
            pg.draw.rect(self.screen, BLACK, pg.Rect(910,10,420,275))
            if self.picture and not self.picture2:
                try:
                    self.screen.blit(pg.transform.scale(pg.image.load("jpeg1.jpg").convert(),(400,255)),(920,20))
                except:
                    pass
            if not self.picture:
                try:
                    self.screen.blit(pg.transform.scale(pg.image.load("jpeg2.jpg").convert(),(400,255)),(920,20))
                except:
                    pg.draw.rect(self.screen, BLACK, pg.Rect(910,10,420,275))
            self.message_display("Instructions",940,300,60)
            self.message_display("W - Forward",1000,370,40)
            self.message_display("S - Backward",991,410,40)
            self.message_display("A - Left",1045,450,40)
            self.message_display("D - Right",1030,490,40)
            self.message_display("Volume: {}".format(self.VOLUME),1000,600,50)
            y = 20
            x = 10
            for button in self.bmes:
                self.button(button[0],x,y,150,30,GREEN,RED,button[1])
                y += 40
                if y >= 630:
                    y = 20
                    x += 160
            pg.draw.rect(self.screen, BLACK, pg.Rect(920,350,400,10))
            pg.display.flip()
            self.Frame += 1
            if self.Frame >= 10 and not self.picture and not self.picture2 and self.take_pictures:
                take_pic = threading.Thread(target=self.take_picture,args=(self.thread_number,))
                take_pic.start()
                self.picture = True
                self.picture2 = True
                self.Frame = 0
                self.thread_number += 1
        pg.quit()
        self.s.close()
    def button(self, msg,x,y,w,h,ic,ac,command):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        pg.draw.rect(self.screen, BLACK, pg.Rect(x-3,y-3,w+6,h+6))
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pg.draw.rect(self.screen,ac,(x,y,w,h))
            if click[0] == 1:
                if command == "V 0":
                    self.VOLUME -= 1
                elif command == "V 1":
                    self.VOLUME += 1
                self.s.send(command.encode('ascii'))
        else:
            pg.draw.rect(self.screen,ic,(x,y,w,h))
        smallText = pg.font.SysFont("comicsansms",15)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x+(w/2)),(y+(h/2)))
        self.screen.blit(textSurf, textRect)
    def take_picture(self,num):
        self.s.send("P L".encode('ascii'))
        with open("jpeg1.jpg",'wb') as jpeg:
            with open("jpeg2.jpg", 'rb') as jpeg2:
                jpeg.write(jpeg2.read())
        self.picture2 = False
        with open("jpeg2.jpg","wb") as jpeg2:
            try:
                len_str = self.s.recv(6).decode('ascii')
                x = True
            except:
                x = False
            if x:
                try:
                    size = int(len_str)
                    while size > 0:
                        if size >= 4096:
                            data = self.s.recv(4096)
                        else:
                            data = self.s.recv(size)
                        if not data:
                            break
                        jpeg2.write(data)
                        size -= len(data)
                except:
                    pass
        self.picture = False
    def text_objects(self,text, font):
        textSurface = font.render(text, True, BLACK)
        return textSurface, textSurface.get_rect()

    def message_display(self,text,x,y,size):
        largeText = pg.font.Font('freesansbold.ttf',size)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.topleft = (x,y)
        self.screen.blit(TextSurf, TextRect)
GameLoop()
