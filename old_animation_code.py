def animation(self):
    if self.current_direction == 'north':
        self.playerImg = pygame.image.load('shipsmallfacenorth.png')
    elif self.current_direction == 'south':
        self.playerImg = pygame.image.load('shipsmallfacesouth.png')
    elif self.current_direction == 'east':
        self.playerImg = pygame.image.load('shipsmallfaceeast.png')
    elif self.current_direction == 'west':
        self.playerImg = pygame.image.load('shipsmallfacewest.png')

    def user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and self.x_position < (screenwidth - self.sprite_width) or keys[pygame.K_d] and self.x_position < (screenwidth - self.sprite_width):
            self.x_position += 1 * self.speed
            self.current_direction = 'east'
        if keys[pygame.K_LEFT] and self.x_position > 0 or keys[pygame.K_a] and self.x_position > 0:
            self.x_position -= 1 * self.speed
            self.current_direction = 'west'
        if keys[pygame.K_UP] and self.y_position > 0 or keys[pygame.K_w] and self.y_position > 0:
            self.y_position -= 1 * self.speed
            self.current_direction = 'north'
        if keys[pygame.K_DOWN] and self.y_position < (screenheight - self.sprite_height) or keys[pygame.K_s]  and self.y_position < (screenheight - self.sprite_height):
            self.y_position += 1 * self.speed
            self.current_direction = 'south'