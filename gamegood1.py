 # Imports
import pygame
import random
import json

#this is a check


# Window settings
GRID_SIZE = 64
WIDTH = 20 * GRID_SIZE
HEIGHT = 13 * GRID_SIZE
TITLE = "Save Candy Land"
FPS = 60


# Create window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (0, 150, 255)
GRAY = (175, 175, 175)
RED = (252, 28, 3)
GOLD = (252, 186, 3)

#STAGEs
START = 0
PLAYING = 1
LOSE = 2
LEVEL_COMPLETE = 3
WIN = 4


# Load fonts
font_xs = pygame.font.Font('assets/fonts/Sweet-Candy.ttf', 14)
font_sm = pygame.font.Font('assets/fonts/Sweet-Candy.ttf', 24)
font_md = pygame.font.Font('assets/fonts/Sweet-Candy.ttf', 50)
font_lg = pygame.font.Font('assets/fonts/Sweet-Candy.ttf', 75)
font_xl = pygame.font.Font('assets/fonts/Sweet-Candy.ttf', 96)

#Load Sounds
jump_snd = pygame.mixer.Sound('assets/sounds/jump.wav')
gem_snd = pygame.mixer.Sound('assets/sounds/pickup_item.wav')
level_up_snd = pygame.mixer.Sound('assets/sounds/achievement.wav')
theme = 'assets/music/candy-rush.wav'

# Music

# Load images
hero_idle_imgs_rt = [pygame.image.load('assets/images/characters/player_idle.png').convert_alpha()]
hero_walk_imgs_rt = [pygame.image.load('assets/images/characters/player_walk2.png').convert_alpha(),
                     pygame.image.load('assets/images/characters/player_walk1.png').convert_alpha()]
hero_jump_imgs_rt = [pygame.image.load('assets/images/characters/player_jump.png').convert_alpha()]

hero_idle_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_idle_imgs_rt ]
hero_walk_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_walk_imgs_rt ]
hero_jump_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_jump_imgs_rt ]

frosting_cake_img = pygame.image.load('assets/images/tiles/cake.png').convert_alpha()
cake_img = pygame.image.load('assets/images/tiles/cakecenter.png').convert_alpha()
candycaneblock1_img = pygame.image.load('assets/images/tiles/hillCanePinkTop.png').convert_alpha()
candycaneblock2_img = pygame.image.load('assets/images/tiles/hillCaneGreenTop.png').convert_alpha()
dirt_img = pygame.image.load('assets/images/tiles/block.png').convert_alpha()
background_img = pygame.image.load('assets/Backgrounds/backgroundCastles.png').convert_alpha()
gem_img = pygame.image.load('assets/images/items/cherry.png').convert_alpha()
gemgold_img = pygame.image.load('assets/images/items/cherrygold.png').convert_alpha()

gemsm_img = pygame.image.load('assets/images/items/cherrysm.png').convert_alpha()
heart_img = pygame.image.load('assets/images/items/heart(1).png').convert_alpha()
icecream_img = pygame.image.load('assets/images/tiles/cupCake.png').convert_alpha()
icecreamtop2_img = pygame.image.load('assets/images/tiles/creamChoco.png').convert_alpha()
icecream_img = pygame.image.load('assets/images/tiles/cupCake.png').convert_alpha()
oreobrown_img = pygame.image.load('assets/images/tiles/cookieBrown.png').convert_alpha()
lollipopred_img = pygame.image.load('assets/images/tiles/lollipopFruitRed.png').convert_alpha()
lollipopstick_img = pygame.image.load('assets/images/tiles/lollipopbase.png').convert_alpha()
cakehillleft_img = pygame.image.load('assets/images/tiles/cakeHillLeft.png').convert_alpha()
cakehillright_img = pygame.image.load('assets/images/tiles/cakeHillRight.png').convert_alpha()



gumdrop_imgs_rt = [pygame.image.load('assets/images/characters/gumdropenemy.png').convert_alpha(),
                pygame.image.load('assets/images/characters/gumdropenemyw1.png').convert_alpha()]
gumdrop_imgs_lt = [pygame.transform.flip(img, True, False) for img in gumdrop_imgs_rt ]

kitkat_imgs_rt = [pygame.image.load('assets/images/characters/kitkat.png').convert_alpha(),
                pygame.image.load('assets/images/characters/kitkatw1.png').convert_alpha()]
kitkat_imgs_lt = [pygame.transform.flip(img, True, False) for img in kitkat_imgs_rt ]

gummyworm_imgs_rt = [pygame.image.load('assets/images/characters/wormenemyw1.png').convert_alpha(),
                  pygame.image.load('assets/images/characters/wormenemyw1c.png').convert_alpha()]
gummyworm_imgs_lt = [pygame.transform.flip(img, True, False) for img in gummyworm_imgs_rt ]


cottoncandy_imgs = [pygame.image.load('assets/images/characters/cottoncandycloud.png').convert_alpha(),
                   pygame.image.load('assets/images/characters/cottoncandycloud2.png').convert_alpha()]

pole_img = pygame.image.load('assets/images/tiles/canePinklong.png').convert_alpha()
flag_img = pygame.image.load('assets/images/tiles/canePinkTop.png').convert_alpha()
backgroundcandy_img = pygame.image.load('assets/Backgrounds/here.png').convert_alpha()
backgroundcandyend_img = pygame.image.load('assets/Backgrounds/here - Copy.png').convert_alpha()
backgroundcandywin_img = pygame.image.load('assets/Backgrounds/win.png').convert_alpha()
candybox_img = pygame.image.load('assets/images/tiles/candybox(1).png').convert_alpha()






# Load levels
levels = ['assets/levels/world-1.json',
          'assets/levels/world-2.json',
          'assets/levels/world-3.json']

#Settings


# Game classes
class Entity(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE // 2

        self.vx = 0
        self.vy = 0

    def apply_gravity(self):
        self.vy += gravity
        if self.vy > terminal_velocity:
            self.vy = terminal_velocity

class AnimatedEntity(Entity):
    def __init__(self, x , y, images):
        super().__init__(x, y, images[0])

        self.images = images
        self.image_index = 0
        self.ticks = 0
        self.animation_speed = 10
        self.facing_right = True

    def check_world_edge(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx = self.speed
        elif self.rect.right > world_width:
            self.rect.right = world_width
            self.vx = -1 * self.speed
            
    def move_and_check_blocks(self):
        self.rect.x += self.vx
        hits = pygame.sprite.spritecollide(self, platforms, False)

        for block in hits:
            if self.vx > 0:
                self.rect.right = block.rect.left
            elif self.vx < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.vy
        hits = pygame.sprite.spritecollide(self, platforms, False)

        for block in hits:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.jumping = False
            elif self.vy < 0:
                self.rect.top = block.rect.bottom

            self.vy = 0

    def set_image_list(self):
        self.images = self.images

    def animate(self):
        self.set_image_list()
        self.ticks += 1

        if self.ticks % self.animation_speed == 0:
            self.image_index += 1

            if self.image_index >= len(self.images):
                self.image_index = 0
                
            self.image = self.images[self.image_index]
        
class Hero(AnimatedEntity):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        
        self.speed = 5
        self.jump_power = 24

        self.vx = 0
        self.vy = 0
        self.hurt_timer = 0
        self.hearts = 50
        self.gems = 0
        self.score = 0
        self.jumping = False

    def move_to(self, x, y):
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE // 2

        
    def move_right(self):
        self.vx = self.speed
        self.facing_right = True
        
    def move_left(self):
        self.vx = -1 * self.speed
        self.facing_right = False

    def stop(self):
        self.vx = 0
    
    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 1

        if len(hits) > 0:
            self.vy = -1 * self.jump_power
            self.jumping = True
            jump_snd.play()

    def move_and_check_blocks(self):
        self.rect.x += self.vx
        hits = pygame.sprite.spritecollide(self, platforms, False)

        for block in hits:
            if self.vx > 0:
                self.rect.right = block.rect.left
            elif self.vx < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.vy
        hits = pygame.sprite.spritecollide(self, platforms, False)

        for block in hits:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.jumping = False
            elif self.vy < 0:
                self.rect.top = block.rect.bottom

            self.vy = 0

    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx = self.speed
        elif self.rect.right > world_width:
            self.rect.right = world_width
            self.vx = -1 * self.speed

    def check_items(self):
        hits = pygame.sprite.spritecollide(self, items, True)

        for item in hits:
            item.apply(self)

    def check_enemies(self):
            hits = pygame.sprite.spritecollide(self, enemies, False)

            for enemy in hits:
                if self.hurt_timer == 0:
                    for enemy in hits:
                        self.hearts -= 1
                        self.hurt_timer = 1.0 * FPS

                if self.rect.centerx < enemy.rect.centerx:
                    self.rect.right = enemy.rect.left
                elif self.rect.centerx > enemy.rect.centerx:
                    self.rect.left = enemy.rect.right

                if self.rect.centery < enemy.rect.centery:
                    self.rect.bottom = enemy.rect.top
                elif self.rect.centery > enemy.rect.centery:
                    self.rect.top = enemy.rect.bottom


            self.hurt_timer -= 1

            if self.hurt_timer < 0:
                self.hurt_timer = 0

    def reached_goal(self):
        return pygame.sprite.spritecollideany(self, goal)

    def set_image_list(self):
        if self.facing_right:
            if self.jumping:
                self.images = hero_jump_imgs_rt
            if self.vx != 0:
                self.images = hero_walk_imgs_rt
            else:
                self.images = hero_idle_imgs_rt
        else:
            if self.jumping:
                self.images = hero_jump_imgs_lt
            elif self.vx == 0:
                self.images = hero_idle_imgs_lt
            else:
                self.images = hero_walk_imgs_lt
        
    def update(self):
        self.apply_gravity()
        self.move_and_check_blocks()
        self.check_world_edges()
        self.check_items()
        self.check_enemies()
        self.animate()

class Enemy(AnimatedEntity):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.speed = 2
        self.vx = -1 * self.speed
        self.vy = 0

    def reverse(self):
        self.vx *= -1

    def move_and_check_blocks(self):
        self.rect.x += self.vx
        hits = pygame.sprite.spritecollide(self, platforms, False)

        for block in hits:
            if self.vx > 0:
                self.rect.right = block.rect.left
            elif self.vx < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.vy
        hits = pygame.sprite.spritecollide(self, platforms, False)

        for block in hits:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
            elif self.vy < 0:
                self.rect.top = block.rect.bottom

            self.vy = 0

    def check_platform_edges(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2

        must_reverse = True

        for platform in hits:
            if self.vx < 0 and platform.rect.left <= self.rect.left:
                must_reverse = False
            elif self.vx > 0 and platform.rect.right >= self.rect.right:
                must_reverse = False

        if must_reverse:
            self.reverse()

    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx = self.speed
        elif self.rect.right > world_width:
            self.rect.right = world_width

       
    def update(self):
        self.move_and_check_blocks()
        self.check_world_edges()
        self.apply_gravity()
        self.check_platform_edges()

        
class Platform(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Flag(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Block(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        

class Gem(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def apply(self, character):
        character.gems += 1
        character.score += 10
        gem_snd.play()

class Gemgold(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def apply(self, character):
        character.gems += 1
        character.score += 20
        character.hearts += 1
        gem_snd.play()


class Icecream(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        

class Icecreamtop2(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        

class Oreobrown(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        

class Lollipopred(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        
class Lollipopstick(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Gumdrop(Enemy):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

    def set_image_list(self):
        if self.vx > 0:
            self.images = gumdrop_imgs_rt
        else:
            self.images = gumdrop_imgs_lt

    def update(self):
        self.move_and_check_blocks()
        self.check_world_edges()
        self.apply_gravity()
        self.check_platform_edges()
        self.animate()


class Kitkat(Enemy):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

    def set_image_list(self):
        if self.vx > 0:
            self.images = kitkat_imgs_rt
        else:
            self.images = kitkat_imgs_lt

    def update(self):
        self.move_and_check_blocks()
        self.check_world_edges()
        self.apply_gravity()
        self.check_platform_edges()
        self.animate()


class Gummyworm(Enemy):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        self.rect.bottom = y * GRID_SIZE + GRID_SIZE
        self.animation_speed = 20

    def set_image_list(self):
        if self.vx > 0:
            self.images = gummyworm_imgs_rt
        else:
            self.images = gummyworm_imgs_lt

    def update(self):
        self.move_and_check_blocks()
        self.check_world_edges()
        self.apply_gravity()
        self.check_platform_edges()
        self.animate()        



class Cottoncandy(Enemy):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        self.rect.bottom = y * GRID_SIZE + GRID_SIZE

        self.speed = .5

        self.vx = -1 * self.speed
        self.vy = 0

    def update(self):
        self.move_and_check_blocks()
        self.check_world_edges()
        self.animate()

        
              
# Helper functoins
def show_start_screen():
    screen.blit(backgroundcandy_img, [0, 0])
    text = font_xl.render(TITLE, True, BLACK)
    rect = text.get_rect()
    rect.center = WIDTH // 3.5, HEIGHT - 703
    screen.blit(text, rect)

    text = font_md.render("Press any key to start", True, BLACK)
    rect = text.get_rect()
    rect.center = WIDTH // 4.6, HEIGHT - 608
    screen.blit(text, rect)

    text = font_xl.render(TITLE, True, WHITE)
    rect = text.get_rect()
    rect.center = WIDTH // 3.5, HEIGHT - 700
    screen.blit(text, rect)

    text = font_md.render("Press any key to start", True, WHITE)
    rect = text.get_rect()
    rect.center = WIDTH // 4.6, HEIGHT - 605
    screen.blit(text, rect)


def show_lose_screen():
    screen.blit(backgroundcandyend_img, [0, 0])
    text = font_xl.render('GAME OVER', True, BLACK)
    rect = text.get_rect()
    rect.center = WIDTH // 3.5, HEIGHT - 703
    screen.blit(text, rect)

    text = font_md.render("Press \'r\' to restart", True, BLACK)
    rect = text.get_rect()
    rect.center = WIDTH // 4.6, HEIGHT - 608
    screen.blit(text, rect)

    text = font_xl.render('GAME OVER', True, RED)
    rect = text.get_rect()
    rect.center = WIDTH // 3.5, HEIGHT - 700
    screen.blit(text, rect)

    text = font_md.render("Press \'r\' to restart", True, RED)
    rect = text.get_rect()
    rect.center = WIDTH // 4.6, HEIGHT - 605
    screen.blit(text, rect)

def show_win_screen():
    screen.blit(backgroundcandywin_img, [0, 0])
    text = font_xl.render('You Win', True, BLACK)
    rect = text.get_rect()
    rect.center = WIDTH // 3.5, HEIGHT - 703
    screen.blit(text, rect)

    text = font_md.render("Press \'r\' to play again", True, BLACK)
    rect = text.get_rect()
    rect.center = WIDTH // 4.6, HEIGHT - 608
    screen.blit(text, rect)

    text = font_xl.render('You Win', True, GOLD)
    rect = text.get_rect()
    rect.center = WIDTH // 3.5, HEIGHT - 700
    screen.blit(text, rect)

    text = font_md.render("Press \'r\' to play again", True, GOLD)
    rect = text.get_rect()
    rect.center = WIDTH // 4.6, HEIGHT - 605
    screen.blit(text, rect)

def show_level_complete_screen():
    screen.blit(candybox_img, [300, 210])

    text = font_xl.render('Level Complete!', True, WHITE)
    rect = text.get_rect()
    rect.center = WIDTH // 2, HEIGHT // 2 - 8
    screen.blit(text, rect)

def show_hud():
    text = font_md.render( str (hero.score), True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, 1
    screen.blit(text, rect)

    screen.blit(gem_img, [WIDTH - 128, 16])
    text = font_md.render(str (hero.gems), True, WHITE)
    rect = text.get_rect()
    rect.topleft = WIDTH - 44, 28
    screen.blit(text, rect)

    text = font_sm.render('X' , True, WHITE)
    rect = text.get_rect()
    rect.topleft = WIDTH - 70, 45
    screen.blit(text, rect)


    for i in range(hero.hearts):
        x = i * 36
        y = 16
        screen.blit(heart_img, [x,y])


#Setup
def start_game():
    global hero, stage, current_level
    hero = Hero(0, 0, hero_idle_imgs_rt)
    stage = START
    current_level = 0
    
def start_level():
    global player, platforms, items, gravity, terminal_velocity, enemies, blocks
    global goal, hero, stage, icecream, icecreamtop2, oreobrown, lollipopred
    global lollipopstick, gumdrops, gummyworms, cottoncandy, world_width
    global world_height, all_sprites, kitkat
    
    platforms = pygame.sprite.Group()
    player = pygame.sprite.GroupSingle()
    icecream = pygame.sprite.Group()
    icecreamtop2 = pygame.sprite.Group()
    oreobrown = pygame.sprite.Group()
    lollipopred = pygame.sprite.Group()
    lollipopstick = pygame.sprite.Group()
    cottoncandy = pygame.sprite.Group()
    gumdrops = pygame.sprite.Group()
    gummyworms = pygame.sprite.Group()
    kitkat = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    items = pygame.sprite.Group()
    goal = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    
    with open (levels[current_level]) as f:
        data = json.load(f)

    world_width = data ['width'] * GRID_SIZE
    world_height = data ['height'] * GRID_SIZE

    hero.move_to(data['start'][0], data['start'][1])
    player.add(hero)
    


    for loc in data['frosting_cake']:
        x = loc[0]
        y = loc[1]
        p = Platform(x, y, frosting_cake_img)
        platforms.add(p)

    for loc in data['cake_locs']:
        x = loc[0]
        y = loc[1]
        p = Platform(x, y, cake_img)
        platforms.add(p)

    for loc in data['candycaneblock1_locs']:
        x = loc[0]
        y = loc[1]
        p = Platform(x, y, candycaneblock1_img)
        platforms.add(p)

    for loc in data['candycaneblock2_locs']:
        x = loc[0]
        y = loc[1]
        p = Platform(x, y, candycaneblock2_img)
        platforms.add(p)

    for loc in data['icecream_locs']:
        x = loc[0]
        y = loc[1]
        i = Icecream(x, y, icecream_img)
        icecream.add(i)

    for loc in data['icecreamtop2_locs']:
        x = loc[0]
        y = loc[1]
        i = Icecreamtop2(x, y, icecreamtop2_img)
        icecreamtop2.add(i)

    for loc in data['oreobrown_locs']:
        x = loc[0]
        y = loc[1]
        o = Oreobrown(x, y, oreobrown_img)
        oreobrown.add(o)

    for loc in data['lollipopred_locs']:
        x = loc[0]
        y = loc[1]
        l = Lollipopred(x, y, lollipopred_img)
        lollipopred.add(l)

    for loc in data['lollipopstick_locs']:
        x = loc[0]
        y = loc[1]
        l = Lollipopstick(x, y, lollipopstick_img)
        lollipopstick.add(l)

    for loc in data['gumdrop_locs']:
        x = loc[0]
        y = loc[1]
        g = Gumdrop(x, y, gumdrop_imgs_rt)
        enemies.add(g)

    for loc in data['gumdrop_locs']:
        x = loc[0]
        y = loc[1]
        g = Gumdrop(x, y, gumdrop_imgs_lt)
        enemies.add(g)

    for loc in data['kitkat_locs']:
        x = loc[0]
        y = loc[1]
        k = Kitkat(x, y, kitkat_imgs_lt)
        enemies.add(k)

    for loc in data['gummyworm_locs']:
        x = loc[0]
        y = loc[1]
        g = Gummyworm(x, y, gummyworm_imgs_lt)
        enemies.add(g)

    for loc in data['cottoncandy_locs']:
        x = loc[0]
        y = loc[1]
        c = Cottoncandy(x, y, cottoncandy_imgs)
        cottoncandy.add(c)

    for loc in data['gem_locs']:
        x = loc[0]
        y = loc[1]
        g = Gem(x, y, gem_img)
        items.add(g)

    for loc in data['gemgold_locs']:
        x = loc[0]
        y = loc[1]
        g = Gemgold(x, y, gemgold_img)
        items.add(g)

    for i, loc in enumerate(data['flag_locs']):
        if i == 0:
            goal.add( Flag(loc[0], loc[1], flag_img) )
        else:
            goal.add( Flag(loc[0], loc[1], pole_img) )

    gravity = data['gravity']
    terminal_velocity = data['terminal_velocity']

    all_sprites.add(player, platforms, items, enemies, goal)
    pygame.mixer.music.load(theme)
    pygame.mixer.music.play(-1)


def draw_grid(offset_x=0, offset_y=0):
    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        adj_x = x - offset_x % GRID_SIZE
        pygame.draw.line(screen, GRAY, [adj_x, 0], [adj_x, HEIGHT], 1)

    for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
        adj_y = y - offset_y % GRID_SIZE
        pygame.draw.line(screen, GRAY, [0, adj_y], [WIDTH, adj_y], 1)

    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
            adj_x = x - offset_x % GRID_SIZE + 4
            adj_y = y - offset_y % GRID_SIZE + 4
            disp_x = x // GRID_SIZE + offset_x // GRID_SIZE
            disp_y = y // GRID_SIZE + offset_y // GRID_SIZE
            
            point = '(' + str(disp_x) + ',' + str(disp_y) + ')'
            text = font_xs.render(point, True, GRAY)
            screen.blit(text, [adj_x, adj_y])


    
# Game loop
running = True

grid_on = False
start_game()
start_level()

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                stage = PLAYING

            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    hero.jump()
                if event.key == pygame.K_g:
                    grid_on = not grid_on

            elif stage == LOSE or stage == WIN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    start_game()
                    start_level()
            

    pressed = pygame.key.get_pressed()

    if stage == PLAYING:

        if pressed[pygame.K_LEFT]:
            hero.move_left()
        elif pressed[pygame.K_RIGHT]:
            hero.move_right()
        else:
            hero.stop()

    
    # Game logic
    if stage == PLAYING:
        all_sprites.update()

        if hero.hearts <= 0:
            stage = LOSE

        elif hero.reached_goal():
            stage = LEVEL_COMPLETE
            countdown = 2 * FPS
            pygame.mixer.music.stop()
            level_up_snd.play()
    elif stage == LEVEL_COMPLETE:
        countdown -= 1
        if countdown <+ 0:
            current_level += 1

            if current_level < len(levels):
                start_level()
                stage = PLAYING
            else:
                stage = WIN

    if hero.rect.centerx < WIDTH // 2:
        offset_x = 0
    elif hero.rect.centerx > world_width - WIDTH // 2:
        offset_x = world_width - WIDTH
    else:
        offset_x = hero.rect.centerx - WIDTH  // 2

        
    # Drawing code
    screen.fill(SKY_BLUE)
    screen.blit(background_img, [0,0])
    screen.blit(background_img, [1000,0])

    for sprite in all_sprites:
        screen.blit(sprite.image, [sprite.rect.x - offset_x, sprite.rect.y])


    show_hud()

    if stage == START:
        show_start_screen()
    elif stage == LOSE:
        show_lose_screen()
    elif stage == LEVEL_COMPLETE:
        show_level_complete_screen()
    elif stage == WIN:
        show_win_screen()


    if grid_on:
            draw_grid(offset_x)


    # Update screen
    pygame.display.update()

    


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()

