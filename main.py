import pygame, random, math, os

pygame.init()

screenwidth = 800
screenheight = 600
screen = pygame.display.set_mode((screenwidth, screenheight))
clock = pygame.time.Clock()
frame_counter = 0
icon = pygame.image.load('graphics/misc/retroFutureTumblr.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Retro Future")
# for writing FPS to screen
fps_font = pygame.font.SysFont("Consolas", 20)

def frame_tracker():
    global frame_counter
    if frame_counter >= 59:
        frame_counter = 0
        level.seconds_elapsed += 1
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
        self.current_level = 1
        # 900 x 600 is for the temporary image, otherwise later will be screenwidth, screenheight
        self.BgImg = pygame.transform.scale(pygame.image.load(f'graphics/bg/{self.current_level}.png'), (900, 600))
        self.spawned_enemies = 0
        self.defeated_enemies = 0
        self.seconds_elapsed = 0
        self.current_level_total_enemies = 1
        self.current_score = 0
        self.score_goal = 0
        self.other_level_finished_flag = False
        self.level_complete = False

        # what type of level is it, this may be unnecessary, but could use this to set score_goal etc. to something
        # un-obtainable
        self.score_objective = False
        self.time_objective = False
        self.kill_objective = True

    def level_transition(self):
        self.level_complete = True
        keys = pygame.key.get_pressed()
        # later will create custom enemies per level, have that list .pop entries to enemies
        # perhaps a list of lists with times? a dictionary with a list of enemies and seconds_elapsed for when to
        # spawn them? or do it based on enemies destroyed alone? or both? based on len(enemies) only would save a lot of
        # complex code imo

        # then when that list len = 0 and len enemies = 0, level is complete

        # let each new level update current_level total enemies


        # current~total needs to be updated by each individual level
        if self.defeated_enemies == self.current_level_total_enemies or self.other_level_finished_flag\
                or self.current_score == self.score_goal:
            self.BgImg = pygame.transform.scale(pygame.image.load(f'graphics/bg/transition_bg.png'), (screenwidth, screenheight))
            player.rect.x = screenwidth / 2 - player.sprite_width / 2
            player.rect.y = screenheight / 2 - player.sprite_height / 2
        if self.level_complete:
            if keys[pygame.K_b]:
                self.current_level += 1  # this increases every time we press b for now

                # reset other variables
                self.other_level_finished_flag = False
                self.current_score = 0
                self.score_goal = 0  # note this + current_level_total_enemies need to be updated in a function
                                    # that is called BEFORE level_transition(), later score_goal will be moved to that place
                                    # or ideally can be updated directly here now that current_level += 1
                                    # e.g. self.score_goal = level_scores[{self.current_level}]
                self.defeated_enemies = 0
                self.spawned_enemies = 0
                self.seconds_elapsed = 0
                print('current level', self.current_level)

    def enemy_patterns(self):
        pass

# need to set better boundaries by including the size of the sprite in the calculation
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # All of these are required for the Sprite class's draw function to work correctly
        super().__init__()
        self.image = pygame.image.load(f'graphics/enemies/{self.__class__.__name__.lower()}/1.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.image_ratio = (self.image.get_width()/self.image.get_height())
        # self.image = self.image.convert_alpha()   # alternative to a new sprite, makes it spawn in with low transparency
        # self.image.set_alpha(150)
        self.image = pygame.image.load(f'graphics/enemies/spawn_in/{self.__class__.__name__.lower()}/1.png')
        self.scaled_width = int(screenwidth * self.image_size_percent / 100)
        self.scaled_height = int(self.scaled_width / self.image_ratio)
        self.image = pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height))  # can be deleted?
        self.sprite_width = self.image.get_width()
        self.sprite_height = self.image.get_height()
        self.sprites = []
        self.original_image = self.image
        self.flipped_image = self.image
        self.animation_counter = 0
        self.animation_speed_per_s = 2

    def animate(self):
        # bro this code is so sick, well chuffed
        folder_path = f'graphics/enemies/{type(enemy).__name__.lower()}'
        if not self.sprites:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename).replace('\\', '/')
                self.sprites.append(file_path)
        if frame_counter % (60 / self.animation_speed_per_s) == 0:
            self.original_image = pygame.image.load(self.sprites[self.animation_counter])  # can be compressed into one
            self.original_image = pygame.transform.scale(self.original_image, (self.scaled_width, self.scaled_height))
            if len(self.sprites)-1 <= self.animation_counter:
                self.animation_counter = 0
            else:
                self.animation_counter += 1

    def flip_towards_player(self):
        if self.flip_image:
            flipped_image = pygame.transform.flip(self.original_image, True, False)

            if player.rect.x - (self.rect.topleft[0] + self.sprite_width / 4) > 0:
                self.flipped_image = self.original_image
            elif player.rect.x - (self.rect.topleft[0] + self.sprite_width / 4) < 0:
                self.flipped_image = flipped_image
        else:
            self.flipped_image = self.original_image


    def undulate(self):
        if self.undulate_image:
            if self.rotation_counter >= 360:
                self.rotation_counter = 0
            self.rotation_counter += self.rotation_speed
            if not (-self.rotation_degrees <= self.rotation_counter <= self.rotation_degrees):
                self.rotation_speed *= -1

            self.image = pygame.transform.rotate(self.flipped_image, -self.rotation_counter)
            self.rect = self.image.get_rect(center=self.rect.center)


    def check_collision_with_player(self):
        if self.rect.colliderect(player.rect):
            print('boom!')
            enemies.remove(self)
            player.kill_player()

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
        self.wiggle_quantity = 3
        super().__init__(x, y)  # the location of the super() does matter! being here allows the parent class to edit
                                # the self.image before it gets set to original_image (now moved)
                                # the child class defines image_size_percent, then the parent uses it

    def movement_method(self):

        result_x = player.rect.x - (self.rect.topleft[0] + self.sprite_width / 4)
        result_y = player.rect.y - (self.rect.topleft[1] + self.sprite_width / 4)

        if result_x >= 0:
            reduce_difference_x = (result_x > 0) * self.speed
        else:
            reduce_difference_x = -1 * self.speed

        if result_y >= 0:
            reduce_difference_y = (result_y > 0) * self.speed
        else:
            reduce_difference_y = -1 * self.speed

        self.rect.move_ip(reduce_difference_x, reduce_difference_y)

        if frame_counter % 3 == 0:  # can use this to reduce shake
            self.rect.move_ip((random.randint(-self.wiggle_quantity,self.wiggle_quantity),)*2)
class Bouncer(Enemy):
    def __init__(self, x, y):

        #preferences
        self.flip_image = False
        self.undulate_image = True
        self.speed = 1
        # to rotate/undulate enemies
        self.rotation_counter = 0
        self.rotation_degrees = 360
        self.rotation_speed = 2
        self.image_size_percent = 8
        super().__init__(x, y)  # the location of the super() does matter! being here allows the parent class to edit
        # the self.image before it gets set to original_image (now moved)
        self.target_coords = (random.randint(self.sprite_width, screenwidth-self.sprite_width),
                              random.randint(self.sprite_height, screenheight-self.sprite_height))



    def movement_method(self):
        if -2 <= self.rect.x - self.target_coords[0] < 2 and -2 <= self.rect.y - self.target_coords[1] < 2:
            self.target_coords = (random.choice([random.randint(self.sprite_width, int(screenwidth / 5)),
                                  random.randint(int(screenwidth * 0.8), screenwidth - self.sprite_width)]),
                                  random.choice([random.randint(self.sprite_height, int(screenheight / 5)),
                                                 random.randint(int(screenheight * 0.8),
                                                                screenheight - self.sprite_height)]))

        enemy_player_difference = tuple(self.target_coords[i] - self.rect.topleft[i] for i in range(2))

        if enemy_player_difference[0] >= 0:
            reduce_difference_x = (enemy_player_difference[0] > 0)
        else:
            reduce_difference_x = -1

        if enemy_player_difference[1] >= 0:
            reduce_difference_y = (enemy_player_difference[1] > 0)
        else:
            reduce_difference_y = -1

        self.rect.move_ip(reduce_difference_x*self.speed, reduce_difference_y*self.speed)

class Twirler(Enemy):
    def __init__(self, x, y):

        #preferences
        self.flip_image = False
        self.undulate_image = True
        self.speed = 1
        self.rotation_counter = 0
        self.rotation_degrees = 180
        self.rotation_speed = 4
        self.image_size_percent = 14
        self.wiggle_quantity = 3
        super().__init__(x, y)  # the location of the super() does matter! being here allows the parent class to edit
        # the self.image before it gets set to original_image (now moved)

    def movement_method(self):
        if frame_counter % 6 == 0:
            self.rect.move_ip((self.wiggle_quantity,)*2)
            self.wiggle_quantity *= -1

class Wedge(Enemy):
    def __init__(self, x, y):
        # preferences
        self.flip_image = False
        self.undulate_image = True
        self.speed = 5
        # to rotate/undulate enemies
        self.rotation_counter = 0
        self.rotation_degrees = 360
        self.rotation_speed = random.choice([1,2,3])
        self.image_size_percent = 6
        self.wiggle_quantity = 3
        super().__init__(x, y)
        self.target_coords = (random.randint(self.sprite_width, screenwidth-self.sprite_width),
                              screenheight+self.sprite_height*2)

        # use this if you want different angles of falling
        self.fall_angle = random.choice([1,-1])*random.choice([1,2,4,8,100])


    def movement_method(self):
        result_x = self.target_coords[0] - (self.rect.topleft[0] + self.sprite_width / 4)
        result_y = self.target_coords[1] - (self.rect.topleft[1] + self.sprite_width / 4)

        reduce_difference_x = -int(self.speed/self.fall_angle)
        reduce_difference_y = self.speed

        self.rect.move_ip(reduce_difference_x, reduce_difference_y)

        # kill once off-screen
        if self.rect.y >= screenheight + self.sprite_height:
            enemies.remove(self)
            level.defeated_enemies += 1
class Player(pygame.sprite.Sprite):

    # the inheriting from sprite.Sprite is currently unused, super can be commented, but makes pycharm underline it
    # necessary for Enemy classes because of group sprites being from the sprite.Sprite class

    def __init__(self):
        super().__init__()
        self.playerImg = pygame.image.load('graphics/player/standard/invadersmalls1.png')
        # later edit self.rect to take from a smaller image to reduce frustration in hitbox detection
        self.hitboxImg = pygame.image.load('graphics/player/hitbox.png')
        self.rect = self.hitboxImg.get_rect()
        self.sprite_width = self.playerImg.get_width()
        self.sprite_height = self.playerImg.get_height()
        self.rect.centerx = screenwidth / 2
        self.rect.centery = screenheight / 2

        self.rotation_angle = 0
        self.y_in_bounds = True
        self.x_in_bounds = True
        self.sprites = []
        self.original_image = self.playerImg
        self.is_boosting = False
        self.animation_counter = 0
        self.animation_speed_per_s = 15  # can remove this variable when happy with speed and place directly in animate()



        # status
        self.is_alive = True
        self.speed = 6
        self.boost_speed = 10
        self.folder_path = None
        self.cooldown_counter = 0  # how long the delay is before the first bullet fired + general counter
        self.concurrent_bullets = 1  # refers to how many bullets, current code limits to 2 or 3 visually
                                    # if plan to use this, need to change the random.choice to be ifs for 2, 3 etc
        self.cooldown_rate = 8  # lower is faster
        self.bullet_direction = 0
    def all(self):
        self.check_in_bounds()
        self.user_input_and_change_xy_pos()
        # self.player_status()
        self.animate()
        self.get_direction_and_rotate_player_sprite()
        self.boost_button()
        self.update_on_screen_position()
        self.shots_fired()

    def get_direction_and_rotate_player_sprite(self):

        keys = pygame.key.get_pressed()

        # Code to ensure there are no other directional inputs, i.e. we are not diagonal
        arrow_keys = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
        arrow_keys_pressed = [keys[key] for key in arrow_keys]
        arrow_keys_sum = sum(arrow_keys_pressed)

        key_values = {pygame.K_w: 0, pygame.K_a: 90, pygame.K_s: 180, pygame.K_d: 270}


        if arrow_keys_sum == 1:
            for key, rotation_angle in key_values.items():
                if keys[key]:
                    self.rotation_angle = rotation_angle
            # # cardinal directions
            # if keys[pygame.K_w]:
            #     self.rotation_angle = 0
            # if keys[pygame.K_a]:
            #     self.rotation_angle = 90
            # if keys[pygame.K_s]:
            #     self.rotation_angle = 180
            # if keys[pygame.K_d]:
            #     self.rotation_angle = 270

        # failed attempt
        # if arrow_keys_sum == 2:
        #     self.rotation_angle = 0
        #     for key, rotation_angle in key_values.items():
        #         if keys[key]:
        #             self.rotation_angle += rotation_angle
        #     if self.rotation_angle == 360:
        #         self.rotation_angle = 270
        #     if self.rotation_angle <= 270:
        #         self.rotation_angle /= 2
        #     if self.rotation_angle > 270:
        #         self.rotation_angle /= 2
        # print(self.rotation_angle)


        #
        #
        # key_values = {pygame.K_w: 0, pygame.K_a: 90, pygame.K_s: 180, pygame.K_d: 270}
        # self.rotation_angle = 0
        # for key, rotation_angle in key_values.items():
        #     if keys[key]:
        #         self.rotation_angle += rotation_angle
        #
        # print(self.rotation_angle)
        #
        # if arrow_keys_sum > 1 and self.rotation_angle > 180:
        #     self.rotation_angle += 45
        # if arrow_keys_sum > 1 and self.rotation_angle < 180:
        #     self.rotation_angle -= 45

        # diagonals
        if keys[pygame.K_a] and keys[pygame.K_w]:
            self.rotation_angle = 45
        if keys[pygame.K_a] and keys[pygame.K_s]:
            self.rotation_angle = 135
        if keys[pygame.K_d] and keys[pygame.K_s]:
            self.rotation_angle = 225
        if keys[pygame.K_d] and keys[pygame.K_w]:
            self.rotation_angle = 315

        self.playerImg = pygame.transform.rotate(self.original_image, self.rotation_angle)

    def boost_button(self):
        keys = pygame.key.get_pressed()

        # move the correct direction if in bounds
        # the current formula will not let you boost the opposite direction either, only an issue if boost becomes larger
        # probably re-write it all, if not can edit use of x_in_bounds to account for self.rotation_angle?
        if keys[pygame.K_SPACE]:

            if self.x_in_bounds:
                if self.rotation_angle in [45, 90, 135]:
                    self.rect.x -= self.boost_speed
                if self.rotation_angle in [225, 270, 315]:
                    self.rect.x += self.boost_speed

            if self.y_in_bounds:
                if self.rotation_angle in [0, 45, 315]:
                    self.rect.y -= self.boost_speed
                if self.rotation_angle in [135, 180, 225]:
                    self.rect.y += self.boost_speed

            self.is_boosting = True
            self.sprites = []
        else:
            self.is_boosting = False
            self.sprites = []


    def check_in_bounds(self):
        pass
        # check x position is inside window + sprite + boost_length
        if 0 + self.boost_speed < self.rect.x < (screenwidth - self.sprite_width) - self.boost_speed:
            self.x_in_bounds = True
        else:
            self.x_in_bounds = False

        # check y position
        if 0 + self.boost_speed < self.rect.y < (screenheight - self.sprite_height) - self.boost_speed:
            self.y_in_bounds = True
        else:
            self.y_in_bounds = False


    def user_input_and_change_xy_pos(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.x < (screenwidth - self.sprite_width):
            self.rect.x += self.speed
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < (screenheight - self.sprite_height):
            self.rect.y += self.speed


    def animate(self):
        # change to be something like self.folder_path = f'graphics/player/{self.status}', remove ifs
        if self.is_alive:
            if self.is_boosting:
                self.folder_path = 'graphics/player/boosting/'
            else:
                self.folder_path = 'graphics/player/standard/'
        else:  # (if self.is_alive = False)
            if self.animation_counter == 0:  # this works but only by waiting till the loop begins, causing delay
                # before the sprite is loaded, fixed by a workaround of adding player.animation_counter = 0 into
                # the enemy check_collision_with_player function
                self.sprites = []
                self.folder_path = 'graphics/player/death/'
        if self.folder_path is None:  # backup to prevent complaining
            self.folder_path = 'graphics/player/standard/'

        if not self.sprites:
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename).replace('\\','/')
                self.sprites.append(file_path)

        if frame_counter % (60 / self.animation_speed_per_s) == 0:
            self.original_image = pygame.image.load(self.sprites[self.animation_counter])  # can be compressed into one
            # self.playerImg = pygame.transform.scale(self.playerImg, (self.scaled_width, self.scaled_height))
            if len(self.sprites)-1 <= self.animation_counter:
                self.animation_counter = 0
            else:
                self.animation_counter += 1


    def kill_player(self):
        player.is_alive = False
        player.animation_counter = 0
        # can place part of player.animate() here later

    def shots_fired(self):
        keys = pygame.key.get_pressed()

        key_values = {pygame.K_UP: 0, pygame.K_LEFT: 90, pygame.K_DOWN: 180, pygame.K_RIGHT: 270}
        if self.cooldown_counter == 0:
            for key, rotation_angle in key_values.items():
                if keys[key]:
                    self.bullet_direction = rotation_angle
                    for i in range(self.concurrent_bullets):
                        bullet = Bullet()
                        bullets.add(bullet)
                    self.cooldown_counter = self.cooldown_rate

        if self.cooldown_counter > 0:
            if frame_counter % 6 == 0:
                self.cooldown_counter -= 1

        # if self.cooldown == 0:
        #     if keys[pygame.K_UP]:
        #         self.bullet_direction = 0
        #     if keys[pygame.K_DOWN]:
        #         self.bullet_direction = 180
        #     if keys[pygame.K_LEFT]:
        #         self.bullet_direction = 90
        #     if keys[pygame.K_RIGHT]:
        #         self.bullet_direction = 270

            # if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            #     for i in range(self.ship_level):
            #         bullet = Bullet()
            #         bullets.add(bullet)
            #     self.cooldown = self.firing_rate

    def update_on_screen_position(self):
        screen.blit(self.hitboxImg, (self.rect.x, self.rect.y))
        screen.blit(self.playerImg, (self.rect.x-self.sprite_width/2+self.hitboxImg.get_width()/2,
                                     self.rect.y-self.sprite_height/2+self.hitboxImg.get_width()/2))
        screen.blit(self.hitboxImg, (self.rect.x, self.rect.y))
        # print(self.playerImg.get_height()/self.hitboxImg.get_width())

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(f'graphics/bullets/{self.__class__.__name__.lower()}/1.png')
        self.image_ratio = (self.image.get_width()/self.image.get_height())
        self.image_size_percent = 1
        self.scaled_width = int(screenwidth * self.image_size_percent / 100)
        self.scaled_height = int(self.scaled_width / self.image_ratio)
        self.image = pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height))  # can be deleted?
        self.sprite_width = self.image.get_width()
        self.sprite_height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = [player.rect.centerx, player.rect.centery]
        # self.rect.center = [player.rect.centerx + random.randint(-2, 2), player.rect.centery + random.randint(-2, 2)]
        self.direction = player.bullet_direction
        self.veer = random.choice([-1,0,1])
        #preferences
        self.speed = 20

    def was_fired(self):

        if self.direction in [45, 90, 135]:
            self.rect.x -= self.speed
        if self.direction in [225, 270, 315]:
            self.rect.x += self.speed

        if self.direction in [0, 45, 315]:
            self.rect.y -= self.speed
        if self.direction in [135, 180, 225]:
            self.rect.y += self.speed

        self.rect.x += self.veer
        self.rect.y += self.veer

        screen.blit(self.image, (self.rect.x, self.rect.y))

    def delete_bullet(self):
        if self.rect.y > screenheight or self.rect.y < 0 or self.rect.x > screenwidth or self.rect.x < 0:
            bullets.remove(self)

    def hit_detection(self):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                bullets.remove(self)
                level.defeated_enemies += 1


level = Level()
player = Player()
bullet = Bullet()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()



def create_enemy(name, quantity):
    def generate_safe_position(potential_x, potential_y, min_distance_from_player):
        if ((player.rect.x - min_distance_from_player) <= potential_x <= (player.rect.x + min_distance_from_player) or
                player.rect.y - min_distance_from_player <= potential_y < - player.rect.y + min_distance_from_player):
            return None
        return (potential_x, potential_y)
    enemy_name = name.capitalize()
    for i in range(quantity):
        co_ords = None
        while co_ords is None:
            # could put these three into a dictionary to reduce code length and increase aesthetics, remove if statements
            # later will probably move the spawning into their own classes anyway
            if enemy_name == 'Twirler':
                co_ords = generate_safe_position(random.randint(0,screenwidth), random.randint(0, screenheight),
                                             200)
            elif enemy_name == 'Bouncer':
                co_ords = generate_safe_position(random.randint(0, screenwidth),
                                                 random.randint(0, screenheight),
                                                 200)
            elif enemy_name == 'Seeker':
                co_ords = generate_safe_position(random.randint(0, int(screenwidth)),
                                                 random.randint(0, int(screenheight)),
                                                 200)
            elif enemy_name == 'Wedge':
                co_ords = generate_safe_position(random.randint(0, int(screenwidth)), -100, 0)
        enemy = globals()[enemy_name](co_ords[0], co_ords[1])
        enemies.add(enemy)
        level.spawned_enemies += 1
        # spawn_sound = pygame.mixer.Sound(f'sound/{enemy_name}.wav')
        # spawn_sound.play()


create_enemy('bouncer', 1)
create_enemy('twirler', 1)
create_enemy('seeker', 1)
create_enemy('wedge', 1)

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
    for shots in bullets:
        shots.was_fired()
        shots.delete_bullet()
        shots.hit_detection()
    frame_tracker()

    if len(enemies) == 0:
        print('level cleared')
    if len(enemies) != 0:
        if frame_counter != 0 and frame_counter % 59 == 0:
            print('hi')
            create_enemy('wedge', 1)
    # if len(enemies) < 20 and level.spawned_enemies < 500:
    #     if frame_counter == 17:
    #         create_enemy('wedge', 1)
    #         create_enemy('seeker', 1)
    #     if frame_counter == 36:
    #         create_enemy('wedge', 1)
    #         create_enemy('bouncer', 1)
    #     if frame_counter == 56:
    #         create_enemy('wedge', 1)
    #         create_enemy('twirler', 1)

    level.level_transition()

    # temporary
    if not player.is_alive:
        print('defeated enemies:', level.defeated_enemies)
    #################################
    ### this section just for FPS ###
    fps = clock.get_fps()
    text = fps_font.render(str(round(fps, 1)), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (10, 10)
    screen.blit(text, text_rect)
    #################################
    pygame.display.flip()
    clock.tick(60)
