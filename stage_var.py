import pygame, math
from random import randint
from pygame.locals import *
import start as st
from start import render_layer,bullets, WIDTH, HEIGHT, small_border, FONT_1, font1, bullet_border, pokemons, items,near_border, boss_movebox,screen_rect, up_render_layer,far_border
from start import magic_circle_sprite, white_circle, died_white_circle,bullet_erase,boss_circle,bullet_size
from start import s_boom, s_cat1, s_ch0, s_ch2, s_damage0, s_damage1, s_enedead, s_good,s_enep1, s_graze, s_item0, s_invalid,s_pldead, s_plst0, s_tan1, s_tan2,s_piyo,s_shoot, s_nodam
from start import item_channel, plst_channel, graze_channel ,enemy_boom_channel, black_screen, enemy_died_circle, bullet_taning, died_channel, damage_channel, sound_channel
from stage import boss_attack
from boss import bullet_type, bullet_levelup, magic_type
from start import WIDTH, HEIGHT
from norm_func import *
from spec_func import *
 
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, health):
        pygame.sprite.Sprite.__init__(self) # 초기화?
        self.image = pygame.Surface((128, 128), pygame.SRCALPHA) # 이미지          
        self.image.blit(st.pokemons[0],(0,-5)) # 이미지 위치조정
        self.rect = self.image.get_rect(center = (round(x), round(y)))
        self.image2 = self.image.copy()
        self.img_num = 0
        self.pos = (x,y)  
        self.real_pos = (x*2,y*2)          
        self.speed = speed
        self.max_health = health
        self.health = health
        self.power = 0
        self.mp = 8
        self.before_health = 0
        self.count = 0
        self.godmod = False # 무적?
        self.godmod_count = 0
        self.max_godmod_count = 0
        self.hit_speed = 0
        self.hit_dir = 0
        self.skill_list = []
        self.skill_pointer = 0
        self.gatcha = 0
        self.gatcha_max = 50
        self.died = False
        self.gihapetii = True
        self.shoot_gatcha = 0
    def update(self,collide,keys):
        global pause, screen_shake_count
        if self.health > self.max_health: self.health = self.max_health
        if not self.died:
            dx, dy = 0 , 0
            inum = self.img_num
            self.img_num = 0
            # 플레이어 이동 조종 SHIFT 를 누르면 느리게 움직이기
            if keys[pygame.K_LSHIFT]:self.speed = 2
            else:
                self.speed = 4       
            # 화면 밖으로 안나감
            if keys[pygame.K_RIGHT]:dx += 0 if self.rect.centerx >= WIDTH-10 else self.speed            
            if keys[pygame.K_LEFT]:dx -= 0 if self.rect.centerx <= 0 + 10 else self.speed            
            if keys[pygame.K_DOWN]:dy += 0 if self.rect.centery >= HEIGHT-10 else self.speed               
            if keys[pygame.K_UP]:dy -= 0 if self.rect.centery <= 0+10 else self.speed
            if self.rect.centerx <= -100: 
                dx = 0
                dy = 0
            
            # 총 쏘기 이벤트
            if keys[pygame.K_z] and frame_count % 4 == 0:
                plst_channel.play(s_plst0)
                beams_group.add(Beam(get_new_pos(player.pos,20,15)))
                beams_group.add(Beam(get_new_pos(player.pos,20,-15)))
                if self.power > 200:
                    beams_group.add(Beam(get_new_pos(player.pos,20,15),2,-10))
                    beams_group.add(Beam(get_new_pos(player.pos,20,-15),2,10))
            if self.shoot_gatcha > 0:self.shoot_gatcha -= 1

            # 모양이 바꼈을 때만 모양 업데이트
            self.img_num = self.img_num + keys[pygame.K_RIGHT] + keys[pygame.K_LEFT]*2
            if inum != self.img_num:
                if self.img_num == 0:self.image = self.image2                
                if self.hit_speed == 0:
                    if self.img_num == 1:self.image = pygame.transform.rotate(self.image2, -10)
                    if self.img_num == 2:self.image = pygame.transform.rotate(self.image2, 10)                      
                self.rect = self.image.get_rect(center = (round(self.pos[0]),round(self.pos[1])))

            # 탄에 닿았을때
            if len(collide) > 0 and not self.godmod and not collide[0].ghost:
                if not collide[0].radius >= 19: collide[0].kill()
                s_pldead.play()
                self.godmod = True
                self.before_health = self.health
                damage = round(collide[0].radius/2 * 7 * (collide[0].speed/2+1))
                self.health -= damage
                if self.gihapetii and self.health <= 0:
                    sound_channel[6].play(st.s_life)
                    self.health=1
                    self.gihapetii = False
                self.hit_speed = 5
                self.hit_dir = -collide[0].direction
                self.godmod_count = round(2*damage//4) # 데미지마다 무적시간 변경
                if self.godmod_count > 70: self.godmod_count = 70
                self.max_godmod_count = self.godmod_count
            
            # 무적이면 2초뒤 풀리기
            if self.godmod and self.hit_speed <= 0:
                boss.spell_clear = False
                self.godmod_count -= 1
                if 0 >= self.godmod_count:
                    self.godmod = False
            
            self.gatcha += 0.1
            if self.gatcha >= self.gatcha_max and self.gatcha < self.gatcha_max+60: 
                sound_channel[0].play(s_piyo)
                self.gatcha += 999
            
            # 넉백
            if self.hit_speed > 0:
                self.pos = calculate_new_xy(self.pos, self.hit_speed, self.hit_dir)
                if self.hit_speed > 0:
                    self.hit_speed -= 0.1
                    if self.hit_speed <= 0: 
                        self.hit_speed = 0
                        if self.health <= 0:
                            screen_shake_count = 90
                            died_channel.play(s_enep1)
                            add_effect(get_new_pos(self.pos,100,0),5)         
                            add_effect(get_new_pos(self.pos,-100,0),5)      
                            add_effect(get_new_pos(self.pos,0,100),5)      
                            add_effect(get_new_pos(self.pos,0,-100),5)    
                            add_effect(self.pos,5)                                             
                            self.died = True
            else:
                # 키보드 먹히기
                self.pos = (self.pos[0] + dx*st.dt, self.pos[1] + dy*st.dt) 
            if self.pos[0] <= 10: self.pos = (10,self.pos[1])
            if self.pos[0] >= WIDTH-10: self.pos = (WIDTH-10,self.pos[1])
            if self.pos[1] <= 10: self.pos = (self.pos[0],10)
            if self.pos[1] >= HEIGHT-10: self.pos = (self.pos[0],HEIGHT-10)
            self.real_pos = (self.pos[0]*2,self.pos[1]*2)            
            self.rect.center = round(self.pos[0]), round(self.pos[1]) 
        if self.died:
            if self.count < 120:self.count += 1
            else:pause = True           
class Player_hit(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface((6,6)) # 이미지  
        self.rect = self.image.get_rect()
        self.pos = (0,0)
        self.radius = 3
    def update(self):
        self.pos = (player.pos[0]*2,player.pos[1]*2)
        self.rect.center = self.pos    
class Tittle():
    def __init__(self,value):
        self.stage = value
        self.count = 999
        self.save = 1
        self.name1 = " 1"
        self.name2 = "드넓은 초원"
        self.defalt = [st.other[6],st.other[7]]
        self.pos = [st.WIDTH//2+50,st.HEIGHT//2]
        self.pos_stage = [st.WIDTH//2+10,st.HEIGHT//2-20]
        self.count_max = 180
        self.more = 1
        self.bool = False
        self.font1 = pygame.font.Font(FONT_1, 50)
        self.font2 = pygame.font.Font(FONT_1, 90)
    def draw(self):
        if self.count < 600:
            if when_time(self.count,0):s_ch2.play()
            self.textfun(self.defalt[0],(35,35),0)
        if self.count > 60:
            if when_time(self.count,61):s_cat1.play()
            pos = (100,220) if st.lang == 1 else (50,220)
            if self.bool:
                self.textfun(self.name2,(50,40),1)
                self.textfun(self.name1,(100,220),1)
            else:
                self.textfun(self.name2,(50,40),2)
                self.textfun(self.name1,(100,220),2)
            if while_time(self.count,4):
                if self.bool: self.bool = False
                else: self.bool = True
            self.textfun(self.defalt[1],(WIDTH-100,HEIGHT-100) if st.lang == 1 else (WIDTH-250,HEIGHT-100),0)
            if self.count > 90: self.more = self.more*1.1
        self.count += 1
            
    def title_start(self,val,name):
        self.count = 0
        self.save = 1
        self.more = 1
        self.bool = False
        self.name1 = pokemon_name(val)
        self.name2 = pokemon_name(name)
        self.pos = [WIDTH//2+50,HEIGHT//2]
        self.pos_stage = [WIDTH//2+10,HEIGHT//2-20]
    def textfun(self,texts,pos,mod):
        if mod == 0:
            oh = self.font1.render(texts,True,"white")
            oh2 = self.font1.render(texts,True,(0,0,0))
            render_layer.blit(oh2,get_new_pos(get_new_pos(pos,self.more),4,4))
            render_layer.blit(oh2,get_new_pos(get_new_pos(pos,self.more),-4,4))
            render_layer.blit(oh2,get_new_pos(get_new_pos(pos,self.more),4,-4))
            render_layer.blit(oh2,get_new_pos(get_new_pos(pos,self.more),-4,-4))
            render_layer.blit(oh,get_new_pos(pos,self.more))
        if mod == 1:
            oh = self.font2.render(texts,True,(214,230,245))
            oh2 = self.font2.render(texts,True,"white")
            oh_rect = oh.get_rect()
            oh_rect.centerx = WIDTH//2
            pos = (oh_rect.topleft[0],pos[1])
            render_layer.blit(oh2,get_new_pos(get_new_pos(pos,self.more),5,5))
            render_layer.blit(oh2,get_new_pos(get_new_pos(pos,self.more),-5,5))
            render_layer.blit(oh2,get_new_pos(get_new_pos(pos,self.more),5,-5))
            render_layer.blit(oh2,get_new_pos(get_new_pos(pos,self.more),-5,-5))
            render_layer.blit(oh,get_new_pos(pos,self.more))
        if mod == 2:
            oh = self.font2.render(texts,True,"white")
            oh2 = self.font2.render(texts,True,(214,230,245))
            oh_rect = oh.get_rect()
            oh_rect.centerx = WIDTH//2
            pos = (oh_rect.topleft[0],pos[1])
            render_layer.blit(oh2,get_new_pos(get_new_pos(pos,self.more),5,5))
            render_layer.blit(oh2,get_new_pos(get_new_pos(pos,self.more),-5,5))
            render_layer.blit(oh2,get_new_pos(get_new_pos(pos,self.more),5,-5))
            render_layer.blit(oh2,get_new_pos(get_new_pos(pos,self.more),-5,-5))
            render_layer.blit(oh,get_new_pos(pos,self.more))
class Beam(pygame.sprite.Sprite):
    def __init__(self, pos, num=0, dir=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,16), pygame.SRCALPHA)                   
        self.rect = self.image.get_rect(center = get_new_pos(pos))            
        self.pos = get_new_pos(pos)
        self.num = num
        self.speed = 0
        self.direction = dir           
        self.damage = 0
        self.radius = 20
        self.appear = True
        self.died = False
        self.effect = False
        if self.num == 0: # 메인
            self.image.fill((82,140,255))
            pygame.draw.rect(self.image, (82,181,255), (1,1,18,14),0)
            self.speed = 40
            self.damage = 1
        if self.num == 2: # 서브
            self.image.fill((247,165,165))
            pygame.draw.rect(self.image, (239,99,107), (0,0,20,16),2)
            self.speed = 40
            self.damage = 2
        if self.num == 4: # 포켓몬
            s_shoot.play()
            self.image = pygame.Surface((48, 16), pygame.SRCALPHA)
            self.image.blit(st.pokeball,(0,0))
            self.speed = 0
            self.damage = 250
            player.gatcha = 0
        if self.num == 5: # 얼음
            self.image = pygame.Surface((25, 16), pygame.SRCALPHA)
            self.image.fill((97, 231, 255,200))
            self.speed = 50
            self.damage = 3
            self.rect = self.image.get_rect(center = get_new_pos(self.pos))  
        #self.image.fill((255, 255, 255, 150), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = pygame.transform.rotate(self.image, self.direction)
        self.a = 0
    def update(self):
        # 화면 나가면 삭제
        if not near_border.colliderect(self.rect):
            if self.appear:
                if self.num == 4:
                    player.gatcha = player.gatcha_max//2
                    sound_channel[2].play(s_invalid)
                self.kill()
        else:
            self.appear = True
        if self.num == 4:
            self.speed += 1
        if not far_border.colliderect(self.rect):
            self.kill()
        if self.died:
            if self.effect:
                if self.a ==0:
                    if self.num == 4:
                        self.image = pygame.Surface((128,128), pygame.SRCALPHA) 
                        self.rect = self.image.get_rect(center = get_new_pos(self.pos))  
                        pygame.draw.circle(self.image, 'red', (64,64), 64)
                    else:
                        self.image.fill((255,255,255,100))
                self.image.fill((255, 255, 255,250), special_flags=pygame.BLEND_RGBA_MULT)
                self.speed=0
                self.a += 1
                if self.a > 40: self.kill()
            else:                
                if self.num == 4: 
                    sound_channel[3].play(s_good)
                self.effect = True
        self.pos = calculate_new_xy(self.pos, self.speed, -self.direction)
        self.rect = self.image.get_rect(center = get_new_pos(self.pos))  
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, dir, speed, health, img, hit_cir, num, skill,item=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((128,128), pygame.SRCALPHA)
        self.image.blit(pokemons[img-1],(0,0)) 
        if not item==0:
            image2 = self.image.copy() 
            mask = pygame.mask.from_surface(self.image)
            mask_surf = mask.to_surface()
            mask_surf.set_colorkey((0,0,0))
            color = (0,0,0)
            if item == 2 or item == 3:
                color = (0,255,0)
            if item == 4:
                color = (255, 0, 234)
            if item == 5:
                color = (255,255,0)
            mask_surf.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
            self.image.blit(mask_surf,(-1,0))
            self.image.blit(mask_surf,(1,0))
            self.image.blit(mask_surf,(0,-1))
            self.image.blit(mask_surf,(0,1))    
            self.image.blit(image2,(0,0))  
        self.rect = self.image.get_rect(center = get_new_pos((x, y)))
        self.radius = hit_cir//2
        self.pos = (x, y)
        #pygame.draw.circle(self.image, (200,0,0), (128,128), self.radius, 3)

        self.count = 0
        self.list = [0,0]
        self.max_health = health
        self.health = health
        self.num = num
        self.skill = skill
        self.item = item
        # 적이동을 위한 값
        self.move_dir = dir
        self.move_speed = speed

        self.screen_apper = False

    def update(self):
        if not self.health <= 0:
            self.pos, self.move_dir, self.move_speed ,self.count,self.list= enemy_attack(self.num, self.count, self.pos, self.move_dir, self.move_speed,self.list)

        if not screen_rect.colliderect(self.rect) and self.screen_apper: # 밖으로 나가면 사라지기
            self.kill() 
        if screen_rect.colliderect(self.rect) and not self.screen_apper:
            self.screen_apper = True
        if self.health <= 0: # 체력 다 달면 죽기
            if self.num == 21 and not self.health == -999:
                bullet_effect(s_tan2,0,self.pos)
                if difficult == 0:
                    for i in range(0,360,60):                       
                        bullet(calculate_new_xy(self.pos,20,-i),i,0,12,0,9.4)
                if difficult == 1:
                    for i in range(0,360,45):                       
                        bullet(calculate_new_xy(self.pos,20,-i),i,0,12,0,9.4)
                if difficult == 2:
                    bullet(self.pos,look_at_player(self.pos),0,15,0,9.4)
                    for i in range(0,360,15):                       
                        bullet(calculate_new_xy(self.pos,20,-i),i,0,12,0,9.4)
            enemy_boom_channel.play(s_enedead)
            effect_group.add(Effect(self.pos,1))
            effect_group.add(Effect(self.pos,3))
            for i in range(0,math.ceil(self.max_health/25)):
                rand = [randint(-100,100),randint(-100,100)]
                if rand[1] < 32: rand[1] = 32
                if rand[1] >688: rand[1] = 688
                item_group.add(Item(get_new_pos((self.pos[0]*2,self.pos[1]*2),rand[0],rand[1]),0))
            if self.item == 2:
                for i in range(0,360,45):
                    item_group.add(Item((self.pos[0]*2,self.pos[1]*2),2,i))
            if self.item == 3:
                for i in range(0,360,90):
                    item_group.add(Item((self.pos[0]*2,self.pos[1]*2),3,i+45))
            if self.item == 4:
                item_group.add(Item((self.pos[0]*2,self.pos[1]*2),4))
            if self.item == 5:
                item_group.add(Item((self.pos[0]*2,self.pos[1]*2),5))
            self.kill()

        self.count += 1
        self.rect.center = (int(self.pos[0]),int(self.pos[1]))    
class Boss_Enemy(pygame.sprite.Sprite):
    def __init__(self,code):
        pygame.sprite.Sprite.__init__(self)
        self.code = code
        self.image = pygame.Surface((128,128), pygame.SRCALPHA)      
        self.rect = self.image.get_rect(center = (-99,-99))
        self.image2 = self.image.copy()
        self.radius = 0
        self.pos = (-99,-99)
        self.image_num = 0

        self.count = 0
        self.death_count = 0
        self.list = [0,0,0,0]
        self.max_health = 2000
        self.health = 1
        self.num = 0

        # 적이동을 위한 값
        self.move_dir = 0
        self.move_speed = 0
        self.move_point = (0,0)
        self.move_time = 0
        self.ready = False
        self.move_ready = False # 스펠 시작시 움직이는중?
        self.godmod = False
        self.dieleft = False
        self.spell = []
        self.dies = False
        self.died_next_stage = False
        self.appear = False
        self.attack_start = False
        self.box_disable = False
        self.really_box_disable = False
        self.sin = 0
        self.dont_stop = False
    def update(self, collide):
        global pause, screen_shake_count, levelup
        if self.health > self.max_health: self.health = self.max_health
        if self.appear:
            inum = self.image_num
            self.image_num = 0
            # 보스가 등장했을때 실행
            if not self.ready:
                self.health = self.max_health
                self.godmod = True 

            # 능력 살아있으면
            if self.health > 0 and not self.dieleft:
                if self.count >= 120 and self.move_ready and not self.ready:
                    self.count = 1
                    self.ready = True
                    self.godmod = False
                self.count, self.pos, self.ready = boss_attack(self.num, self.count, self.pos, self.ready, self)
            if self.move_speed == 0:self.image_num =0
            else:
                imgdir = self.move_dir
                if imgdir < 0: 360+imgdir
                if big_small(imgdir,90,269): self.image_num =2
                else: self.image_num =1
            if inum != self.image_num:
                if self.image_num == 0:self.image = self.image2                               
                if self.image_num == 1:self.image = pygame.transform.rotate(self.image2, -10)
                if self.image_num == 2:self.image = pygame.transform.rotate(self.image2, 10)     
                self.rect.center = self.pos                   
            # 빔에 맞았을때
            if len(collide) > 0 and not self.godmod:                               
                for beam in collide:
                    if not beam.died:
                        if self.health > 1:
                            self.health -= beam.damage
                            if beam.num == 4: st.score += st.score_setting[4]
                            if self.health <= 0: self.health = 1
                        if self.health < 10 and beam.num == 4:
                            self.health -= beam.damage
                            st.score += st.score_setting[4]
                        if self.health < 10:damage_channel.play(s_nodam) 
                        else:
                            if self.health/self.max_health < 0.25:damage_channel.play(s_damage1) 
                            else: damage_channel.play(s_damage0) 
                        beam.died = True
            if self.health <= 0 and not self.dieleft and self.ready: # 체력다 닳음 죽은적이없고 스펠시전 중이였을때 실행
                self.image = self.image2 
                self.image_num = 0
                self.count = 0
                self.move_ready = False
                self.ready = False
                self.box_disable = False
                self.move_time  = 0
                self.move_speed = 0
                self.spell_clear = True
                add_effect(self.pos,5)
                died_channel.play(s_enep1)
                self.image_num = 0
                self.dieleft = True
                self.appear = False
                self.move_point = (0,0)
                self.attack_start = False
                self.died_next_stage = True
                self.count = 0
            self.count += 1
            if self.move_speed == 0: self.sin += 6
            self.rect = self.image.get_rect(center = self.pos)
                    
        if self.dieleft: # 죽었을때 이벤트
            st.clock_fps = 60
            self.death_count += 1
            self.pos = calculate_new_xy(self.pos,1,self.move_dir)
            if self.death_count == 60:
                remove_allbullet()
                if not levelup: 
                    levelup = True
                    boss.count = 0
                    boss2.count = 0
                screen_shake_count = 30
                died_channel.play(s_enep1)
                add_effect(get_new_pos(self.pos,100,0),5)               
                add_effect(get_new_pos(self.pos,-100,0),5)           
                add_effect(get_new_pos(self.pos,0,100),5)      
                add_effect(get_new_pos(self.pos,0,-100),5)                                            
                self.pos = (-128,-128)                                                        
                self.real_appear = False   
                self.dieleft = False
                self.appear = False
                self.death_count = 0                
        self.rect.center = get_new_pos(self.pos,0,math.sin(self.sin*math.pi/180)*3)

    def reset(self):
        self.image = pygame.Surface((128,128), pygame.SRCALPHA)      
        self.rect = self.image.get_rect(center = (-99,-99))
        self.image2 = self.image.copy()
        self.radius = 0
        self.pos = (-99,-99)
        self.image_num = 0

        self.count = 0
        self.list = [0,0,0,0]
        self.max_health = 0
        self.health = 1
        self.real_max_health = 0
        self.real_health = 0
        self.num = 0

        # 적이동을 위한 값
        self.move_dir = 0
        self.move_speed = 0
        self.move_point = (0,0)
        self.move_time = 0
        self.ready = False
        self.move_ready = False # 스펠 시작시 움직이는중?
        self.godmod = False
        self.dieleft = False
        self.spell = []
        self.dies = False
        self.died_next_stage = False
        self.appear = False
        self.real_appear = False
        self.attack_start = False
        self.box_disable = False
        self.fire_field = [0,0]
        self.fire_field_radius = 0            
class Spell():
    def __init__(self,number,health,spellcard,col=0,sub_name="",name=""):
        self.health = health
        self.spellcard = spellcard
        self.num = number
        self.count = 0
        self.font = pygame.font.Font(st.FONT_2, 10)
        self.font2 = pygame.font.Font(st.FONT_1, 20)
        self.image = pygame.Surface((200,40), pygame.SRCALPHA)
        if self.spellcard:
            self.image.blit(st.skill_img,(0,0),(0,0+37*col,200,37))
            text = self.font.render(sub_name, True, 'white')
            self.image.blit(text,(13,2))
            text = self.font2.render(name, True, 'white')
            self.image.blit(text,(25,15))
    def draw(self):
        if self.count < 60: up_render_layer.blit(self.image,(WIDTH-200,0))
        if big_small(self.count,60,85): 
            up_render_layer.blit(self.image,(WIDTH-200,(self.count-60)**2))
        if self.count > 85: up_render_layer.blit(self.image,(WIDTH-200,320))
        self.count += 1

class Skill():
    def __init__(self,num,col,sub_msg,msg,pp,cool,refill=0):
        font2 = pygame.font.Font(st.FONT_2, 9)
        self.image = pygame.Surface((200,37), SRCALPHA)
        self.image.blit(st.skill_img,(0,0),(0,37*col,200,37))
        self.image = pygame.transform.flip(self.image, True, True)
        self.num = num
        self.cool = cool
        text = st.font1.render(msg, True, (255,255,255))
        self.image.blit(text,(1,1))
        text = font2.render(sub_msg, True, (255,255,255))
        self.image.blit(text,(1,24))
        self.max_pp = pp
        self.pp = self.max_pp  
        self.refill = 0
        self.max_refill = refill 
    def draw(self):
        sub_image = self.image.copy()    

        text = font1.render(str(self.pp)+"/"+str(self.max_pp), True, (255,255,255))  
        sub_image.blit(text,(123,1))
        if self.refill >= self.max_refill:
            if self.pp < self.max_pp:self.pp+=1
            self.refill -=self.max_refill
        a=0
        try:a = 188/self.max_refill*self.refill
        except:a=0
        pygame.draw.rect(sub_image, (0, 221, 255), (0,22,a,2))
        sub_image.fill((255, 255, 255, 100 if Rect(0,HEIGHT-74,250,74).collidepoint(player.pos) else 255), special_flags=pygame.BLEND_RGBA_MULT)
        up_render_layer.blit(sub_image,(0,HEIGHT-37))
class Spell_Obj(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed,  mod):
        pygame.sprite.Sprite.__init__(self)   
        self.image = pygame.Surface((80,80),SRCALPHA)
        if mod == 1:
            pygame.draw.circle(self.image, (255,255,255,150), (40,40), 40)
            pygame.draw.circle(self.image, (255,255,255,100), (40,40), 30)
        if mod == 5:
            pygame.draw.circle(self.image, (0,0,255,150), (40,40), 40)
        if mod == 6:
            pygame.draw.circle(self.image, (143, 255, 255,150), (40,40), 20)
        if mod == 10:
            pygame.draw.circle(self.image, (204, 204, 204,200), (40,40), 40)
            pygame.draw.circle(self.image, (204, 204, 204,255), (40,40), 45,2)
        if mod == 12:
            pygame.draw.circle(self.image, (170, 0, 232,230), (40,40), 5)
        self.rect = self.image.get_rect(center = pos)
        self.num = mod
        self.pos = pos
        self.direction = direction
        self.speed = speed
        self.count = 0
    def update(self,screen):

        if self.num == 1:
            self.pos = player.pos
            for bul in spr.sprites():
                if distance(self.pos,bul.pos) <= 40:
                    bul.kill()
            if self.count >= 800:
                self.kill()
        if self.num ==5:
            if self.count == 0:
                for enemy in enemy_group.sprites():
                    if distance(self.pos,enemy.pos) <= 40:
                        enemy.health -= 5
                if distance(self.pos,boss.pos) <= 40:
                    boss.health -= 5
            if self.count >= 50:
                self.kill()
        if self.num == 6:
            for enemy in enemy_group.sprites():
                if distance(self.pos,enemy.pos) <= 20:
                    self.speed = 0
                    self.pos = enemy.pos
            if distance(self.pos,boss.pos) <= 20:
                self.speed = 0
                self.pos = boss.pos
            if self.count >= 80:
                for enemy in enemy_group.sprites():
                    if distance(self.pos,enemy.pos) <= 20:
                        enemy.health -= 20  
                if distance(self.pos,boss.pos) <= 20:
                    boss.health -= 20               
                self.kill()
        if self.num == 10:
            for bulls in spr.sprites():
                if distance(self.pos,(bulls.pos[0]//2,bulls.pos[1]//2)) <= 40:
                    if not bulls.shape[0] == 19:
                        bulls.kill()
                    self.direction += 1
            if self.direction >= 30:
                self.kill()
        if self.num == 12:
            if self.speed == 0:
                for enemy in enemy_group.sprites():
                    if distance(self.pos,enemy.pos) <= 2:
                        enemy.health -= 1
                        if enemy.health <= 0: self.kill()     
            for enemy in enemy_group.sprites():
                if distance(self.pos,enemy.pos) <= 20:
                    self.speed = 0
                    self.pos = enemy.pos 
            if distance(self.pos,boss.pos) <= 20:
                self.speed = 0
                self.pos = boss.pos
            if distance(self.pos,boss.pos) <= 2:
                boss.health -= 1
                if boss.health <= 0: self.kill()  
            
        if self.pos[0] >= WIDTH:self.kill()
        self.count += 1
        if not small_border.colliderect(self.rect): self.kill()
        self.pos = calculate_new_xy(self.pos, self.speed, -self.direction)
        self.rect.center = self.pos
class Skill_Core(): # 스킬 능력 구현
    def __init__(self, num, cool):
        self.num = num
        self.cool = cool
        self.max_cool = cool
        self.draw_cool = cool
        self.pos = (0,0)
        self.radius = 0
    def update(self,bos):
        if self.cool > 0:
            if self.num == 1: # 주변 탄 삭제
                self.pos = player.pos
                for bul in spr.sprites():
                    if distance(double(self.pos),bul.pos) <= 128 and not bul.shape[0] == 19 and not bul.shape[0] == 20:
                        add_effect(double(bul.pos,True),7,bul.shape[1])
                        item_group.add(Item(bul.pos,1))
                        bul.kill()
                

            if self.num == 2: # 쪼기
                beams_group.add(Beam(player.pos,5))
            if self.num == 3: # 바람일으키기
                if player.godmod: 
                    sound_channel[3].play(s_invalid)
                    self.cool = 0
                    self.draw_cool = 0
                    for bul in spr.sprites():
                        if distance(player.pos,double(bul.pos,True)) < 300:
                            bul.pos = double(bul.pos,True)
                            add_effect(bul.pos,7,bul.shape[1])
                            item_group.add(Item(bul.pos,1))
                            bul.kill()
                if self.cool == 1:
                    sound_channel[4].play(s_good)
                    player.health += 100
                    if player.health > player.max_health: player.health = player.max_health

        if not self.cool == 0:self.cool -= 1
        if not self.draw_cool == 0:self.draw_cool -= 1
    def draw(self,screen):
        if self.num == 1:
            pygame.draw.circle(screen, (255,0,0,100),player.pos, 64)
            pygame.draw.circle(screen, (255,0,0,50),player.pos, 40)
        if self.num == 2:
            pygame.draw.circle(screen, (52, 204, 235,200),player.pos, 50)
        if self.num == 3:
            pygame.draw.circle(screen, (0,255,0,100),player.pos, self.draw_cool)

# 탄
class Bullet(pygame.sprite.Sprite):    
    def __init__(self, x, y, direction, speed, bul, col, mod, num=(0,0)):
        # 이미지
        pygame.sprite.Sprite.__init__(self)
        self.shape = (bul, col)
        self.pos = (x, y)
        self.image = bullets[bul][col] if not (bul == 10 or bul == 11 or bul == 14) else bullets[bul][col][0]
        self.image2 = self.image.copy()

        self.add_dir = 0
        self.move_fun = False
        # 쓸 값
        self.rect = self.image.get_rect(center = (int(x), int(y)))
        
        self.direction = direction
        self.speed = speed
        self.radius = bullet_size[bul]
        self.count = 0
        self.mod = mod
        self.num = num
        self.grazed = True
        self.lotate = False if bul == 2 or bul == 3 or bul == 10 or bul==11 or bul == 12 or bul == 15 or bul == 10 or bul == 14 or bul == 19 or bul == 20 else True   
        if self.lotate: 
            self.image = pygame.transform.rotate(self.image2, round(self.direction-90))
            self.rect = self.image.get_rect(center = (int(self.pos[0]),int(self.pos[1])))
        self.keeplotate = True if (bul == 10 or bul == 11 or bul == 14) else False
        self.keeplotate_count = 0
        self.screen_die = 0
        self.fade = False # 탄 숨기기
        self.ghost = False # 피탄없음
    def update(self, screen):
        mod, sub = math.trunc(self.mod), (self.mod*10)%10
        direc = self.direction
        #모드 값이 있으면 탄 속성 변화###############################################
        if levelup:bullet_levelup(self,mod,sub) 
        else:bullet_type(self,mod,sub)        
        ################################################
                    
        if direc != self.direction and self.lotate:# 각도 계산후 위치 업데이트
            self.image = pygame.transform.rotate(self.image2, round(self.direction-90))
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))  
        if self.keeplotate:
            self.keeplotate_count += 1
            if self.keeplotate_count == 180:
                self.keeplotate_count = 0
            self.image = bullets[self.shape[0]][self.shape[1]][self.keeplotate_count]
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))  
        if not self.move_fun and not time_stop:
            self.pos = calculate_new_xy(self.pos, self.speed*2, -self.direction)
        self.rect.center = self.pos
        dist = distance(self.pos,(player.pos[0]*2,player.pos[1]*2))

        # 플레이어가 탄을 스치면 추가점수
        if self.grazed and dist <= 80+self.radius: #and not player.godmod:
            graze_channel.play(s_graze)
            st.score += st.score_setting[3]
            player.skill_list[player.skill_pointer].refill += 1
            self.grazed = False    
            if player.gatcha < player.gatcha_max: 
                player.gatcha += 1   
        if self.fade and dist <= 200+self.radius:
            self.fade = False
            bullet_effect(s_kira1,self.shape[1],double(self.pos,True))
            self.change_shape(self.shape[0],self.shape[1])
        # 화면에 없으면 없애기    
                
        if self.screen_die==0 and not small_border.colliderect(self.rect):       
            self.kill()
        elif self.screen_die==1 and not bullet_border.colliderect(self.rect):
            self.kill()
        elif self.screen_die == 2 and small_border.colliderect(self.rect):
            self.screen_die = 0    
    def change_shape(self,bul,col):
        try:
            self.image = bullets[bul][col] if not (bul == 10 or bul == 11 or bul == 14) else bullets[bul][col][0]
            self.image2 = self.image.copy()
            self.lotate = False if bul == 2 or bul == 3 or bul == 10 or bul==11 or bul == 12 or bul == 15 or bul == 10 or bul == 14 or bul == 19 else True   
            if self.lotate: 
                self.image = pygame.transform.rotate(self.image2, self.direction-90)
                self.rect = self.image.get_rect(center = (int(self.pos[0]),int(self.pos[1])))
            self.keeplotate = True if (bul == 10 or bul == 11 or bul == 14) else False
            self.rect = self.image.get_rect(center = (round(self.pos[0]),round(self.pos[1])))
        except: pass
    def hide(self):
        self.change_shape(self.shape[0],8)
        self.fade = True
    def size_change(self,size):
        self.radius += size/2
        self.image = pygame.transform.scale(self.image2, (self.rect.width+size, self.rect.height+size))    
        if self.lotate: self.image = pygame.transform.rotate(self.image, round(self.direction-90))    
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
class MagicField(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, mod, screen_die = 0):
        # 이미지
        pygame.sprite.Sprite.__init__(self)
        self.image = magic_circle_sprite[0]
        
        # 쓸 값
        self.rect = self.image.get_rect(center = pos)
        self.pos = (pos[0], pos[1])
        self.direction = direction
        self.speed = speed
        self.radius = 8
        self.count = 0
        self.count2 = 1
        self.num = 0
        self.spr_trun = 0
        self.mod = mod
        self.screen_die = screen_die

    def update(self, screen):
        mod = math.trunc(self.mod)
        magic_type(self,mod)

        try:
            self.spr_trun += 1
            self.image =magic_circle_sprite[self.spr_trun]
        except:
            self.spr_trun = 0
            self.image =magic_circle_sprite[0]
        # 각도 계산후 위치 업데이트
        self.pos = calculate_new_xy(self.pos, self.speed, -self.direction)
        self.rect = self.image.get_rect(center = get_new_pos((self.pos)))
            # 화면에 없으면 없애기
        if self.screen_die==0 and not near_border.colliderect(self.rect):       
            self.kill()
        elif self.screen_die==1 and not bullet_border.colliderect(self.rect):
            self.kill()
        elif self.screen_die == 2 and near_border.colliderect(self.rect):
            self.screen_die = 0   
class Effect(pygame.sprite.Sprite):
    def __init__(self, pos, num, col=0, speed=0, dir=0):
        pygame.sprite.Sprite.__init__(self) # 초기화?
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA) # 이미지          
        self.rect = self.image.get_rect(center = (round(pos[0]), round(pos[1])))
        self.image2 = self.image.copy()
        self.pos = pos
        self.count = 0
        self.num = num
        self.col = col
        self.speed = speed
        self.direction = dir
        if self.num == 33:
            self.image = pygame.Surface((128,128), pygame.SRCALPHA) # 이미지   
            pygame.draw.circle(self.image, (0,0,0,100), (64,64), 64)
            pygame.draw.circle(self.image, (0,0,0), (64,64), 60)

    def update(self):
        if self.num == 1: # 적 사망 파란 포켓볼
            self.count += 1
            try: self.image = enemy_died_circle[self.count -1]
            except:self.kill()
        if self.num == 2: # 탄 효과
            self.count += 1
            try:
                self.image = bullet_taning[self.col][len(bullet_taning)-self.count]
                if 64-self.count < 1: self.kill()
            except: self.kill()
        if self.num == 3: # 커지고 투명 원 안채워짐
            self.count += 1
            try: self.image = died_white_circle[self.count -1]
            except:self.kill()
        if self.num == 5: # 커지는 투명 원
            self.count += 1
            try:self.image = white_circle[self.col][self.count]
            except: self.kill()
        if self.num == 6:
            self.pos = boss.pos
            self.count += 1
            try:self.image = white_circle[self.col][256-self.count]
            except: self.kill()
        if self.num == 7: # 탄 삭제 효과
            try:self.image = bullet_erase[self.col][len(bullet_erase)-1-self.count]  
            except:
                if not self.count == 0:
                    self.kill()
                else:
                    self.col -= 1
            self.count += 1
        if self.num == 8: # 기보으기
            if self.count == 0:s_ch2.play()
            self.count += 6
            if self.count >= 255:self.kill() 
            self.image = white_circle[self.col][256-self.count]                    
        if self.num == 33: # 암흑
            self.pos = calculate_new_xy(self.pos,self.speed,-self.direction)
            if not self.rect.colliderect(small_border): self.kill()

        if self.num == 99:
            self.count += 1
            try:self.image = black_screen[self.count-1]   
            except:self.kill()  

        self.rect = self.image.get_rect(center = get_new_pos((self.pos)))
        self.count += 1
class Item(pygame.sprite.Sprite):
    def __init__(self, pos, num, dir=0):
        pygame.sprite.Sprite.__init__(self) # 초기화?
        self.image = items[num]      # 이미지          
        self.rect = self.image.get_rect(center = (round(pos[0]), round(pos[1])))
        self.pos = (pos[0]/2,pos[1]/2)
        self.count = 0
        self.num = num
        self.lock = False
        self.dir = dir

    def update(self):
        # 화면 넘어가면 삭제:
        if self.num == 2 or self.num == 3:
            if self.count == 0:self.pos = calculate_new_xy(self.pos,100,self.dir)
        else:
            if not self.lock:
                if self.count < 80:
                    self.pos = (self.pos[0]+5-self.count/8,self.pos[1])
                else:
                    if self.num == 1: self.lock = True
                    self.pos = (self.pos[0]-2.5,self.pos[1])

            if self.pos[0] < -10:
                self.kill() 
            # 플레이어 범위 작으면 먹기

            self.pos = calculate_new_xy(self.pos,18,-look_at_player(self.pos))

        if distance(self.pos,player.pos) < 35:
            if self.num == 0: 
                if player.power < 450: player.power += 1 # 먹으면 파워업
                if player.gatcha < player.gatcha_max: player.gatcha += 1 # 먹으면 파워업
                st.score += st.score_setting[1]
            if self.num == 1:
                st.score += st.score_setting[2]
                if player.gatcha < player.gatcha_max: 
                    player.gatcha += 1  
            item_channel.play(s_item0)
            self.kill()


        self.rect = self.image.get_rect(center = get_new_pos((self.pos)))
        self.count += 1
class UI():
    def __init__(self,val):
        self.val = val
        self.ui_font = pygame.font.Font(st.FONT_1, 15)
        self.ui_font2 = pygame.font.Font(st.FONT_1, 14)
        self.power= pygame.Surface((100, 20), pygame.SRCALPHA)
        self.power_xy = (30,29)
        self.skill_xy = (115,6)
        self.ui_img = pygame.Surface((400,80), pygame.SRCALPHA)
        self.ui_img.blit(self.ui_img,(0,0),(0,0,400,80))
        self.ui_img = pygame.transform.scale(self.ui_img, (200, 40))

    def draw(self):        
        score_text = st.score_font.render(str(st.score).zfill(10), True, (255,255,255))
        up_render_layer.blit(score_text,(WIDTH-160,0))    
        score_text = st.score_font.render(str(st.hiscore).zfill(10), True, (46, 46, 46))
        up_render_layer.blit(score_text,(WIDTH-160,HEIGHT-25))        
class Under_PI():
    def __init__(self):
        self.slow_image = st.slow_player_circle[0]
        self.rect = self.slow_image.get_rect(center = get_new_pos(player.pos))
        self.slow_count = 0
        self.pos = player.pos
        self.count = [0,0,0]

    def draw(self, keys):
        if keys[pygame.K_LSHIFT]:
            self.pos = player.pos
            
            self.slow_image = st.slow_player_circle[self.slow_count]
            self.rect = self.slow_image.get_rect(center = get_new_pos(self.pos))
            render_layer.blit(self.slow_image, self.rect.topleft)
            self.slow_count += 1
            if self.slow_count >= len(st.slow_player_circle): self.slow_count = 0
        if boss2.health > 0: # 보스 체력바 그리기
            try:
                drawArc(render_layer, (0, 0, 0), boss2.pos, 80, 5, 360*100,255 if distance(player.pos,boss2.pos) >= 100 else 50)
                drawArc(render_layer, health_color(boss2.health/boss.max_health), boss2.pos, 79, 3, 360*boss2.health/boss2.max_health,255 if distance(player.pos,boss2.pos) >= 100 else 50)
            except:pass
        if boss.health > 0: # 보스 체력바 그리기
            try:
                drawArc(render_layer, (0, 0, 0), boss.pos, 80, 5, 360*100,255 if distance(player.pos,boss.pos) >= 100 else 50)
                drawArc(render_layer, health_color(boss.health/boss.max_health), boss.pos, 79, 3, 360*boss.health/boss.max_health,255 if distance(player.pos,boss.pos) >= 100 else 50)
            except:pass
        
        if starting and not read_end and player.health > 0: # 원형 체력바 그리기
            psi = player.pos
            if not player.gihapetii:# 기합의띠 파괴
                drawArc(render_layer, (255,0,0), psi, 100+ round(math.sin(math.radians(self.count[1]*5))*3), 2, 360,255)
                drawArc(render_layer, (255,0,0), psi, 95+ round(math.sin(math.radians(self.count[1]*5))*3), 2, 360,255)
                # 그레이즈
            drawArc(render_layer, health_color(player.health/player.max_health), psi, 38 + round(math.sin(math.radians(self.count[1]*5))*3), 4, 360,150)
            drawArc(render_layer, health_color(player.health/player.max_health), psi, 38, 2, 360,200)
            self.count[1] += 1
            # 포켓몬 게이지
            if player.gatcha < player.gatcha_max:
                drawArc(render_layer, (100, 194, 247), psi, 45, 10, 360*player.gatcha/player.gatcha_max,200)
            else:
                self.count[0] += 1 # 빈도 포켓볼 깜빡거림
                if self.count[0] < 10:
                    drawArc(render_layer, (100, 194, 247), psi, 45, 10, 360*player.gatcha/player.gatcha_max,200)
                if self.count[0] == 20: 
                    self.count[0] = 0
                    sound_channel[0].play(st.s_piyo2)
            # 플레이어 체력
            try:
                if player.godmod: drawArc(render_layer, (0, 194, 247), psi, 58, 11, 360*player.godmod_count/player.max_godmod_count,255)
                drawArc(render_layer, (0,0,0), psi, 56, 8, 360*100,120 if not player.godmod else 255)
            except: pass
            if player.godmod: drawArc(render_layer, health_color(player.health/player.max_health), psi, 55, 5, 360*player.before_health/player.max_health,120)
            drawArc(render_layer, health_color(player.health/player.max_health), psi, 55, 5, 360*player.health/player.max_health,120 if not player.godmod else 255)
class Back_Ground():
    def __init__(self, img, rect, speed):
        image = pygame.Surface((rect[2],rect[3]), pygame.SRCALPHA)
        image.blit(img, (0,0), rect)
        self.image = image
        self.speed = speed
        self.x = 0
        self.y = rect[1]
        if self.y >= 360:
            self.y -= 360*(self.y // 360)
    def update(self):
        self.x -= self.speed

play = True
music_playing = False
cur_full_mod = False
pause = False
pause_lock = False
frame_count = 0
cur_count = 0
time_stop = False
stage_count = 0
screen_shake_count = 0
all_trig = False
game_clear = False   
curser = 0
curser_max = 4
select_mod = 0
menu_mod = []
character = 0
difficult = 0
cur_screen = 0
stage_fun = 0
stage_line = 0
stage_cline = 0
stage_repeat_count = 0
stage_condition = 1
stage_challenge = 0
stage_end = 0
skill_activating = []
practicing = False
levelup = False
# 게임 시작전 메뉴 변수들
boss = Boss_Enemy(1)
boss2 = Boss_Enemy(2)
boss_group = pygame.sprite.Group(boss2,boss)
enemy_group = pygame.sprite.Group()
spr = pygame.sprite.Group()
magic_spr = pygame.sprite.Group()
player = Player(-125,-125,5,500)
player_group = pygame.sprite.Group(player)
player_hitbox = Player_hit()
skillobj_group = pygame.sprite.Group()
title = Tittle(1)
ui = UI(1)
under_ui = Under_PI()
beams_group = pygame.sprite.Group()
effect_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

starting = True
read_end = False
player.skill_list.append(sv.Skill(1,2,st.other[0],st.other[1],2,90,80))
player.skill_list.append(sv.Skill(2,0,st.other[2],st.other[3],2,90,50))
player.skill_list.append(sv.Skill(3,10,st.other[4],st.other[5],5,120,80))

stages = [[(1,2),(3,1),(2,3),(6,7),(7,8),(8,6),(1,8),(2,6),(3,7)],\
        [(12,13),(13,27),(12,27),(14,13),(14,12),(14,27)],\
        [(15,16),(16,30),(22,23),(23,24),(22,24),(15,22),(24,30) ,(23,16),(30,15),(30,22) ],\
          [(1,13),(2,14),(3,15),(12,7),(7,16),(23,27),(30,13) ,(1,1),(22,14),(30,2) ]]  #,\
            #   [(11,34),(31,32),(31,11),(32,34),(32,11),(31,34)],\
            #       [(9,10),(20,21),(20,9),(21,10),(10,20),(21,9)],\
            #           [(17,18),(25,26),(26,17),(25,18),(17,25),(26,18)],\
            #               [(17,18),(25,26),(26,17),(25,18),(17,25),(26,18)]]#,\
                      #        [(19,33),(25,26),(26,17),(25,18),(17,25),(26,18)],\
                     #             [(4,5),(29,35),(4,29),(35,5),(35,4),(5,29)]]

stage_playing = (1,2)
