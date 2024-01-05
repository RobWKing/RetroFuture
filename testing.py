import pygame, random, math

pygame.init()

screenwidth = 800
screenheight = 600
screen = pygame.display.set_mode((screenwidth, screenheight))
clock = pygame.time.Clock()
seeker_image = pygame.image.load('graphics/enemies/invade.png')

class Level:
    def __init__(self):
        self.BgImg = pygame.image.load('graphics/bg/800600centralcross.png')

class Enemy(pygame.sprite.Sprite):
    def __init__(self):

        # All of these are required for the Sprite class's draw function to work correctly
        super().__init__()
        self.image = seeker_image
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.sprite_width = self.image.get_width()
        self.sprite_height = self.image.get_height()
        self.speed = 4


    def animate(self):
        global x
        x += 0.1
        if x < 89:
            self.image = pygame.transform.rotate(self.original_image, math.degrees(x))
            self.rect = self.image.get_rect(center=self.rect.center)

    def update_on_screen_position(self):

        screen.blit(self.image, self.rect)

level = Level()
enemies = pygame.sprite.Group()

for x in range(1):
    new_enemy = Enemy()
    # new_enemy = Seeker(random.randint(0,screenwidth), random.randint(0, screenheight))
    enemies.add(new_enemy)

running = True

while running:
    for event in pygame.event.get():  # this will check for all events in the whole program, arrow presses, buttons etc
        if event.type == pygame.QUIT:
            running = False
    screen.blit(level.BgImg, (0, 0))
    for enemy in enemies:
        enemy.animate()
        enemy.update_on_screen_position()
    # enemies.draw(screen)
    pygame.display.update()  # this can be used for specific parts of teh screen if fed as argument e.g. update(player.rect)
    clock.tick(60)
