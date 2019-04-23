import pygame


class Button:
    def __init__(self, x, y, w, h, text='Искать'):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('gray')
        self.color_active = (255, 204, 0)
        self.color = self.color_inactive

    def update(self, events):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.color_active
        else:
            self.color = self.color_inactive

    def draw(self, screen):
        font = pygame.font.Font(None, 30)
        text = font.render(self.text, 1, self.color)
        screen.blit(text, (self.x + 5, self.y + 5))
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.w, self.h), 1)


class PygameTextBox:
    def __init__(self, x, y, w, h, text='Sample Text'):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color_inactive = pygame.Color('gray')
        self.color_active = (255, 204, 0)
        self.color = self.color_inactive
        self.active = False
        self.ready = False

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                    self.color = self.color_active
                else:
                    self.active = False
                    self.color = self.color_inactive
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.ready = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

    def draw(self, screen):
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 30)
        text = font.render(self.text, 1, self.color)
        screen.blit(text, (self.x + 5, self.y + 5))
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.w, self.h), 1)

    def get_name(self):
        if self.ready:
            self.ready = False
            return self.text

    def is_not_active(self):
        return not self.active
