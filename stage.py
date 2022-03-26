from numpy import s_
import start as st
from start import WIDTH,HEIGHT, bg_image, bg2_image, pokemons, boss_movebox, small_border, BGM1,BGM2,BGM3,BGM4,BGM5
from spec_func import *
import stage_var as sv
import pygame, math
from random import randint, choice
from start import s_lazer1, s_enep2, s_ch0,  s_tan1, s_tan2, s_boom
from norm_func import *

# 다음 챌린지 넘어가기
def end_challenge(time):

    if time == sv.stage_count and sv.stage_line == sv.stage_cline:
        sv.pause_lock = True
        sv.pause = True  
        sv.curser = 0       
# 스테이지 이름
# 뒷배경 소환
def bground_spawn(val,time):

    # x, y, dir, speed, health, img, hit_cir, num = val
    if time == sv.stage_count and sv.stage_line == sv.stage_cline:
        sv.stage_count = 0
        sv.stage_line += 1
        if val == 1:st.bkgd_list.append(sv.Back_Ground(bg_image,(540,0,540,120),1,3,0,True))
        if val == 2:st.bkgd_list.append(sv.Back_Ground(bg_image,(540,240,540,120),3,4,240,True))
        if val == 3:st.bkgd_list.append(sv.Back_Ground(bg_image,(1080,0,540,290),2,5,0,True)) 
        if val == 8:st.bkgd_list.append(sv.Back_Ground(bg_image,(1080//2,972//2,1080//2,468//2),2,8,126,True))
        if val == 9:st.bkgd_list.append(sv.Back_Ground(bg_image,(1080//2,720//2,1080//2,252//2),1,9,0,True))
    sv.stage_cline += 1
# 게임의 배경, 스테이지
def game_defalt_setting(fun): # 게임 스테이지 배경 정하기
    st.bkgd_list = []
    ##############################################
    if fun == 1:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,0,1080,240),1,0,0))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,240,1080,240),2,1,240))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,480,1080,240),3,2,480))
    if fun == 2:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,360,540,232),2,6,0))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,592,540,128),3,7,232))
    if fun == 3:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,720,540,126),5,8,0))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(540,776,540,304),7,9,118))
    if fun == 4:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1080,720,360),10,10))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(540,1080,540,360),8,11))
    if fun == 5:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1440,540,72),7,8,0))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1440+72,540,72),5,8,72))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1440+72*2,540,72),3,8,72*2))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1440+72*3,540,72),5,8,72*3))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1440+72*4,540,72),7,8,72*4))
    if fun == 6:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1800,540,360),5,8,0))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(540,2070,540,90),3,8,280))

def game_music_setting(fun):
    if not sv.music_playing:
        pygame.mixer.music.stop()
        if fun == 1:
            pygame.mixer.music.load(BGM1)
        if fun == 2:
            pygame.mixer.music.load(BGM2)
        if fun == 3:
            pygame.mixer.music.load(BGM5)
        if fun == 4:
            pygame.mixer.music.load(BGM4)
        if fun == 5:
            pygame.mixer.music.load(BGM4)
        if fun == 6:
            pygame.mixer.music.load(BGM4)
        pygame.mixer.music.play(-1)
        sv.music_playing = True
    else:
        pass

def title_spawn():
    sv.title.title_start(sv.boss.num,sv.boss2.num)

    ###############################################
# 소환하는 적 
#################################################
def boss_spawn(nm,nm2): # 보스 시작, 배경
    
    # 적이동을 위한 값
    boli = [sv.boss,sv.boss2]
    nuli = [nm,nm2]
    for boss,num in zip(boli, nuli):
        boss.image.fill((0,0,0,0))
        boss.move_dir = 0
        boss.move_speed = 0
        boss.move_point = (0,0)
        boss.ready = False
        boss.move_ready = False # 스펠 시작시 움직이는중?
        boss.godmod = False
        boss.dieleft = False
        boss.attack_start = False
        boss.real_appear = False
        boss.died_next_stage = False
        boss.image_num = 0
        boss.num = num
        boss.image.blit(pokemons[num],(0,0))  
        boss.radius = 90  
        boss.pos = (WIDTH+64,HEIGHT//2)
        boss.spell = sv.Spell(num,1500,False)     
        boss.radius /= 2
        boss.image2 = boss.image.copy()
        boss.appear = True
        boss.rect = boss.image.get_rect(center = (boss.pos))

def boss_attack(num,count,pos,ready,boss):
    if boss.code == 1:
        pos = set_bossmove_point((WIDTH-150,HEIGHT//2+50),60,3,boss)
    if boss.code == 2:
        pos = set_bossmove_point((WIDTH-150,HEIGHT//2-50),60,3,boss)
    if ready:
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
                bullet(pos,boss.list[0]+25,14,0,6,2,120-count)
                bullet(pos,boss.list[0]-25,14,0,6,2,120-count)
                bullet(pos,boss.list[0]+50,14,0,6,2,120-count)
                bullet(pos,boss.list[0]-50,14,0,6,2,120-count)
            if when_time(count,120):
                set_go_boss(5,randint(0,360),20,boss)
            if when_time(count,240):
                count = 0       
        if num == 3: # 파이어
            if count > 60:
                if when_time(count,61): s_lazer1.play()
                if while_time(count,1):
                    bullet(pos,look_at_player(pos)+10,20,0,1) 
                    bullet(pos,look_at_player(pos)-10,20,0,1)   
                if while_time(count,20):
                    bullet_effect(s_tan1,1,pos)
                    bullet(pos,randint(-10,10)+look_at_player(pos),5,15,1) 
            if count > 240:
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
                for i in range(3,12):
                    for j in range(0,360,5):
                        bullet(pos,j,i,9,4)
                set_go_boss(3,randint(0,360),20,boss)        
        if num == 12: # 레지락
            if while_time(count+60,120):
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
        if num == 22:
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
        if num == 23:
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
        if num == 24:
            if while_time(count+160,180):
                add_effect(pos,8)
            if while_time(count+120,180):
                rand = randint(0,300)
                rerand = rand + 60
                bullet_effect(s_boom,3,sv.player.pos)
                for i in range(0,360,5):
                    if not big_small(i,rand,rerand):
                        bullet(calculate_new_xy(sv.player.pos,400,i,True),look_at_player(calculate_new_xy(sv.player.pos,400,i,True))+180,3,2,3,24,double(sv.player.pos))
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
        if num == 30: # 크레세리아
            if while_time(count,4) and count < 60:
                bullet_effect(s_tan1,2,pos)
                for _ in range(0,6):
                    bullet(pos,randint(45,315),randfloat(3,6),3,2)        
            if when_time(count,60):
                set_go_boss(3,randint(0,360),50,boss)
            if while_time(count,4) and big_small(count,120,180):
                bullet_effect(s_tan1,2,pos)
                for _ in range(0,6):
                    bullet(pos,randint(45,315),randfloat(3,6),3,2)
            if while_time(count,20) and big_small(count,181,245):
                bullet_effect(s_tan1,2,pos)
                add_effect(pos,8,2)
                sv.boss.health += 50
                sv.boss2.health += 50
                for i in range(0,360,20):
                    bullet(pos,i+count*2.7,5,19,7)
            if when_time(count,260): count = 0
    if ready:pos = go_boss(boss)
    else:pos = calculate_new_xy(pos,boss.move_speed,boss.move_dir)
    return count,pos,ready
# 스테이지
def bullet_type(self,mod,sub):
    if mod == 1:
        if sub == 0:
            self.screen_die = 1
            if not sv.small_border.collidepoint(self.pos):
                rand_pos = (self.pos[0] + randint(-90,90),self.pos[1] + randint(-90,90))
                rand_num = randint(0,90)
                sbullet_effect(s_tan1,3,self.pos)
                for i in range(0,360,90):                       
                    sbullet(rand_pos,i+rand_num,12,6,4,1.1)
                self.kill()
        if sub == 1:
            self.screen_die = 1
            self.count += 1
            if self.count <= self.speed:
                self.speed -= 0.1
            elif self.count <= 90:
                self.speed = 0
            elif self.count <= 91:
                sbullet(self.pos,self.direction,4,4,3)
            else:
                self.speed = 6
    if mod == 2:
        self.count += 1
        if self.num <= self.count:
            sbullet_effect(s_tan2,6,self.pos)
            rand = randint(0,90)
            for i in range(0,360,180):
                sbullet(self.pos,i+rand,3,9,6)       
            self.kill()
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

    if mod == 27:
        self.count += 1
        if self.count > 240:
            add_effect(double(self.pos,True),7,1)
            self.kill()
    if mod == 28:
        if self.pos[0] <= self.num and self.speed > 0:
            self.speed -= 0.5

    if mod == 22: #반사탄
        if self.pos[0] > WIDTH*2:
            self.direction  = 180-self.direction
            self.pos = (WIDTH*2,self.pos[1])
        if self.pos[1] > HEIGHT*2: 
            self.direction  = -self.direction
            self.pos = (self.pos[0],HEIGHT*2)
        if self.pos[1] < 0:
            self.direction  = -self.direction
            self.pos = (self.pos[0],0)
    if mod == 23:
        if self.count == 0:self.screen_die = 2
        self.count += 1
        if distance((self.pos[0]//2,self.pos[1]//2),sv.boss.pos) <= 20:
            self.kill()

def magic_type(self,mod):
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
def stage_manager():    
    if sv.stage_end <= 0:
        if True:
            if sv.stage_condition == 1:
                add_effect((WIDTH/2,HEIGHT/2),99)
                sv.stage_fun += 1
                sv.stage_count = 0
                sv.stage_condition += 1
            if sv.stage_condition == 2:
                sv.stage_count += 1
                if sv.stage_count >= 60:
                    sv.stage_condition += 1
            if sv.stage_condition == 3:
                game_defalt_setting(sv.stage_fun)
                sv.player.pos = (WIDTH/4,HEIGHT/2)
                sv.stage_condition += 1
            if sv.stage_condition == 4:
                sv.stage_count += 1
                if sv.stage_count >= 180:
                    sv.stage_condition += 1
            if sv.stage_condition == 5:
                game_music_setting(sv.stage_fun)
                sv.stage_condition += 1
                sv.stage_count = 0
        if sv.stage_condition == 6:
            if not sv.boss.appear and not sv.boss.died_next_stage and not sv.boss2.died_next_stage: 
                stage_play()
                title_spawn()
            if not (sv.boss.died_next_stage and sv.boss2.died_next_stage):
                sv.stage_count -= 1
            if sv.stage_count > 0:                
                end_challenge(180) 
            sv.stage_cline = 0
    else:
        sv.stage_end -= 1

def stage_play():
    if sv.stage_fun == 1:
        if sv.stage_challenge == 0: boss_spawn(1,2) 
        if sv.stage_challenge == 1: boss_spawn(3,1) 
        if sv.stage_challenge == 2: boss_spawn(2,3) 
        if sv.stage_challenge == 3: boss_spawn(6,7) 
        if sv.stage_challenge == 4: boss_spawn(7,8) 
        if sv.stage_challenge == 5: boss_spawn(8,6) 
        if sv.stage_challenge == 6: boss_spawn(1,8) 
        if sv.stage_challenge == 7: boss_spawn(2,6) 
        if sv.stage_challenge == 8: boss_spawn(3,7) 
    if sv.stage_fun == 2:
        if sv.stage_challenge == 0: boss_spawn(12,13) 
        if sv.stage_challenge == 1: boss_spawn(13,27) 
        if sv.stage_challenge == 2: boss_spawn(14,28) 
        if sv.stage_challenge == 3: boss_spawn(12,27) 
        if sv.stage_challenge == 4: boss_spawn(14,13) 
        if sv.stage_challenge == 5: boss_spawn(14,12)  
        if sv.stage_challenge == 6: boss_spawn(12,28) 
        if sv.stage_challenge == 7: boss_spawn(28,13) 
        if sv.stage_challenge == 8: boss_spawn(14,27)
    if sv.stage_fun == 3:
        if sv.stage_challenge == 0: boss_spawn(15,16) 
        if sv.stage_challenge == 1: boss_spawn(16,30) 
        if sv.stage_challenge == 2: boss_spawn(22,23) 
        if sv.stage_challenge == 3: boss_spawn(23,24) 
        if sv.stage_challenge == 4: boss_spawn(22,24)
        if sv.stage_challenge == 5: boss_spawn(15,22) 
        if sv.stage_challenge == 6: boss_spawn(24,30)  
        if sv.stage_challenge == 7: boss_spawn(23,16) 
        if sv.stage_challenge == 8: boss_spawn(30,15) 
        