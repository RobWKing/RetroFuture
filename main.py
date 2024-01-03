import pygame, random

pygame.init()

screenwidth = 800
screenheight = 600
screen = pygame.display.set_mode((screenwidth, screenheight))
clock = pygame.time.Clock()
image_of_spaceship = pygame.image.load('graphics/player/shipsmall.png')
image_of_enemy = pygame.image.load('graphics/enemies/invade.png')
seeker_image =  pygame.image.load('graphics/enemies/seeker.png')
frame_counter = 0
icon = pygame.image.load('graphics/misc/retroFutureTumblr.ico')
pygame.display.set_icon(icon)
pygame.display.set_caption("Retro Future")
def frame_tracker():
    global frame_counter
    if frame_counter >= 60:
        frame_counter = 0
    else:
        frame_counter += 1
    print(frame_counter)
class Level:
    def __init__(self):
        self.BgImg = pygame.image.load('graphics/bg/800600centralcross.png')


# need to set better boundaries by including the size of the sprite in the calculation
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):

        # All of these are required for the Sprite class's draw function to work correctly
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.sprite_width = self.image.get_width()
        self.sprite_height = self.image.get_height()
        self.speed = 4

    def animate(self):
        pass
        # deform shape horizontally and vertically to create illusion of pulsing etc

    def update_on_screen_position(self, x, y):
        screen.blit(self.image, (x, y))

    def reorientation_towards_player(self, playerx, playery):
        pass
        # self.x_position  and something to do with player.xpos, ypos
    def undulate(self):
        if frame_counter % 20 == 0:
            self.image = pygame.transform.scale(self.image, (self.sprite_width+5, self.sprite_height+5))
        elif frame_counter % 10 == 5:
            self.image = pygame.transform.scale(self.image, (self.sprite_width - 5, self.sprite_height - 5))



class Seeker(Enemy):
    def __init__(self, x, y):

        self.image = seeker_image
        super().__init__(x, y)  # the location of the super() does matter!
        self.image = pygame.transform.scale(seeker_image, (self.sprite_width, self.sprite_height))
        self.speed = 8



class Player:
    def __init__(self):

        self.playerImg = image_of_spaceship
        self.rect = self.playerImg.get_rect()
        self.sprite_width = self.playerImg.get_width()
        self.sprite_height = self.playerImg.get_height()
        self.speed = 4
        self.boost_length = 10
        self.x_position = screenwidth / 2 - self.sprite_width / 2
        self.y_position = screenheight / 2 - self.sprite_height / 2
        self.rotation_angle = 0
        self.y_in_bounds = True
        self.x_in_bounds = True

    def all(self):
        self.check_in_bounds()
        self.user_input_and_change_xy_pos()
        self.get_direction_and_rotate_player_sprite()
        self.boost_button()
        self.update_on_screen_position(self.x_position, self.y_position)
    def get_direction_and_rotate_player_sprite(self):
        keys = pygame.key.get_pressed()

        # Code to ensure there are no other directional inputs, i.e. we are not diagonal
        arrow_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                      pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
        arrow_keys_pressed = [keys[key] for key in arrow_keys]
        arrow_keys_sum = sum(arrow_keys_pressed)

        if arrow_keys_sum == 1:
            # cardinal directions
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.rotation_angle = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rotation_angle = 90
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.rotation_angle = 180
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rotation_angle = 270

        # diagonals
        if keys[pygame.K_LEFT] and keys[pygame.K_UP] or keys[pygame.K_a] and keys[pygame.K_w]:
            self.rotation_angle = 45
        if keys[pygame.K_LEFT] and keys[pygame.K_DOWN] or keys[pygame.K_a] and keys[pygame.K_s]:
            self.rotation_angle = 135
        if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] or keys[pygame.K_d] and keys[pygame.K_s]:
            self.rotation_angle = 225
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP] or keys[pygame.K_d] and keys[pygame.K_w]:
            self.rotation_angle = 315
        self.playerImg = pygame.transform.rotate(image_of_spaceship, self.rotation_angle)

    def boost_button(self):
        keys = pygame.key.get_pressed()

        # move the correct direction if in bounds
        # the current formula will not let you boost the opposite direction either, only an issue if boost becomes larger
        if keys[pygame.K_SPACE]:
            if self.x_in_bounds:
                if self.rotation_angle in [45, 90, 135]:
                    self.x_position -= self.boost_length
                if self.rotation_angle in [225, 270, 315]:
                    self.x_position += self.boost_length
            if self.y_in_bounds:
                if self.rotation_angle in [0, 45, 315]:
                    self.y_position -= self.boost_length
                if self.rotation_angle in [135, 180, 225]:
                    self.y_position += self.boost_length

    def check_in_bounds(self):
        # check x position is inside window + sprite + boost_length
        if 0 + self.boost_length < self.x_position < (screenwidth - self.sprite_width) - self.boost_length:
            self.x_in_bounds = True
        else:
            self.x_in_bounds = False

        # check y position
        if 0 + self.boost_length < self.y_position < (screenheight - self.sprite_height) - self.boost_length:
            self.y_in_bounds = True
        else:
            self.y_in_bounds = False

    def update_on_screen_position(self, x, y):
        screen.blit(self.playerImg, (x, y))

    def user_input_and_change_xy_pos(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.x_position < (screenwidth - self.sprite_width) or keys[
            pygame.K_d] and self.x_position < (screenwidth - self.sprite_width):
            self.x_position += 1 * self.speed
        if keys[pygame.K_LEFT] and self.x_position > 0 or keys[pygame.K_a] and self.x_position > 0:
            self.x_position -= 1 * self.speed
        if keys[pygame.K_UP] and self.y_position > 0 or keys[pygame.K_w] and self.y_position > 0:
            self.y_position -= 1 * self.speed
        if keys[pygame.K_DOWN] and self.y_position < (screenheight - self.sprite_height) or keys[
            pygame.K_s] and self.y_position < (screenheight - self.sprite_height):
            self.y_position += 1 * self.speed


level = Level()
player = Player()
enemies = pygame.sprite.Group()

for x in range(5):
    new_enemy = Seeker(random.randint(0,screenwidth), random.randint(0, screenheight))
    enemies.add(new_enemy)
running = True

while running:
    for event in pygame.event.get():  # this will check for all events in the whole program, arrow presses, buttons etc
        if event.type == pygame.QUIT:
            running = False
    screen.blit(level.BgImg, (0, 0))
    player.all()
    # enemies.undulate()
    for enemy in enemies:
        enemy.undulate()
        enemy.update_on_screen_position((enemy.rect.center[0]-(enemy.sprite_width/2)),enemy.rect.center[1]-(enemy.sprite_height/2))
    # player.user_input_and_change_xy_pos()
    # player.get_direction_and_rotate_player_sprite()
    # player.boost_button()
    # player.update_on_screen_position(player.x_position, player.y_position)
    # enemy1.update_on_screen_position(enemy1.x_position,enemy1.y_position)
    enemies.draw(screen)
    pygame.display.update()
    frame_tracker()
    clock.tick(60)
