import pygame
from Util.Shared_Functions import get_name_label, get_params_label, delete_object, rename_object, change_params_object, item_state_logic, name_label_logic, param_label_logic, name_label_render, params_label_render, hold_on_state, not_hold_on_state, conector_line_logic, conector_line_render, cursor_item_collide


class Start_item(pygame.sprite.Sprite):
    def __init__(self, pos=(220, 220), tamaño=(20, 20), name="Start"):
        pygame.sprite.Sprite.__init__(self)
        self.name_pos = (0, 10)
        self.rect = pygame.Surface((tamaño)).get_rect(
            center=(round((pos[0])/30)*30, round((pos[1])/30)*30))
        self.stage_font = pygame.font.SysFont("Lucida Console", 16)
        self.font = pygame.font.SysFont("Lucida Console", 12)
        self.stage_name_surface = self.stage_font.render(
            "0", True, (0, 0, 0))
        self.stage_name_rect = self.stage_name_surface.get_rect()
        self.marco, self.fondo, self.state = [0, 0, 0], [230, 250, 230], 1
        self.options = {"Delete": delete_object, "Change label": rename_object}
        self.on = False
        self.turned_on_by = False
        get_name_label(self, name)

    def update(self, cursor=object, ui=object, *args):
        if not self.turned_on_by:
            self.on = False
        if ui.play:
            self.on = True
        else:
            self.on = False
        item_state_logic(self, cursor, ui)
        name_label_logic(self, cursor, ui)

    def render(self, screen=pygame.surface, *args):
        pygame.draw.rect(screen, self.fondo, self.rect, 0)
        pygame.draw.rect(screen, self.marco, self.rect, 1, 0)
        pygame.draw.rect(screen, self.marco, (self.rect.x -
                                              10, self.rect.y-5, 80, 70), 1)
        name_label_render(self, screen)
        screen.blit(self.stage_name_surface,
                    (self.rect.x+2,  self.rect.y+2))


class Stage_item(pygame.sprite.Sprite):
    def __init__(self, pos=(220, 220),  tamaño=(20, 20), name: str = "Stage", stage: int = 0):
        pygame.sprite.Sprite.__init__(self)
        self.marco, self.fondo = [20, 20, 20], [220, 220, 240]
        self.stage, self.state = stage, 1
        self.name_pos = (0, 10)
        self.rect = pygame.Surface((tamaño)).get_rect(
            center=(round((pos[0])/30)*30, round((pos[1])/30)*30))
        self.stage_font = pygame.font.SysFont("Lucida Console", 16)
        self.font = pygame.font.SysFont("Lucida Console", 12)
        self.stage_name_surface = self.stage_font.render(
            str(self.stage), True, (0, 0, 0))
        self.stage_name_rect = self.stage_name_surface.get_rect()
        self.options = {"Delete": delete_object,
                        "Change label": rename_object, "Hold on state": hold_on_state, "Not hold on state": not_hold_on_state}
        self.on = False
        self.turned_on_by = False
        self.was_on = False
        self.hold_on = False
        get_name_label(self, name)

    def update(self, cursor=object, ui=object, *args):
        if not self.turned_on_by:
            self.on = False
        item_state_logic(self, cursor, ui)
        name_label_logic(self, cursor, ui)
        if self.on == True:
            self.was_on = True
        if self.hold_on and self.was_on:
            self.turned_on_by = True
            self.on = True

    def render(self, screen=pygame.Surface, *args):
        if self.hold_on:
            pygame.draw.rect(screen, (250, 20, 20)if self.hold_on and self.was_on else (
                0, 0, 0), (self.rect[0]-10, self.rect[1]-10, 10, 10), 0)
        pygame.draw.rect(screen, self.fondo, self.rect, 0, 2)
        pygame.draw.rect(screen, self.marco, self.rect, 1, 2)
        name_label_render(self, screen)
        screen.blit(self.stage_name_surface,
                    (self.rect.x+2,  self.rect.y+2))


class Action_item(pygame.sprite.Sprite):
    def __init__(self, pos=(220, 220),  tamaño=(20, 20), name="Action", output_index=0):
        pygame.sprite.Sprite.__init__(self)
        self.name_pos = (0, 6)
        self.rect = pygame.Surface((tamaño)).get_rect(
            center=(round((pos[0])/30)*30, round((pos[1])/30)*30))
        self.output_font = pygame.font.SysFont("Lucida Console", 16)
        self.font = pygame.font.SysFont("Lucida Console", 12)
        self.output_name_surface = self.output_font.render(
            "Q" + str(output_index), True, (0, 0, 0))
        self.marco, self.fondo, self.state = [0, 0, 0], [250, 250, 230], 1
        self.options = {"Delete": delete_object, "Change label": rename_object}
        self.on = False
        self.turned_on_by = False
        self.output_index = output_index
        get_name_label(self, name)

    def update(self, cursor=object, ui=object, *args):
        if not self.turned_on_by:
            self.on = False
        item_state_logic(self, cursor, ui)
        name_label_logic(self, cursor, ui)

    def render(self, screen=pygame.Surface, *args):
        pygame.draw.rect(screen, self.fondo, (self.rect.x -
                                              10, self.rect.y+5, 80, 50), 0)
        pygame.draw.rect(screen, self.marco, (self.rect.x -
                                              10, self.rect.y+5, 80, 50), 1)
        name_label_render(self, screen)
        screen.blit(self.output_name_surface,
                    (self.rect.x-8,  self.rect.y+6))


class Text_item(pygame.sprite.Sprite):
    def __init__(self, pos=(220, 220), tamaño=(20, 20), name="Text"):
        pygame.sprite.Sprite.__init__(self)
        self.name_pos = (0, 0)
        self.rect = pygame.Surface((tamaño)).get_rect(
            center=(round((pos[0])/30)*30, round((pos[1])/30)*30))
        self.font = pygame.font.SysFont("Lucida Console", 12)
        self.marco, self.fondo, self.state = [0, 0, 0], [250, 250, 230], 1
        self.options = {"Delete": delete_object, "Change label": rename_object}
        get_name_label(self, name)

    def update(self, cursor=object, ui=object, *args):
        self.rect[2], self.rect[3] = self.name_label_rect[2], self.name_label_rect[3]
        item_state_logic(self, cursor, ui)
        name_label_logic(self, cursor, ui)

    def render(self, screen=pygame.surface, *args):
        name_label_render(self, screen)


class Conector(pygame.sprite.Sprite):
    def __init__(self, first_object=Stage_item, start_pos=(0, 0), name="", name_pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.first_object = first_object
        self.last_object = None
        self.state, self.point_list = 1, [start_pos]
        self.nofijo, self.position = [(0, 0), (0, 0)], []
        self.color, self.dire, self.dist = [0, 0, 0], 0, 0
        self.name_pos = name_pos
        self.rect = pygame.Surface((30, 30)).get_rect()
        self.font = pygame.font.SysFont("Lucida Console", 12)
        self.last_moved = "last"
        self.on_dir_indicator = 0
        self.line_lenght = 0
        self.on = False
        self.options = {"Delete": delete_object,
                        "Change label": rename_object}
        get_name_label(self, name)

    def update(self, cursor=object, ui=object, *args):
        if self.state == 0:
            if self.first_object.on:
                self.last_object.turned_on_by = True
                self.on = True
            else:
                self.on = False
        conector_line_logic(self, cursor, ui)
        name_label_logic(self, cursor, ui)

    def render(self, screen=pygame.surface, *args):
        conector_line_render(self, screen)
        if self.state == 0:
            if self.condition_dir in ["down", "up"]:
                pygame.draw.line(screen, (220, 20, 20)if self.on else (20, 20, 20), (
                    self.condition_point[0]-10, self.condition_point[1]+(10 if self.condition_dir == "up" else -10)), (self.condition_point[0], self.condition_point[1]), 4)
                pygame.draw.line(screen, (220, 20, 20)if self.on else (20, 20, 20), (
                    self.condition_point[0]+10, self.condition_point[1]+(10 if self.condition_dir == "up" else -10)), (self.condition_point[0], self.condition_point[1]), 4)
                self.name_pos = (6, 6)
            else:
                pygame.draw.line(screen, (220, 20, 20)if self.on else (20, 20, 20), (
                    self.condition_point[0]+(10 if self.condition_dir == "left" else -10), self.condition_point[1]-10), (self.condition_point[0], self.condition_point[1]), 4)
                pygame.draw.line(screen, (220, 20, 20)if self.on else (20, 20, 20), (
                    self.condition_point[0]+(10 if self.condition_dir == "left" else -10), self.condition_point[1]+10), (self.condition_point[0], self.condition_point[1]), 4)
                self.name_pos = (-self.name_label_rect[2]/2, 20)
            name_label_render(self, screen, "left")


class Condition(pygame.sprite.Sprite):
    def __init__(self, first_object=Stage_item, start_pos=(0, 0), name="", name_pos=(40, 0), function=callable, params=()):
        pygame.sprite.Sprite.__init__(self)
        self.first_object = first_object
        self.last_object = None
        self.state, self.point_list = 1, [start_pos]
        self.nofijo, self.position = [(0, 0), (0, 0)], []
        self.color, self.dire, self.dist = [0, 0, 0], 0, 0
        self.name = name
        self.name_pos = (0, 0)
        self.rect = pygame.Surface((30, 30)).get_rect()
        self.params_font = pygame.font.SysFont("Lucida Console", 16)
        self.font = pygame.font.SysFont("Lucida Console", 12)
        self.last_moved = "last"
        self.on_dir_indicator = 0
        self.line_lenght = 0
        self.on = False
        self.options = {"Delete": delete_object,
                        "Change label": rename_object,
                        "Change condition": change_params_object}
        self.condition_func = function
        self.params = params
        self.params_pos = (0, 0)
        self.condition_point = start_pos
        self.condition_dir = 'vertical'
        get_name_label(self, name)
        get_params_label(self, params)

    def update(self, cursor=object, ui=object, *args):
        if self.state == 0:
            if self.first_object.on:
                if self.condition_func(ui, self, self.params) == True:
                    self.last_object.turned_on_by = True
                    self.on = True
                else:
                    self.on = False
            else:
                self.on = False
        conector_line_logic(self, cursor, ui)
        name_label_logic(self, cursor, ui)
        param_label_logic(self, cursor, ui)

    def render(self, screen=pygame.Surface, *args):
        conector_line_render(self, screen)
        if self.state == 0:
            if self.condition_dir in ["down", "up"]:
                pygame.draw.line(screen, (220, 20, 20)if self.on else (20, 20, 20), (
                    self.condition_point[0]-10, self.condition_point[1]), (self.condition_point[0]+10, self.condition_point[1]), 4)
                self.name_pos = (20, 6)
                self.params_pos = (4, -10)
            else:
                pygame.draw.line(screen, (220, 20, 20)if self.on else (20, 20, 20), (
                    self.condition_point[0], self.condition_point[1]-10), (self.condition_point[0], self.condition_point[1]+10), 4)
                self.name_pos = (-self.name_label_rect[2]/2, 30)
                self.params_pos = (-self.params_label_rect[2]/2, 18)
            name_label_render(self, screen, "left")
            params_label_render(self, screen, "left")
