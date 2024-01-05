#
# user_input = input("Give me your list")
#
# user_input = user_input.strip("{}")
# user_input = user_input.strip("[]")
# user_input = user_input.strip("()")
#
# # Split the remaining string into a list of words using the split() method
# words_list = user_input.split(" ")
# words_list = [item for sublist in [s.split() for s in user_input.split(',')] for item in sublist]
# words_string = "', '".join(words_list)
#
# choice = int(input("1 for list, 2 for tuple, 3 for set: "))
#
# if choice == 1:
#     words_string = '[' + words_string + ']'
# if choice == 2:
#     words_string = '(' + words_string + ')'
# if choice == 3:
#     words_string = '{' + words_string + '}'
# print(words_string)

# k = input("Press Enter to exit...")
# def locate_player(self):
#         # print('player co-ords:', (player.x_position, player.y_position))
#         # print('self xpos', (self.rect.center[0], self.rect.center[1]))
#         # self.rect.center = [player.x_position+self.sprite_width/4, player.y_position+self.sprite_height/4]
#         # target = player.x_position+self.sprite_width/4, player.y_position+self.sprite_height/4
#         # enemy_pos = (self.rect.topleft[0], self.rect.topleft[1])
#         target_x = player.x_position
#         target_y = player.y_position
#         # print('Target:', target)
#         # print('Self:', enemy_pos)
#
#         result_x = target_x - self.rect.topleft[0] - self.sprite_width / 4
#         result_y = target_y - self.rect.topleft[1] - self.sprite_width / 4
#         if result_x > 0:
#             changex = 2
#         elif result_x < 0:
#             changex = -2
#         if result_x == 0:
#             changex = 0
#         if result_y > 0:
#             changey = 2
#         elif result_y < 0:
#             changey = -2
#         if result_y == 0:
#             changey = 0
#
#         self.rect = self.image.get_rect(center=self.rect.center)
#         self.rect.topleft = (self.rect.topleft[0] + changex, self.rect.topleft[1] + changey)
#
#         print('my co-ords topleft:', self.rect.topleft)
#         print('our x axis difference:', result_x)
#         if frame_counter % 2 == 0:
#             self.rect.topleft = (self.rect.topleft[0] + random.randint(-2,2), self.rect.topleft[1] + random.randint(-2,2))
#
#
#
#
#  def locate_player(self):
#     # print('player co-ords:', (player.x_position, player.y_position))
#     # print('self xpos', (self.rect.center[0], self.rect.center[1]))
#     # self.rect.center = [player.x_position+self.sprite_width/4, player.y_position+self.sprite_height/4]
#     target = player.x_position + self.sprite_width / 4, player.y_position + self.sprite_height / 4
#     enemy_pos = (self.rect.topleft[0], self.rect.topleft[1])
#     target_x = player.x_position + self.sprite_width / 4
#     target_y = player.y_position + self.sprite_height / 4
#     print('Target:', target)
#     print('Self:', enemy_pos)
#
#     if frame_counter % 2 == 0:  # half the frame-rate/speed
#         result_x = target_x - self.rect.topleft[0]
#         result_y = target_y - self.rect.topleft[1]
#         self.rect.topleft = (
#         self.rect.topleft[0] + math.ceil(int(result_x / 60)), self.rect.topleft[1] + math.ceil(int(result_y / 60)))
#

# print(type(enemy).__name__.lower())  # returns 'seeker'


# this code makes the bouncers move further to the edges, but in current state makes them stick to bottom right corner
# i'm afraid code will get too long to create another if to balance it out with other 3 corners

# def movement_method(self):
#     if self.need_refresh_timer:
#         self.initial_timer = random.randint(2, 5)
#         # self.target_coords = (random.randint(self.sprite_width, screenwidth - self.sprite_width),
#         #                       random.randint(self.sprite_height, screenheight - self.sprite_height))
#
#         coord_x = random.randint(self.sprite_width, screenwidth - self.sprite_width) * 2
#         coord_y = random.randint(self.sprite_height, screenheight - self.sprite_height) * 2
#         if coord_x > screenwidth - self.sprite_width:
#             coord_x = screenwidth - self.sprite_width
#         if coord_y > screenheight - self.sprite_height:
#             coord_y = screenheight - self.sprite_height
#         self.target_coords = (coord_x, coord_y)
#
#         self.need_refresh_timer = False
#     if frame_counter == 59:
#         self.initial_timer -= 1
#     if self.initial_timer >= 0:
#         result_x = self.target_coords[0] - self.rect.topleft[0]
#         result_y = self.target_coords[1] - self.rect.topleft[1]
#
#         if result_x > 0:
#             reduce_difference_x = (result_x > 0) * self.speed
#         elif result_x == 0:
#             self.need_refresh_timer = True
#             reduce_difference_x = 0
#         else:
#             reduce_difference_x = -1 * self.speed
#
#         if result_y >= 0:
#             reduce_difference_y = (result_y > 0) * self.speed
#         elif result_y == 0:
#             self.need_refresh_timer = True
#             reduce_difference_y = 0
#         else:
#             reduce_difference_y = -1 * self.speed
#
#         self.rect.topleft = (self.rect.topleft[0] + reduce_difference_x, self.rect.topleft[1] + reduce_difference_y)
#
#         # if frame_counter % 10 == 0:  # can use this to reduce shake
#         #     self.rect.topleft = (
#         #     self.rect.topleft[0] + random.randint(-3, 3), self.rect.topleft[1] + random.randint(-3, 3))
#     if self.initial_timer == 0:
#         self.need_refresh_timer = True