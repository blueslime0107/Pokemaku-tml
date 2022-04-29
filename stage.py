from numpy import s_
import start as st
from start import WIDTH,HEIGHT, bg_image, pokemons, boss_movebox, small_border, BGM1,BGM2,BGM3,BGM4,BGM5
from spec_func import *
import stage_var as sv
import pygame, math
from random import randint, choice
from start import s_lazer1, s_enep2, s_ch0,  s_tan1, s_tan2, s_boom
from norm_func import *
from boss import boss_file, boss_levelup

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
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,0,540,120),1))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,120,540,120),2))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,240,540,120),3))      
    if fun == 2:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1080,540,187),2))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(540,1170,540,97),3))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1267,540,173),4,))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(540,1080,540,90),5,))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(540,1350,640,90),5,))       
    if fun == 3:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(540,360,540,75),0.1))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,390,540,90),2))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,480,540,30),3))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,510,540,90),4))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,600,540,120),5))
    if fun == 4:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(540,360,540,75),0.1))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,390,540,90),2))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,480,540,30),3))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,510,540,90),4))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,600,540,120),5))
    if fun == 5:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(540,360,540,75),0.1))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,390,540,90),2))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,480,540,30),3))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,510,540,90),4))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,600,540,120),5))
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
            pygame.mixer.music.load(BGM3)
        if fun == 4:
            pygame.mixer.music.load(BGM4)
        if fun == 5:
            pygame.mixer.music.load(BGM5)
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
        if sv.levelup:count = boss_levelup(num,pos,boss,count)
        else:count = boss_file(num,pos,boss,count)
    
    if ready:pos = go_boss(boss)
    else:pos = calculate_new_xy(pos,boss.move_speed,boss.move_dir)
    return count,pos,ready
# 스테이

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
    boss_spawn(sv.stage_playing[0],sv.stage_playing[1])

        