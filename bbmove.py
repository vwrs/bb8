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
        for edg in [[0,6],[6,12],[0,15],[15,21],[0,24],[0,33],[24,33],[6,24],[15,33]]:
            pygame.draw.line(screen, (126,126,126), (pose[edg[0]],pose[edg[0]+1]), (pose[edg[1]],pose[edg[1]+1]),3)
        for i in [0,6,12,15,21,24,33]:
            pygame.draw.circle(screen, (0,0,255), (int(pose[i]*resize),int(pose[i+1]*resize)), 5)
        if act!=0:
            if act==1:
                pygame.draw.circle(screen, (255,0,0), (int(pose[12]*resize),int(pose[12+1]*resize)), 10)
            elif act==2:
                pygame.draw.circle(screen, (255,0,0), (int(pose[21]*resize),int(pose[21+1]*resize)), 10)
            elif act==3:
                pygame.draw.circle(screen, (255,0,0), (int(pose[12]*resize),int(pose[12+1]*resize)), 10)
                pygame.draw.circle(screen, (255,0,0), (int(pose[21]*resize),int(pose[21+1]*resize)), 10)
                pygame.draw.circle(screen, (255,0,0), (int(pose[0]*resize),int(pose[1]*resize)), 10)
            elif act==4:
                pygame.draw.circle(screen, (0,255,0), (int(pose[12]*resize),int(pose[12+1]*resize)), 10)
                pygame.draw.circle(screen, (0,255,0), (int(pose[21]*resize),int(pose[21+1]*resize)), 10)
                pygame.draw.circle(screen, (0,255,0), (int(pose[0]*resize),int(pose[1]*resize)), 10)
                for edg in [[0,6],[6,12],[0,15],[15,21],[0,24],[0,33],[24,33],[6,24],[15,33]]:
                    pygame.draw.line(screen, (0,255,0), (pose[edg[0]],pose[edg[0]+1]), (pose[edg[1]],pose[edg[1]+1]),10)

        texta=str(pose[6])+' '+str(pose[7])+' '+str(pose[8])
        textb=str(pose[12])+' '+str(pose[13])+' '+str(pose[14])
        texta=unicode(texta.decode('utf-8'))
        textb=unicode(textb.decode('utf-8'))
    except:
        texta=u'NULL'
        textb=u'NULL'
    hello1 = myfont.render(u'右肩'+texta, False, (0,0,0))
    hello2 = myfont.render(u'右腕'+textb,True, (0,0,0))
    hello3 = myfont.render(str(i), True, (0,0,0))
    screen.blit(hello1, (90,50))
    screen.blit(hello2, (90,150))
    screen.blit(hello3, (90,250))
    pygame.display.update()

def main():
    poselist = dict(
        nose=0,
        neck=1,
        rshoulder=2,
        relbow=3,
        rwrist=4,
        lshoulder=5,
        lelbow=6,
        lwrist=7,
        rhip=8,
        rknee=9,
        rankle=10,
        lhip=11,
        lknee=12,
        lankle=13,
        reye=14,
        leye=15,
        rear=16,
        lear=17,
        bkg=18,
    )
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

    act = 0
# start
    while True:
        if counta == COUNTA:
            pose = get_values()
            try:
                rshould_x = pose[poselist["rshould"]*3]
                rshould_y = pose[poselist["rshould"]*3+1]
                relbow_x  = pose[poselist["relbow"]*3]
                relbow_y  = pose[poselist["relbow"]*3+1]
                rwrist_x  = pose[poselist["rwrist"]*3]
                rwrist_y  = pose[poselist["rwrist"]*3+1]
                lshould_x = pose[poselist["lshould"]*3]
                lshould_y = pose[poselist["lshould"]*3+1]
                lelbow_x  = pose[poselist["lelbow"]*3]
                lelbow_y  = pose[poselist["lelbow"]*3+1]
                lwrist_x  = pose[poselist["lwrist"]*3]
                lwrist_y  = pose[poselist["lwrist"]*3+1]

                display_values(pose,i,myfont,screen,act)
            except:
                print type(pose)
                print 'read_next'
            counta = 0
        counta += 1

        # BB-8を動かすルール
        try:
            # 両手を肩よりあげる→前進
            if rshould_y > rwrist_y && lshould_y > lwrist_y:
                speed = 50
                state = 1
                act = 3
            # 両手をクロス→ターボ
            elif rwrist_x > lwrist_x && rwrist_y < relbow_y && lwrist_y < lelbow_y:
                speed = 255
                act = 4
                state = 1
            # 右手だけを肩より上げる→右回転
            elif rshould_y > rwrist_y && lshould_y < lwrist_y:
                heading += 8
                state = 0
                act = 1
            # 左手だけを肩より上げる→左回転
            elif rshould_y < rwrist_y && lshould_y > lwrist_y:
                heading -= 8
                state = 0
                act = 2
            else:
                state = 0
                act = 0
        except:
            state = 0


      #   for event in pygame.event.get():
      #   #キーボード操作
      #       if event.type == KEYDOWN:
      #           score=0
      #           if event.key == K_UP:
                    # speed += 10
      #           if event.key == K_LEFT:
      #               heading -= 10
      #           if event.key == K_RIGHT:
      #               heading += 10
      #           if event.key == K_DOWN:
                    # speed -= 10
      #
      #           if event.key == K_SPACE:
      #               score=0
      #               state = 1 - state

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
