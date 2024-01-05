def user_input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        self.x_position += 0.25 * self.speed
        self.current_direction = 'right'
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        self.x_position -= 0.25 * self.speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        self.y_position -= 0.25 * self.speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        self.y_position += 0.25 * self.speed

    if keys[pygame.K_SPACE]:
        if self.current_direction == 'right':
            self.x_position += 10
        else:
            pass