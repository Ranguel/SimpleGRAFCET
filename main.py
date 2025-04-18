import pygame
import os

from Util.Diagram_Items import *
from Util.UI_Items import *
from Util.Object_Setup import *
from Util.Shared_Functions import *


clif = [230, 230, 230], [160, 160, 160], [200, 200, 200]
style = [250, 150, 70], [250, 190, 150]


class Custom_group(pygame.sprite.Group):
    def __init__(self, pos=[0, 0], size=(0, 0), color=(120, 120, 120), transparent=False):
        super().__init__()
        self.pos = list(pos)
        self.surface = pygame.surface.Surface(
            size, pygame.SRCALPHA).convert_alpha() if transparent else pygame.surface.Surface(size).convert_alpha()
        self.color = color
        self.transparent = transparent
        self.zoom = 1
        self.hide_surface = False

    def toggle_hide_surface(self, *args):
        self.hide_surface = not self.hide_surface

    def update(self, cursor, ui, ignore=[], *args):
        for obj in self:
            if obj.__class__.__name__ not in ignore:
                obj.update(cursor, ui, *args)

    def render(self, surface=pygame.Surface, ignore=[], fill=True, *args):
        if fill:
            self.surface.fill((self.color))
        for obj in self:
            if obj.__class__.__name__ not in ignore:
                obj.render(self.surface, *args)
        if not self.hide_surface:
            escaled_surface = pygame.transform.smoothscale_by(
                self.surface, self.zoom)
            surface.blit(escaled_surface, self.pos)


class UI(object):
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 1024)
        pygame.init()
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.active, self.frame = 1, pygame.time.Clock()
        self.etapas = 1
        self.resolution = (1080, 720)
        self.pygame_events = pygame.event.get()
        self.main_screen = pygame.display.set_mode(
            self.resolution, pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
        pygame.display.set_caption("Simple Grafcet")
        self.cursor = Cursor()
        self.diagram_group = Custom_group(
            (0, 0), (1000, 1000), [240, 240, 240])
        self.side_menu_group = Custom_group(
            (0, 0), (150, self.resolution[1]), [180, 180, 180])
        self.action_menu_group = Custom_group(
            (0, 0), self.resolution, [200, 200, 200, 0], True)
        self.io_menu_group = Custom_group(
            (self.resolution[0] - 150, 0),  (150, self.resolution[1]), [220, 220, 220])
        self.indicator_group = Custom_group(
            (0, 0), self.resolution, [0, 0, 0, 0], True)
        self.undo_list = []
        self.def_font = pygame.font.SysFont("Lucida Console", 12)
        button_setup(self)
        self.input_text = ""
        self.pendant_input_text = None
        self.play = False
        self.input = 1
        self.output = 1
        self.input_list = []
        self.output_list = []

    def toggle_play(self, *args):
        self.play = not self.play
        if self.play == False:
            for item in self.diagram_group:
                item.on = False
                item.was_on = False

    def modification_back(self, *args):
        if not len(self.undo_list):
            return
        changes = self.undo_list.pop()
        for state in changes:
            if state["tipe"] == "none":
                continue
            elif state["tipe"] == "mod":
                set_nested_attr(state["objective"],
                                state["property"], state["last value"])
            elif state["tipe"] == "kill":
                self.diagram_group.add(state["objective"])
            elif state["tipe"] == "add":
                state["objective"].kill()

    def modification_safe(self, modifications, *args):
        mod_list = []
        for tipe, objective, prop in modifications:
            try:
                last_value = deepcopy(get_nested_attr(
                    objective, prop) if prop != "" else "")
            except:
                last_value = get_nested_attr(
                    objective, prop) if prop != "" else ""
            mod_list.append({
                "tipe": tipe,
                "objective": objective,
                "property": prop,
                "last value": last_value
            })
        self.undo_list.append(mod_list)
        if len(self.undo_list) > 20:
            self.undo_list.pop(0)

    def event_handler(self):
        self.pygame_events = pygame.event.get()
        for event in self.pygame_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and self.diagram_group.zoom < 1.5:
                    self.diagram_group.zoom, self.diagram_group.pos = apply_zoom(
                        self.diagram_group.surface, self.diagram_group.zoom, self.diagram_group.pos, self.cursor.rect.center, 1.01)
                elif event.button == 5 and self.diagram_group.zoom > 0.75:
                    self.diagram_group.zoom, self.diagram_group.pos = apply_zoom(
                        self.diagram_group.surface, self.diagram_group.zoom, self.diagram_group.pos, self.cursor.rect.center, 0.99)
            if event.type == pygame.QUIT:
                self.active = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and (event.mod & pygame.KMOD_CTRL) or event.key == pygame.K_z and (event.mod & pygame.KMOD_META):
                    self.modification_back()
                if event.key == pygame.K_LEFT:
                    self.diagram_group.pos[0] += 30
                if event.key == pygame.K_RIGHT:
                    self.diagram_group.pos[0] -= 30
                if event.key == pygame.K_UP:
                    self.diagram_group.pos[1] += 30
                if event.key == pygame.K_DOWN:
                    self.diagram_group.pos[1] -= 30
                if event.key == pygame.K_ESCAPE:
                    self.input_text = ""
                    self.pendant_input_text = None
                    for elemento in self.side_menu_group:
                        elemento.state = 0
                    if self.cursor.subject:
                        self.cursor.subject.kill()
                        self.cursor.subject = False
                    self.cursor.event = 0
                    self.cursor.crear = [False, False]
                if event.key == pygame.K_BACKSPACE:
                    if self.pendant_input_text != None:
                        self.input_text = self.input_text[:-1]
                elif self.pendant_input_text != None:
                    self.input_text += event.unicode
                if event.key == pygame.K_RETURN:
                    if self.pendant_input_text != None:
                        self.pendant_input_text[0](
                            *self.pendant_input_text[1]+[self.input_text])
                        self.input_text = ""
                        self.pendant_input_text = None

    def start(self):
        while self.active:
            self.main_screen.fill([0, 0, 0])

            create_object(self)
            self.indicator_group.update(self.cursor, self)
            self.side_menu_group.update(self.cursor, self)
            self.io_menu_group.update(self.cursor, self)
            self.action_menu_group.update(self.cursor, self)
            self.diagram_group.update(
                self.cursor, self, ["Condition", "Conector", "Grid_diagram"])
            io_indicators_state(self)
            self.diagram_group.update(
                self.cursor, self, ["Text_item", "Action_item", "Stage_item", "Start_item"])

            self.diagram_group.render(
                self.main_screen, ["Text_item", "Action_item", "Stage_item", "Start_item"])
            self.diagram_group.render(
                self.main_screen, ["Condition", "Conector", "Grid_diagram"], False)
            self.side_menu_group.render(self.main_screen)
            self.io_menu_group.render(self.main_screen)
            self.action_menu_group.render(self.main_screen)
            self.indicator_group.render(self.main_screen)

            pygame.display.update()
            self.frame.tick(30)
            self.event_handler()


ui = UI()
ui.start()
