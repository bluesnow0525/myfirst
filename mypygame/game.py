
import pygame
import os
import random 

FPS=60
WIDTH=600
HEIGHT=600
ground_color=(250,250,250)
player1_color=(255,69,0)
player2_color=(0,191,255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
#game start
pygame.init()
screen=pygame.display.set_mode((600,600))
clock=pygame.time.Clock()
pygame.display.set_caption("閩客械鬥")
#img
background_img = pygame.image.load(os.path.join("img", "back3.jpg")).convert()
player1_img = pygame.image.load(os.path.join("img", "p1_pic.png")).convert()
player2_img = pygame.image.load(os.path.join("img", "p2_pic.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet_pic.png")).convert()
ground_img = pygame.image.load(os.path.join("img", "ground.jpg")).convert()
fire_img = pygame.image.load(os.path.join("img", "fire2.jpg")).convert()
rock_imgs = []
for i in range(5):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
power_img= pygame.image.load(os.path.join("img", "gun.png")).convert()

for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
#music
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound", "back2.ogg"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
#sprite 物件
class Player1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player1_img, (80, 60))
        self.image.set_colorkey((255,255,255))
        self.rect=self.image.get_rect()
        self.rect.centerx=WIDTH*3/4
        self.rect.bottom=HEIGHT-51
        self.radius=35
        self.ori_botton=0
        self.speed_x=6
        self.speed_y=3
        self.speed_jumpup=10
        self.ifjump=0
        self.ifjumpup=0
        self.way=1
        self.life=100
        self.bullets=20
    def update(self):
        key_press=pygame.key.get_pressed()
        if(self.ifjumpup==1):
            self.rect.y-=self.speed_jumpup
            ifhit=pygame.sprite.spritecollide(player1,grounds,False)
            if(self.rect.bottom<=self.ori_botton-200 or ifhit):
                if ifhit:
                    self.rect.y+=10
                self.ifjumpup=0
                self.ifjump=1
        if(self.ifjump==1):
            self.rect.y+=self.speed_y
            ifhit=pygame.sprite.spritecollide(player1,grounds,False)
            if(self.rect.bottom>=HEIGHT-50 or ifhit):
                self.rect.y-=3
                self.ifjump=0
        if(key_press[pygame.K_RIGHT]):
            if(self.way==1):
                self.rotate()
            self.way=2
            self.rect.x+=self.speed_x
            ifhit=pygame.sprite.spritecollide(player1,grounds,False)
            if ifhit:
                self.rect.x-=7
                self.rect.y-=3
            if(self.rect.bottom<=HEIGHT-200 and self.rect.left>=405):
                self.ifjump=1
            if(self.rect.bottom<=250 and self.rect.left>=100):
                self.ifjump=1
        if(key_press[pygame.K_LEFT]):
            if(self.way==2):
                self.rotate()
            self.way=1
            self.rect.x-=self.speed_x
            ifhit=pygame.sprite.spritecollide(player1,grounds,False)
            if ifhit:
                self.rect.x+=7
                self.rect.y-=3
            if(self.rect.bottom<=HEIGHT-200 and self.rect.right<=175):
                self.ifjump=1
            if(self.rect.bottom<=250 and self.rect.right<=500):
                self.ifjump=1
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.left<0:
            self.rect.left=0
    def jump(self):
        self.ori_botton=self.rect.bottom
        self.ifjumpup=1
        self.ifjump=0
    def shoot(self):
        bullet=Bullet(self.rect.center,self.way)
        all_sprites.add(bullet)
        p1bullets.add(bullet)
        shoot_sound.play()
    def rotate(self):
        self.image = pygame.transform.flip(self.image,True,False)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player2_img, (80, 60))
        self.image.set_colorkey((255,255,255))
        self.rect=self.image.get_rect()
        self.rect.centerx=WIDTH/4
        self.rect.bottom=HEIGHT-50
        self.radius=35
        self.ori_botton=0
        self.speed_x=6
        self.speed_y=3
        self.speed_jumpup=10
        self.ifjump=0
        self.ifjumpup=0
        self.way=2
        self.life=100
        self.bullets=20
    def update(self):
        key_press=pygame.key.get_pressed()
        if(self.ifjumpup==1):
            self.rect.y-=self.speed_jumpup
            ifhit=pygame.sprite.spritecollide(player2,grounds,False)
            if(self.rect.bottom<=self.ori_botton-200 or ifhit):
                if ifhit:
                    self.rect.y+=10
                self.ifjumpup=0
                self.ifjump=1
        if(self.ifjump==1):
            self.rect.y+=self.speed_y
            ifhit=pygame.sprite.spritecollide(player2,grounds,False)
            if(self.rect.bottom>=HEIGHT-50 or ifhit):
                self.rect.y-=3
                self.ifjump=0
        if(key_press[pygame.K_d]):
            if(self.way==1):
                self.rotate()
            self.way=2
            self.rect.x+=self.speed_x
            ifhit=pygame.sprite.spritecollide(player2,grounds,False)
            if ifhit:
                self.rect.x-=7
                self.rect.y-=3
            if(self.rect.bottom<=HEIGHT-200 and self.rect.left>=405):
                self.ifjump=1
            if(self.rect.bottom<=250 and self.rect.left>=100):
                self.ifjump=1
        if(key_press[pygame.K_a]):
            if(self.way==2):
                self.rotate()
            self.way=1
            self.rect.x-=self.speed_x
            ifhit=pygame.sprite.spritecollide(player2,grounds,False)
            if ifhit:
                self.rect.x+=7
                self.rect.y-=3
            if(self.rect.bottom<=HEIGHT-200 and self.rect.right<=175):
                self.ifjump=1
            if(self.rect.bottom<=250 and self.rect.right<=500):
                self.ifjump=1
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.left<0:
            self.rect.left=0
    def jump(self):
        self.ori_botton=self.rect.bottom
        self.ifjumpup=1
        self.ifjump=0
    def shoot(self):
        bullet=Bullet(self.rect.center,self.way)
        all_sprites.add(bullet)
        p2bullets.add(bullet)
        shoot_sound.play()
    def rotate(self):
        self.image = pygame.transform.flip(self.image,True,False)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
class Bullet(pygame.sprite.Sprite):
    def __init__(self, xy, lr):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = pygame.transform.scale(bullet_img, (25, 25))
        self.image_ori.set_colorkey((255,255,255))
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.total_degree = 0
        self.rot_degree = random.randrange(-30, 30)
        if(lr==1):
            self.speedx = -10
        else:
            self.speedx = 10
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        if self.rect.left<0 or self.rect.right>WIDTH:
            self.kill()
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ground_img, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs) 
        self.image_ori.set_colorkey((0,0,0))
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 4)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)
class Fire(pygame.sprite.Sprite):
    def __init__(self,x,y,l):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(fire_img, (l, 30))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
class Power(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = power_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 4)
        self.speedx = random.randrange(-1, 1)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

all_sprites=pygame.sprite.Group()
p1bullets=pygame.sprite.Group()
p2bullets=pygame.sprite.Group()
grounds=pygame.sprite.Group()
rocks = pygame.sprite.Group()
fires=pygame.sprite.Group()
powers=pygame.sprite.Group()
g1=Ground(0,HEIGHT-50,WIDTH,50)
grounds.add(g1)
all_sprites.add(g1)
g2=Ground(175,HEIGHT-200,250,30)
grounds.add(g2)
all_sprites.add(g2)
g3=Ground(0,250,100,30)
grounds.add(g3)
all_sprites.add(g3)
g4=Ground(500,250,100,30)
grounds.add(g4)
all_sprites.add(g4)
fire1=Fire(0,HEIGHT-70,200)
all_sprites.add(fire1)
fires.add(fire1)
fire2=Fire(200,HEIGHT-70,200)
all_sprites.add(fire2)
fires.add(fire2)
fire3=Fire(400,HEIGHT-70,200)
all_sprites.add(fire3)
fires.add(fire3)
fire4=Fire(0,230,100)
all_sprites.add(fire4)
fires.add(fire4)
fire5=Fire(500,230,100)
all_sprites.add(fire5)
fires.add(fire5)
player1=Player1()
player2=Player2()
p1=pygame.sprite.Group()
p2=pygame.sprite.Group()
p1.add(player1)
p2.add(player2)
all_sprites.add(player1)
all_sprites.add(player2)

font_name = os.path.join("font.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)
def new_power():
    p = Power()
    all_sprites.add(p)
    powers.add(p)
#screens
def draw_init():
    draw_text(screen, "按任意鍵開始", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "客家人:上、左、右、右Ctrl鍵", 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "閩南人:W、A、D、空白鍵", 22, WIDTH/2-15, HEIGHT/2+40)
    draw_text(screen, "PS:飛鏢射到落石可回血，吃到能量可增加飛鏢數量", 14, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:
                waiting = False
                return False
def drawp1win():
    screen.fill((0,0,0))
    draw_text(screen,"客家人 win",64,WIDTH/2,HEIGHT/4)
    draw_text(screen, "按m後重新開始", 22, WIDTH/2, HEIGHT/2)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:                   
                    waiting = False                    
                    return False  
def drawp2win():
    screen.fill((0,0,0))
    draw_text(screen,"閩南人 win",64,WIDTH/2,HEIGHT/4)
    draw_text(screen, "按m後重新開始", 22, WIDTH/2, HEIGHT/2)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    waiting = False
                    return False
def draw_life(surf,hp,x,y,bul):
    if hp<0:
        hp=0
    BAR_LENGTH=80
    BAR_HEIGHT=10
    fill = (hp/100)*BAR_LENGTH
    fill2 = (bul/20)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y-15, BAR_LENGTH, BAR_HEIGHT)
    outline_rect2 = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y-15, fill, BAR_HEIGHT)
    fill_rect2 = pygame.Rect(x, y, fill2, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    pygame.draw.rect(surf, YELLOW, fill_rect2)
    pygame.draw.rect(surf, WHITE, outline_rect2, 2)
    #draw_blacktext(screen, str(bul), 14, x+40, y-25)
#game
running=True
show_init=True
show_p1win=False
show_p2win=False
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        for i in range(4):
            new_rock()
        new_power()
    if show_p1win:
        close = drawp1win()
        if close:
            break
        player1=Player1()
        player2=Player2()
        p1=pygame.sprite.Group()
        p2=pygame.sprite.Group()
        p1.add(player1)
        p2.add(player2)
        all_sprites.add(player1)
        all_sprites.add(player2)
        show_p1win=False
    if show_p2win:
        close = drawp2win()
        if close:
            break
        player1=Player1()
        player2=Player2()
        p1=pygame.sprite.Group()
        p2=pygame.sprite.Group()
        p1.add(player1)
        p2.add(player2)
        all_sprites.add(player1)
        all_sprites.add(player2)
        show_p2win=False
    clock.tick(FPS)
    #get
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            running=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if(player1.ifjump==0 and player1.ifjumpup==0):
                    player1.jump()
            if event.key == pygame.K_w:
                if(player2.ifjump==0 and player2.ifjumpup==0):
                    player2.jump()
            if event.key == pygame.K_RCTRL:
                if player1.bullets!=0:
                    player1.shoot()
                    player1.bullets-=1
            if event.key == pygame.K_SPACE:
                if player2.bullets!=0:
                    player2.shoot() 
                    player2.bullets-=1
                    
    #更新game 
    all_sprites.update()
    hitp1=pygame.sprite.spritecollide(player1,p2bullets,True)
    hitp2=pygame.sprite.spritecollide(player2,p1bullets,True)
    fhitp1=pygame.sprite.spritecollide(player1,fires,False)
    fhitp2=pygame.sprite.spritecollide(player2,fires,False)
    pygame.sprite.groupcollide(grounds,p1bullets,False,True)
    pygame.sprite.groupcollide(grounds,p2bullets,False,True)
    brhit1=pygame.sprite.groupcollide(rocks,p1bullets,True,True)
    brhit2=pygame.sprite.groupcollide(rocks,p2bullets,True,True)
    hits=pygame.sprite.groupcollide(p1,p2,False,False)  
    rhit=pygame.sprite.groupcollide(rocks,grounds,True,False)
    rhitp1=pygame.sprite.spritecollide(player1,rocks,True,pygame.sprite.collide_circle)
    rhitp2=pygame.sprite.spritecollide(player2,rocks,True,pygame.sprite.collide_circle)
    phitp1=pygame.sprite.groupcollide(p1,powers,False,True)
    phitp2=pygame.sprite.groupcollide(p2,powers,False,True)
    for hit in brhit1:
        new_rock()
        player1.life+=3
        if player1.life>100:
            player1.life=100
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
    for hit in brhit2:
        new_rock()
        player2.life+=3
        if player2.life>100:
            player2.life=100
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
    if rhit:
        new_rock()
    if hits:
        if(player1.rect.x>player2.rect.x):
            player1.rect.x+=20
            player2.rect.x-=20
        else:
            player1.rect.x-=20
            player2.rect.x+=20  
        player2.life-=0.5
        player1.life-=0.5
    if hitp1:
        random.choice(expl_sounds).play()
        player1.life-=7.5
    if hitp2:
        random.choice(expl_sounds).play()
        player2.life-=7.5
    for hit in rhitp1:
        new_rock()
        player1.life-=hit.radius * 1.5
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
    for hit in rhitp2:
        new_rock()
        player2.life-=hit.radius * 1.5
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
    if fhitp1:
        player1.life-=0.05
    if fhitp2:
        player2.life-=0.05
    for hit in phitp1:
        new_power()
        player1.bullets+=5
        if player1.bullets>=20:
            player1.bullets=20
    for hit in phitp2:
        new_power()
        player2.bullets+=5
        if player2.bullets>=20:
            player2.bullets=20
    if(player1.life<=0):
        player1.kill()
        player2.kill()
        die_sound.play()
        show_p2win=True
    if(player2.life<=0):
        player1.kill()
        player2.kill()
        die_sound.play()
        show_p1win=True
    
    #screen show
    #screen.blit(background_img, (0,0))
    screen.fill(ground_color)
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    draw_life(screen,player1.life,player1.rect.x,player1.rect.y-12,player1.bullets)
    draw_life(screen,player2.life,player2.rect.x,player2.rect.y-12,player2.bullets)
    pygame.display.update()

pygame.quit()