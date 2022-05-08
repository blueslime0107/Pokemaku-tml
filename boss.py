from re import L
from norm_func import *
from spec_func import set_go_boss, add_effect, bullet, look_at_player, bullet_effect, magic_bullet, sbullet, sbullet_effect, slook_at_player
from random import randint, choice
from start import s_boom, s_cancel, s_cat1, s_dark,s_kak,s_ch0, s_ch2, s_damage0, s_damage1, s_enedead, s_enep1, s_enep2, s_graze, s_item0, s_kira0, s_kira1, s_lazer1, s_ok, s_pause, s_pldead, s_plst0, s_select, s_slash, s_tan1, s_tan2, s_piyo, s_shoot, s_nodam
from start import WIDTH, HEIGHT, small_border, dark_channel , lazer_channel
import stage_var as sv
import start as st
import pygame

def boss_file(num,pos,boss,count):
    if num == 1: # 프리져
        if when_time(count,1):
            s_ch0.play()
            set_go_boss(5,randint(0,360),20,boss)
        if when_time(count,5):
            add_effect(pos,8)
            boss.list[0] = look_at_player(pos)
        if when_time(count,90):
            s_lazer1.play()
        if while_time(count,1) and big_small(count,90,120):
            bullet(pos,boss.list[0],20,0,3,1)
        if when_time(count,180):
            s_kira0.play()
        if when_time(count,180):
            count = 0 
    if num == 2: # 썬더
        if when_time(count,1):
            boss.list[0] = look_at_player(pos)
        if when_time(count,1): s_lazer1.play()
        if when_time(count,120): s_lazer1.play()
        if while_time(count,1) and count <= 120:
            bullet(pos,boss.list[0]+40,14,0,6,2,120-count)
            bullet(pos,boss.list[0]-40,14,0,6,2,120-count)
        if when_time(count,120):
            set_go_boss(5,randint(0,360),20,boss)
        if when_time(count,240):
            count = 0       
    if num == 3: # 파이어
        if count > 60:
            if when_time(count,61): 
                s_lazer1.play()
                boss.list[0] = sv.player.pos
            if while_time(count,1):
                bullet(pos,look_at_point(pos,boss.list[0])+20,20,0,1) 
                bullet(pos,look_at_point(pos,boss.list[0])-20,20,0,1)   
            if while_time(count,20):
                bullet_effect(s_tan1,1,pos)
                bullet(pos,randint(-10,10)+look_at_player(pos),5,3,1) 
            if when_time(count,180):
                set_go_boss(4,choice([-90,90]),60,boss)
        if count > 240:
            count = 0   
    if num == 4: # 뮤츠
        boss.box_disable = True
        if while_time(count,90):
            bullet_effect(s_enep2,2,pos)
            bullet(pos,look_at_player(pos),10,20,2,4)
            for i in range(7,10):
                bullet(pos,look_at_player(pos)+randint(-9,9),i,15,2)
                bullet(pos,look_at_player(pos)+randint(-9,9),i-0.5,15,2)
            for i in range(4,7):
                bullet(pos,look_at_player(pos)+randint(-9,9),i,2,2)
                bullet(pos,look_at_player(pos)+randint(-9,9),i-0.5,2,2)
            for i in range(1,4):
                bullet(pos,look_at_player(pos)+randint(-9,9),i,12,2)
                bullet(pos,look_at_player(pos)+randint(-9,9),i-0.5,12,2)
        if while_time(count+60,180):
            set_go_boss(18,-look_at_player(pos),30,boss)
            boss.list[0] = look_at_player(pos)
        if while_time(count,180):
            add_effect(pos,5)
            for j in range(0,360,45):
                bullet(pos,j,10,20,2,4.1)
                for i in range(7,10):
                    bullet(pos,j+randint(-9,9),i,15,2)
                    bullet(pos,j+randint(-9,9),i-0.5,15,2)
                for i in range(4,7):
                    bullet(pos,j+randint(-9,9),i,2,2)
                    bullet(pos,j+randint(-9,9),i-0.5,2,2)
                for i in range(1,4):
                    bullet(pos,j+randint(-9,9),i,12,2)
                    bullet(pos,j+randint(-9,9),i-0.5,12,2)
            s_kak.play()
    if num == 5: # 뮤
        boss.box_disable = True
        if when_time(count,1):
            set_go_boss(3,-look_at_player(pos),60,boss)
        if while_time(count,6) and big_small(count,60,240):
            for i in range(0,360,120):
                bullet_effect(s_tan1,0,0,True)
                bullet(calculate_new_xy(pos,1000,-i-count*2.3,True),i+180+count*2.3,5,14,randint(1,7),5,pos)
        if when_time(count,420):
            sv.screen_shake_count = 20
            s_enep2.play()
            s_dark.play()
            bullet(pos,look_at_player(pos),0,20,2,5.1)
        if when_time(count,700):
            count = 0
    if num == 6: # 라이코
        if while_time(count+180,240):
            bullet(pos,0,6,15,6,6)
            bullet(pos,-20,6,15,6,6)
            bullet(pos,-40,6,15,6,6)
            bullet(pos,20,6,15,6,6)
            bullet(pos,40,6,15,6,6)
            set_go_boss(2,randint(0,360),20,boss)
    if num == 7: # 엔테이
        if when_time(count,120):
            bullet_effect(s_tan1,1,pos)
            bullet(pos,randint(100,130),7,19,1,7)
        if when_time(count,180):
            set_go_boss(2,randint(0,360),20,boss)
        if when_time(count,240):
            bullet_effect(s_tan1,1,pos)
            bullet(pos,randint(100,130)+120,7,19,1,7)
            count = 0
    if num == 8: # 스이쿤
        if while_time(count+60,180):
            set_go_boss(6,choice([110,-80,110,-80]),60,boss)
        if while_time(count,180):
            bullet_effect(s_kira0,4,pos)
            for i in range(3,8):
                for j in range(0,360,5):
                    bullet(pos,j,i,9,4)
            set_go_boss(3,randint(0,360),20,boss)        
    if num == 9: # 칠색조
        if when_time(count,1):
            s_ch0.play()  
        if while_time(count,5) and count <= 120:                      
            for _ in range(0,8):
                bullet(pos,randint(0,360),5,2,4) 
        if when_time(count,120):
            s_enep2.play()
            bullet(pos,look_at_player(pos),10,19,2,9,sv.player.pos)
        if when_time(count,240):
            count = 0   
    if num == 10: # 루기아
        if when_time(count,1):
            boss.list[0] = look_at_player(pos)
        if while_time(count,1) and big_small(count,60,180):
            bullet_effect(0,3,pos)
            bullet(pos,boss.list[0],16,0,3)
        if when_time(count,60):
            s_lazer1.play()
            magic_bullet(pos,boss.list[0],32,10)
        if when_time(count,300): count = 0
    if num == 11: # 세레비
        if when_time(count,30):
            bullet_effect(s_kira0,5,pos)
            magic_bullet(pos,look_at_player(pos),1,11)
        if when_time(count,60):
            set_go_boss(3,randint(0,360),60,boss)
        if when_time(count,120):
            bullet_effect(s_kira0,5,pos)
            magic_bullet(pos,look_at_player(pos),1,11)
        if when_time(count,150):
            set_go_boss(3,randint(0,360),60,boss)
        if when_time(count,210):
            bullet_effect(s_kira0,5,pos)
            magic_bullet(pos,look_at_player(pos),1,11)
        if when_time(count,240):
            set_go_boss(3,randint(0,360),60,boss)
        if when_time(count,360):
            count = 0
    if num == 12: # 레지락
        if while_time(count+60,120):
            add_effect(pos,8)
            set_go_boss(1,randint(0,360),30,boss)
            for _ in range(0,10):
                bullet_effect(s_tan1,7,get_new_pos(pos,randint(-50,50),randint(-50,50)))
                bullet(get_new_pos(pos,randint(-50,50),randint(-50,50)),look_at_player(pos),randfloat(5,8),15,7,12)
    if num == 13: # 레지아이스
        if while_time(count,1):
            poss = calculate_new_xy(pos,randint(10,200),randint(0,360),True)
            bullet_effect(s_tan2,4,poss)
            bullet(poss,look_at_point(pos,poss),2,4,4,13,120-count)
            poss = calculate_new_xy(pos,randint(10,200),randint(0,360),True)
            bullet_effect(s_tan2,0,poss)
            bullet(poss,look_at_point(pos,poss),2,12,0,13,120-count)
        if count > 120:
            set_go_boss(1,randint(0,360),30,boss)
            bullet_effect(s_kira0,0,0,True)
            count = 0
    if num == 14: # 레지스틸
        if while_time(count+120,180):
            for i in range(0,360,10):
                bullet_effect(s_tan2,4,pos)
                bullet(pos,i+5,6,15,0,14,[120-count,look_at_player(pos)])
            for i in range(0,360,10):
                bullet_effect(s_tan2,0,pos)
                bullet(pos,i,5,3,0,14,[120-count,look_at_player(pos)])
        if count > 120:
            set_go_boss(1,randint(0,360),30,boss)
            bullet_effect(s_tan1,0,0,True)
            count = 0
    if num == 15: # 라티아스
        if while_time(count+180,240):
            bullet_effect(s_tan1,0,pos)
            bullet(pos,look_at_player(pos),5,15,0,15)
        if while_time(count+180,240):
            set_go_boss(4,-look_at_point(pos,(pos[0],sv.player.pos[1]))+180,60,boss)
    if num == 16: # 라티오스
        if while_time(count+120,180):
            bullet_effect(s_tan1,0,pos)
            add_effect(pos,8)
            bullet(pos,90,5,19,2,16)
        if while_time(count,180):
            set_go_boss(3,-look_at_point(pos,(pos[0],sv.player.pos[1])),40,boss)
    if num == 17: # 가이오가
        if while_time(count+300,360):
            boss.list[0] = look_at_player(pos)
            bullet_effect(s_tan1,3,pos)
            for i in range(0,360,36):
                bullet(pos,i,randfloat(4,6),3,3,17,boss)
    if num == 18: # 그란돈
        if while_time(count+340,400):
            sv.screen_shake_count = 30
            # bullet_effect(s_enep1,7,pos)
            # for i in range(0,360,45):
            #     bullet_effect(s_tan1,1,calculate_new_xy(pos,50,i,True))
            #     for j in range(0,360,10):
            #         bullet(calculate_new_xy(pos,50,i,True),j,4,3,7)
            magic_bullet((WIDTH,HEIGHT),180,14,18)    
    if num == 19: # 레쿠쟈
        boss.box_disable = True
        if while_time(count,2) and big_small(count,0,150):
            ran = randint(0,45)
            for i in range(0,360,45):
                poi = calculate_new_xy(pos,100,-i-ran,True)
                bullet_effect(s_tan1,5,poi)
                bullet(poi,i+ran,8,17,5)
        if when_time(count,120):
            s_enep2.play()
            bullet(pos,look_at_player(pos),18,1,4,19)
            set_go_boss(18,-look_at_player(pos),30,boss)
            boss.list[0] = look_at_player(pos)
        if when_time(count,150):
            add_effect(pos,5)
            s_kak.play()
        if when_time(count,240):
            count = 0  
    if num == 20: # 지라치
        if while_time(count,2) and boss.list[0] < 540 and big_small(count,1,61):
            bullet_effect(s_tan1,2,(540-boss.list[0],0))
            rand = [randint(1,2),randint(-5,5)]
            for i in range(2,10):
                bullet((540-boss.list[0],0),-90+rand[1],i,7,rand[0])
            boss.list[0] += 20
        if count >= 240:
            set_go_boss(3,randint(0,360),60,boss)
            count = 0
            boss.list[0] = 0
    if num == 21: # 태오뭐시기
        boss.box_disable = True
        if when_time(count,30):
            s_ch0.play()
            bullet(pos,look_at_player(pos),0,3,2,21)
        if when_time(count,120):
            s_enep2.play()
            set_go_boss(12,-look_at_player(pos),30,boss)
            boss.list[0] = look_at_player(pos)
        if while_time(count,3) and big_small(count,120,150):
            for _ in range(0,5):
                bullet(get_new_pos(pos,randint(-70,70),randint(-70,70)),boss.list[0],16,4,2)
                bullet(get_new_pos(pos,randint(-70,70),randint(-70,70)),boss.list[0]+180,4,4,3)
        if when_time(count,150):
            add_effect(pos,5)
            s_kak.play()
        if when_time(count,240):
            count = 0    
    if num == 22: # 유크시
        if while_time(count,30):
            bullet_effect(s_tan1,6,pos)
            for i in range(0,360,20):
                bullet(pos,look_at_player(pos)+i,4,15,6)
        if while_time(count,120):
            set_go_boss(3,-look_at_point(pos,(pos[0],sv.player.pos[1])),40,boss)
            bullet_effect(s_kira0,6,pos)
            for bule in sv.spr.sprites():
                if big_small(distance(bule.pos,double(sv.player.pos)),300,600):
                    bullet_effect(s_tan2,bule.shape[1],double(bule.pos,True))
                    bule.hide()
    if num == 23: # 엠라이트
        if while_time(count,5) and count < 80:
            bullet_effect(s_tan1,0,pos)
            for i in range(0,360,90):
                bullet(pos,i+count*2.4,6,13,1)
            for i in range(0,360,90):
                bullet(pos,i+count*2.4+30,4,13,2)
        if when_time(count,110):
            count = 0
            s_lazer1.play()
            boss.pos = (randint(0,WIDTH),randint(0,HEIGHT))
    if num == 24: # 아그놈
        if while_time(count+160,180):
            add_effect(pos,8)
        if while_time(count+120,180):
            rand = randint(0,300)
            rerand = rand + 60
            bullet_effect(s_boom,3,sv.player.pos)
            for i in range(0,360,5):
                if not big_small(i,rand,rerand):
                    bullet(calculate_new_xy(sv.player.pos,400,i,True),look_at_player(calculate_new_xy(sv.player.pos,400,i,True))+180,3,2,3,24,double(sv.player.pos))
    if num == 25: # 디아루가
        boss.dont_stop = True
        if when_time(count,1):
            bullet_effect(s_enep2,3,pos)
            for i in range(0,360,10):
                bullet(pos,look_at_player(pos)+i,7,19,3)
        if while_time(count,2) and big_small(count,60,120):
            sv.time_stop = True
            for j in range(0,360,20):
                apos = calculate_new_xy(sv.player.pos,(count-60)*4+80,-j+randint(0,20),True)
                bullet_effect(s_tan1,0,apos,True)
                bullet(apos,j+180+randint(60,300),3,5,3)
            for j in range(0,360,20):
                bpos = calculate_new_xy(pos,(count-60)*4+80,-j+randint(0,20),True)
                bullet_effect(s_tan1,0,bpos,True)
                bullet(bpos,j+180+randint(60,300),3,5,0)
        if when_time(count,180):
            s_kira0.play()
            sv.time_stop = False
        if when_time(count,420):
            count = 0
    if num == 26: # 펄기아
        boss.really_box_disable = True
        if when_time(count,10):
            set_go_boss(10,0,60,boss)
        if when_time(count,50):
           posa = (randint(0,WIDTH),0)     
           bullet_effect(s_slash,2,posa)
           bullet(posa,look_at_player(posa),14,1,2,26)
        if when_time(count,110):
           posa = (WIDTH,randint(0,HEIGHT))     
           bullet_effect(s_slash,2,posa)
           bullet(posa,look_at_player(posa),14,1,2,26)
        if when_time(count,170):
           posa = (randint(0,WIDTH),HEIGHT)     
           bullet_effect(s_slash,2,posa)
           bullet(posa,look_at_player(posa),14,1,2,26)
        if when_time(count,230):
           posa = (0,randint(0,HEIGHT))     
           bullet_effect(s_slash,2,posa)
           bullet(posa,look_at_player(posa),14,1,2,26)
           boss.pos[1] = HEIGHT//2
           set_go_boss(10,180,60,boss)
        if when_time(count,350):
            s_kira0.play()
            sv.all_trig = True
        if when_time(count,470):
            count = 0
            sv.all_trig = False
    if num == 27: # 히드런
        if while_time(count+180,240):
            magic_bullet(pos,90,8,27,1)
            magic_bullet(pos,-90,8,27,1)
    if num == 28: # 레지기가스
        if while_time(count+120,180):
            bullet_effect(s_enep2,0,0,True)
            for i in range(0,HEIGHT+24,24):
                bullet((WIDTH,i),180,3,19,randint(0,7),28,sv.player.pos[0]*2)
    if num == 29: # 기라티나
        if while_time(count+180,240):
            bullet(pos,look_at_player(pos),2,20,6,29)
            dark_channel.play(s_dark)
        if while_time(count+140,240):
            set_go_boss(1,randint(0,360),50,boss)
    if num == 30: # 크레세리아
        if while_time(count,4) and count < 60:
            bullet_effect(s_tan1,2,pos)
            for _ in range(0,7):
                bullet(pos,randint(45,315),randfloat(3,6),3,2)        
        if when_time(count,60):
            set_go_boss(3,randint(0,360),50,boss)
        if while_time(count,4) and big_small(count,120,180):
            bullet_effect(s_tan1,2,pos)
            for _ in range(0,7):
                bullet(pos,randint(45,315),randfloat(3,6),3,2)
        if while_time(count,20) and big_small(count,181,245):
            bullet_effect(s_tan1,2,pos)
            add_effect(pos,8,2)
            sv.boss.health += 50
            sv.boss2.health += 50
            for i in range(0,360,20):
                bullet(pos,i+count*2.7,5,19,7)
        if when_time(count,260): count = 0
    if num == 31: # 모나
        if when_time(count,30):
            for i in range(0,360,6):
                bullet_effect(s_tan1,3,pos)
                for s in range(4,8):
                    bullet(pos,i,s/2,3,3)
        if when_time(count,60):
            add_effect(pos,8)
        if while_time(count,3) and big_small(count,120,240):
            bullet_effect(s_tan1,3,pos)
            bullet(pos,look_at_player(pos),randfloat(6,8),19,3)
        if when_time(count,241):
            set_go_boss(4,randint(0,360),20,boss)
        if when_time(count,300):
            count = 0
    if num == 32: # 마나
        if when_time(count,30):
            for i in range(0,360,6):
                bullet_effect(s_tan1,3,pos)
                bullet(pos,i,8,18,3,32)
        if when_time(count,120):
            set_go_boss(2,choice([-90,90]),120,boss)
        if when_time(count,240):
            count = 0
    if num == 33: # 다크라이
        if while_time(count+400,420):
            s_dark.play()
            for i in range(0,360,20):
                add_effect(calculate_new_xy(sv.player.pos,100,-i,True),33,0,2,i)
                magic_bullet(calculate_new_xy(sv.player.pos,100,-i,True),i,4,33)
            add_effect(pos,33,0,2,look_at_player(pos))
    if num == 34: # 쉐이미
        if when_time(count+180,240):
            add_effect(pos,8)
        if while_time(count+120,240):
            bullet_effect(s_tan1,5,pos)
            for i in range(0,360,36):
                bullet(pos,i+randint(-10,10),1,11,5,34,i)
        if when_time(count,360):
            count = 0
    if num == 35: # 아르세우스
        if while_time(count,90):
            bullet_effect(s_tan1,6,pos)
            ran = randint(0,360)
            for i in range(0,360,4):            
                bullet(pos,i+ran,4,3,6,35,2)
                bullet(pos,i+ran,4,3,6,35,-2)
        if while_time(count,120):
            set_go_boss(1,randint(0,360),50,boss)
    
    return count

def bullet_type(self,mod,sub):
    if mod == 1:
        if sub == 0:
            self.screen_die = 1
            if not sv.small_border.collidepoint(self.pos):
                rand_pos = (self.pos[0] + randint(-90,90),self.pos[1] + randint(-90,90))
                rand_num = randint(0,90)
                sbullet_effect(s_tan1,3,self.pos)
                for i in range(0,360,120):                       
                    sbullet(rand_pos,i+rand_num,12,6,4,1.1)
                self.kill()
        if sub == 1:
            self.screen_die = 1
            self.count += 1
            if self.count <= self.speed:
                self.speed -= 0.1
            elif self.count <= 90:
                self.speed = 0
            else:
                self.speed = 4
    if mod == 2:
        self.count += 1
        if self.num <= self.count:
            sbullet_effect(s_tan2,6,self.pos)
            rand = randint(0,90)
            for i in range(0,360,180):
                sbullet(self.pos,i+rand,3,9,6)       
            self.kill()
    if mod == 4:
        if sub == 0:
            if self.count == 0: self.size_change(180)
            self.count += 1
        if sub == 1:
            if self.count == 0: self.size_change(90)
            self.count += 1
    if mod == 5:
        self.count += 1
        self.screen_die = 2
        if sub == 0:
            if distance(double(self.pos,True),self.num) <= 2: self.kill()
        if sub == 1:
            if big_small(self.count,0,30): self.size_change(25)
            if big_small(self.count,30,210): self.size_change(1)
            if big_small(self.count,210,270): self.size_change(-15)
            if self.count == 270: self.kill()
    if mod == 6:
        if self.pos[0] >= WIDTH*2:
            if self.count == 0: 
                self.speed = 0
                self.num = randint(160,200)
            self.count += 1
            if while_time(self.count, 3):
                sbullet_effect(s_tan1,6,get_new_pos(self.pos,randint(-10,10),randint(-30,30)))
                sbullet(get_new_pos(self.pos,randint(-10,10),randint(-30,30)),self.num,12,3,6)
            if self.count >= 120: self.kill()
    if mod == 7:
        if sub == 0:
            if not small_border.collidepoint(self.pos):
                shape = (2,11,15,18)
                sv.screen_shake_count = 10
                s_boom.play()
                for j in range(0,720,20):
                    sbullet((self.pos[0]+j,self.pos[1]),90,randfloat(6,10),shape[randint(0,3)],1,7.1)
                    sbullet((self.pos[0]+j,self.pos[1]),-90,randfloat(6,10),shape[randint(0,3)],1,7.1) 
                    sbullet((self.pos[0]-j,self.pos[1]),90,randfloat(6,10),shape[randint(0,3)],1,7.1)
                    sbullet((self.pos[0]-j,self.pos[1]),-90,randfloat(6,10),shape[randint(0,3)],1,7.1)
                self.kill()
        if sub == 1:
            self.screen_die = 1
            if self.speed >= -3 : self.speed -= 0.1
        if sub == 2:
            self.screen_die = 1
            if self.speed >= 3 : self.speed -= 0.1
    if mod == 9:
        if distance(double(self.pos,True),self.num) < 50 and self.speed != 0:
            self.speed -= 1
        if self.speed <= 2:
            if self.count == 0:
                s_enep2.play()
                for i in range(0,360,15):
                    sbullet(self.rect.center,i+self.count,5,15,4)
            if while_time(self.count,10):
                for i in range(0,360,45):
                    sbullet(self.rect.center,i+self.count,5,18,4)
            if while_time(self.count,30):
                s_tan1.play()
                for i in range(0,360,45):
                    sbullet(self.rect.center,i+self.count*2,3,12,4)
            self.count += 1
            if self.count == 120:
                self.kill()
    if mod == 10:
        self.count += 1
        if self.count <= 120:
            self.direction += 3
    if mod == 11:        
        if self.count == 0:
            self.ghost = True
            self.image.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
        self.count += 1
        if self.count == 120:
            self.ghost = False
            self.image = pygame.transform.rotate(self.image2, round(self.direction-90))          
            self.speed = self.num
    if mod == 12:
        self.count += 1
        if self.count > 60:
            sbullet_effect(s_tan1,7,self.pos)
            for i in range(0,360,45):
                sbullet(self.pos,i,self.speed//2,11,7)
            self.kill()
    if mod == 13:
        self.count += 1
        if self.num == self.count:
            self.speed += 2
    if mod == 14:
        self.count += 1
        if self.num[0] == self.count:
            self.speed /= 2
            self.direction = self.num[1]
    if mod == 15:
        self.count += 1
        if sub == 0:        
            if while_time(self.count,2):
                pos = calculate_new_xy(self.pos,randint(2,100),randint(0,360),True)
                sbullet_effect(s_kira1,0,pos)
                sbullet(pos,randint(0,360),2,4,0,15.1,randint(-2,2))
                pos = calculate_new_xy(self.pos,randint(2,100),randint(0,360),True)
                sbullet_effect(s_kira1,0,pos)
                sbullet(pos,randint(0,360),2,4,0,15.1,randint(-2,2))
        if sub == 1:
            if self.count < 180:
                self.direction += self.num
    if mod == 16:
        self.screen_die = 1
        if self.pos[1] <= 0:
            self.count += 1
            if while_time(self.count,5):
                sbullet_effect(s_tan1,1,(sv.player.pos[0]*2+randint(-20,20),0))
                for i in range(4,20):
                    sbullet((sv.player.pos[0]*2+randint(-20,20),0),-90,i,18,1)
            if self.count >= 60: self.kill()
    if mod == 17:
        self.count += 1
        if self.speed > 1: self.speed -= 0.1
        if self.count == 70:
            self.speed = 0
            self.num = look_at_player(self.num.pos)
        if big_small(self.count,70,130):
            sbullet_effect(s_tan1,4,self.pos)
            sbullet(self.pos,self.num,20,1,4)
        if self.count == 130: 
            self.speed = 10
            self.direction = look_at_player(double(self.pos,True))
        if big_small(self.count,200,260) and while_time(self.count,5):
            sbullet_effect(s_tan1,3,self.pos)
            for i in range(0,360,90):
                sbullet(self.pos,self.count*2.3 + i,5,1,3)
        if self.count == 260: self.kill()
    if mod == 18:
        self.count += 1
        if self.count == 60:            
            self.num = self.speed
            self.speed = 0
        if self.count == 240: 
            self.speed = -self.num
    if mod == 19:
        if self.count == 0: self.size_change(180)
        self.count += 1
    if mod == 21:
        self.size_change(2)
        self.count += 1
        if self.count == 90:
            self.direction = look_at_player(double(self.pos,True))
            self.speed = 12
    if mod == 24:
        self.screen_die = 2
        self.count += 2
        self.direction += 2
        self.pos = move_circle(self.num,self.direction,400-self.count)
        if distance(self.pos,self.num) <= 2:
            if self.direction == 700: 
                sbullet_effect(s_enep2,3,self.pos)
                sbullet(self.pos,look_at_player(double(sv.player.pos)),1,19,2)
            self.kill()
    if mod == 26:
        
        if sub == 0:
            self.count += 1
            if self.count == 1:
                self.size_change(80)            
            if while_time(self.count,2):
                sbullet_effect(s_tan1,6,self.pos)
                sbullet(self.pos,self.direction,0,9,6,26.1)
                sbullet(self.pos,self.direction,0,9,6,26.2)
        if sub == 1 and sv.all_trig:
            self.count += 1
            if self.count == 1:self.direction += 90
            if self.speed <= 4:               
                self.speed += 0.2
        if sub == 2 and sv.all_trig:
            self.count += 1
            if self.count == 1:self.direction -= 90
            if self.speed <= 4:               
                self.speed += 0.2
    if mod == 27:
        self.count += 1
        if self.count > 240:
            add_effect(double(self.pos,True),7,1)
            self.kill()
    if mod == 28:
        if self.pos[0] <= self.num and self.speed > 0:
            self.speed -= 0.5
    if mod == 29:
        if sub == 0:
            self.count += 1
            if self.count < 30:self.size_change(10)    
            if self.num == 0:
                for bul in sv.spr.sprites():
                    if not bul == self:
                        if not bul.mod == 29.1:
                            if distance(self.pos,bul.pos) <= self.radius:
                                sbullet_effect(s_tan1,1,bul.pos)
                                sbullet(bul.pos,randint(0,360),randfloat(2,5),3,1,29.1)
                                sbullet(bul.pos,randint(0,360),randfloat(2,5),3,1,29.1)
                                sbullet(bul.pos,randint(0,360),randfloat(2,5),3,1,29.1)
                                bul.kill()
                                if self.count > 30:
                                    self.size_change(-5)
                                    if self.radius <= 10:
                                        self.num = 1
            if not sv.small_border.collidepoint(self.pos) or self.num > 0:
                self.num += 1
                if self.num <= 2: 
                    lazer_channel.play(s_lazer1)
                    bullet_effect(s_enep2,0,0,True)
                    self.speed = 0
                sbullet_effect(0,1,self.pos)
                for i in range(0,360,60):
                    sbullet(self.pos,i+15,15,0,1)
                for i in range(0,360,60):
                    sbullet(self.pos,i+45,15,0,6)
                if self.num > 120: self.kill()
    if mod == 32:
        self.screen_die = 1
        self.count += 1
        if self.count == 30:
            self.direction = look_at_player(double(self.pos,True))
        if self.count == 60:
            sbullet_effect(s_kira0,3,self.pos)
            sbullet(self.pos,look_at_player(double(self.pos,True)),4,4,4)
            self.speed -= 2
        if self.count == 90:
            self.direction = look_at_player(double(self.pos,True))
        if self.count == 120:
            sbullet_effect(s_kira0,3,self.pos)
            sbullet(self.pos,look_at_player(double(self.pos,True)),4,4,4)
            self.speed -= 2
        if self.count == 150:
            self.direction = look_at_player(double(self.pos,True))
        if self.count == 180:
            sbullet_effect(s_kira0,3,self.pos)
            sbullet(self.pos,look_at_player(double(self.pos,True)),4,4,4)
            self.speed -= 2
        if self.count >= 180:
            self.screen_die = 0   
    if mod == 34:
        self.count += 1
        if self.count >= 120+(self.num//36)*10:
            sbullet_effect(s_tan1,5,self.pos)
            for i in range(0,8):
                sbullet(self.pos,look_at_player(double(self.pos,True))+5*i,7-0.5*i,1,4)
                sbullet(self.pos,look_at_player(double(self.pos,True))-5*i,7-0.5*i,1,4)
            self.kill()
    if mod == 35:
        self.count += 1
        if big_small(self.count,20,80):
            self.direction += self.num

def magic_type(self,mod):
    if mod == 10:
        if while_time(self.count,4):
            bullet_effect(s_tan1,3,self.pos)
            for i in range(0,360,30):
                bullet(self.pos,i+self.count*2.3,3,1,3,10)
            
        self.count += 1
    if mod == 11:
        self.count += 1
        self.speed += 0.1
        if while_time(self.count,10):
            for i in range(0,10):
                bullet(get_new_pos(self.pos,randint(-100,100),randint(-100,100)),self.direction+randint(-30,30),0,4,5,11,3)
    if mod == 18:
        self.count += 1
        if while_time(self.count,5):
            bullet_effect(s_tan1,7,self.pos)
            for i in range(0,6):
                bullet(get_new_pos(self.pos,i*2),90,6-i,2,7,18)
                bullet(get_new_pos(self.pos,-i*2),90,6-i,2,7,18)
            # bullet(self.pos,80,4,11,1)
            # bullet(self.pos,90,4,11,1)
            # bullet(self.pos,100,4,11,1)
        if big_small(self.pos[0],sv.player.pos[0]-20,sv.player.pos[0]+20) and self.num == 0:
            bullet_effect(s_enep2,1,self.pos)
            for i in range(0,24,2):
                bullet(get_new_pos(self.pos,i*2),90,24-i,15,1,18)
                bullet(get_new_pos(self.pos,-i*2),90,24-i,15,1,18)
                bullet(get_new_pos(self.pos,i*2),90,(24-i)//2,3,1,18)
                bullet(get_new_pos(self.pos,-i*2),90,(24-i)//2,3,1,18)
            self.num = 1


    if mod == 27:
        self.count += 1
        if while_time(self.count,4):
            bullet_effect(s_tan1,1,self.pos)
            bullet(self.pos,0,0,3,1,27)
        if when_time(self.count,60):
            self.screen_die = 0
            self.speed += 4
            self.direction = look_at_player(self.pos)
            self.num = sv.player.pos
        if distance(self.pos,self.num) <= 2:
            bullet_effect(s_enep2,1,self.pos)
            rand = randint(0,30)
            for i in range(0,360,30):                
                bullet(self.pos,i+rand,3,15,1)
    if mod == 33:
        self.count += 1
        if while_time(self.count,20):
            bullet_effect(s_tan2,0,self.pos,True)
            bullet(self.pos,randint(0,360),randfloat(1,2),3,2)
            bullet(self.pos,randint(0,360),randfloat(1,2),3,2)

def boss_levelup(num,pos,boss,count):
    if num == 1: # 프리져
        if when_time(count,1):
            s_ch0.play()
            set_go_boss(5,randint(0,360),20,boss)
        if when_time(count,5):
            add_effect(pos,8)
            boss.list[0] = look_at_player(pos)
        if when_time(count,90):
            s_lazer1.play()
        if while_time(count,1) and big_small(count,90,120):
            bullet(pos,boss.list[0],20,0,3,1)
        if when_time(count,130):
            s_kira0.play()
        if when_time(count,130):
            count = 0 
    if num == 2: # 썬더
        if when_time(count,1):
            boss.list[0] = look_at_player(pos)
        if when_time(count,1): s_lazer1.play()
        if when_time(count,120): s_lazer1.play()
        if while_time(count,1) and count <= 120:
            bullet(pos,boss.list[0]+50,14,0,6,2,120-count)
            bullet(pos,boss.list[0]-50,14,0,6,2,120-count)
            bullet(pos,boss.list[0]+25,14,0,6,2,120-count)
            bullet(pos,boss.list[0]-25,14,0,6,2,120-count)
        if when_time(count,120):
            set_go_boss(5,randint(0,360),20,boss)
        if when_time(count,240):
            count = 0       
    if num == 3: # 파이어
        if count > 60:
            if when_time(count,61): 
                s_lazer1.play()
                boss.list[0] = sv.player.pos
            if while_time(count,1):
                bullet(pos,look_at_point(pos,boss.list[0])+10,20,0,1) 
                bullet(pos,look_at_point(pos,boss.list[0])-10,20,0,1)   
            if while_time(count,2):
                bullet_effect(s_tan1,1,pos)
                bullet(pos,randint(-10,10)+look_at_player(pos),5,3,1) 
            if when_time(count,180):
                set_go_boss(4,choice([-90,90]),60,boss)
        if count > 240:
            count = 0   
    if num == 4: # 뮤츠
        boss.box_disable = True
        if while_time(count,90):
            bullet_effect(s_enep2,2,pos)
            bullet(pos,look_at_player(pos),10,20,2,4)
            for i in range(7,10):
                bullet(pos,look_at_player(pos)+randint(-9,9),i,15,2)
                bullet(pos,look_at_player(pos)+randint(-9,9),i-0.5,15,2)
            for i in range(4,7):
                bullet(pos,look_at_player(pos)+randint(-9,9),i,2,2)
                bullet(pos,look_at_player(pos)+randint(-9,9),i-0.5,2,2)
            for i in range(1,4):
                bullet(pos,look_at_player(pos)+randint(-9,9),i,12,2)
                bullet(pos,look_at_player(pos)+randint(-9,9),i-0.5,12,2)
        if while_time(count+60,180):
            set_go_boss(18,-look_at_player(pos),30,boss)
            boss.list[0] = look_at_player(pos)
        if while_time(count,180):
            add_effect(pos,5)
            for j in range(0,360,45):
                bullet(pos,j,10,20,2,4.1)
                for i in range(7,10):
                    bullet(pos,j+randint(-9,9),i,15,2)
                    bullet(pos,j+randint(-9,9),i-0.5,15,2)
                for i in range(4,7):
                    bullet(pos,j+randint(-9,9),i,2,2)
                    bullet(pos,j+randint(-9,9),i-0.5,2,2)
                for i in range(1,4):
                    bullet(pos,j+randint(-9,9),i,12,2)
                    bullet(pos,j+randint(-9,9),i-0.5,12,2)
            s_kak.play()
    if num == 5: # 뮤
        boss.box_disable = True
        if when_time(count,1):
            set_go_boss(3,-look_at_player(pos),60,boss)
        if while_time(count,6) and big_small(count,60,240):
            for i in range(0,360,120):
                bullet_effect(s_tan1,0,0,True)
                bullet(calculate_new_xy(pos,1000,-i-count*2.3,True),i+180+count*2.3,5,14,randint(1,7),5,pos)
        if when_time(count,420):
            sv.screen_shake_count = 20
            s_enep2.play()
            s_dark.play()
            bullet(pos,look_at_player(pos),0,20,2,5.1)
        if when_time(count,700):
            count = 0
    if num == 6: # 라이코
        if while_time(count+180,200):
            bullet(pos,0,6,15,6,6)
            bullet(pos,-20,6,15,6,6)
            bullet(pos,-40,6,15,6,6)
            bullet(pos,20,6,15,6,6)
            bullet(pos,40,6,15,6,6)
            set_go_boss(2,randint(0,360),20,boss)
    if num == 7: # 엔테이
        if when_time(count,100):
            bullet_effect(s_tan1,1,pos)
            bullet(pos,randint(100,130),7,19,1,7)
        if when_time(count,150):
            set_go_boss(2,randint(0,360),20,boss)
        if when_time(count,200):
            bullet_effect(s_tan1,1,pos)
            bullet(pos,randint(100,130)+120,7,19,1,7)
            count = 0
    if num == 8: # 스이쿤
        if while_time(count+60,120):
            set_go_boss(6,choice([110,-80,110,-80]),40,boss)
        if while_time(count,160):
            bullet_effect(s_kira0,4,pos)
            for i in range(3,13):
                for j in range(0,360,5):
                    bullet(pos,j,i,9,4)
            set_go_boss(3,randint(0,360),20,boss)        
    if num == 9: # 칠색조
        if when_time(count,1):
            s_ch0.play()  
        if while_time(count,5) and count <= 120:                      
            for _ in range(0,8):
                bullet(pos,randint(0,360),5,2,4) 
        if when_time(count,120):
            s_enep2.play()
            bullet(pos,look_at_player(pos),10,19,2,9,sv.player.pos)
        if when_time(count,240):
            count = 0   
    if num == 10: # 루기아
        if when_time(count,1):
            boss.list[0] = look_at_player(pos)
        if while_time(count,1) and big_small(count,60,180):
            bullet_effect(0,3,pos)
            bullet(pos,boss.list[0],16,0,3)
        if when_time(count,60):
            s_lazer1.play()
            magic_bullet(pos,boss.list[0],32,10)
        if when_time(count,300): count = 0
    if num == 11: # 세레비
        if when_time(count,30):
            bullet_effect(s_kira0,5,pos)
            magic_bullet(pos,look_at_player(pos),1,11)
        if when_time(count,60):
            set_go_boss(3,randint(0,360),60,boss)
        if when_time(count,120):
            bullet_effect(s_kira0,5,pos)
            magic_bullet(pos,look_at_player(pos),1,11)
        if when_time(count,150):
            set_go_boss(3,randint(0,360),60,boss)
        if when_time(count,210):
            bullet_effect(s_kira0,5,pos)
            magic_bullet(pos,look_at_player(pos),1,11)
        if when_time(count,240):
            set_go_boss(3,randint(0,360),60,boss)
        if when_time(count,360):
            count = 0
    if num == 12: # 레지락
        if while_time(count+60,100):
            add_effect(pos,8)
            set_go_boss(1,randint(0,360),30,boss)
            for _ in range(0,20):
                bullet_effect(s_tan1,7,get_new_pos(pos,randint(-50,50),randint(-50,50)))
                bullet(get_new_pos(pos,randint(-50,50),randint(-50,50)),look_at_player(pos),randfloat(5,8),15,7,12)
    if num == 13: # 레지아이스
        if while_time(count,1):
            poss = calculate_new_xy(pos,randint(10,200),randint(0,360),True)
            bullet_effect(s_tan2,4,poss)
            bullet(poss,look_at_point(pos,poss),2,4,4,13,120-count)
            poss = calculate_new_xy(pos,randint(10,200),randint(0,360),True)
            bullet_effect(s_tan2,0,poss)
            bullet(poss,look_at_point(pos,poss),2,12,0,13,120-count)
            poss = calculate_new_xy(pos,randint(10,200),randint(0,360),True)
            bullet_effect(s_tan2,4,poss)
            bullet(poss,look_at_point(pos,poss),2,4,4,13,120-count)
            poss = calculate_new_xy(pos,randint(10,200),randint(0,360),True)
            bullet_effect(s_tan2,0,poss)
            bullet(poss,look_at_point(pos,poss),2,12,0,13,120-count)
        if count > 120:
            set_go_boss(1,randint(0,360),30,boss)
            bullet_effect(s_kira0,0,0,True)
            count = 0
    if num == 14: # 레지스틸
        if while_time(count+120,180):
            for i in range(0,360,10):
                bullet_effect(s_tan2,4,pos)
                bullet(pos,i+5,6,15,0,14,[120-count,look_at_player(pos)])
            for i in range(0,360,10):
                bullet_effect(s_tan2,0,pos)
                bullet(pos,i,5,3,0,14,[120-count,look_at_player(pos)])
        if count > 120:
            set_go_boss(1,randint(0,360),30,boss)
            bullet_effect(s_tan1,0,0,True)
            count = 0
    if num == 15: # 라티아스
        if while_time(count+120,180):
            bullet_effect(s_tan1,0,pos)
            bullet(pos,look_at_player(pos),5,15,0,15)
        if while_time(count+180,240):
            set_go_boss(4,-look_at_point(pos,(pos[0],sv.player.pos[1]))+180,60,boss)
    if num == 16: # 라티오스
        if while_time(count+60,120):
            bullet_effect(s_tan1,0,pos)
            add_effect(pos,8)
            bullet(pos,90,5,19,2,16)
        if while_time(count,180):
            set_go_boss(3,-look_at_point(pos,(pos[0],sv.player.pos[1])),40,boss)
        if while_time(count,26):
            bullet_effect(s_tan1,1,pos)
            for i in range(0,360,6):               
                bullet(pos,i+count*1.2,3,1,3)
    if num == 17: # 가이오가
        if while_time(count+300,360):
            boss.list[0] = look_at_player(pos)
            bullet_effect(s_tan1,3,pos)
            for i in range(0,360,36):
                bullet(pos,i,randfloat(4,6),3,3,17,boss)
    if num == 18: # 그란돈
        if while_time(count+340,400):
            sv.screen_shake_count = 30
            # bullet_effect(s_enep1,7,pos)
            # for i in range(0,360,45):
            #     bullet_effect(s_tan1,1,calculate_new_xy(pos,50,i,True))
            #     for j in range(0,360,10):
            #         bullet(calculate_new_xy(pos,50,i,True),j,4,3,7)
            magic_bullet((WIDTH,HEIGHT),180,14,18)    
    if num == 19: # 레쿠쟈
        boss.box_disable = True
        if while_time(count,2) and big_small(count,0,150):
            ran = randint(0,45)
            for i in range(0,360,45):
                poi = calculate_new_xy(pos,100,-i-ran,True)
                bullet_effect(s_tan1,5,poi)
                bullet(poi,i+ran,8,17,5)
        if when_time(count,120):
            s_enep2.play()
            bullet(pos,look_at_player(pos),18,1,4,19)
            set_go_boss(18,-look_at_player(pos),30,boss)
            boss.list[0] = look_at_player(pos)
        if when_time(count,150):
            add_effect(pos,5)
            s_kak.play()
        if when_time(count,240):
            count = 0  
    if num == 20: # 지라치
        if while_time(count,2) and boss.list[0] < 540 and big_small(count,1,61):
            bullet_effect(s_tan1,2,(540-boss.list[0],0))
            rand = [randint(1,2),randint(-5,5)]
            for i in range(2,10):
                bullet((540-boss.list[0],0),-90+rand[1],i,7,rand[0])
            boss.list[0] += 20
        if count >= 240:
            set_go_boss(3,randint(0,360),60,boss)
            count = 0
            boss.list[0] = 0
    if num == 21: # 태오뭐시기
        boss.box_disable = True
        if when_time(count,30):
            s_ch0.play()
            bullet(pos,look_at_player(pos),0,3,2,21)
        if when_time(count,120):
            s_enep2.play()
            set_go_boss(12,-look_at_player(pos),30,boss)
            boss.list[0] = look_at_player(pos)
        if while_time(count,3) and big_small(count,120,150):
            for _ in range(0,5):
                bullet(get_new_pos(pos,randint(-70,70),randint(-70,70)),boss.list[0],16,4,2)
                bullet(get_new_pos(pos,randint(-70,70),randint(-70,70)),boss.list[0]+180,4,4,3)
        if when_time(count,150):
            add_effect(pos,5)
            s_kak.play()
        if when_time(count,240):
            count = 0    
    if num == 22: # 유크시
        if while_time(count,20):
            bullet_effect(s_tan1,6,pos)
            for i in range(0,360,10):
                bullet(pos,look_at_player(pos)+i,4,15,6)
        if while_time(count+10,20):
            ran = randint(0,20)
            bullet_effect(s_tan1,3,pos)
            for i in range(0,360,10):
                bullet(pos,look_at_player(pos)+i+ran,5,15,3)
        if while_time(count,20):
            set_go_boss(3,-look_at_point(pos,(pos[0],sv.player.pos[1])),40,boss)
            bullet_effect(s_kira0,6,pos)
            for bule in sv.spr.sprites():
                if big_small(distance(bule.pos,double(sv.player.pos)),300,600):
                    bullet_effect(s_tan2,bule.shape[1],double(bule.pos,True))
                    bule.hide()
    if num == 23: # 엠라이트
        if while_time(count,5) and count < 80:
            bullet_effect(s_tan1,0,pos)
            for i in range(0,360,90):
                bullet(pos,i+count*2.4,6,13,1)
            for i in range(0,360,90):
                bullet(pos,i+count*2.4+30,5,13,2)
            for i in range(0,360,90):
                bullet(pos,i+count*1.4+30,4,13,3)
            for i in range(0,360,90):
                bullet(pos,i+count*3.4+30,3,13,5)
        if when_time(count,110):
            count = 0
            s_lazer1.play()
            boss.pos = (randint(0,WIDTH),randint(0,HEIGHT))
    if num == 24: # 아그놈
        if while_time(count+40,60):
            add_effect(pos,8)
        if while_time(count,60):
            rand = randint(0,300)
            rerand = rand + 60
            bullet_effect(s_boom,3,sv.player.pos)
            for i in range(0,360,5):
                if not big_small(i,rand,rerand):
                    bullet(calculate_new_xy(sv.player.pos,400,i,True),look_at_player(calculate_new_xy(sv.player.pos,400,i,True))+180,3,2,3,24,double(sv.player.pos))
    if num == 25: # 디아루가
        boss.dont_stop = True
        if when_time(count,1):
            bullet_effect(s_enep2,3,pos)
            for i in range(0,360,10):
                bullet(pos,look_at_player(pos)+i,7,19,3)
        if while_time(count,2) and big_small(count,60,120):
            sv.time_stop = True
            for j in range(0,360,20):
                apos = calculate_new_xy(sv.player.pos,(count-60)*4+80,-j+randint(0,20),True)
                bullet_effect(s_tan1,0,apos,True)
                bullet(apos,j+180+randint(60,300),3,5,3)
            for j in range(0,360,20):
                bpos = calculate_new_xy(pos,(count-60)*4+80,-j+randint(0,20),True)
                bullet_effect(s_tan1,0,bpos,True)
                bullet(bpos,j+180+randint(60,300),3,5,0)
        if when_time(count,180):
            s_kira0.play()
            sv.time_stop = False
        if when_time(count,420):
            count = 0
    if num == 26: # 펄기아
        boss.really_box_disable = True
        if when_time(count,10):
            set_go_boss(10,0,60,boss)
        if when_time(count,50):
           posa = (randint(0,WIDTH),0)     
           bullet_effect(s_slash,2,posa)
           bullet(posa,look_at_player(posa),14,1,2,26)
        if when_time(count,110):
           posa = (WIDTH,randint(0,HEIGHT))     
           bullet_effect(s_slash,2,posa)
           bullet(posa,look_at_player(posa),14,1,2,26)
        if when_time(count,170):
           posa = (randint(0,WIDTH),HEIGHT)     
           bullet_effect(s_slash,2,posa)
           bullet(posa,look_at_player(posa),14,1,2,26)
        if when_time(count,230):
           posa = (0,randint(0,HEIGHT))     
           bullet_effect(s_slash,2,posa)
           bullet(posa,look_at_player(posa),14,1,2,26)
           boss.pos[1] = HEIGHT//2
           set_go_boss(10,180,60,boss)
        if when_time(count,350):
            s_kira0.play()
            sv.all_trig = True
        if when_time(count,470):
            count = 0
            sv.all_trig = False
    if num == 27: # 히드런
        if while_time(count+180,240):
            magic_bullet(pos,45,8,27,1)
            magic_bullet(pos,135,8,27,1)
            magic_bullet(pos,-135,8,27,1)
            magic_bullet(pos,-45,8,27,1)
    if num == 28: # 레지기가스
        if while_time(count+120,180):
            bullet_effect(s_enep2,0,0,True)
            for i in range(0,HEIGHT+24,24):
                bullet((WIDTH,i),180,3,19,randint(0,7),28,sv.player.pos[0]*2)
    if num == 29: # 기라티나
        if while_time(count+180,240):
            bullet(pos,look_at_player(pos),2,20,6,29)
            dark_channel.play(s_dark)
        if while_time(count+140,240):
            set_go_boss(1,randint(0,360),50,boss)
    if num == 30: # 크레세리아
        if while_time(count,2):
            bullet_effect(s_tan1,2,pos)
            for _ in range(0,7):
                bullet(pos,randint(45,315),randfloat(3,6),3,2)        
        if when_time(count,60):
            set_go_boss(3,randint(0,360),50,boss)
        if while_time(count,20) and big_small(count,181,245):
            bullet_effect(s_tan1,2,pos)
            add_effect(pos,8,2)
            sv.boss.health += 50
            sv.boss2.health += 50
            for i in range(0,360,20):
                bullet(pos,i+count*2.7,5,19,7)
        if when_time(count,260): count = 0
    if num == 31: # 모나
        if when_time(count,30):
            for i in range(0,360,6):
                bullet_effect(s_tan1,3,pos)
                for s in range(4,8):
                    bullet(pos,i,s/2,3,3)
        if when_time(count,60):
            add_effect(pos,8)
        if while_time(count,3) and big_small(count,120,240):
            bullet_effect(s_tan1,3,pos)
            bullet(pos,look_at_player(pos),randfloat(6,8),19,3)
        if when_time(count,241):
            set_go_boss(4,randint(0,360),20,boss)
        if when_time(count,300):
            count = 0
    if num == 32: # 마나
        if when_time(count,30):
            for i in range(0,360,6):
                bullet_effect(s_tan1,3,pos)
                bullet(pos,i,8,18,3,32)
        if when_time(count,120):
            set_go_boss(2,choice([-90,90]),120,boss)
        if when_time(count,240):
            count = 0
    if num == 33: # 다크라이
        if while_time(count+400,420):
            s_dark.play()
            for i in range(0,360,20):
                add_effect(calculate_new_xy(sv.player.pos,100,-i,True),33,0,2,i)
                magic_bullet(calculate_new_xy(sv.player.pos,100,-i,True),i,4,33)
            add_effect(pos,33,0,2,look_at_player(pos))
    if num == 34: # 쉐이미
        if when_time(count+180,240):
            add_effect(pos,8)
        if while_time(count+120,240):
            bullet_effect(s_tan1,5,pos)
            for i in range(0,360,36):
                bullet(pos,i+randint(-10,10),1,11,5,34,i)
        if when_time(count,360):
            count = 0
    if num == 35: # 아르세우스
        if while_time(count,90):
            bullet_effect(s_tan1,6,pos)
            ran = randint(0,360)
            for i in range(0,360,4):            
                bullet(pos,i+ran,4,3,6,35,2)
                bullet(pos,i+ran,4,3,6,35,-2)
        if while_time(count,120):
            set_go_boss(1,randint(0,360),50,boss)
    
    return count

def bullet_levelup(self,mod,sub):
    if mod == 1:
        if sub == 0:
            self.screen_die = 1
            if not sv.small_border.collidepoint(self.pos):
                rand_pos = (self.pos[0] + randint(-90,90),self.pos[1] + randint(-90,90))
                rand_num = randint(0,90)
                sbullet_effect(s_tan1,3,self.pos)
                for i in range(0,360,120):                       
                    sbullet(rand_pos,i+rand_num,12,6,4,1.1)
                self.kill()
        if sub == 1:
            self.screen_die = 1
            self.count += 1
            if self.count <= self.speed:
                self.speed -= 0.1
            elif self.count <= 90:
                self.speed = 0
            else:
                self.speed = 5
                if self.count == 91:
                    sbullet(self.pos,self.direction,3,4,3)
    if mod == 2:
        self.count += 1
        if self.num <= self.count:
            sbullet_effect(s_tan2,6,self.pos)
            rand = randint(0,90)
            for i in range(0,360,180):
                sbullet(self.pos,i+rand,3,9,6)       
            self.kill()
    if mod == 4:
        if sub == 0:
            if self.count == 0: self.size_change(180)
            self.count += 1
        if sub == 1:
            if self.count == 0: self.size_change(90)
            self.count += 1
    if mod == 5:
        self.count += 1
        self.screen_die = 2
        if sub == 0:
            if distance(double(self.pos,True),self.num) <= 2: self.kill()
        if sub == 1:
            if big_small(self.count,0,30): self.size_change(25)
            if big_small(self.count,30,210): self.size_change(1)
            if big_small(self.count,210,270): self.size_change(-15)
            if self.count == 270: self.kill()
    if mod == 6:
        if self.pos[0] >= WIDTH*2:
            if self.count == 0: 
                self.speed = 0
                self.num = randint(160,200)
            self.count += 1
            sbullet_effect(s_tan1,6,get_new_pos(self.pos,randint(-10,10),randint(-30,30)))
            sbullet(get_new_pos(self.pos,randint(-10,10),randint(-30,30)),self.num,20,3,6)
            if self.count >= 120: self.kill()
    if mod == 7:
        if sub == 0:
            if not small_border.collidepoint(self.pos):
                shape = (2,11,15,18)
                sv.screen_shake_count = 10
                s_boom.play()
                for j in range(0,720,20):
                    sbullet((self.pos[0]+j,self.pos[1]),90,randfloat(6,10),shape[randint(0,3)],1,7.1)
                    sbullet((self.pos[0]+j,self.pos[1]),-90,randfloat(6,10),shape[randint(0,3)],1,7.1) 
                    sbullet((self.pos[0]-j,self.pos[1]),90,randfloat(6,10),shape[randint(0,3)],1,7.1)
                    sbullet((self.pos[0]-j,self.pos[1]),-90,randfloat(6,10),shape[randint(0,3)],1,7.1)
                    if j % 40 == 0:  
                        sbullet((self.pos[0]+j,self.pos[1]),90,randfloat(6,10),11,0,7.2)
                        sbullet((self.pos[0]+j,self.pos[1]),-90,randfloat(6,10),11,0,7.2)
                        sbullet((self.pos[0]-j,self.pos[1]),90,randfloat(6,10),11,0,7.2)
                        sbullet((self.pos[0]-j,self.pos[1]),-90,randfloat(6,10),11,0,7.2)
                self.kill()
        if sub == 1:
            self.screen_die = 1
            if self.speed >= -3 : self.speed -= 0.1
        if sub == 2:
            self.screen_die = 1
            if self.speed >= 3 : self.speed -= 0.1
    if mod == 9:
        if distance(double(self.pos,True),self.num) < 50 and self.speed != 0:
            self.speed -= 1
        if self.speed <= 2:
            if self.count == 0:
                s_enep2.play()
                for i in range(0,360,15):
                    sbullet(self.rect.center,i+self.count,5,15,4)
            if while_time(self.count,10):
                for i in range(0,360,45):
                    sbullet(self.rect.center,i+self.count,5,18,4)
            if while_time(self.count,30):
                s_tan1.play()
                for i in range(0,360,45):
                    sbullet(self.rect.center,i+self.count*2,3,12,4)
            self.count += 1
            if self.count == 120:
                self.kill()
    if mod == 10:
        self.count += 1
        if self.count <= 120:
            self.direction += 3
    if mod == 11:        
        if self.count == 0:
            self.ghost = True
            self.image.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
        self.count += 1
        if self.count == 120:
            self.ghost = False
            self.image = pygame.transform.rotate(self.image2, round(self.direction-90))          
            self.speed = self.num
    if mod == 12:
        self.count += 1
        if self.count > 60:
            sbullet_effect(s_tan1,7,self.pos)
            for i in range(0,360,30):
                sbullet(self.pos,i,self.speed//2,11,7)
            self.kill()
    if mod == 13:
        self.count += 1
        if self.num == self.count:
            self.speed += 0.5
    if mod == 14:
        self.count += 1
        if self.num[0] == self.count:
            self.speed /= 2
            self.direction = self.num[1]
    if mod == 15:
        self.count += 1
        if sub == 0:        
            if while_time(self.count,2):
                pos = calculate_new_xy(self.pos,randint(2,100),randint(0,360),True)
                sbullet_effect(s_kira1,0,pos)
                sbullet(pos,randint(0,360),2,4,0,15.1,randint(-2,2))
                pos = calculate_new_xy(self.pos,randint(2,100),randint(0,360),True)
                sbullet_effect(s_kira1,0,pos)
                sbullet(pos,randint(0,360),2,4,0,15.1,randint(-2,2))
        if sub == 1:
            if self.count < 180:
                self.direction += self.num
    if mod == 16:
        self.screen_die = 1
        if self.pos[1] <= 0:
            self.count += 1
            if while_time(self.count,5):
                sbullet_effect(s_tan1,1,(sv.player.pos[0]*2+randint(-20,20),0))
                for i in range(4,20):
                    sbullet((sv.player.pos[0]*2+randint(-20,20),0),-90,i,18,1)
            if self.count >= 60: self.kill()
    if mod == 17:
        self.count += 1
        if self.speed > 1: self.speed -= 0.1
        if self.count == 70:
            self.speed = 0
            self.num = look_at_player(self.num.pos)
        if big_small(self.count,70,130):
            sbullet_effect(s_tan1,4,self.pos)
            sbullet(self.pos,self.num,20,1,4)
        if self.count == 130: 
            self.speed = 10
            self.direction = look_at_player(double(self.pos,True))
        if big_small(self.count,200,260) and while_time(self.count,5):
            sbullet_effect(s_tan1,3,self.pos)
            for i in range(0,360,90):
                sbullet(self.pos,self.count*2.3 + i,5,1,3)
        if self.count == 260: self.kill()
    if mod == 18:
        self.count += 1
        if self.count == 60:            
            self.num = self.speed
            self.speed = 0
        if self.count == 240: 
            self.speed = -self.num
    if mod == 19:
        if self.count == 0: self.size_change(180)
        self.count += 1
    if mod == 21:
        self.size_change(2)
        self.count += 1
        if self.count == 90:
            self.direction = look_at_player(double(self.pos,True))
            self.speed = 12
    if mod == 24:
        self.screen_die = 2
        self.count += 2
        self.direction += 2
        self.pos = move_circle(self.num,self.direction,400-self.count)
        if distance(self.pos,self.num) <= 2:
            if self.direction == 700: 
                sbullet_effect(s_enep2,3,self.pos)
                sbullet(self.pos,look_at_player(double(sv.player.pos)),1,19,2)
            self.kill()
    if mod == 26:
        
        if sub == 0:
            self.count += 1
            if self.count == 1:
                self.size_change(80)            
            if while_time(self.count,2):
                sbullet_effect(s_tan1,6,self.pos)
                sbullet(self.pos,self.direction,0,9,6,26.1)
                sbullet(self.pos,self.direction,0,9,6,26.2)
        if sub == 1 and sv.all_trig:
            self.count += 1
            if self.count == 1:self.direction += 90
            if self.speed <= 4:               
                self.speed += 0.2
        if sub == 2 and sv.all_trig:
            self.count += 1
            if self.count == 1:self.direction -= 90
            if self.speed <= 4:               
                self.speed += 0.2
    if mod == 27:
        self.count += 1
        if self.count > 240:
            add_effect(double(self.pos,True),7,1)
            self.kill()
    if mod == 28:
        if self.pos[0] <= self.num and self.speed > 0:
            self.speed -= 0.5
    if mod == 29:
        if sub == 0:
            self.count += 1
            if self.count < 30:self.size_change(10)    
            if self.num == 0:
                for bul in sv.spr.sprites():
                    if not bul == self:
                        if not bul.mod == 29.1:
                            if distance(self.pos,bul.pos) <= self.radius:
                                sbullet_effect(s_tan1,1,bul.pos)
                                sbullet(bul.pos,randint(0,360),randfloat(2,5),3,1,29.1)
                                sbullet(bul.pos,randint(0,360),randfloat(2,5),3,1,29.1)
                                sbullet(bul.pos,randint(0,360),randfloat(2,5),3,1,29.1)
                                bul.kill()
                                if self.count > 30:
                                    self.size_change(-5)
                                    if self.radius <= 10:
                                        self.num = 1
            if not sv.small_border.collidepoint(self.pos) or self.num > 0:
                self.num += 1
                if self.num <= 2: 
                    lazer_channel.play(s_lazer1)
                    bullet_effect(s_enep2,0,0,True)
                    self.speed = 0
                sbullet_effect(0,1,self.pos)
                for i in range(0,360,60):
                    sbullet(self.pos,i+15,15,0,1)
                for i in range(0,360,60):
                    sbullet(self.pos,i+45,15,0,6)
                if self.num > 120: self.kill()
    if mod == 32:
        self.screen_die = 1
        self.count += 1
        if self.count == 30:
            self.direction = look_at_player(double(self.pos,True))
        if self.count == 60:
            sbullet_effect(s_kira0,3,self.pos)
            sbullet(self.pos,look_at_player(double(self.pos,True)),4,4,4)
            self.speed -= 2
        if self.count == 90:
            self.direction = look_at_player(double(self.pos,True))
        if self.count == 120:
            sbullet_effect(s_kira0,3,self.pos)
            sbullet(self.pos,look_at_player(double(self.pos,True)),4,4,4)
            self.speed -= 2
        if self.count == 150:
            self.direction = look_at_player(double(self.pos,True))
        if self.count == 180:
            sbullet_effect(s_kira0,3,self.pos)
            sbullet(self.pos,look_at_player(double(self.pos,True)),4,4,4)
            self.speed -= 2
        if self.count >= 180:
            self.screen_die = 0   
    if mod == 34:
        self.count += 1
        if self.count >= 120+(self.num//36)*10:
            sbullet_effect(s_tan1,5,self.pos)
            for i in range(0,8):
                sbullet(self.pos,look_at_player(double(self.pos,True))+5*i,7-0.5*i,1,4)
                sbullet(self.pos,look_at_player(double(self.pos,True))-5*i,7-0.5*i,1,4)
            self.kill()
    if mod == 35:
        self.count += 1
        if big_small(self.count,20,80):
            self.direction += self.num
