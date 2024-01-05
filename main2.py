import pygame, random, math, os

pygame.init()

screenwidth = 800
screenheight = 600
screen = pygame.display.set_mode((screenwidth, screenheight))
clock = pygame.time.Clock()
frame_counter = 0
icon = pygame.image.load('graphics/misc/retroFutureTumblr.ico')
pygame.display.set_icon(icon)
pygame.display.set_caption("Retro Future")

animation_speed_per_s = 1  # cannot go below 1
animation_counter = 0

player_animation_counter = 0
player_animation_speed_per_s = 15  # can remove this variable when happy with speed and place directly in animate()
# for writing FPS to screen
font = pygame.font.Font(None, 36)


def frame_tracker():
    global frame_counter
    if frame_counter >= 59:
        frame_counter = 0
    else:
        frame_counter += 1
    print('current frame:', frame_counter)


# more beautiful way to track frames without global variable, but less efficient
# requires changing all instances of frame_counter to tracker(), calling the function versus just reading a global variable
# def frame_tracker():
#     frame_counter = 0
#
#     def count_frames():
#         nonlocal frame_counter
#         if frame_counter >= 59:
#             frame_counter = 0
#         else:
#             frame_counter += 1
#         print('current frame:', frame_counter)
#
#     return count_frames
# tracker = frame_tracker()

class Level:
    def __init__(self):
        self.BgImg = pygame.transform.scale(pygame.image.load('graphics/bg/retroaesthetic_dark.png'), (900, 600))


# need to set better boundaries by including the size of the sprite in the calculation
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # All of these are required for the Sprite class's draw function to work correctly
        super().__init__()
        self.image = pygame.image.load(f'graphics/enemies/{self.__class__.__name__.lower()}/1.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        # to re-scale the image
        self.image_ratio = (self.image.get_width() / self.image.get_height())
        self.scaled_width = int(screenwidth * self.image_size_percent / 100)
        self.scaled_height = int(self.scaled_width / self.image_ratio)
        self.image = pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height))  # can be deleted?
        self.sprite_width = self.image.get_width()
        self.sprite_height = self.image.get_height()
        self.sprites = []
        self.original_image = self.image
        self.flipped_image = self.image
        # self.name = None

    def animate(self):
        global animation_counter
        # bro this code is so sick, well chuffed
        folder_path = f'graphics/enemies/{type(enemy).__name__.lower()}'
        if not self.sprites:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename).replace('\\', '/')
                self.sprites.append(file_path)
        if frame_counter % (60 / animation_speed_per_s) == 0:
            self.original_image = pygame.image.load(self.sprites[animation_counter])  # can be compressed into one
            self.original_image = pygame.transform.scale(self.original_image, (self.scaled_width, self.scaled_height))
            if len(self.sprites) - 1 <= animation_counter:
                animation_counter = 0
            else:
                animation_counter += 1

    def flip_towards_player(self):
        if self.flip_image:
            flipped_image = pygame.transform.flip(self.original_image, True, False)

            if player.x_position - (self.rect.topleft[0] + self.sprite_width / 4) > 0:
                self.flipped_image = self.original_image
            elif player.x_position - (self.rect.topleft[0] + self.sprite_width / 4) < 0:
                self.flipped_image = flipped_image

    def undulate(self):
        if self.undulate_image:
            if self.rotation_counter >= 360:
                self.rotation_counter = 0
            self.rotation_counter += self.rotation_speed
            if self.rotation_counter > self.rotation_degrees:
                self.rotation_speed *= -1
            if self.rotation_counter < -self.rotation_degrees:
                self.rotation_speed *= -1

            self.image = pygame.transform.rotate(self.flipped_image, -self.rotation_counter)
            self.rect = self.image.get_rect(center=self.rect.center)
            # print(self.rotation_counter)

    def check_collision_with_player(self):
        if self.rect.colliderect(player.rect):
            print('boom!')

    def update_on_screen_position(self):
        screen.blit(self.image, self.rect)


class Seeker(Enemy):
    def __init__(self, x, y):

        # preferences
        self.image_size_percent = 10
        self.flip_image = True
        self.undulate_image = True
        self.speed = 1
        # to rotate/undulate enemies
        self.rotation_counter = 0
        self.rotation_degrees = 15
        self.rotation_speed = 1

        super().__init__(x, y)  # the location of the super() does matter! being here allows the parent class to edit
        # the self.image before it gets set to original_image (now moved)

    def movement_method(self):

        result_x = player.x_position - (self.rect.topleft[0] + self.sprite_width / 4)
        result_y = player.y_position - (self.rect.topleft[1] + self.sprite_width / 4)

        if result_x >= 0:
            reduce_difference_x = (result_x > 0) * self.speed
        else:
            reduce_difference_x = -1 * self.speed

        if result_y >= 0:
            reduce_difference_y = (result_y > 0) * self.speed
        else:
            reduce_difference_y = -1 * self.speed

        self.rect.topleft = (self.rect.topleft[0] + reduce_difference_x, self.rect.topleft[1] + reduce_difference_y)

        if frame_counter % 3 == 0:  # can use this to reduce shake
            self.rect.topleft = (
            self.rect.topleft[0] + random.randint(-3, 3), self.rect.topleft[1] + random.randint(-3, 3))


class Bouncer(Enemy):
    def __init__(self, x, y):

        # preferences
        self.flip_image = False
        self.undulate_image = True
        self.speed = 1
        # to rotate/undulate enemies
        self.rotation_counter = 0
        self.rotation_degrees = 360
        self.rotation_speed = 2
        self.image_size_percent = 8
        self.need_refresh_timer = True
        self.initial_timer = random.randint(3, 5)
        super().__init__(x, y)  # the location of the super() does matter! being here allows the parent class to edit
        # the self.image before it gets set to original_image (now moved)
        self.target_coords = (random.randint(self.sprite_width, screenwidth - self.sprite_width),
                              random.randint(self.sprite_height, screenheight - self.sprite_height))

    def movement_method(self):
        if self.need_refresh_timer:
            self.initial_timer = random.randint(2, 5)
            self.target_coords = (random.randint(self.sprite_width, screenwidth - self.sprite_width),
                                  random.randint(self.sprite_height, screenheight - self.sprite_height))
            self.need_refresh_timer = False
        if frame_counter == 59:
            self.initial_timer -= 1
        if self.initial_timer >= 0:
            result_x = self.target_coords[0] - self.rect.topleft[0]
            result_y = self.target_coords[1] - self.rect.topleft[1]

            if result_x > 0:
                reduce_difference_x = (result_x > 0) * self.speed
            elif result_x == 0:
                self.need_refresh_timer = True
                reduce_difference_x = 0
            else:
                reduce_difference_x = -1 * self.speed

            if result_y >= 0:
                reduce_difference_y = (result_y > 0) * self.speed
            elif result_y == 0:
                self.need_refresh_timer = True
                reduce_difference_y = 0
            else:
                reduce_difference_y = -1 * self.speed

            self.rect.topleft = (self.rect.topleft[0] + reduce_difference_x, self.rect.topleft[1] + reduce_difference_y)

            # if frame_counter % 10 == 0:  # can use this to reduce shake
            #     self.rect.topleft = (
            #     self.rect.topleft[0] + random.randint(-3, 3), self.rect.topleft[1] + random.randint(-3, 3))
        if self.initial_timer == 0:
            self.need_refresh_timer = True


class Twirler(Enemy):
    def __init__(self, x, y):
        # preferences
        self.flip_image = False
        self.undulate_image = True
        self.speed = 1
        # to rotate/undulate enemies
        self.rotation_counter = 0
        self.rotation_degrees = 180
        self.rotation_speed = 4
        self.image_size_percent = 14
        self.need_refresh_timer = True
        self.initial_timer = random.randint(3, 5)
        super().__init__(x, y)  # the location of the super() does matter! being here allows the parent class to edit
        # the self.image before it gets set to original_image (now moved)

    def movement_method(self):
        if frame_counter % 6 == 0:  # can use this to reduce shake
            self.rect.topleft = (
            self.rect.topleft[0] + random.randint(-3, 3), self.rect.topleft[1] + random.randint(-3, 3))


class Player(pygame.sprite.Sprite):

    # the inheriting from sprite.Sprite is currently unused, proven by the lack of super__

    def __init__(self):

        self.playerImg = pygame.image.load('graphics/player/invadersmalls1.png')
        self.rect = self.playerImg.get_rect()
        self.sprite_width = self.playerImg.get_width()
        self.sprite_height = self.playerImg.get_height()
        self.speed = 6
        self.boost_length = 10
        self.x_position = screenwidth / 2 - self.sprite_width / 2
        self.y_position = screenheight / 2 - self.sprite_height / 2
        self.rotation_angle = 0
        self.y_in_bounds = True
        self.x_in_bounds = True
        self.sprites = []
        self.original_image = self.playerImg

    def all(self):
        self.check_in_bounds()
        self.user_input_and_change_xy_pos()
        self.animate()
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
        self.playerImg = pygame.transform.rotate(self.original_image, self.rotation_angle)

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

    def animate(self):
        global player_animation_counter
        folder_path = 'graphics/player/'
        if not self.sprites:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename).replace('\\', '/')
                self.sprites.append(file_path)
        if frame_counter % (60 / player_animation_speed_per_s) == 0:
            self.original_image = pygame.image.load(
                self.sprites[player_animation_counter])  # can be compressed into one
            # self.playerImg = pygame.transform.scale(self.playerImg, (self.scaled_width, self.scaled_height))
            if len(self.sprites) - 1 <= player_animation_counter:
                player_animation_counter = 0
            else:
                player_animation_counter += 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(f'graphics/bullets/{self.__class__.__name__.lower()}/1.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.image_ratio = (self.image.get_width() / self.image.get_height())
        self.image_size_percent = 8
        self.scaled_width = int(screenwidth * self.image_size_percent / 100)
        self.scaled_height = int(self.scaled_width / self.image_ratio)
        self.image = pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height))  # can be deleted?
        self.sprite_width = self.image.get_width()
        self.sprite_height = self.image.get_height()

        # preferences
        self.speed = 1

    def fired(self):
        pass


level = Level()
player = Player()
enemies = pygame.sprite.Group()

for i in range(1):
    enemy = Seeker(random.randint(-300, int(screenwidth * 1.5)), random.randint(-300, int(screenheight * 1.5)))
    # new_enemy = Seeker(random.randint(0,screenwidth), random.randint(0, screenheight))
    enemies.add(enemy)

for i in range(1):
    enemy = Bouncer(random.randint(-300, int(screenwidth * 1.5)), random.randint(-300, int(screenheight * 1.5)))
    enemies.add(enemy)

for i in range(1):
    enemy = Twirler((random.randint(50, screenwidth - 50)), random.randint(50, screenheight - 50))
    enemies.add(enemy)
running = True

while running:
    for event in pygame.event.get():  # this will check for all events in the whole program, arrow presses, buttons etc
        if event.type == pygame.QUIT:
            running = False
    screen.blit(level.BgImg, (0, 0))
    player.all()
    for enemy in enemies:
        enemy.movement_method()
        enemy.animate()
        enemy.flip_towards_player()
        enemy.undulate()
        enemy.check_collision_with_player()
        enemy.update_on_screen_position()

    # enemies.draw(screen)
    # player.user_input_and_change_xy_pos()
    # player.get_direction_and_rotate_player_sprite()
    # player.boost_button()
    # player.update_on_screen_position(player.x_position, player.y_position)
    # enemy1.update_on_screen_position(enemy1.x_position,enemy1.y_position)
    # enemies.draw(screen)
    # pygame.display.update()  # this can be used for specific parts of teh screen if fed as argument e.g. update(player.rect)
    frame_tracker()

    #################################
    ### this section just for FPS ###
    text = font.render(str(frame_counter), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (10, 10)
    screen.blit(text, text_rect)
    #################################

    pygame.display.flip()
    clock.tick(60)
