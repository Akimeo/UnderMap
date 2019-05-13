import pygame

pygame.init()
FONT = pygame.font.Font("UbuntuMono-R.ttf", 20)


class PygameTextBox:
    def __init__(self, x, y, w, h, text='Sample Text'):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.vis_text = text
        self.info = ''
        self.post_code = '-'
        self.org = ''
        self.rect = pygame.Rect(x, y, w, h)
        self.info_rect = pygame.Rect(x, y + 27, w, 357)
        self.color_inactive = (160, 160, 160)
        self.color_active = (255, 204, 0)
        self.color = self.color_inactive
        self.cursor_pos = 0
        self.lb = ''
        self.rb = ''
        self.cursor_animation = 0
        self.al_image = pygame.image.load('active_lupa.png')
        self.il_image = pygame.image.load('inactive_lupa.png')
        self.lupa_image = self.il_image
        self.lupa_rect = pygame.Rect(x + 226, y, 28, 28)
        self.ac_image = pygame.image.load('active_cross.png')
        self.ic_image = pygame.image.load('inactive_cross.png')
        self.cross_image = self.ic_image
        self.cross_rect = pygame.Rect(x + 264, y, 28, 28)
        self.ap_image = pygame.image.load('active_post.png')
        self.ip_image = pygame.image.load('inactive_post.png')
        self.tp_image = pygame.image.load('toggled_post.png')
        self.post_image = self.ip_image
        self.post_rect = pygame.Rect(x + 5, y + 33, 28, 28)
        self.ao_image = pygame.image.load('active_org.png')
        self.io_image = pygame.image.load('inactive_org.png')
        self.to_image = pygame.image.load('toggled_org.png')
        self.org_image = self.io_image
        self.org_rect = pygame.Rect(x + 40, y + 33, 28, 28)
        self.active = False
        self.ready = False
        self.drop = False
        self.print_code = False
        self.print_org = False
        self.found = False

    def update(self, events):
        if self.lupa_rect.collidepoint(pygame.mouse.get_pos()):
            self.lupa_image = self.al_image
        else:
            self.lupa_image = self.il_image
        if self.cross_rect.collidepoint(pygame.mouse.get_pos()):
            self.cross_image = self.ac_image
        else:
            self.cross_image = self.ic_image
        if self.post_rect.collidepoint(pygame.mouse.get_pos()):
            self.post_image = self.ap_image
        elif self.print_code:
            self.post_image = self.tp_image
        else:
            self.post_image = self.ip_image
        if self.org_rect.collidepoint(pygame.mouse.get_pos()):
            self.org_image = self.ao_image
        elif self.print_org:
            self.org_image = self.to_image
        else:
            self.org_image = self.io_image
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.lupa_rect.collidepoint(event.pos):
                    self.ready = True
                elif self.cross_rect.collidepoint(event.pos):
                    self.lb = self.rb = self.vis_text = self.text = self.info = ''
                    self.cursor_pos = 0
                    self.found = False
                    self.drop = True
                elif self.post_rect.collidepoint(event.pos):
                    self.print_code = not self.print_code
                elif self.org_rect.collidepoint(event.pos):
                    self.print_org = not self.print_org
                elif self.rect.collidepoint(event.pos):
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
                    if event.key == pygame.K_ESCAPE:
                        self.active = False
                        self.color = self.color_inactive
                    elif event.key == pygame.K_RETURN:
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
                        if self.rb and self.cursor_pos == 21:
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
                            if len(self.vis_text) > 21:
                                self.rb = self.vis_text[-1] + self.rb
                                self.vis_text = self.vis_text[:-1]
                        self.cursor_pos = max(self.cursor_pos - 1, 0)
                    elif event.key == pygame.K_RIGHT:
                        if self.rb and self.cursor_pos == 21:
                            self.lb += self.vis_text[0]
                            self.vis_text = self.vis_text[1:] + self.rb[0]
                            self.rb = self.rb[1:]
                        self.cursor_pos = min(
                            self.cursor_pos + 1, len(self.vis_text))
                    else:
                        self.vis_text = self.vis_text[:self.cursor_pos] + \
                            event.unicode + self.vis_text[self.cursor_pos:]
                        if len(self.vis_text) > 21:
                            if self.cursor_pos == 21:
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
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.x, self.y, self.w, 384))
        self.cursor_animation = (self.cursor_animation + 1) % 30
        text = FONT.render(self.vis_text, 1, self.color)
        screen.blit(text, (self.x + 5, self.y + 5))
        if self.active and self.cursor_animation < 15:
            text = FONT.render("|", 1, self.color)
            screen.blit(text, (self.x + self.cursor_pos * 10, self.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 1)
        screen.blit(self.lupa_image, (self.lupa_rect.x, self.lupa_rect.y))
        pygame.draw.line(screen, self.color, (259, 5), (259, 23), 2)
        screen.blit(self.cross_image, (self.cross_rect.x, self.cross_rect.y))
        screen.blit(self.post_image, (self.post_rect.x, self.post_rect.y))
        screen.blit(self.org_image, (self.org_rect.x, self.org_rect.y))
        row = ''
        height = 0
        for word in self.info.split():
            if len(row + word + ' ') > 29:
                info_text = FONT.render(row, 1, self.color)
                screen.blit(info_text, (self.x + 5, self.y + 63 + 20 * height))
                row = ''
                height += 1
            row += word + ' '
        if row:
            info_text = FONT.render(row, 1, self.color)
            screen.blit(info_text, (self.x + 5, self.y + 63 + 20 * height))
            height += 1
        row = ''
        if self.found and self.print_code:
            pygame.draw.line(screen, self.color, (5, self.y + 66 + 20 * height),
                             (295, self.y + 66 + 20 * height), 1)
            post_text = FONT.render(
                'Почтовый код: ' + self.post_code, 1, self.color)
            screen.blit(post_text, (self.x + 5, self.y + 68 + 20 * height))
        if self.found and self.print_org:
            if self.print_code:
                temp = 25
            else:
                temp = 0
            pygame.draw.line(screen, self.color, (5, self.y + 66 + temp + 20 * height),
                             (295, self.y + 66 + temp + 20 * height), 1)
            org = 'Ближайшая организация: ' + self.org
            for word in org.split():
                if len(row + word + ' ') > 29:
                    org_text = FONT.render(row, 1, self.color)
                    screen.blit(
                        org_text, (self.x + 5, self.y + 68 + temp + 20 * height))
                    row = ''
                    height += 1
                row += word + ' '
            if row:
                org_text = FONT.render(row, 1, self.color)
                screen.blit(
                    org_text, (self.x + 5, self.y + 68 + temp + 20 * height))
        pygame.draw.rect(screen, self.color, self.info_rect, 1)

    def get_name(self):
        if self.ready and self.text:
            self.ready = False
            self.found = True
            self.active = False
            self.color = self.color_inactive
            return self.text

    def drop_check(self):
        if self.drop:
            self.drop = False
            return True
        return False

    def add_info(self, info):
        self.info = info

    def add_post_code(self, post_code):
        self.post_code = post_code

    def add_org(self, org):
        self.org = org

    def is_not_active(self):
        return not self.active
