#!/usr/bin/env python
#coding: utf-8

#jsonを指定時間ごとに開けて最新を読み取って表示するやつです
import os
import glob
import json
import pygame
from pygame.locals import *
import sys
import time
import BB8_driver as BB8

def get_values():
    filetmp=glob.glob('/home/ubuntu/output/*.json')
    if len(filetmp)!=0:
        try:
             filetmp.sort()
            print filetmp[-2]
            with open(filetmp[-1],'r') as f:
                tmp=json.load(f)
            data=tmp["people"][0]["body_parts"]
            if data:#からじゃなかったら
                #残りのファイルを削除する
                for this in filetmp:
                    os.remove(this)
                print data
                return data
            else:
                print 'cant get value2'
                return 1
        except:
            print 'cant get value1'
            return 1

def display_values(pose,i,myfont,screen,act=0):
    resize=0.4
    screen.fill((255,255,255))
    try:
        for i in [0,6,12,15,21,24,33]:
            pygame.draw.circle(screen, (0,0,255), (pose[i]*resize,pose[i+1]*resize), 5)
        if act!=0:
            if act=1:
                pygame.draw.circle(screen, (255,0,0), (pose[12]*resize,pose[12+1]*resize), 5)
            elif act=2:
                pygame.draw.circle(screen, (255,0,0), (pose[21]*resize,pose[21+1]*resize), 5)
            elif act=3:
                pygame.draw.circle(screen, (255,0,0), (pose[12]*resize,pose[12+1]*resize), 5)
                pygame.draw.circle(screen, (255,0,0), (pose[21]*resize,pose[21+1]*resize), 5)
                pygame.draw.circle(screen, (255,0,0), (pose[0]*resize,pose[1]*resize), 5)
            elif act=4:
                pygame.draw.circle(screen, (0,255,0), (pose[12]*resize,pose[12+1]*resize), 5)
                pygame.draw.circle(screen, (0,255,0), (pose[21]*resize,pose[21+1]*resize), 5)
                pygame.draw.circle(screen, (0,255,0), (pose[0]*resize,pose[1]*resize), 5)
                    
        texta=str(pose[6])+' '+str(pose[7])+' '+str(pose[8])
        textb=str(pose[12])+' '+str(pose[13])+' '+str(pose[14])
        texta=unicode(texta.decode('utf-8'))
        textb=unicode(textb.decode('utf-8'))
    except:
        texta=u'NULL'
        textb=u'NULL'
    hello1 = myfont.render(u'右肩'+texta, False, (0,0,0))
    hello2 = imyfont.render(u'右腕'+textb,True, (0,0,0))
    hello3 = myfont.render(str(i), True, (0,0,0))
    screen.blit(hello1, (90,50))
    screen.blit(hello2, (90,150))
    screen.blit(hello3, (90,250))
    pygame.display.update()

def main():
    data2=[]
    READ_RATE=80#milisec
    SCREEN_SIZE = (640, 480)
    framerate=10
    COUNTA=READ_RATE/framerate
    clock = pygame.time.Clock()

    i=0
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(u"bb8controler".encode('utf-8'))

# フォントの作成
    myfont = pygame.font.Font("ipag.ttf", 30)

#描画（毎回やる）
    pose=get_values()
    display_values(pose,i,myfont,screen)
# テキストを描画したSurfaceを作成
    counta=0


# connect to BB8
    bb8 = BB8.Sphero('F5:6B:10:17:17:17')
    bb8.connect()

    bb8.start()
    time.sleep(2)

    #bb8.set_rgb_led(0,0,255, False, False)
    bb8.set_back_led(255, False)
    speed = 50


    state = 0
    heading = 0
    while True:
        if counta == COUNTA:
            pose = get_values()
            try:
                a = pose[10]
                display_values(pose,i,myfont,screen)
            except:
                print type(pose)
                print 'read_next'
            counta = 0
        counta += 1
        # テキストを描画する
        counta += 1
        ##
        try:
            if pose[6] - pose[12]>100:
                heading += 8
            elif pose[12] - pose[6]>100:
                heading -= 8


	   
            if pose[13] < pose[7]:
		state = 1
            else:
                state = 0
        except:
            state = 0


        for event in pygame.event.get():
        #キーボード操作
            if event.type == KEYDOWN:
                score=0
                if event.key == K_UP:
		    speed += 10
                if event.key == K_LEFT:
                    heading -= 10 
                if event.key == K_RIGHT:
                    heading += 10
                if event.key == K_DOWN:
		    speed -= 10

                if event.key == K_SPACE:
                    score=0
                    state = 1 - state

	if heading < 0:
	    heading += 360
	if heading > 359:
	    heading -= 360
        bb8.roll(speed, heading, state, False)
        #終了処理
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        clock.tick(framerate)

if __name__ == '__main__':
    main()
