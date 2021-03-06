from cgi import test
import pygame
from pygame.locals import *
import time
from tkinter import *
import tkinter.font as tkFont

root = Tk()
root.title("language")

w = 200 # width for the Tk root
h = 200 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))


testfont = tkFont.Font(family="Arial", size=16, weight="bold")
root.resizable(False, False)

label = Label(root, text = "language", font=testfont)
label.pack()

lang_var = IntVar()
button_kor = Radiobutton(root, text="한국어", value=1, variable=lang_var, height=2, font=testfont)
button_kor.invoke()
button_eng = Radiobutton(root, text="English", value=2, variable=lang_var, height=2,font=testfont)
button_kor.pack()
button_eng.pack()

button = Button(root, text="▶", command=root.quit, font=testfont)
button.pack()

root.mainloop()



pygame.init()
pygame.mixer.pre_init(44100,-16,2,512)

# 해상도
WIDTH = 540
HEIGHT = 360
render_layer = pygame.Surface((WIDTH,HEIGHT))
up_render_layer = pygame.Surface((WIDTH,HEIGHT), SRCALPHA)
skill_surface = pygame.Surface((WIDTH,HEIGHT), SRCALPHA)
screen = pygame.display.set_mode((WIDTH*2,HEIGHT*2))
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen_rect = render_layer.get_rect()
lang = lang_var.get()
bgm_num = 0
# 소리 초기설정, 불러오기
pygame.mixer.set_num_channels(64)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])


# 이미지 불러오기
bullet_image = pygame.image.load('resources\Image\Bullets.png').convert_alpha()
bg_image = pygame.image.load('resources\Image\Bg1.png').convert_alpha()
bg2_image = pygame.image.load('resources\Image\Bg2.png').convert_alpha()
pkmon_image = pygame.image.load('resources\Image\pokemon.png').convert_alpha()
background_img = pygame.image.load('resources\Image\\background.jpg').convert()
background2_img = pygame.image.load('resources\Image\\background2.png').convert()
menu_img = pygame.image.load('resources\Image\Menus.png').convert_alpha()
item_img = pygame.image.load('resources\Image\item.png').convert_alpha()
skill_img = pygame.image.load('resources\Image\skill.png').convert_alpha()
loding_img = pygame.image.load('resources\Image\Loding.png').convert()
title_img = pygame.image.load('resources\Image\\title.png').convert_alpha()
poligon = pygame.image.load('resources\Image\polligonz.png').convert_alpha()
screen.blit(pygame.transform.scale2x(loding_img),(0,0))
pygame.display.flip()
text_text = ""
text_credit = "resources\credit.txt"

pkm_text = ""
other_txt = ""
if lang == 1:
    pkm_text = "resources\kor_pk_name.txt"
    other_txt = "resources\kor_other.txt"
    text_text = "resources\kor_how_to_play.txt"
if lang == 2:
    pkm_text = "resources\pk_name.txt"
    other_txt = "resources\other.txt"
    text_text = "resources\how_to_play.txt"
score_text = "resources\score.txt"
score_index = []
score_value = []
with open(score_text, "r", encoding="UTF-8") as t:
    lines = t.readlines()
    for line in lines:
        line = line.strip()
        if not line == "":
            line = line.split('_')
            score_index.append([int(line[0]),int(line[1])])
            score_value.append(int(line[2]))
        else: pass
htp_scroll = []
with open(text_text, "r", encoding="UTF-8") as t:
    lines = t.readlines()
    for line in lines:
        line = line.strip()
        htp_scroll.append(line)
credit_scroll = []
with open(text_credit, "r", encoding="UTF-8") as t:
    lines = t.readlines()
    for line in lines:
        line = line.strip()
        credit_scroll.append(line)
pk_name = []
with open(pkm_text, "r", encoding="UTF-8") as t:
    lines = t.readlines()
    for line in lines:
        line = line.strip()
        pk_name.append(line)
other = []
with open(other_txt, "r", encoding="UTF-8") as t:
    lines = t.readlines()
    for line in lines:
        line = line.strip()
        other.append(line)


full_on = False
sfx_volume = 0
music_volume = 0

with open('resources\setting.txt','r',encoding="UTF-8") as f:
    lines = f.readlines()
    line = lines[0].strip()
    line = line.split('=')
    if line[1] == 'False' or line[1] == '0':
        full_on = False
    else:
        full_on = True
    line = lines[1].strip()
    line = line.split('=')
    sfx_volume = int(line[1])
    line = lines[2].strip()
    line = line.split('=')
    music_volume = int(line[1])

s_lazer1 = pygame.mixer.Sound('resources\Music\SFX\se_lazer00.wav')
s_tan1 = pygame.mixer.Sound('resources\Music\SFX\se_tan00.wav')
s_tan2 = pygame.mixer.Sound('resources\Music\SFX\se_tan01.wav')
s_ch2 = pygame.mixer.Sound('resources\Music\SFX\se_ch02.wav')
s_ch0 = pygame.mixer.Sound('resources\Music\SFX\se_ch00.wav')
s_cat1 = pygame.mixer.Sound('resources\Music\SFX\se_cat00.wav')
s_enep1 = pygame.mixer.Sound('resources\Music\SFX\se_enep01.wav')
s_enep2 = pygame.mixer.Sound('resources\Music\SFX\se_enep02.wav')
s_slash = pygame.mixer.Sound('resources\Music\SFX\se_slash.wav')
s_pldead = pygame.mixer.Sound('resources\Music\SFX\se_pldead00.wav')
s_plst0 = pygame.mixer.Sound('resources\Music\SFX\se_plst00.wav')
s_damage0 = pygame.mixer.Sound('resources\Music\SFX\se_damage00.wav')
s_damage1 = pygame.mixer.Sound('resources\Music\SFX\se_damage01.wav')
s_graze = pygame.mixer.Sound('resources\Music\SFX\se_graze.wav')
s_kira0 = pygame.mixer.Sound('resources\Music\SFX\se_kira00.wav')
s_kira1 = pygame.mixer.Sound('resources\Music\SFX\se_kira01.wav')
s_boom = pygame.mixer.Sound('resources\Music\SFX\se_enep02.wav')
s_item0 = pygame.mixer.Sound('resources\Music\SFX\se_item00.wav')
s_enedead = pygame.mixer.Sound('resources\Music\SFX\se_enep00.wav')
s_ok = pygame.mixer.Sound('resources\Music\SFX\se_select00.wav')
s_select = pygame.mixer.Sound('resources\Music\SFX\se_ok00.wav')
s_cancel = pygame.mixer.Sound('resources\Music\SFX\se_cancel00.wav')
s_pause = pygame.mixer.Sound('resources\Music\SFX\se_pause.wav')
s_piyo = pygame.mixer.Sound('resources\Music\SFX\se_piyo.wav')
s_shoot = pygame.mixer.Sound('resources\Music\SFX\se_focusfix.wav')
s_nodam = pygame.mixer.Sound('resources\Music\SFX\se_nodamage.wav')
s_kak = pygame.mixer.Sound('resources\Music\SFX\se_nice.wav')
s_dark = pygame.mixer.Sound('resources\Music\SFX\se_boon01.wav')
s_good = pygame.mixer.Sound('resources\Music\SFX\se_bonus2.wav')
s_release = pygame.mixer.Sound('resources\Music\SFX\se_release.wav')
s_invalid = pygame.mixer.Sound('resources\Music\SFX\se_invalid.wav')
s_life = pygame.mixer.Sound('resources\Music\SFX\se_life1.wav')
s_piyo2 = pygame.mixer.Sound('resources\Music\SFX\se_ufoalert.wav')
FONT_1 = 'resources\Font\SEBANG Gothic Bold.ttf' 
FONT_2 = 'resources\Font\SEBANG Gothic.ttf'
FIELD_1 = 'resources\Music\BGM\\1Stage.wav'
BGM1 = 'resources\Music\BGM\stage1.wav'
BGM2 = 'resources\Music\BGM\stage2.wav'
BGM3 = 'resources\Music\BGM\stage3.wav'
BGM4 = 'resources\Music\BGM\stage4.wav'
BGM5 = 'resources\Music\BGM\stage5.wav'
BGM6 = 'resources\Music\BGM\stage6.wav'
BGM7 = 'resources\Music\BGM\stage7.wav'
BGM8 = 'resources\Music\BGM\stage8.wav'
BGM9 = 'resources\Music\BGM\stage9.wav'
BGM10 = 'resources\Music\BGM\stage10.wav'
TITLE = 'resources\Music\BGM\Menu.wav'

tan_channel = pygame.mixer.Channel(0)
kira_channel = pygame.mixer.Channel(1)
kira2_channel = pygame.mixer.Channel(3)
tan2_channel = pygame.mixer.Channel(4)
enemy_boom_channel = pygame.mixer.Channel(2)
item_channel = pygame.mixer.Channel(5)
bossdam_channel = pygame.mixer.Channel(6)
plst_channel = pygame.mixer.Channel(7)
graze_channel = pygame.mixer.Channel(8)
enep_channel = pygame.mixer.Channel(9)
died_channel = pygame.mixer.Channel(10)
damage_channel = pygame.mixer.Channel(11)
lazer_channel = pygame.mixer.Channel(12)
dark_channel = pygame.mixer.Channel(13)
sound_channel = []
for i in range(14,60):
    sound_channel.append(pygame.mixer.Channel(i))
a_list = []
cur_list = []
if True:
    for i in range (0,176,16):
        for j in range (0,128,16):
            image = pygame.Surface((16, 16), pygame.SRCALPHA)
            image.blit(bullet_image, (0,0), Rect(j,i,16,16))
            image = pygame.transform.scale2x(image)
            if i == 160:
                k_list = []
                for k in range(0,180):
                    image2 = pygame.transform.rotate(image, k*2)
                    k_list.append(image2)
                a_list.append(k_list)
            else:
                a_list.append(image)
        cur_list.append(a_list)
        a_list = []
    for i in range (192,201,8):
        for j in range (0,64,8):
            image = pygame.Surface((8, 8), pygame.SRCALPHA)
            image.blit(bullet_image, (0,0), Rect(j,i,8,8))
            image = pygame.transform.scale2x(image)
            if i == 192:
                k_list = []
                for k in range(0,180):
                    image2 = pygame.transform.rotate(image, k*2)
                    k_list.append(image2)
                a_list.append(k_list)
            else:
                a_list.append(image)
        cur_list.append(a_list)
        a_list = []
    for i in range (208,400,32):
        for j in range (0,256,32):
            image = pygame.Surface((32, 32), pygame.SRCALPHA)
            image.blit(bullet_image, (0,0), Rect(j,i,32,32))
            image = pygame.transform.scale2x(image)
            if i == 240:
                k_list = []
                for k in range(0,180):
                    image2 = pygame.transform.rotate(image, k*2)
                    k_list.append(image2)
                a_list.append(k_list)
            else:
                a_list.append(image)
        cur_list.append(a_list)
        a_list = []
    for i in range(0,4):
        image = pygame.Surface((64, 64), pygame.SRCALPHA)
        image.blit(bullet_image, (0,0), Rect(i*64,432,64,64))
        image = pygame.transform.scale2x(image)
        a_list.append(image)
        a_list.append(image)
    cur_list.append(a_list)
    a_list = []
    for j in range (0,256,64):
        image = pygame.Surface((64, 64), pygame.SRCALPHA)
        image.blit(bullet_image, (0,0), Rect(j,496,64,64))
        image = pygame.transform.scale2x(image)
        a_list.append(image)
    for j in range (0,256,64):
        image = pygame.Surface((64, 64), pygame.SRCALPHA)
        image.blit(bullet_image, (0,0), Rect(j,560,64,64))
        image = pygame.transform.scale2x(image)
        a_list.append(image)
    cur_list.append(a_list)
    a_list = []
bullets = cur_list
image = pygame.Surface((32, 32), pygame.SRCALPHA)
bullets[0].append(image)
bullets[1].append(image)
bullets[2].append(image)
bullets[3].append(image)
bullets[4].append(image)
bullets[5].append(image)
bullets[6].append(image)
bullets[7].append(image)
bullets[8].append(image)
bullets[9].append(image)
bullets[10].append(image)
image = pygame.Surface((16, 16), pygame.SRCALPHA)
bullets[11].append(image)
bullets[12].append(image)
image = pygame.Surface((64, 64), pygame.SRCALPHA)
bullets[13].append(image)
bullets[14].append(image)
bullets[15].append(image)
bullets[16].append(image)
bullets[17].append(image)
bullets[18].append(image)
image = pygame.Surface((128, 128), pygame.SRCALPHA)
bullets[19].append(image)

pokeball = pygame.Surface((48, 16), pygame.SRCALPHA)
pokeball.blit(item_img,(0,0),(64,0,48,16))


cur_list = []
for i in range(0,112,16):
    image = pygame.Surface((16,16),pygame.SRCALPHA)
    image.blit(bullet_image,(0,0),Rect(i,176,16,16))
    for j in range(1,33):
        image2 = pygame.transform.scale(image, (j//2,j//2))
        a_list.append(image2)
    cur_list.append(a_list)
    a_list = []
bullet_erase = cur_list
cur_list = []
for i in range(0,256,32):
    image = pygame.Surface((32,32), pygame.SRCALPHA)
    image.blit(bullet_image, (0,0), Rect(i,400,32,32))
    for i in range(1,65,2):
        image2 = pygame.transform.scale(image,(i,i))
        a_list.append(image2)
    cur_list.append(a_list)
    a_list = []
bullet_taning = cur_list

cur_list = []
for i in range(0,128,16):
    image = pygame.Surface((16,16),pygame.SRCALPHA)
    image.blit(item_img, (0,0), Rect(i,0,16,16))
    cur_list.append(image)
items = cur_list

cur_list = []
a_list = []
for i in range(0,4):
    for j in range(0,10):
        image = pygame.Surface((64, 64), pygame.SRCALPHA)
        image.blit(pkmon_image, (0,0), Rect(j*64,i*64,64,64))
        image = pygame.transform.scale2x(image)
        cur_list.append(image)
image = pygame.Surface((64, 64), pygame.SRCALPHA)
image.blit(pkmon_image, (0,0), Rect(0,0,64,64))
image = pygame.transform.scale2x(image)
image = pygame.transform.flip(image, True, False)
cur_list.append(image)
image = pygame.Surface((64, 64), pygame.SRCALPHA)
image.blit(pkmon_image, (0,0), Rect(64,0,64,64))
image = pygame.transform.scale2x(image)
image = pygame.transform.flip(image, True, False)
cur_list.append(image)
pokemons = cur_list
# 이펙트 미리 그려놓기
cur_list = []
for i in range(0,360):
    image = pygame.Surface((256,256), pygame.SRCALPHA)
    image.blit(bullet_image,(0,0),(0,496,256,256))
    image = pygame.transform.scale(image,(128,128))
    image = pygame.transform.rotate(image, i)
    cur_list.append(image)
boss_circle = cur_list
white_circle = []
cur_list = []
for i in range(1,256):
    image = pygame.Surface((2*i,2*i), pygame.SRCALPHA)
    pygame.draw.circle(image, (255,255,255,256-i), (2*i//2,2*i//2), 2*i//2)
    cur_list.append(image)
white_circle.append(cur_list)

cur_list = []
for i in range(1,256):
    image = pygame.Surface((2*i,2*i), pygame.SRCALPHA)
    pygame.draw.circle(image, (255,0,0,256-i), (2*i//2,2*i//2), 2*i//2)
    cur_list.append(image)
white_circle.append(cur_list)

cur_list = []
for i in range(1,256):
    image = pygame.Surface((2*i,2*i), pygame.SRCALPHA)
    pygame.draw.circle(image, (255,0,255,256-i), (2*i//2,2*i//2), 2*i//2)
    cur_list.append(image)
white_circle.append(cur_list)

cur_list = []



for i in range(0,60):
    image = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
    image.fill((0,0,0,0+i*4))
    cur_list.append(image)
for i in range(0,60):
    image = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
    image.fill((0,0,0))
    cur_list.append(image)
for i in range(0,60):
    image = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
    image.fill((0,0,0,255-i*4))
    cur_list.append(image)
black_screen = cur_list
cur_list = []
for i in range(100,256,4):
    image = pygame.Surface((64,64), pygame.SRCALPHA)        
    image.blit(bullet_image,(0,0),(192,128,64,64))
    image = pygame.transform.scale(image, (i/2, i/2))
    image.fill((255, 255, 255, 340-i), special_flags=pygame.BLEND_RGBA_MULT)
    cur_list.append(image)
enemy_died_circle = cur_list
cur_list = []
for i in range(1,255,4):
    width = 256-i
    image = pygame.Surface((width,width), pygame.SRCALPHA)
    rect2 = round(image.get_width()/2)
    pygame.draw.circle(image, (255,255,255,256-i), (rect2,rect2), 1 if rect2-1 < 1 else rect2-1,1)
    cur_list.append(image)
died_white_circle = cur_list
cur_list = []
for i in range(0,1):
    image = pygame.Surface((64,64), pygame.SRCALPHA)
    image.blit(bullet_image,(0,0),(128,128,64,64))
    for j in range(0,90):
        image2 = pygame.transform.rotate(image, j*2)  
        image3 = pygame.transform.rotate(image, -j*2)  
        rect = image2.get_rect() 
        pygame.draw.circle(image2 , (200,100,100),rect.center, 4)
        pygame.draw.circle(image2 , (255,255,255),rect.center, 3)     
        rect3 = image3.get_rect() 
        pygame.draw.circle(image3 , (200,100,100),rect3.center, 4)
        pygame.draw.circle(image3 , (255,255,255),rect3.center, 3) 
        image2.blit(image3,(0,0))
        cur_list.append(image2)
slow_player_circle = cur_list
cur_list = []
for i in range(0,1):
    image = pygame.Surface((64,64), pygame.SRCALPHA)
    image.blit(bullet_image,(0,0),(128,0,64,64))
    for j in range(0,180):
        image2 = pygame.transform.rotate(image, j*2)  
        rect = image2.get_rect()   
        cur_list.append(image2)
magic_circle_sprite = cur_list

# 이미지 나눠 저장하기 
RIGHT_POS = [(WIDTH+64,-64),(WIDTH+64,HEIGHT/6-32),(WIDTH+64,HEIGHT/4),(WIDTH+64,HEIGHT/6*2+32),(WIDTH+64,HEIGHT/2),(WIDTH+64,HEIGHT/6+HEIGHT/2-32),(WIDTH+64,HEIGHT/4+HEIGHT/2),(WIDTH+64,HEIGHT/6*2+HEIGHT/2+32),(WIDTH+64,HEIGHT+64)]
RIGHT_POS2 = [(WIDTH+64,HEIGHT/6-32),(WIDTH+64,HEIGHT/4),(WIDTH+64,HEIGHT/6*2+32),(WIDTH+64,HEIGHT/2),(WIDTH+64,HEIGHT/6+HEIGHT/2-32),(WIDTH+64,HEIGHT/4+HEIGHT/2),(WIDTH+64,HEIGHT/6*2+HEIGHT/2+32)]
UP_POS = [(WIDTH/2,-64),(WIDTH/2+54,-64),(WIDTH/2+54*2,-64),(WIDTH/2+54*3,-64),(WIDTH/2+54*4,-64)]
DOWN_POS = [(WIDTH/2,HEIGHT+64),(WIDTH/2+54,HEIGHT+64),(WIDTH/2+54*2,HEIGHT+64),(WIDTH/2+54*3,HEIGHT+64),(WIDTH/2+54*4,HEIGHT+64)]

clock = pygame.time.Clock()
prev_time = time.time()
dt = 0
FPS = 60
clock_fps = 60
TARGET_FPS = 60
keys = pygame.key.get_pressed() 
boss_movebox = Rect(300,35,204,292)
score = 0
hiscore = 0
bkgd_list = []
# 폰트 불러오기
score_font = pygame.font.Font(FONT_1, 25)
debug_font = pygame.font.Font(FONT_1, 21)
font1 = pygame.font.Font(FONT_1, 18)
#쌀점,경험치,고속주행,그레이즈, 포획, 스펠클리어
score_setting = (1000,2000,1,200,50000,777777,0,0,0)
bullet_border_wide = 200
bullet_border = Rect(0-bullet_border_wide, 0-bullet_border_wide, WIDTH*2 + bullet_border_wide*2, HEIGHT*2 + bullet_border_wide*2)
small_border = Rect(0, 0, WIDTH*2, HEIGHT*2)
near_border= Rect(0, 0, WIDTH, HEIGHT)
far_border= Rect(-50, -50, WIDTH+100, HEIGHT+100)
bullet_size = (10,6,8,8,6,6,6,9,6,7,7,4,5,15,15,20,10,10,10,20,15)
game_restart = False
effect_group = 0  