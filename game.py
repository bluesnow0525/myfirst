from matplotlib.pyplot import draw
import pygame
import os

FPS=60
WIDTH=600
HEIGHT=600
ground_color=(230,230,250)
player1_color=(255,69,0)
player2_color=(0,191,255)
bullet_color=(255,215,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
#game start
pygame.init()
screen=pygame.display.set_mode((600,600))
clock=pygame.time.Clock()
pygame.display.set_caption("決鬥寶")
#img
player1_img = pygame.image.load(os.path.join("img", "player1.jpg")).convert()
player2_img = pygame.image.load(os.path.join("img", "player2.jpg")).convert()
ground_img = pygame.image.load(os.path.join("img", "ground.jpg")).convert()
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
#sprite 物件
class Player1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player1_img, (80, 60))
        self.image.set_colorkey((255,255,255))
        self.rect=self.image.get_rect()
        self.rect.centerx=WIDTH*3/4
        self.rect.bottom=HEIGHT-51
        self.ori_botton=0
        self.speed_x=4
        self.speed_y=2
        self.speed_jumpup=10
        self.ifjump=0
        self.ifjumpup=0
        self.way=1
        self.life=100
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
                self.rect.y-=2
                self.ifjump=0
        if(key_press[pygame.K_RIGHT]):
            if(self.way==1):
                self.rotate()
            self.way=2
            self.rect.x+=self.speed_x
            ifhit=pygame.sprite.spritecollide(player1,grounds,False)
            if ifhit:
                self.rect.x-=5
                self.rect.y-=2
            if(self.rect.bottom<=HEIGHT-200 and self.rect.left>=325):
                self.ifjump=1
        if(key_press[pygame.K_LEFT]):
            if(self.way==2):
                self.rotate()
            self.way=1
            self.rect.x-=self.speed_x
            ifhit=pygame.sprite.spritecollide(player1,grounds,False)
            if ifhit:
                self.rect.x+=5
                self.rect.y-=2
            if(self.rect.bottom<=HEIGHT-200 and self.rect.right<=175):
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
        self.ori_botton=0
        self.speed_x=4
        self.speed_y=2
        self.speed_jumpup=10
        self.ifjump=0
        self.ifjumpup=0
        self.way=2
        self.life=100
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
                self.rect.y-=2
                self.ifjump=0
        if(key_press[pygame.K_d]):
            if(self.way==1):
                self.rotate()
            self.way=2
            self.rect.x+=self.speed_x
            ifhit=pygame.sprite.spritecollide(player2,grounds,False)
            if ifhit:
                self.rect.x-=5
                self.rect.y-=2
            if(self.rect.bottom<=HEIGHT-200 and self.rect.left>=325):
                self.ifjump=1
        if(key_press[pygame.K_a]):
            if(self.way==2):
                self.rotate()
            self.way=1
            self.rect.x-=self.speed_x
            ifhit=pygame.sprite.spritecollide(player2,grounds,False)
            if ifhit:
                self.rect.x+=5
                self.rect.y-=2
            if(self.rect.bottom<=HEIGHT-200 and self.rect.right<=175):
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
    def rotate(self):
        self.image = pygame.transform.flip(self.image,True,False)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
class Bullet(pygame.sprite.Sprite):
    def __init__(self, xy, lr):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,10))
        self.image.fill(bullet_color)
        self.rect = self.image.get_rect()
        self.rect.center = xy
        if(lr==1):
            self.speedx = -10
        else:
            self.speedx = 10

    def update(self):
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
        
all_sprites=pygame.sprite.Group()
p1bullets=pygame.sprite.Group()
p2bullets=pygame.sprite.Group()
grounds=pygame.sprite.Group()
g1=Ground(0,HEIGHT-50,WIDTH,50)
grounds.add(g1)
all_sprites.add(g1)
g2=Ground(175,HEIGHT-200,250,30)
grounds.add(g2)
all_sprites.add(g2)
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
#screens
def draw_init():
    draw_text(screen, "遊戲開始", 64, WIDTH/2, HEIGHT/4)
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
    draw_text(screen,"人類 win",64,WIDTH/2,HEIGHT/2)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True   
def drawp2win():
    screen.fill((0,0,0))
    draw_text(screen,"企鵝 win",64,WIDTH/2,HEIGHT/2)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
def draw_life(surf,hp,x,y):
    if hp<0:
        hp=0
    BAR_LENGTH=80
    BAR_HEIGHT=10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
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
    if show_p1win:
        drawp1win()
    if show_p2win:
        drawp2win()
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
            if event.key == pygame.K_p:
                player1.shoot()
            if event.key == pygame.K_SPACE:
                player2.shoot() 
                    
    #更新game 
    all_sprites.update()
    hitp1=pygame.sprite.spritecollide(player1,p2bullets,True)
    hitp2=pygame.sprite.spritecollide(player2,p1bullets,True)
    pygame.sprite.groupcollide(grounds,p1bullets,False,True)
    pygame.sprite.groupcollide(grounds,p2bullets,False,True)
    hits=pygame.sprite.groupcollide(p1,p2,False,False)  
    if hits:
        if(player1.rect.x>player2.rect.x):
            player1.rect.x+=20
            player2.rect.x-=20
        else:
            player1.rect.x-=20
            player2.rect.x+=20
        
    if hitp1:
        player1.life-=10
    if hitp2:
        player2.life-=10
    if(player1.life<=0):
        player1.kill()
        player2.kill()
        show_p2win=True
    if(player2.life<=0):
        player1.kill()
        player2.kill()
        show_p1win=True
    
    #screen show
    #screen.blit(background_img, (0,0))
    screen.fill(ground_color)
    all_sprites.draw(screen)
    draw_life(screen,player1.life,player1.rect.x,player1.rect.y-12)
    draw_life(screen,player2.life,player2.rect.x,player2.rect.y-12)
    pygame.display.update()

pygame.quit()