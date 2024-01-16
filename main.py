import pygame, random, math, os
from spawns import spawn_data, calculate_total_enemies
pygame.init()

screenwidth = 1200
screenheight = 700
screen = pygame.display.set_mode((screenwidth, screenheight))
clock = pygame.time.Clock()
frame_counter = 0
total_frames = 0
icon = pygame.image.load('graphics/misc/retroFutureTumblr.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Retro Future")
menu_font = "PressStart2P-vaV7.ttf"
HUD_font = "AerologicaRegular-K7day.ttf"
fps_font = menu_font

def text_setter(text, font_name, font_size, rgb=(0, 255, 0)):
    r, g, b = rgb
    return pygame.font.Font('fonts/'+font_name, font_size).render(str(text), True, (r,g,b))

def create_rect_with_pos(text, x_pos, y_pos):
    text_rect = text.get_rect()
    text_rect.midtop = (x_pos, y_pos)
    return text_rect


# fps_font = pygame.font.SysFont("Consolas", 20)
# score_font_path = "fonts/AerologicaRegular-K7day.ttf"
# score_font = pygame.font.Font(score_font_path, 50)
# splash_font_path = "fonts/PressStart2P-vaV7.ttf"
# splash_font = pygame.font.Font(splash_font_path, 50)
# splash_font_small = pygame.font.Font(splash_font_path, 20)
# splash_font_x_small = pygame.font.Font(splash_font_path, 10)

# splash_text = 'Welcome to RetroFuture!'
# splash_screen_text = splash_font.render(splash_text, True, (0, 255, 0))
# splash_screen_text_rect = splash_screen_text.get_rect()
# splash_screen_text_rect.midtop = (screenwidth / 2, self.splash_text_start_y)

def frame_tracker():
    global frame_counter, total_frames
    if frame_counter >= 59:
        frame_counter = 0
    else:
        frame_counter += 1
        total_frames += 1
        # level.seconds_elapsed = round(total_frames / 60, 2)

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


class MenuSystem:
    def __init__(self, pass_info_to_menu, current_score):
        self.current_mode = 'MenuSystem'
        self.current_screen = 'splash_screen'
        self.BgImg = None  # this is set in the run() function based on what self.current_screen is
        self.splash_text_starting_position = -10

        # related to navigating in menus
        self.current_menu_navigation_coordinate = [0]
        self.cursor_image = pygame.image.load('graphics/misc/cursor.png')
        self.cursor_rotation_angle = 0
        self.cursor_rotation_direction = 1
        self.current_cursor_position = 0
        self.cursor_cooldown = 0

        # logic
        self.pass_info = pass_info_to_menu
        self.difficulty = None
        self.current_level = None
        self.game_mode = None

        # to receive from level later

        self.current_score = current_score

    def pass_info_to_game(self):
        self.pass_info(self.difficulty, self.current_level, self.game_mode, self.current_mode)

    def run(self):
        # blit the background
        self.BgImg = pygame.transform.scale(pygame.image.load(f'graphics/bg/{self.current_screen}.png'),
                                            (screenwidth, screenheight))
        screen.blit(self.BgImg, (0, 0))

        # runs the function for whichever screen the game is currently on
        run_current_screen = getattr(self, self.current_screen)
        run_current_screen()

        if self.current_screen in ('main_menu', 'choose_difficulty_screen'):
            self.menu_navigator()
            self.menu_button_cooldown()

        self.pass_info_to_game()

    def obtain_menu_navigation_coordinates(self, dictionary):
        # get and set navigation co_ordinates
        self.current_menu_navigation_coordinate = []
        for _, rect in dictionary.items():
            self.current_menu_navigation_coordinate.append(rect.y)

    def menu_button_cooldown(self):
        if self.cursor_cooldown > 0:
            self.cursor_cooldown -= 1
    def menu_navigator(self):

        # create cursor
        cursor_image = pygame.image.load('graphics/misc/cursor.png')
        cursor_rect = cursor_image.get_rect()
        cursor_width = cursor_image.get_width()

        # animate cursor
        if self.cursor_rotation_angle > 8:
            self.cursor_rotation_direction = -0.5
        elif self.cursor_rotation_angle < -8:
            self.cursor_rotation_direction = 0.5

        self.cursor_rotation_angle += self.cursor_rotation_direction
        self.cursor_image = pygame.transform.rotate(cursor_image, self.cursor_rotation_angle)


        # place cursor using list self.current_menu_navigation_coordinate to dictate where it can be rendered
        # use w and s keys to control cursor's vertical movement

        # x co-ordinate fixed at center of screen
        cursor_rect.x = screenwidth/2 - (cursor_width/2)

        # y co-ordinate determined by list options
        if self.cursor_cooldown == 0:
            if keys[pygame.K_s]:
                if self.current_cursor_position < len(self.current_menu_navigation_coordinate)-1:
                    self.current_cursor_position += 1
                    self.cursor_cooldown = 15

            if keys[pygame.K_w]:
                if self.current_cursor_position > 0:
                    self.current_cursor_position -= 1
                    self.cursor_cooldown = 15


        cursor_rect.y = self.current_menu_navigation_coordinate[self.current_cursor_position]+10

        # draw cursor
        screen.blit(self.cursor_image, cursor_rect)

        # handle going back to main_menu
        if keys[pygame.K_ESCAPE]:
            self.current_screen = 'main_menu'


    def splash_screen(self):

        # draw the title screen text and blit to screen
        splash_screen_text = text_setter('Welcome to RetroFuture',
                                         menu_font,
                                         50)

        splash_screen_text_rect = create_rect_with_pos(splash_screen_text,
                                                       (screenwidth/2),
                                                       self.splash_text_starting_position)

        screen.blit(splash_screen_text, splash_screen_text_rect)

        # animate the text, falling down to a certain position, then loading second line of text
        if self.splash_text_starting_position < screenheight/3:
            self.splash_text_starting_position += 3

        if self.splash_text_starting_position >= screenheight/3:
            splash_under_text = text_setter('Press \'Enter\' to continue',
                                            menu_font,
                                            20)
            splash_under_text_rect = create_rect_with_pos(splash_under_text,
                                                          screenwidth/2,
                                                          screenheight/2)

            screen.blit(splash_under_text, splash_under_text_rect)

        # how to advance from the splash screen
        if keys[pygame.K_RETURN]:
            self.current_screen = 'main_menu'
            self.cursor_cooldown = 15

    def main_menu(self):

        # variables to establish names of menu items which also align with level.game_mode,
        # the values in options_to_level_mapping are self.currentlevel values
        menu_options = ['Gauntlet', 'Endless', 'Survive']
        options_to_level_mapping = {'Gauntlet': 5, 'Endless': 12, 'Survive': 11}

        # for calculating where to draw the items evenly across the screen (y co-ordinate only)
        # menu_options_dictionary for storing {text:rect} to iterate through later
        number_of_options = len(menu_options)
        text_size = 20
        total_spacing = screenheight - (number_of_options * text_size)
        spacing = total_spacing // (number_of_options + 1)
        menu_options_dictionary = {}
        current_item = 1

        # iterates through the list of menu options and creates the text and the rectangle for it,
        # with it's co-ords set to be evenly spaced across the screen in a vertical list
        for option in menu_options:
            menu_text = text_setter(option,
                                    menu_font,
                                    text_size)
            rect = create_rect_with_pos(menu_text,
                                        screenwidth/2,
                                        spacing*current_item)
            current_item += 1
            menu_options_dictionary[menu_text] = rect

        # draw menu items on-screen
        for menu_text, rects in menu_options_dictionary.items():
            screen.blit(menu_text, rects)

        # if mouse clicks on the text, acquire the name of the rectangle, and use it to set the current game_mode
        # and current_level as well as background sprite, then move the menu onto the next screen
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            for menu_text, rect in menu_options_dictionary.items():
                if rect.collidepoint(mouse_pos):
                    option_name = menu_options[(rect.y//spacing)-1]
                    self.game_mode = option_name
                    self.current_level = options_to_level_mapping[option_name]
                    # level.game_mode = option_name
                    # level.current_level = options_to_level_mapping[option_name]
                    # level.BgImg = pygame.transform.scale(pygame.image.load(f'graphics/bg/{level.current_level}.png'),
                    #                                      (screenwidth, screenheight))
                    self.current_screen = 'choose_difficulty_screen'
                    # print('level.game_mode:', level.game_mode, '| self.current_level: ', level.current_level)

        if self.cursor_cooldown == 0:
            if keys[pygame.K_RETURN]:
                option_name = menu_options[self.current_cursor_position]
                self.game_mode = option_name
                self.current_level = options_to_level_mapping[option_name]
                # level.game_mode = option_name
                # level.current_level = options_to_level_mapping[option_name]
                # level.BgImg = pygame.transform.scale(pygame.image.load(f'graphics/bg/{level.current_level}.png'),
                #                                      (screenwidth, screenheight))
                self.current_screen = 'choose_difficulty_screen'
                self.current_cursor_position = 0
                self.cursor_cooldown = 15

        # get and set navigation co_ordinates for UI navigation
        self.obtain_menu_navigation_coordinates(menu_options_dictionary)

    def choose_difficulty_screen(self):

        menu_options = ['Regular', 'Challenging']
        number_of_options = len(menu_options)
        text_size = 20
        total_spacing = screenheight - (number_of_options * text_size)
        spacing = total_spacing // (number_of_options + 1)
        menu_options_dictionary = {}
        current_item = 1

        # iterates through the list of menu options and creates the text and the rectangle for it,
        # with it's co-ords set to be evenly spaced across the screen in a vertical list
        for option in menu_options:
            menu_text = text_setter(option,
                                    menu_font,
                                    text_size)
            rect = create_rect_with_pos(menu_text,
                                        screenwidth / 2,
                                        spacing * current_item)
            current_item += 1
            menu_options_dictionary[menu_text] = rect

        # draw menu items on-screen
        for menu_text, rects in menu_options_dictionary.items():
            screen.blit(menu_text, rects)

        # find rectangle's corresponding string, use it to set the difficulty, start the game loop
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            for menu_text, rect in menu_options_dictionary.items():
                if rect.collidepoint(mouse_pos):
                    option_name = menu_options[(rect.y//spacing)-1]
                    self.difficulty = option_name
                    # level.difficulty = option_name
                    self.current_mode = 'game'

        # do effectively the same thing, but with key inputs, and related to the cursor's current position
        if self.cursor_cooldown == 0:
            if keys[pygame.K_RETURN]:
                option_name = menu_options[self.current_cursor_position]
                self.difficulty = option_name
                # level.difficulty = option_name
                self.current_cursor_position = 0
                self.current_mode = 'game'

        # get and set navigation co_ordinates for UI navigation
        self.obtain_menu_navigation_coordinates(menu_options_dictionary)



class Game:
    def __init__(self):
        # for first cycle
        self.mode = 'MenuSystem'
        self.menu = None
        self.level = None

        # from menu
        self.difficulty = None
        self.current_level = None
        self.game_mode = None

        # from level
        self.current_score = 0
        self.previous_mode = None

        # unused for gauntlet mode later
        self.gauntlet_level = 1
        # need to find a way to communicate whether level was won or lost to know what to tell menu to render

    def create_menu(self):
        self.menu = MenuSystem(self.get_info_from_menu, self.current_score)

    def create_level(self):
        self.level = Level(self.difficulty, self.current_level, self.game_mode, self.get_info_from_level)

    def get_info_from_menu(self, difficulty, current_level, game_mode, mode):
        self.difficulty = difficulty
        self.current_level = current_level
        self.game_mode = game_mode
        self.mode = mode

    def get_info_from_level(self, current_score, previous_mode, gauntlet_level):
        self.current_score = current_score
        self.previous_mode = previous_mode
        self.gauntlet_level = gauntlet_level

    def show_highscore(self):

        if self.difficulty == 'Regular':
            file_path = "scores_regular.lp"
        else:  # elif level.difficulty == 'Challenging':
            file_path = "scores_difficult.lp"

        with open(file_path, "r") as file:
            current_highscore = int(file.read())

        if self.current_score > current_highscore:
            current_highscore = self.current_score

            with open(file_path, "w") as file:
                file.write(str(current_highscore))

        # variables to establish name of scores, put them into a list then pass the list to create text on screen
        difficulty = self.difficulty+' Mode'
        record_score = 'Record Highscore: ' + str(current_highscore)
        current_score = 'Your score: ' + str(self.current_score)
        # the variables that will be blitted onto the screen
        menu_options = [difficulty, record_score, current_score, 'Press Enter to return to main menu']

        # to calculate even spacing across the y-axis of the page
        number_of_options = len(menu_options)
        text_size = 20
        total_spacing = screenheight - (number_of_options * text_size)
        spacing = total_spacing // (number_of_options + 1)

        # iterates through the list of menu options and creates the text and the rectangle for it,
        # with it's co-ords set to be evenly spaced across the screen in a vertical list
        menu_options_dictionary = {}
        current_item = 1

        for option in menu_options:
            menu_text = text_setter(option,
                                    menu_font,
                                    text_size)
            rect = create_rect_with_pos(menu_text,
                                        screenwidth/2,
                                        spacing*current_item)
            current_item += 1
            menu_options_dictionary[menu_text] = rect

        # draw items on-screen
        for menu_text, rects in menu_options_dictionary.items():
            screen.blit(menu_text, rects)

        # return to menu otherwise
        if keys[pygame.K_RETURN]:
            self.previous_mode = None

    def run(self):

        # creates and runs levels and menus depending on the current self.mode. Also shows highscores in the case
        # that the previous level was 'Endless' mode. show_highscore() then resets previous_mode to None, and self.menu
        # is created in the next loop

        if self.mode == 'MenuSystem':
            self.level = None

            if self.menu is None:
                # if the previous game was endless, show the scores (other modes aren't score-based)
                if self.previous_mode == 'Endless':
                    self.show_highscore()
                # otherwise, create a new menu
                else:
                    self.create_menu()

            else:
                self.menu.run()


        elif self.mode == 'game':
            self.menu = None

            if self.level is None:
                self.create_level()

            self.level.run()

class Level:
    def __init__(self, difficulty, current_level, game_mode, pass_info_to_menu):
        self.current_level = current_level
        # 900 x 600 is for the temporary image, otherwise later will be screenwidth, screenheight
        self.BgImg = pygame.transform.scale(pygame.image.load(f'graphics/bg/{self.current_level}.png'), (screenwidth, screenheight))
        self.data = dict(spawn_data)

        # for endless mode
        self.current_score = 0
        self.score_goal = 10000  # for score based levels (none existing)

        # for survive mode
        self.seconds_elapsed = 0
        self.total_frames_elapsed = 0
        self.time_goal = 60

        # for gauntlet mode
        self.current_level_total_enemies = (calculate_total_enemies(spawn_data)).get(self.current_level)
        self.spawned_enemies = 0  # this may now be obsolete
        self.defeated_enemies = 0

        self.max_enemies = 5
        self.max_enemies_endless = 5

        # general settings
        self.game_mode = game_mode
        self.difficulty = difficulty



        self.other_level_finished_flag = False  # e.g. touching a portal   UNUSED
        self.level_complete = False     # UNUSED

        self.spawn_cooldown = 0
        self.announcement_played = False
        self.music_playing = False

        # share self.current_score, self.game_mode, self.current_level (temporary) to Game
        self.pass_info = pass_info_to_menu


        # TEMPORARY
        self.music = False
        self.bg_track = pygame.mixer.Sound(f'sound/music/a_hero_of_the_80s.ogg')
        self.temporaryself_bg_ogg = pygame.mixer.Sound('sound/music/a_hero_of_the_80s.ogg')

    def pass_info_to_menu(self):
        self.pass_info(self.current_score, self.game_mode, self.current_level)


    def run(self):

        screen.blit(self.BgImg, (0, 0))

        self.set_difficulty()

        if self.game_mode == 'Endless':
            self.endless_enemies()

        elif self.game_mode == 'Survive':
            self.survival_mode_enemies()

        elif self.game_mode == 'Gauntlet':
            self.gauntlet_enemies()

        self.display_timer()
        self.track_seconds_elapsed()
        self.pass_info_to_menu()
        self.level_transition()

    def set_difficulty(self):
        if self.difficulty == 'Regular':
            self.max_enemies = 10
            self.max_enemies_endless = 30
            self.time_goal = 60
        elif self.difficulty == 'Challenging':
            self.max_enemies = 75
            self.max_enemies_endless = 1000
            self.time_goal = 99
    def track_seconds_elapsed(self):
        if frame_counter < 59:
            self.total_frames_elapsed += 1
            self.seconds_elapsed = round(self.total_frames_elapsed / 60, 2)

    def level_transition(self):

        survival_win_condition = self.game_mode == 'Survive' and self.time_goal == self.seconds_elapsed
        endless_win_condition = self.game_mode == 'Endless' and player.is_alive is False

        if survival_win_condition or endless_win_condition:
            # if ((self.game_mode == 'Survive' and self.time_goal == self.seconds_elapsed)
            #         or (self.game_mode == 'Endless' and player.is_alive is False)):

            self.level_complete = True
            # self.BgImg = pygame.transform.scale(pygame.image.load(f'graphics/bg/transition_bg.png'), (screenwidth, screenheight))
            player.rect.x = screenwidth / 2 - player.sprite_width / 2
            player.rect.y = screenheight / 2 - player.sprite_height / 2
            self.BgImg = pygame.transform.scale(pygame.image.load(f'graphics/bg/yay.png'), (screenwidth, screenheight))
            self.temporaryself_bg_ogg.stop()
            mission_complete = pygame.mixer.Sound('sound/announcer/mission_completed.wav')
            mission_complete.play()

            # may only work for endless mode?
            for enemy in enemies:
                enemies.remove(enemy)
            #GAME_ACTIVE = FALSE
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

        # has become more verbose and can probably be re-shortened, but it works properly now
        for current_level, level_data in self.data.items():
            if current_level == self.current_level:
                for data in level_data:
                    for seconds, enemy_list in data.items():
                        if seconds == self.seconds_elapsed:
                            for bad_guy in enemy_list:
                                if bad_guy:
                                    for name, quantity in bad_guy.items():
                                        self.create_enemy(name, quantity)

    def create_enemy(self, name, quantity):
        def generate_safe_position(potential_x, potential_y, min_distance_from_player):
            if ((player.rect.x - min_distance_from_player) <= potential_x <= (
                    player.rect.x + min_distance_from_player) and
                    player.rect.y - min_distance_from_player <= potential_y < player.rect.y + min_distance_from_player):
                return None
            return (potential_x, potential_y)

        enemy_name = name.capitalize()

        for i in range(quantity):
            co_ords = None
            while co_ords is None:
                # could put these three into a dictionary to reduce code length and increase aesthetics, remove if statements
                # later will probably move the spawning into their own classes anyway
                if enemy_name == 'Twirler':
                    co_ords = generate_safe_position(random.randint(0, screenwidth), random.randint(0, screenheight),
                                                     200)
                elif enemy_name == 'Bouncer' or enemy_name == 'Seeker':
                    co_ords = generate_safe_position(random.randint(0, screenwidth),
                                                     random.randint(0, screenheight),
                                                     200)
                elif enemy_name == 'Wedge':
                    co_ords = generate_safe_position(random.randint(0, int(screenwidth)), -100, 0)
                elif enemy_name == 'Palm':
                    left_or_right_choice = random.choice([-100,screenwidth+100])
                    co_ords = generate_safe_position(left_or_right_choice, random.randint(0, screenheight), 0)

            # creates an enemy of enemy_name class, e.g. Seeker(co_ords[0], co_ords[1])
            enemy = globals()[enemy_name](co_ords[0], co_ords[1])
            enemies.add(enemy)

            self.spawned_enemies += 1
            # spawn_sound = pygame.mixer.Sound(f'sound/{enemy_name}.wav')
            # spawn_sound.play()

    def gauntlet_enemies(self):

        self.enemy_patterns()

        if self.defeated_enemies == self.spawned_enemies:
            print('level completed')

    def endless_enemies(self):

        if self.game_mode == 'Endless':
            if self.seconds_elapsed > 0.2:
                if self.music_playing is False:
                    self.temporaryself_bg_ogg = pygame.mixer.Sound('sound/music/stranger-things.ogg')
                    self.temporaryself_bg_ogg.play()
                    self.music_playing = True
            # number of enemies ramps up from 2, maxes at 50, this is temporary code for easy adjusting
            self.max_enemies = min(math.ceil(((self.current_score+100)/100)),self.max_enemies_endless)


        # if max_enemies = 50, once every 200 enemies, cause a delay of 6-20 seconds (to clear screen)
        if self.defeated_enemies != 0 and self.defeated_enemies % (self.max_enemies*4) == 0:
            self.spawn_cooldown = random.randint(6,10)

        # if no enemies at all, start spawning new enemies
        if self.spawned_enemies == 0:
            self.spawn_cooldown = 0
        if self.spawn_cooldown > 0:
            if frame_counter % 59 == 0:
                self.spawn_cooldown -= 1

        if self.spawn_cooldown == 0:
            if len(enemies) < self.max_enemies:
                if frame_counter % 6 == 0:
                    choice_weights = [0.4, 0.4, 0.2, 0.2, 0.2]
                    enemy_choice = random.choices(['Seeker', 'Bouncer','Wedge', 'Palm', 'Twirler'], weights=choice_weights, k=1).pop()
                    if enemy_choice == 'Seeker' or 'Bouncer':
                        min_max = (1,3)
                    elif enemy_choice == 'Twirler':
                        min_max = (10,11)
                    elif enemy_choice == 'Wedge':
                        min_max = (12,20)
                    elif enemy_choice == 'Palm':
                        min_max = (3,10)
                    self.create_enemy(enemy_choice, random.randint(*min_max))

    def survival_mode_enemies(self):
        # survival mode is level 4

        self.enemy_patterns()

        # if want this to be more graceful have to switch to using mixer.music with init() to measure length of tracks,
        # would probably make sense if ultimately create a music class
        if self.seconds_elapsed > 18:
            if self.announcement_played is False:
                announcement = pygame.mixer.Sound('sound/announcer/do_you_have_the_will.wav')
                announcement.play()
                self.announcement_played = True

            if self.seconds_elapsed > 24.5:
                if not self.music_playing:
                    self.temporaryself_bg_ogg = pygame.mixer.Sound('sound/music/a_hero_of_the_80s.ogg')
                    # bg_ogg = pygame.mixer.Sound('sound/music/a_hero_of_the_80s.ogg') turn back on when properly handled
                    # kill_player
                    self.temporaryself_bg_ogg.play()
                    # self.endless_mode = True
                    self.music_playing = True
                if not self.level_complete:
                    self.endless_enemies()


    def display_timer(self):
        # set default hud colour to green
        rgb = (0,255,0)

        # display remaining time if playing Survive mode, change colour to orange and red as nears 0.
        if self.game_mode == 'Survive':
            remaining_time = self.time_goal - math.floor(self.seconds_elapsed)

            if 5 < remaining_time <= 9:
                rgb = (255,165,0)
            if remaining_time <= 5:
                rgb = (255,0,0)
            hud_data = str(remaining_time)

        # display the current score, calculated by using the score of the enemies
        if self.game_mode in ('Endless', 'Gauntlet'):
            hud_data = str(self.current_score)

        if self.game_mode == '(UN-USED) REMAINING_ENEMIES':
            hud_data = str(self.current_level_total_enemies - self.defeated_enemies)

        # create the text box and set its co-ordinates
        hud_text = text_setter(hud_data,HUD_font,50,rgb)
        hud_text_rect = hud_text.get_rect()
        hud_text_rect.midtop = (screenwidth / 2, 10)

        # blit to screen, with some temporary code to make it disappear at time = 0
        if self.game_mode == 'Survive':
            if remaining_time > 0:
                screen.blit(hud_text, hud_text_rect)
        if not self.game_mode == 'Survive':
            screen.blit(hud_text, hud_text_rect)


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
            # level.bg_track.fadeout(500)  # example code
    def update_on_screen_position(self):
        screen.blit(self.image, self.rect)


class Seeker(Enemy):
    def __init__(self, x, y):

        self.score_value = 50
        # preferences
        self.image_size_percent = 4
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

        self.score_value = 50
        #preferences
        self.flip_image = False
        self.undulate_image = True
        self.speed = 1
        # to rotate/undulate enemies
        self.rotation_counter = 0
        self.rotation_degrees = 360
        self.rotation_speed = 2
        self.image_size_percent = 4
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

        self.score_value = 25
        #preferences
        self.flip_image = False
        self.undulate_image = True
        self.speed = 1
        self.rotation_counter = 0
        self.rotation_degrees = 180
        self.rotation_speed = 4
        self.image_size_percent = 7
        self.wiggle_quantity = 3
        super().__init__(x, y)  # the location of the super() does matter! being here allows the parent class to edit
        # the self.image before it gets set to original_image (now moved)

    def movement_method(self):
        if frame_counter % 6 == 0:
            self.rect.move_ip((self.wiggle_quantity,)*2)
            self.wiggle_quantity *= -1

class Wedge(Enemy):
    def __init__(self, x, y):

        self.score_value = 100
        # preferences
        self.flip_image = False
        self.undulate_image = True
        self.speed = 5
        # to rotate/undulate enemies
        self.rotation_counter = 0
        self.rotation_degrees = 360
        self.rotation_speed = random.choice([1,2,3])
        self.image_size_percent = 3
        self.wiggle_quantity = 3
        super().__init__(x, y)
        self.target_coords = (random.randint(self.sprite_width, screenwidth-self.sprite_width),
                              screenheight+self.sprite_height*2)

        # use this if you want different angles of falling
        self.fall_angle = random.choice([1,-1])*random.choice([1,2,4,8,100])


    def movement_method(self):

        reduce_difference_x = -int(self.speed/self.fall_angle)
        reduce_difference_y = self.speed

        self.rect.move_ip(reduce_difference_x, reduce_difference_y)

        # kill once off-screen
        if self.rect.y >= screenheight + self.sprite_height:
            enemies.remove(self)
            game.level.defeated_enemies += 1

class Palm(Enemy):
    def __init__(self, x, y):

        self.score_value = 200
        # preferences
        self.image_size_percent = 5
        self.flip_image = False
        self.undulate_image = True
        self.speed = 2
        # to rotate/undulate enemies
        self.rotation_counter = 0
        self.rotation_degrees = 15
        self.rotation_speed = 1
        self.wiggle_quantity = 3
        self.fall_angle = random.choice([1, -1]) * random.choice([1, 2, 4, 8, 100])
        self.come_from_left = False
        self.starting_x_coord = x
        super().__init__(x, y)

    def movement_method(self):
        # speed_modifier is to change direction of Palms x movement based on which side of the screen they spawn on
        # starting_x_coord compares to where the player is, if it's to the left of the player, speed_modifier will
        # be positive (moves Palm right), if x_coord to the right of player, will be negative (move Palm left)
        speed_modifier = self.speed * ((self.starting_x_coord < player.rect.x) * 2 - 1)

        reduce_difference_x = speed_modifier
        reduce_difference_y = -int(speed_modifier / self.fall_angle)

        self.rect.move_ip(reduce_difference_x, reduce_difference_y)

        # kill once off-screen
        if 0 - self.sprite_width > self.rect.x >= screenwidth + self.sprite_width:
            enemies.remove(self)
            game.level.defeated_enemies += 1

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

        # shooting
        self.fire_mode = 'increasing'
        self.fire_rate_stage = 1  # to make toggles of firepower one way only
        self.cooldown_counter = 0  # how long the delay is before the first bullet fired + general counter
        self.concurrent_bullets = 1  # refers to how many bullets, current code limits to 2 or 3 visually
                                    # if plan to use this, need to change the random.choice to be ifs for 2, 3 etc
        self.cooldown_rate = 8  # lower is faster
        self.bullet_direction = 0

    def run(self):
        self.check_in_bounds()
        self.user_input_and_change_xy_pos()
        self.animate()
        self.get_direction_and_rotate_player_sprite()
        self.boost_button()
        self.update_on_screen_position()
        self.adjust_fire_rate()
        self.shots_fired()

    def get_direction_and_rotate_player_sprite(self):

        # keys = pygame.key.get_pressed()

        # Code to ensure there are no other directional inputs, i.e. we are not diagonal
        arrow_keys = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
        arrow_keys_pressed = [keys[key] for key in arrow_keys]
        arrow_keys_sum = sum(arrow_keys_pressed)

        key_values = {pygame.K_w: 0, pygame.K_a: 90, pygame.K_s: 180, pygame.K_d: 270}


        if arrow_keys_sum == 1:
            for key, rotation_angle in key_values.items():
                if keys[key]:
                    self.rotation_angle = rotation_angle

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
        # keys = pygame.key.get_pressed()

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
        # keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.centerx < (screenwidth - self.sprite_width):
            self.rect.x += self.speed

        if keys[pygame.K_a] and self.rect.centerx > 0 + self.sprite_height:
            self.rect.x -= self.speed
        if keys[pygame.K_w] and self.rect.centery > 0 + self.sprite_width:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.centery < (screenheight - self.sprite_height):
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
        death_sound = pygame.mixer.Sound(f'sound/boom.wav')
        death_sound.play()
        # all of this is temporary!, but is a guide to what has to be toggled to restore default state at current time
        for enemy in enemies:
            enemies.remove(enemy)
        self.concurrent_bullets = 1
        self.cooldown_rate = 8
        self.rotation_angle = 0
        for bullet in bullets:
            bullets.remove(bullet)
        player.is_alive = True
        global frame_counter, total_frames
        frame_counter = 0
        total_frames = 0
        player.rect.centerx = screenwidth / 2
        player.rect.centery = screenheight / 2
        game.level.temporaryself_bg_ogg.fadeout(1000)

        game.mode = 'MenuSystem'



    def adjust_fire_rate(self):
        # this function changes the rate at which bullets are fired and how many bullets are fired at once,
        # dictated by the fire_mode which is dictated by the current_level passed when player is created

        # for now, it is unfinished and just set to 'increasing', because 'level' does not yet create 'player'

        if self.fire_mode == 'increasing':
            if len(enemies) < 20 and self.fire_rate_stage == 1:
                self.concurrent_bullets = 1
                self.cooldown_rate = 8
                self.fire_rate_stage = 2
            if len(enemies) >= 20 and self.fire_rate_stage == 2:
                self.concurrent_bullets = 3
                self.cooldown_rate = 2
                self.fire_rate_stage = 3
            if len(enemies) > 100 and self.fire_rate_stage == 3:
                self.concurrent_bullets = 3
                self.cooldown_rate = 1

        if self.fire_mode == 'pacifist':
            self.concurrent_bullets = 0

        if self.fire_mode == 'weak':
            self.concurrent_bullets = 1
            self.cooldown_rate = 8

        if self.fire_mode == 'strong':
            self.concurrent_bullets = 3
            self.cooldown_rate = 2

    def shots_fired(self):

        arrow_keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]
        arrow_keys_pressed = [keys[key] for key in arrow_keys]
        arrow_keys_sum = sum(arrow_keys_pressed)

        key_values = {pygame.K_UP: 0, pygame.K_LEFT: 90, pygame.K_DOWN: 180, pygame.K_RIGHT: 270}


        if arrow_keys_sum == 1 and self.cooldown_counter == 0:
            for key, rotation_angle in key_values.items():
                if keys[key]:
                    self.bullet_direction = rotation_angle
                    self.create_bullet()

        # lower the cooldown by 10 per second
        if self.cooldown_counter > 0:
            if frame_counter % 6 == 0:
                self.cooldown_counter -= 1

    def create_bullet(self):
        # creates as many bullets as specified in player's init
        if self.concurrent_bullets > 0:
            for i in range(self.concurrent_bullets):
                bullet = Bullet(self.bullet_direction, self.rect.centerx, self.rect.centery)
                bullets.add(bullet)
            bullet_sound = pygame.mixer.Sound(f'sound/laser.ogg')
            bullet_sound.set_volume(0.3)
            bullet_sound.play()

            # adjust how long the cooldown is between each bullet by altering the cooldown_rate
            self.cooldown_counter = self.cooldown_rate

    def update_on_screen_position(self):
        # reset to center of rectangle
        re_calibrate_rect_x = self.rect.x-self.sprite_width/2
        re_calibrate_rect_y = self.rect.y-self.sprite_height/2

        # add 1/2 size of hitboxImg, so player image is centered over the hitbox
        adjusted_player_rect_x = re_calibrate_rect_x + self.hitboxImg.get_width()/2
        adjusted_player_rect_y = re_calibrate_rect_y + self.hitboxImg.get_height()/2

        # draw to screen
        screen.blit(self.playerImg, (adjusted_player_rect_x, adjusted_player_rect_y))


class Bullet(pygame.sprite.Sprite):

    # direction = direction player is facing when bullet created
    # start_points = player's x and y position when bullet created
    def __init__(self, direction, start_point_x, start_point_y):
        super().__init__()
        self.image = pygame.image.load(f'graphics/bullets/{self.__class__.__name__.lower()}/1.png')
        self.image_ratio = (self.image.get_width()/self.image.get_height())
        self.image_size_percent = 0.5
        self.scaled_width = int(screenwidth * self.image_size_percent / 100)
        self.scaled_height = int(self.scaled_width / self.image_ratio)
        self.image = pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height))
        self.sprite_width = self.image.get_width()
        self.sprite_height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = [start_point_x, start_point_y]
        self.direction = direction
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

        # creates slight variation in bullet path
        self.rect.x += self.veer
        self.rect.y += self.veer

        screen.blit(self.image, (self.rect.x, self.rect.y))

    def delete_bullet(self):
        if self.rect.y > screenheight or self.rect.y < 0 or self.rect.x > screenwidth or self.rect.x < 0:
            bullets.remove(self)

    def hit_detection(self):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                game.level.current_score += enemy.score_value
                enemies.remove(enemy)
                bullets.remove(self)
                game.level.defeated_enemies += 1

game = Game()
# menu = MenuSystem(game.get_info_from_menu)  # temporary
# level = Level()

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # screen.blit(level.BgImg, (0, 0))  # this doesn't belong here

    keys = pygame.key.get_pressed()
    frame_tracker()

    game.run()

    if game.mode == 'game':

        player.run()

        for enemy in enemies:
            enemy.movement_method()
            enemy.animate()
            enemy.flip_towards_player()
            enemy.undulate()
            enemy.check_collision_with_player()
            enemy.update_on_screen_position()

        for bullet in bullets:
            bullet.was_fired()
            bullet.delete_bullet()
            bullet.hit_detection()


    #################################
    ### this section just for FPS ###
    fps = clock.get_fps()
    fps_text = text_setter(math.floor(fps),fps_font,20,(255,255,255))
    fps_text_rect = create_rect_with_pos(fps_text,25,5)
    screen.blit(fps_text, fps_text_rect)
    #################################
    pygame.display.flip()
    # print(level.seconds_elapsed)
    clock.tick(60)
