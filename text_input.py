import pygame

pygame.init()
FONT = pygame.font.Font("UbuntuMono-R.ttf", 20)


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
        text = FONT.render(self.text, 1, self.color)
        screen.blit(text, (self.x + 5, self.y + 5))
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.w, self.h), 1)


class PygameTextBox:
    def __init__(self, x, y, w, h, text='Sample Text'):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.vis_text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('gray')
        self.color_active = (255, 204, 0)
        self.color = self.color_inactive
        self.cursor_pos = 0
        self.lb = ''
        self.rb = ''
        self.cursor_animation = 0
        self.active = False
        self.ready = False

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                    self.color = self.color_active
                    self.cursor_pos = min(event.pos[0] // 10,
                                          len(self.vis_text))
                    self.cursor_animation = 0
                else:
                    self.active = False
                    self.color = self.color_inactive
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.ready = True
                    elif event.key == pygame.K_BACKSPACE:
                        if self.cursor_pos == 0:
                            if self.lb:
                                self.lb = self.lb[:-1]
                        elif self.rb:
                            self.vis_text = \
                                self.vis_text[:max(self.cursor_pos - 1, 0)] + \
                                self.vis_text[self.cursor_pos:] + self.rb[0]
                            self.rb = self.rb[1:]
                            self.cursor_pos = max(self.cursor_pos - 1, 0)
                        elif self.lb:
                            self.vis_text = self.lb[-1] + \
                                self.vis_text[:max(self.cursor_pos - 1, 0)] + \
                                self.vis_text[self.cursor_pos:]
                            self.lb = self.lb[:-1]
                        else:
                            self.vis_text = \
                                self.vis_text[:max(self.cursor_pos - 1, 0)] + \
                                self.vis_text[self.cursor_pos:]
                            self.cursor_pos = max(self.cursor_pos - 1, 0)
                    elif event.key == pygame.K_DELETE:
                        if self.rb and self.cursor_pos == 42:
                            self.rb = self.rb[1:]
                        else:
                            self.vis_text = self.vis_text[:self.cursor_pos] + \
                                self.vis_text[self.cursor_pos + 1:]
                            if self.rb:
                                self.vis_text += self.rb[0]
                                self.rb = self.rb[1:]
                    elif event.key == pygame.K_LEFT:
                        if self.lb and self.cursor_pos == 0:
                            self.vis_text = self.lb[-1] + self.vis_text
                            self.lb = self.lb[:-1]
                            if len(self.vis_text) > 42:
                                self.rb = self.vis_text[-1] + self.rb
                                self.vis_text = self.vis_text[:-1]
                        self.cursor_pos = max(self.cursor_pos - 1, 0)
                    elif event.key == pygame.K_RIGHT:
                        if self.rb and self.cursor_pos == 42:
                            self.lb += self.vis_text[0]
                            self.vis_text = self.vis_text[1:] + self.rb[0]
                            self.rb = self.rb[1:]
                        self.cursor_pos = min(
                             self.cursor_pos + 1, len(self.vis_text))
                    else:
                        self.vis_text = self.vis_text[:self.cursor_pos] + \
                            event.unicode + self.vis_text[self.cursor_pos:]
                        if len(self.vis_text) > 42:
                            if self.cursor_pos == 42:
                                self.lb += self.vis_text[0]
                                self.vis_text = self.vis_text[1:]
                            else:
                                self.cursor_pos += len(event.unicode)
                                self.rb += self.vis_text[-1]
                                self.vis_text = self.vis_text[:-1]
                        else:
                            self.cursor_pos += len(event.unicode)
                    self.text = self.lb + self.vis_text + self.rb


    def draw(self, screen):
        self.cursor_animation = (self.cursor_animation + 1) % 30
        screen.fill((255, 255, 255))
        text = FONT.render(self.vis_text, 1, self.color)
        screen.blit(text, (self.x + 5, self.y + 5))
        if self.active and self.cursor_animation < 15:
            text = FONT.render("|", 1, self.color)
            screen.blit(text, (self.x + self.cursor_pos * 10, self.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 1)

    def get_name(self):
        if self.ready:
            self.ready = False
            return self.text

    def is_not_active(self):
        return not self.active

'''
screen = pygame.display.set_mode((512, 412))
input_box = PygameTextBox(0, 20, 430, 28)
clock = pygame.time.Clock()
FPS = 30
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        input_box.update(events)
    name = input_box.get_name()
    if name:
        print(name)
    input_box.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
'''
