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
##
from bb8 import BB8
import BB8_driver

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

data2=[]
READ_RATE=80#milisec
SCREEN_SIZE = (640, 480)
framerate=10
COUNTA=READ_RATE/framerate
clock = pygame.time.Clock()

i=0
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"値を読むだけだよ".encode('utf-8'))

# フォントの作成
myfont = pygame.font.Font("ipag.ttf", 30)

#描画（毎回やる）
try:
    pose=get_values()
    texta=str(pose[6])+' '+str(pose[7])+' '+str(pose[8])
    textb=str(pose[12])+' '+str(pose[13])+' '+str(pose[14])
    texta=unicode(texta.decode('utf-8'))
    textb=unicode(textb.decode('utf-8'))
except:
    texta=u'ぬる'
    textb=u'塗る'

# テキストを描画したSurfaceを作成
hello1 = myfont.render(u'右肩'+texta, False, (0,0,0))
hello2 = myfont.render(u'右腕'+textb,True, (0,0,0))
hello3=myfont.render(str(i), True, (0,0,0))
counta=0

## const
SPEED = 100

##
#bb = BB8('F5:6B:10:17:17:17')
bb8 = BB8_driver.Sphero('F5:6B:10:17:17:17')
bb8.connect()
bb8.start()
time.sleep(2)

#bb8.cmd(0x02, 0x20, [0x10, 0x10, 0x10, 0]) # set LED
#bb8.cmd(0x02, 0x21, [0xff]) # set back LED


h=0
while True:
    if counta==COUNTA:
        pose=get_values()
        try:
            a=pose[10]
            texta=str(pose[6])+' '+str(pose[7])+' '+str(pose[8])
            textb=str(pose[12])+' '+str(pose[13])+' '+str(pose[14])
            texta=unicode(texta.decode('utf-8'))
            textb=unicode(textb.decode('utf-8'))

            # テキストを描画したSurfaceを作成
            hello1 = myfont.render(u'右肩'+texta, False, (0,0,0))
            hello2 = myfont.render(u'右腕'+textb,True, (0,0,0))
            hello3=myfont.render(str(h), True, (0,0,0))
        except:
            print type(pose)
            print 'read_next'
        counta=0
    screen.fill((255,255,255))
    counta+=1
    # テキストを描画する
    screen.blit(hello1, (90,50))
    screen.blit(hello2, (90,150))
    screen.blit(hello3, (90,250))

    pygame.display.update()
    counta+=1
    ##
    try:
	if pose[6]-pose[12]>100:
        	h += 8
    	elif pose[12]-pose[6]>100:
        	h -= 8
    	while h<0:
        	h += 360
    	while h>359:
        	h -= 360

        if pose[13]<pose[7]:
            v = 250
            #bb8.cmd(0x02, 0x30, [v, (h&0xff00)>>8, h&0xff, 1])
            i+=1
        else:
            v = 0
	    #bb8.cmd(0x02, 0x30, [v, (h&0xff00)>>8, h&0xff, 1])
    except:
        v=0


    for event in pygame.event.get():
    #キーボード操作
    
        if event.type == KEYDOWN:
            score=0
            if event.key == K_LEFT:
                v=125
		#bb8.cmd(0x02, 0x30, [v, (h&0xff00)>>8, h&0xff, 1])
		bb8.roll(SPEED,270,1,False)
            if event.key == K_RIGHT:
		v=50
                #bb8.cmd(0x02, 0x30, [v, (h&0xff00)>>8, h&0xff, 1])
		bb8.roll(SPEED,90,1,False)
            if event.key == K_SPACE:
                score=0

    #終了処理
    if event.type == QUIT:
        pygame.quit()
        sys.exit()

    clock.tick(framerate)
    bb8.disconnect()
