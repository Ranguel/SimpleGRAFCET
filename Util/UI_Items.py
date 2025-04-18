import pygame
from Util.Shared_Functions import cursor_item_collide, cursor_group_relative_pos

clif = [230, 230, 230], [160, 160, 160], [200, 200, 200]  # color interface


def no_act(*args):
    pass


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

        self.rect = pygame.Surface((4, 4)).get_rect()
        self.position, self.event = [0, 0], 0
        self.last_press, self.actual = [0, 0, 0], 0
        self.redond, self.offset = False, [0, 0]
        self.crear = [False, False]
        self.subject = False
        self.inter_click_menu = None
        self.click_menu = None

    def redondear(self, *args): self.redond = not self.redond

    def save_object_to_create(self, ui, object_to_create, params):
        self.crear = [object_to_create, params]

    def update(self, cursor=object, ui=object, *args):
        self.current_press = pygame.mouse.get_pressed()
        self.rect.center = pygame.mouse.get_pos()
        if not self.last_press[0] and self.current_press[0]:
            self.event = 2
            if ui.pendant_input_text:
                ui.input_text = ""
                ui.pendant_input_text = None
                self.event = 0
        elif not self.last_press[2] and self.current_press[2]:
            self.event = 3
            if ui.pendant_input_text:
                ui.input_text = ""
                ui.pendant_input_text = None
                self.event = 0
        elif self.current_press[0] == self.last_press[0] or self.current_press[2] == self.last_press[2]:
            self.event = 0
        else:
            self.event = 1
        self.last_press = self.current_press
        if self.inter_click_menu != None:
            if self.inter_click_menu[0] == "Menu":
                self.inter_click_menu = Menu_UI, self.inter_click_menu[1]
            self.click_menu = self.inter_click_menu[0](
                *[self.rect.center]+list(self.inter_click_menu[1]))
            self.groups()[0].add(self.click_menu)
            self.inter_click_menu = None
        if self.click_menu != None:
            self.click_menu.update(cursor, ui, *args)

    def render(self, screen=pygame.Surface, *args):
        pass


class Menu_UI(pygame.sprite.Sprite):
    def __init__(self, pos, options={}, parent=object):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.options = {}
        self.menu_surface_size = [0, 0]
        self.state = 0
        self.parent = parent
        self.kill_timer = 20
        for op in options:
            self.options[op] = {}
            self.options[op]["func"] = options[op]
            self.options[op]["surface"] = pygame.font.SysFont(
                "Segoe UI", 12).render(str(op), True, (0, 0, 0))
            self.options[op]["rect"] = self.options[op]["surface"].get_rect()
            self.options[op]["high"] = False
            self.menu_surface_size = self.options[op]["rect"][2] if self.options[op]["rect"][2] > self.menu_surface_size[
                0] else self.menu_surface_size[0], self.menu_surface_size[1]+self.options[op]["rect"][3]
        self.rect = pygame.Surface(
            ([self.menu_surface_size[0]+8, self.menu_surface_size[1]+8*len(self.options)])).get_rect(topleft=(pos))

    def update(self, cursor=object, ui=object, *args):
        offset = 0
        if cursor_item_collide(cursor, self):
            self.kill_timer = 20
        else:
            self.kill_timer -= 1
        if self.kill_timer <= 0:
            self.kill()
            self.update = no_act

        for option in self.options:
            rect_list = (self.rect[0], self.rect[1]+offset,
                         self.menu_surface_size[0]+8, self.options[option]["rect"][3]+8)
            if cursor.rect.colliderect(rect_list):
                self.options[option]["high"] = True
                if cursor.event == 2:
                    self.options[option]["func"](self.parent, ui)
                    cursor.event == 0
                    self.kill()
                    break
            else:
                self.options[option]["high"] = False
            offset += self.options[option]["rect"][3]+8

    def render(self, screen=pygame.surface, *args):
        offset = 0
        for option in self.options:
            rect_list = (self.rect[0], self.rect[1]+offset,
                         self.menu_surface_size[0]+8, self.options[option]["rect"][3]+8)
            if self.options[option]["high"]:
                pygame.draw.rect(screen, (200, 200, 200), rect_list)
            else:
                pygame.draw.rect(screen, (160, 160, 160), rect_list)
            screen.blit(self.options[option]["surface"],
                        (self.rect[0]+4, self.rect[1]+offset+4))
            offset += self.options[option]["rect"][3]+8


class Floting_label_UI(pygame.sprite.Sprite):
    def __init__(self, pos, name="", button=pygame.sprite.Sprite, *args):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.pos = pos
        self.name = name
        self.button = button
        self.font = pygame.font.SysFont("Segoe UI", 12)
        self.name_label_surface = self.font.render(
            str(self.name), True, (255, 255, 255))
        self.name_label_rect = self.name_label_surface.get_rect()
        self.time_to_kill = 60

    def update(self, cursor=object, ui=object, *args):
        self.pos = cursor_group_relative_pos(
            cursor, self.groups()[0]) if len(self.groups()) else [0, 0]
        if not cursor_item_collide(cursor, self.button):
            self.kill()

    def render(self, screen=pygame.Surface, *args):
        pygame.draw.rect(screen, (60, 60, 60), (
            self.pos[0]-4, self.pos[1] - 14, self.name_label_rect[2]+8, self.name_label_rect[3]+8))
        screen.blit(self.name_label_surface, (self.pos[0], self.pos[1]-10))


class Button_UI(pygame.sprite.Sprite):
    def __init__(self, pos, surface, function, params, name="Button", tipe="toggle"):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.function, self.params = function, params
        self.size, self.state = surface, 0
        self.rect = self.size.get_rect(topleft=(pos))
        self.color = clif
        self.indicator_timer = 0
        self.name = name
        self.tipe = tipe

    def on_press(self, cursor, ui, *args):
        if self.tipe == "toggle":
            if self.state == 2:
                self.state = 0
            else:
                self.state = 2
        elif self.tipe == "unique":
            if self.state != 2:
                for button in self.groups()[0]:
                    button.state = 0
                self.state = 2
        elif self.tipe == "hold":
            if self.state != 2:
                self.state = 2
        elif self.tipe == "press":
            self.state = 2
        cursor.actual = 1
        self.function(*[ui]+list(self.params))
        cursor.event = 0

    def update(self, cursor=object, ui=object, *args):
        if self.tipe == "press":
            self.state = 0
        if cursor_item_collide(cursor, self):
            if not self.state == 2:
                self.state = 1
            if cursor.event == 2:
                self.on_press(cursor, ui)
                cursor.event = 0
        elif self.state != 2:
            self.state = 0
        if self.state == 0:
            self.indicator_timer = 0
        elif self.state == 1:
            self.indicator_timer += 1
        else:
            self.indicator_timer = 0
        if self.indicator_timer > 20:
            cursor.inter_click_menu = Floting_label_UI, (self.name, self)

    def render(self, screen=pygame.Surface, *args):
        if self.state == 2:
            pygame.draw.rect(screen, self.color[1], self.rect, 0, 1)
        elif self.state == 1:
            pygame.draw.rect(screen, self.color[0], self.rect, 0, 4)
        elif self.state == 0:
            pygame.draw.rect(screen, self.color[2], self.rect, 0, 8)
        screen.blit(self.size, self.rect)


class On_indiactor_UI(pygame.sprite.Sprite):
    def __init__(self, pos, name="I0", name_pos=(0, 0), function=callable, params=(), tipe="IN", number=0):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.condition_func, self.params = function, params
        self.state = 0
        self.size = pygame.Surface((10, 10))
        self.color = clif
        self.indicator_timer = 0
        self.name = name
        self.font = pygame.font.SysFont("Lucida Console", 18)
        self.name_label_surface = self.font.render(
            str(self.name), True, (20, 20, 20))
        self.name_label_rect = self.name_label_surface.get_rect()
        self.time_to_kill = 60
        self.on = False
        self.rect = self.name_label_surface.get_rect(
            topleft=((pos[0], pos[1])))
        self.tipe = tipe
        self.number = number
        self.toggle_on = False

    def update(self, cursor=object, ui=object, *args):
        if cursor_item_collide(cursor, self):
            if cursor.event == 2 and self.tipe == "IN":
                self.toggle_on = not self.toggle_on
                cursor.event = 0
                self.on = self.toggle_on
        if self.toggle_on:
            self.on = True

    def render(self, screen=pygame.Surface, *args):
        if self.toggle_on:
            pygame.draw.line(screen, (20, 20, 20), (self.rect.centerx - 5,
                             self.rect.top - 5), (self.rect.centerx, self.rect.top), 4)
            pygame.draw.line(screen, (20, 20, 20), (self.rect.centerx + 5,
                             self.rect.top - 5), (self.rect.centerx, self.rect.top), 4)
            pygame.draw.line(screen, (20, 20, 20), (self.rect.centerx,
                             self.rect.top - 10), (self.rect.centerx, self.rect.top), 4)

        pygame.draw.rect(screen, (255, 20, 20) if self.on else (
            60, 60, 60), (self.rect[0]+self.name_label_rect[2]+10, self.rect[1]+self.name_label_rect[3]/2-5, 10, 10))
        screen.blit(self.name_label_surface, (self.rect[0], self.rect[1]))


class Grid_diagram(pygame.sprite.Sprite):
    def __init__(self, size, divitions):
        pygame.sprite.Sprite.__init__(self)
        self.rect = [0, 0, 0, 0]
        self.size = size
        self.divition = divitions
        self.color = (220, 220, 220)
        self.active = False

    def cuadricula(self, *args): self.active = not self.active

    def update(self, *args):
        pass

    def render(self, screen=pygame.Surface, *args):
        if self.active:
            for column in range(round(self.size[0]/self.divition)):
                pygame.draw.line(screen, self.color, (column*self.divition,
                                                      0), (column*self.divition, self.size[1]), 1)
            for row in range(round(self.size[1]/self.divition)):
                pygame.draw.line(screen, self.color, (0, row*self.divition),
                                 (self.size[0], row*self.divition), 1)
