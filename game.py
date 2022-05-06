from re import I
import pygame, math
from random import randint
from pygame.locals import *

import time
import start as st
import stage_var as sv
from norm_func import *
from spec_func import background_scroll
from start import render_layer, WIDTH, HEIGHT, TITLE, FONT_1, FONT_2, score_font, menu_img, monitor_size, up_render_layer,skill_surface, debug_font, sound_channel
from start import s_boom,s_life, s_cancel, s_release,s_cat1, s_invalid,s_ch0, s_ch2, s_dark,s_damage0, s_good,s_damage1, s_enedead, s_enep1, s_enep2, s_graze, s_item0, s_kira0, s_kira1, s_lazer1, s_kak,s_ok, s_pause, s_pldead, s_plst0, s_select, s_slash, s_tan1, s_tan2, s_piyo, s_shoot, s_nodam
from stage import stage_manager, game_music_setting
# 게임에 핵심적인 기능만 주석을 넣었습니다 ##

screen = pygame.display.set_mode((WIDTH*2,HEIGHT*2))
    # 플레이어
def music_and_sfx_volume(m,s):
    try:s = s/100
    except:s = 0
    try:m = m/100
    except:m = 0
    pygame.mixer.music.set_volume(m)
    s_life.set_volume(s*1.5)
    st.s_piyo2.set_volume(s*0.5)
    s_lazer1.set_volume(s)
    s_tan1.set_volume(s)
    s_tan2.set_volume(s)
    s_ch2.set_volume(s)
    s_ch0.set_volume(s)
    s_cat1.set_volume(s)
    s_enep1.set_volume(s)
    s_enep2.set_volume(s)
    s_slash.set_volume(s*2)
    s_pldead.set_volume(s)
    s_plst0.set_volume(s)
    s_damage0.set_volume(s*2)
    s_damage1.set_volume(s*2)
    s_graze.set_volume(s)
    s_kira0.set_volume(s)
    s_kira1.set_volume(s)
    s_boom.set_volume(s)
    s_item0.set_volume(s)
    s_enedead.set_volume(s)
    s_ok.set_volume(s)
    s_cancel.set_volume(s)
    s_select.set_volume(s)
    s_pause.set_volume(s)
    s_piyo.set_volume(s*2)
    s_shoot.set_volume(s)
    s_nodam.set_volume(s)
    s_release.set_volume(s*0.5)
    s_kak.set_volume(s*1.5)
    s_dark.set_volume(s*1.5)
    s_good.set_volume(s*2)
    s_invalid.set_volume(s*2)
def all_reset(reset):
    if not reset:
        sv.music_playing = False #
        sv.play = True #
        sv.cur_full_mod = False #    
        sv.frame_count = 0 #
        sv.cur_count = 0 #
        sv.time_stop = False #
        sv.stage_count = 0 #
        sv.screen_shake_count = 0 #        
        sv.game_clear = False #   
        sv.curser = sv.stage_challenge #
        sv.character = 0 #
        sv.cur_screen = 0 #        
        sv.stage_end = 0 #        
        sv.practicing = False #
       
    # 게임 시작전 메뉴 변수들
    sv.pause = False
    sv.all_trig = False #
    sv.stage_line = 0
    sv.stage_cline = 0
    sv.stage_repeat_count = 0
    sv.stage_condition = 1
    sv.skill_activating = []
    sv.levelup = False
    sv.boss = sv.Boss_Enemy(1)
    sv.boss2 = sv.Boss_Enemy(2)
    sv.boss_group = pygame.sprite.Group(sv.boss2,sv.boss)
    sv.enemy_group = pygame.sprite.Group()
    sv.spr = pygame.sprite.Group()
    sv.magic_spr = pygame.sprite.Group()
    sv.player = sv.Player(-125,-125,5,500)
    sv.player_group = pygame.sprite.Group(sv.player)
    sv.player_hitbox = sv.Player_hit()
    sv.skillobj_group = pygame.sprite.Group()
    sv.title = sv.Tittle(1)
    sv.ui = sv.UI(1)
    sv.under_ui = sv.Under_PI()
    sv.beams_group = pygame.sprite.Group()
    sv.effect_group = pygame.sprite.Group()
    sv.item_group = pygame.sprite.Group()
    sv.starting = True
    sv.read_end = False
    if reset:
        sv.pause_lock = False
        sv.player.skill_list = []
        sv.player.power = 400
        st.score = 0    
        sv.stage_fun -= 1
        sv.stage_playing = sv.stages[sv.stage_fun][sv.stage_challenge] 
    sv.player.skill_list.append(sv.Skill(1,4,st.other[0],st.other[1],2,90,200))
    sv.player.skill_list.append(sv.Skill(2,5,st.other[2],st.other[3],3,90,50))
    sv.player.skill_list.append(sv.Skill(3,0,st.other[4],st.other[5],5,120,80))

def play_game():
    global screen
    all_reset(False)
    music_and_sfx_volume(st.music_volume,st.sfx_volume)    
    count = 0
    bgx = 0

    ################################################# 
    while sv.play:
        # 60 프레임
        st.clock.tick(st.clock_fps)
        st.TARGET_FPS = st.clock_fps
        now = st.time.time()        
        st.dt = (now-st.prev_time)*st.TARGET_FPS        
        st.prev_time = now
        keys = pygame.key.get_pressed() 
        if sv.cur_screen == 1:
            # 키 이벤트
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: # 게임끄기
                    pygame.quit()
                    exit()
                if ev.type == pygame.KEYDOWN:    
                    if not sv.pause:                
                        if ev.key == pygame.K_ESCAPE and sv.frame_count >= 60:
                            s_pause.play()
                            sv.pause = True                      
                        if ev.key == pygame.K_z and sv.player.gatcha >= sv.player.gatcha_max:
                            if sv.player.shoot_gatcha > 0:
                                sv.beams_group.add(sv.Beam(get_new_pos(sv.player.pos,5),4))
                            if sv.player.shoot_gatcha == 0:
                                sv.player.shoot_gatcha = 20                                                            
                        if (ev.key == pygame.K_x or ev.key == pygame.K_c) and sv.player.skill_list[sv.player.skill_pointer].pp > 0 and not sv.skill_activating and not sv.player.godmod:
                            sound_channel[1].play(s_slash)
                            sv.player.skill_list[sv.player.skill_pointer].pp -= 1       
                            sv.skill_activating.append(sv.Skill_Core(sv.player.skill_list[sv.player.skill_pointer].num,sv.player.skill_list[sv.player.skill_pointer].cool))
                        if ev.key == pygame.K_d:
                            sv.player.skill_list.append(sv.player.skill_list.pop(0))
                        if ev.key == pygame.K_s:
                            sv.player.skill_list.insert(0,(sv.player.skill_list.pop(2)))
                    else:
                        if ev.key == pygame.K_UP:
                            s_ok.play()
                            sv.curser = 2 if sv.curser == 0 else sv.curser-1
                        if ev.key == pygame.K_DOWN:
                            s_ok.play()
                            sv.curser = 0 if sv.curser == 2 else sv.curser+1
                        if ev.key == pygame.K_z:
                            s_select.play()
                            if sv.curser == 0: 
                                if sv.pause_lock:
                                    sv.curser = 1                                   
                                    if sv.stage_challenge+1 >= len(sv.stages[sv.stage_fun-1]):
                                        sv.curser = 2
                                    else:
                                        sv.stage_challenge += 1
                                elif sv.player.died:
                                    sv.curser = 1
                                else:
                                    sv.pause = False
                            if sv.curser == 1:
                                all_reset(True)
                                            
                            if sv.curser == 2: 
                                sv.stage_fun -= 1
                                sv.pause_lock = False
                                st.game_restart = True
                        if ev.key == pygame.K_ESCAPE:
                            if not sv.pause_lock:
                                sv.pause = False
            # 재시작이면 반복 나가기
            if st.game_restart:
                sv.frame_count = 0
                break
            
            # 탄에 박았는가
            hit_list = pygame.sprite.spritecollide(sv.player_hitbox, sv.spr, False, pygame.sprite.collide_circle)
            sv.boss.rect.center = get_new_pos(sv.boss.rect.center,-50)     
            sv.boss2.rect.center = get_new_pos(sv.boss2.rect.center,-50)             
            boss_collide = pygame.sprite.spritecollide(sv.boss, sv.beams_group, False, pygame.sprite.collide_circle)            
            boss2_collide = pygame.sprite.spritecollide(sv.boss2, sv.beams_group, False, pygame.sprite.collide_circle)
            sv.boss.rect.center = get_new_pos(sv.boss.rect.center,50)  
            sv.boss2.rect.center = get_new_pos(sv.boss2.rect.center,50)  
            
            # 연산 업데이트
            
            if not sv.pause:  
                if not sv.time_stop:    
                    if sv.magic_spr.sprites():sv.magic_spr.update(screen)    
                    if sv.skill_activating:
                        for skill in sv.skill_activating[:]:
                            skill.update(sv.boss)
                            if skill.cool <= 0 and skill.draw_cool <= 0: sv.skill_activating.remove(skill)
                    if sv.skillobj_group: sv.skillobj_group.update(screen)
                    sv.spr.update(screen)                
                    if sv.beams_group: sv.beams_group.update()                            
                    sv.player_group.update(hit_list,keys)
                    sv.player_hitbox.update()
                    if sv.enemy_group:sv.enemy_group.update()
                    if sv.item_group: sv.item_group.update()
                    sv.boss.update(boss_collide)
                    sv.boss2.update(boss2_collide)
                if sv.time_stop:
                    if sv.boss.dont_stop: sv.boss.update(boss_collide)
                    if sv.boss2.dont_stop: sv.boss2.update(boss2_collide)
                if not sv.time_stop: 
                    if sv.effect_group: sv.effect_group.update()
                    stage_manager()
                    sv.frame_count += 1
                    sv.stage_count += 1
                    if not st.bkgd_list == []:
                        for i in st.bkgd_list:i.update()

            # 그리기 시작
            if sv.frame_count >= 60:
                if not sv.pause:
                    background_scroll() 
                    if sv.title.count < sv.title.count_max: sv.title.draw()              
                    skill_surface.fill((0,0,0,0))
                    if sv.skill_activating:                    
                        for skill in sv.skill_activating[:]:
                            skill.draw(skill_surface)
                    if sv.skillobj_group: sv.skillobj_group.draw(skill_surface)
                    render_layer.blit(skill_surface,(0,0))              
                    sv.item_group.draw(render_layer)
                    sv.magic_spr.draw(render_layer)      
                    sv.beams_group.draw(render_layer)  
                    if (not sv.player.died):sv.player_group.draw(render_layer) 
                    sv.enemy_group.draw(render_layer)            
                    if not sv.starting or sv.read_end: sv.enemy_group.draw(render_layer)
                    sv.under_ui.draw(keys)
                    sv.boss_group.draw(render_layer)
                    
                    screen.blit(pygame.transform.scale2x(render_layer),(0,0))                    
                    sv.spr.draw(screen)
                    up_render_layer.fill((255,255,255,0))
                    sv.effect_group.draw(up_render_layer)   
                    sv.player.skill_list[sv.player.skill_pointer].draw()                  
                   
                    sv.ui.draw()
                    if sv.boss.spell and sv.boss.appear:sv.boss.spell.draw()                  
                    screen.blit(pygame.transform.scale2x(up_render_layer),(0,0))
                    if sv.screen_shake_count > 0:
                        screen.blit(screen,(randint(-20,20),randint(-20,20)))
                        sv.screen_shake_count -= 1
                else: 
                    screen.blit(pygame.transform.scale2x(render_layer),(0,0))
                    sv.spr.draw(screen)
                    screen.blit(pygame.transform.scale2x(up_render_layer),(0,0))
                    pause_menu = pygame.Surface((WIDTH,HEIGHT), SRCALPHA)  
                    pause_menu.fill((255, 0, 85,100))
                    pause_menu.blit(menu_img,(10,100),(160,48,160,32))
                    for i in range(0,3): # 메뉴 그리기
                        menu = pygame.Surface((256,32), SRCALPHA)
                        if sv.curser == i: menu.fill((0,0,0,200))
                        if i == 0:
                            if sv.player.died:
                                menu.blit(menu_img,(0,0),(160,144,256,32))
                            elif sv.pause_lock:
                                menu.blit(menu_img,(0,0),(160,112,256,32))
                            else:
                                menu.blit(menu_img,(0,0),(160,80,256,32))
                        else:menu.blit(menu_img,(0,0),(160,112+32*i,160,32))
                        pause_menu.blit(menu,(0,200+32*i))
                    screen.blit(pygame.transform.scale2x(pause_menu),(0,0))     
            else:pass 
            
            text_color = (255,255,255)
            text1 = debug_font.render(str(len(sv.spr.sprites())), True, text_color)
            screen.blit(text1,(980,650)) 
            
            pygame.display.flip()       
        if sv.cur_screen == 0:
            if sv.frame_count == 0:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(TITLE)
                pygame.mixer.music.play(-1)
                sv.frame_count -= 1
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: # 게임끄기
                    sv.play = False
                if ev.type == pygame.KEYDOWN:   
                    if ev.key == pygame.K_UP:
                        sv.curser = curser_max if sv.curser == 0 else sv.curser - 1 # 커서위로
                        st.s_ok.play()
                    if ev.key == pygame.K_DOWN:
                        sv.curser = 0 if sv.curser == curser_max else sv.curser + 1 # 커서밑으로
                        st.s_ok.play()
                    if sv.select_mod == 0: # 시작화면
                        if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                            st.s_select.play()
                            if sv.curser == 5: sv.play = False # 게임끄기
                            else:sv.select_mod += 1 ############ 게임시작
                            sv.menu_mod.append(sv.curser) # 현재 어떤 버튼 눌렀는지 저장
                            sv.curser = 0
                            if sv.menu_mod[0] == 4:
                                sv.play = False 
                            break
                    if sv.select_mod == 1:
                        if sv.menu_mod[0] == 0:
                            if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                pygame.mixer.music.stop()
                                s_select.play()
                                sv.character = 0
                                sv.player.power = 400                                  
                                sv.stage_challenge = sv.curser
                                sv.stage_playing = sv.stages[sv.stage_fun][sv.stage_challenge]
                                sv.frame_count = 0
                                sv.curser = 0
                                sv.cur_screen = 1
                                break    
                            if ev.key == pygame.K_RIGHT:
                                s_ok.play()
                                sv.stage_fun += 1 
                                if sv.stage_fun == len(sv.stages): sv.stage_fun = 0                             
                            if ev.key == pygame.K_LEFT:
                                s_ok.play()
                                sv.stage_fun -= 1 
                                if sv.stage_fun == -1: sv.stage_fun = len(sv.stages)-1                            
                            if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                s_cancel.play()
                                sv.curser = 0
                                sv.select_mod -= 1
                                del sv.menu_mod[len(sv.menu_mod)-1]      
                                break                
                        if sv.menu_mod[0] == 1:
                            if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                s_cancel.play()
                                sv.curser = 0
                                sv.select_mod -= 1
                                del sv.menu_mod[len(sv.menu_mod)-1]   
                                break
                        if sv.menu_mod[0] == 2:
                            if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                s_cancel.play()
                                sv.curser = 0
                                sv.select_mod -= 1
                                del sv.menu_mod[len(sv.menu_mod)-1]   
                                break
                        if sv.menu_mod[0] == 3:
                            if ev.key == pygame.K_RIGHT:
                                s_ok.play()
                                if sv.curser == 0:
                                    sv.st.full_on = 1 if sv.st.full_on == 0 else 0
                                if sv.curser == 1:
                                    st.music_volume = st.music_volume + 5 if st.music_volume < 100 else 100
                                if sv.curser == 2:
                                    st.sfx_volume = st.sfx_volume + 5 if st.sfx_volume < 100 else 100                                
                            if ev.key == pygame.K_LEFT:
                                s_ok.play()
                                if sv.curser == 0:
                                    st.full_on = 1 if st.full_on == 0 else 0
                                if sv.curser == 1:
                                    st.music_volume = st.music_volume - 5 if st.music_volume > 0 else 0
                                if sv.curser == 2:
                                    st.sfx_volume = st.sfx_volume - 5 if st.sfx_volume > 0 else 0
                            if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                s_cancel.play()
                                music_and_sfx_volume(st.music_volume,st.sfx_volume)
                                with open('resources\setting.txt','w',encoding="UTF-8") as f:
                                    f.write("fullscreen"+"="+str(st.full_on)+"\n")
                                    f.write("sfx"+"="+str(st.sfx_volume)+"\n")
                                    f.write("bgm"+"="+str(st.music_volume)+"\n")
                                sv.curser = 0
                                sv.select_mod -= 1
                                del sv.menu_mod[len(sv.menu_mod)-1]     
                                break 
                                            
            if st.game_restart:
                sv.frame_count = 0
                break    
            
            # 배경과 폴리곤
            if True:
                rel_x = bgx % WIDTH
                render_layer.blit(st.background_img, (rel_x - WIDTH,0))
                if rel_x < WIDTH:
                    render_layer.blit(st.background_img,(rel_x,0))

                rel_x = bgx % 1022
                sub_bg = pygame.Surface((1022,82), SRCALPHA)
                sub_bg.blit(st.background2_img, (rel_x - 1022,0))    
                if rel_x < 1022:
                    sub_bg.blit(st.background2_img,(rel_x,0)) 
                sub_bg = pygame.transform.rotate(sub_bg, 85) 
                sub_bg.fill((0, 0, 255, 150), special_flags=pygame.BLEND_RGBA_MULT)
                render_layer.blit(sub_bg,(0,-50))

                rel_x = -bgx % 1022
                sub_bg = pygame.Surface((1022,82), SRCALPHA)
                sub_bg.blit(st.background2_img, (rel_x - 1022,0))    
                if rel_x < 1022:
                    sub_bg.blit(st.background2_img,(rel_x,0)) 
                sub_bg = pygame.transform.rotate(sub_bg, -5) 
                sub_bg.fill((0, 0, 255, 150), special_flags=pygame.BLEND_RGBA_MULT)
                render_layer.blit(sub_bg,(0,50))

                rel_x = bgx % 1022
                sub_bg = pygame.Surface((1022,82), SRCALPHA)
                sub_bg.blit(st.background2_img, (rel_x - 1022,0))    
                if rel_x < 1022:
                    sub_bg.blit(st.background2_img,(rel_x,0)) 
                sub_bg = pygame.transform.rotate(sub_bg, 30) 
                sub_bg.fill((0, 0, 255, 150), special_flags=pygame.BLEND_RGBA_MULT)
                render_layer.blit(sub_bg,(0,-50))

                bgx += 1         
                ui_x = WIDTH - 220
                ui_y = 150
                count += 1

                poli_mask = pygame.mask.from_surface(st.poligon)
                poli_mask = poli_mask.to_surface()
                poli_mask.set_colorkey((0,0,0))
                poli_mask.fill((0,0,255), special_flags=pygame.BLEND_RGBA_MULT)
                render_layer.blit(poli_mask, (10,150+math.sin(math.radians(count*2)) * 5))

            # 그리기
            if sv.select_mod == 0: # 시작화면
                curser_max = 4
                render_layer.blit(st.title_img,(0,0))# 타이틀
                for i in range(0,5): # 메뉴 그리기
                    menu = pygame.Surface((160,32), SRCALPHA)
                    if sv.curser == i: menu.fill((0,0,255,200))
                    menu.blit(st.menu_img,(0,0),(0,48+32*i,320,48))
                    render_layer.blit(menu,(ui_x,ui_y+32*i))
            if sv.select_mod == 1: # 다음옴션
                if sv.menu_mod[0] == 0: # 시작>난이도 정하기
                    curser_max = len(sv.stages[sv.stage_fun])-1
                    if sv.curser > curser_max: sv.curser = curser_max
                    text_color = (0,0,255)
                    text1 = score_font.render("BOX"+str(sv.stage_fun+1), True, text_color)
                    render_layer.blit(text1,(240,50))
                    for i in range(0,len(sv.stages[sv.stage_fun])):
                        
                        text_color = (246, 255, 0) if list(sv.stages[sv.stage_fun][i]) in st.score_index  else  (0,0,255)
                        if i == sv.curser: text_color = (255,0,255) 
                        text1 = score_font.render(str(sv.stage_fun+1) +"-"+str(i+1), True, text_color)
                        render_layer.blit(text1,(240,60+25*(i+1)))  

                    txtli = ["","",""]
                    # 스코어 보드
                    if list(sv.stages[sv.stage_fun][sv.curser]) in st.score_index: 
                        asd = sv.stages[sv.stage_fun][sv.curser]
                        txtli[0] = st.pk_name[asd[1]-1]    
                        txtli[1] = st.pk_name[asd[0]-1] 
                        txtli[2] = str(st.score_value[st.score_index.index(list(sv.stages[sv.stage_fun][sv.curser]))]).zfill(10)
                    else: # 스코어 없으면 nan
                        txtli = [st for st in ['NaN','NaN','NaN']]
                    score_b = pygame.Surface((300,200), SRCALPHA)
                    score_b.fill((0,0,0,200))
                    render_layer.blit(score_b,(320,40))
                    for i in range(0,3):
                        text1 = score_font.render(txtli[i], True, (0,0,255))
                        render_layer.blit(text1,(350,50+50*i))
                   
                if sv.menu_mod[0] == 1: # 설명
                    font = pygame.font.Font(FONT_2, 20)
                    pygame.draw.rect(render_layer, (0,0,0), (20,20,WIDTH-40,HEIGHT-40), width=0)
                    for texta in range(0,len(st.htp_scroll)):
                        text1 = font.render(st.htp_scroll[texta], True, (255,255,255))
                        render_layer.blit(text1,(40,30*texta+30))
                if sv.menu_mod[0] == 2: # 크레딧
                    font = pygame.font.Font(FONT_2, 10)
                    pygame.draw.rect(render_layer, (0,0,0), (20,20,WIDTH-40,HEIGHT-40), width=0)
                    for texta in range(0,len(st.credit_scroll)):
                        text1 = font.render(st.credit_scroll[texta], True, (255,255,255))
                        render_layer.blit(text1,(30,10*texta+30))
                if sv.menu_mod[0] == 3: # 설정
                    curser_max = 2
                    text_box = ["Mod","Music","Sound"]
                    text_box[0] = "Mod    Window" if st.full_on == 0 else "Mod    Window"
                    text_box[1] = "Music   " + str(st.music_volume)
                    text_box[2] = "Sound  " + str(st.sfx_volume)
                    for i in range(0,3):
                        text_color = (255,0,255) if i == sv.curser else (0,0,255)
                        text1 = score_font.render(text_box[i], True, text_color)
                        render_layer.blit(text1,(200,100+40*i))                    
            if sv.frame_count > 0:
                sv.frame_count -= 1
                if sv.frame_count == 0:
                    sv.character = 0 if sv.curser == 0 else 41
                    sv.player.power = 0
                    sv.cur_screen = 1  
                    sv.stage_fun = 0
                    sv.start_fun = sv.stage_fun  
                    sv.curser = 0 

            if sv.cur_screen == 0:screen.blit(pygame.transform.scale2x(render_layer),(0,0))
            pygame.display.flip()
        # 전체화면
        if st.full_on != sv.cur_full_mod:
            if st.full_on:
                screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN|pygame.SCALED)
            else:
                screen = pygame.display.set_mode((WIDTH*2, HEIGHT*2))
            sv.cur_full_mod = st.full_on
    if st.game_restart:
        st.game_restart = False
        all_reset(False)
        play_game()

if __name__ == "__main__":
    play_game()

