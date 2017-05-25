#!/usr/bin/env python
#coding: utf-8

#jsonを指定時間ごとに開けて最新を読み取って表示するやつです
import os
import glob
import json
import pygame
from pygame.locals import *
import sys
from bb8_2 import BB8

def get_values():
    filetmp=glob.glob('~/output/*.json')
    if len(filetmp)!=0:
        try:
            filetmp.sort()
	    print filetmp[-1]
            with open(filetmp[-1],'r') as f:
                tmp=json.load(f)
            data=tmp["people"][0]["body_parts"]
            #残りのファイルを削除する
            for this in filetmp:
                os.remove(this)
            return data
        except:
            print 'read_nexttime'
            return 1

data2=[]
READ_RATE=1000
SCREEN_SIZE = (640, 480)
framerate=100
COUNTA=READ_RATE/framerate
clock = pygame.time.Clock()

bb = BB8('F5:6B:10:17:17:17')
bb.cmd(0x02, 0x20, [0x10, 0x10, 0x10, 0])
bb.cmd(0x02, 0x21, [0xff])

keys = [False] * 1024
h = 0



i=0
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"値を".encode('utf-8'))

# フォントの作成
myfont = pygame.font.Font("ipag.ttf", 30)

#描画（毎回やる）
#pose=get_values()
#texta=str(pose[6])+' '+str(pose[7])+' '+str(pose[8])
#textb=str(pose[12])+' '+str(pose[13])+' '+str(pose[14])
#texta=unicode(texta.decode('utf-8'))
#textb=unicode(textb.decode('utf-8'))
#
## テキストを描画したSurfaceを作成
#hello1 = myfont.render(u'右肩'+texta, False, (0,0,0))
#hello2 = myfont.render(u'右腕'+textb,True, (0,0,0))
#hello3=myfont.render(str(i), True, (0,0,0))
counta=0

while True:
    clock.tick(framerate)
    screen.fill((255,255,255))
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
            hello3=myfont.render(str(i), True, (0,0,0))
	    # テキストを描画する
	    screen.blit(hello1, (90,50))
	    screen.blit(hello2, (90,150))
	    screen.blit(hello3, (90,250))
        except:
            print 'read_next'
        counta=0
    tmp1 = myfont.render('test', False, (0,0,0))
    screen.blit(tmp1, (90,50))
    counta+=1

    pygame.display.update()
    try:
        if pose[13]>pose[7]:
            v=100
        else:
            v=255
    except:
        v=0

    for event in pygame.event.get():
    #エージェントの操作を書く
        if event.type == KEYDOWN:
            score=0
            if event.key == K_LEFT:
                score=-1
            if event.key == K_RIGHT:
                score=1
            if event.key == K_SPACE:
                score=0
            i+=1
#             texta=str(pose[6])+' '+str(pose[7])+' '+str(pose[8])
#             textb=str(pose[11])+' '+str(pose[12])+' '+str(pose[13])
#             texta=unicode(texta.decode('utf-8'))
#             textb=unicode(textb.decode('utf-8'))

#             # テキストを描画したSurfaceを作成
#             hello1 = myfont.render(u'右肩'+texta, False, (0,0,0))
#             hello2 = myfont.render(u'右腕'+textb,True, (0,0,0))
#             hello3=myfont.render(str(i), True, (0,0,0))
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    bb.cmd(0x02, 0x30, [v, (h&0xff00)>>8, h&0xff, 1])
