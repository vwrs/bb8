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
            #print filetmp[-2]
            with open(filetmp[-1],'r') as f:
                tmp=json.load(f)
            data=tmp["people"][0]["pose_keypoints"]
            if data:#からじゃなかったら
                #残りのファイルを削除する
                for this in filetmp:
                    os.remove(this)
                #print data
                return data
            else:
                return 1
        except:
            return 1

def display_values(pose,i,myfont,screen,act=0):
    resize=0.6
    screen.fill((255,255,255))
    try:
        for edg in [[0,6],[6,12],[0,15],[15,21],[0,24],[0,33],[24,33],[6,24],[15,33]]:
            pygame.draw.line(screen, (126,126,126), (pose[edg[0]]*resize,pose[edg[0]+1]*resize), (pose[edg[1]]*resize,pose[edg[1]+1]*resize))
        for i in [0,6,12,15,21,24,33]:
            pygame.draw.circle(screen, (0,0,255), (int(pose[i]*resize),int(pose[i+1]*resize)),5)
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
            	    pygame.draw.line(screen, (0,256,0), (pose[edg[0]],pose[edg[0]+1]), (pose[edg[1]],pose[edg[1]+1]),5)
    except:
        pass
    acts = [u'ストップ',u'右回転',u'左回転',u'前進',u'全速力']
    rgb = [(0,0,255),(255,0,0),(255,0,0),(255,0,0),(0,255,0)]
    act_message = myfont.render(acts[act], True, rgb[act])
    screen.blit(act_message, (240,50))

    pygame.display.update()

def main():
   # nose=0,
   # neck=1,
   # rshoulder=2,
   # relbow=3,
   # rwrist=4,
   # lshoulder=5,
   # lelbow=6,
   # lwrist=7,
   # rhip=8,
   # rknee=9,
   # rankle=10,
   # lhip=11,
   # lknee=12,
   # lankle=13,
   # reye=14,
   # leye=15,
   # rear=16,
   # lear=17,
   # bkg=18
    os.system("rm -f ~/output/*.json")
    argv = sys.argv
    if len(argv) != 2:
	sys.exit("usage: python %s 0(new) or 1(old)" % argv[0])
    # 0: new 1: old
    macaddress = "C8:F1:05:23:A1:A4" if int(argv[1]) == 0 else "F5:6B:10:17:17:17"

    data2=[]
    READ_RATE=80#milisec
    SCREEN_SIZE = (640, 480)
    framerate=22
    COUNTA=READ_RATE/framerate
    clock = pygame.time.Clock()

    i=0
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(u"BB8コントローラー".encode('utf-8'))

# フォントの作成
    myfont = pygame.font.Font("ipag.ttf", 80)

#描画（毎回やる）
    pose=get_values()
    display_values(pose,i,myfont,screen)
# テキストを描画したSurfaceを作成
    counta=0


# connect to BB8
    bb8 = BB8.Sphero(macaddress)
    bb8.connect()

    bb8.start()
    time.sleep(2)

    bb8.set_rgb_led(0,0,0, False, False)
    bb8.set_back_led(255, False)
    speed = 0


    state = 0
    heading = 0

    act = 0

    readall = False
# start
    while True:
        if counta == COUNTA:
            pose = get_values()
            try:
                rshould_x = pose[2*3]
                rshould_y = pose[2*3+1]
                relbow_x  = pose[3*3]
                relbow_y  = pose[3*3+1]
                rwrist_x  = pose[4*3]
                rwrist_y  = pose[4*3+1]
                lshould_x = pose[5*3]
                lshould_y = pose[5*3+1]
                lelbow_x  = pose[6*3]
                lelbow_y  = pose[6*3+1]
                lwrist_x  = pose[7*3]
                lwrist_y  = pose[7*3+1]
      	        if not (rshould_x == 0 or
		        relbow_x == 0  or
                        rwrist_x == 0  or
                        lshould_x == 0 or
		        lelbow_x == 0  or
                        lwrist_x == 0):
		    readall = True
            except:
                #print type(pose)
                #print 'read_next'
		readall = False
	    try:
		display_values(pose,i,myfont,screen,act)
	    except:
		print 'display values error'
            counta = 0
        counta += 1

        # BB-8を動かすルール
        # 両手をあげる→前進
	if readall:
            if rshould_y - rwrist_y > 50 and lshould_y - lwrist_y > 50:
                speed = 80 
                state = 1
                act = 3
            # 両手を肩と平行にする 
            elif abs(rshould_y - relbow_y) < 30 and abs(lshould_y - lelbow_y) < 30 and abs(relbow_y - lelbow_y) < 30:
                speed = 255
                state = 1
                act = 4
            # 右手だけを肩より上げる→右回転
            elif rshould_y - rwrist_y > 80 and lshould_y < lwrist_y:
                heading += 4
                state = 0
                act = 1
            # 左手だけを肩より上げる→左回転
            elif rshould_y < rwrist_y and lshould_y - lwrist_y > 80:
                heading -= 4
                state = 0
                act = 2
            else:
                state = 0
                act = 0
        else:
	    state = 0
	    act = 0

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
      	    #終了処理
      	    if event.type == QUIT:
      	        pygame.quit()
      	        sys.exit()

        if heading < 0:
            heading += 360
        if heading > 359:
            heading -= 360
        bb8.roll(speed, heading, state, False)

        clock.tick(framerate)

if __name__ == '__main__':
    main()
