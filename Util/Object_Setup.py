import pygame
from copy import deepcopy
from Util.Diagram_Items import Start_item, Stage_item, Action_item, Conector, Condition, Text_item
from Util.UI_Items import On_indiactor_UI, Button_UI, Grid_diagram
from Util.Shared_Functions import save_surface_as_image, cursor_group_collide, cursor_group_relative_pos, input_condition, input_binding_key, output_action_on

clif = [230, 230, 230], [160, 160, 160], [200, 200, 200]  # color interface


def button_setup(self):
    add_start_button = pygame.surface.Surface(
        (60, 60), pygame.SRCALPHA, 32)
    pygame.draw.line(add_start_button, clif[1], (30, 30), (30, 60), 3)
    pygame.draw.rect(add_start_button, (200, 250, 230),
                     (15, 14, 30, 30), 0)
    pygame.draw.rect(add_start_button, (20, 20, 20), (15, 14, 30, 30), 2)
    pygame.draw.rect(add_start_button, (20, 20, 20), (10, 11, 40, 36), 2)
    add_start_button.blit(self.def_font.render(
        '0', True, (0, 0, 0)), (20, 20))
    self.side_menu_group.add(Button_UI((10, 80), add_start_button,
                                       self.cursor.save_object_to_create, (Start_item, (60, 60)), "Start", "unique"))

    # add_finish_button = pygame.surface.Surface(
    #     (60, 60), pygame.SRCALPHA, 32)
    # pygame.draw.rect(add_finish_button, (250, 230, 230),
    #                  (15, 15, 30, 30), 0)
    # pygame.draw.rect(add_finish_button, (20, 20, 20), (15, 15, 30, 30), 2)
    # pygame.draw.lines(add_finish_button, (0, 0, 0), 0, [
    #     (15, 15), (44, 45), (44, 15), (15, 45)], 2)
    # self.side_menu_group.add(Button_UI((80, 80), add_finish_button,
    #                                    self.cursor.save_object_to_create, (Stage_item, (60, 60)), "Finish", "unique"))

    add_stage_button = pygame.surface.Surface(
        (60, 60), pygame.SRCALPHA, 32)
    pygame.draw.lines(add_stage_button, (140, 140, 140), 0, [
        (30, 0), (30, 30), (60, 30)], 3)
    pygame.draw.rect(add_stage_button, (230, 230, 250),
                     (15, 15, 30, 30), 0)
    pygame.draw.rect(add_stage_button, (20, 20, 20), (15, 15, 30, 30), 2)
    add_stage_button.blit(self.def_font.render(
        'N', True, (0, 0, 0)), (20, 20))
    self.side_menu_group.add(Button_UI((10, 150), add_stage_button,
                                       self.cursor.save_object_to_create, (Stage_item, (60, 60)), "Stage", "unique"))

    add_action_button = pygame.surface.Surface(
        (60, 60), pygame.SRCALPHA, 32)
    pygame.draw.line(add_action_button, (140, 140, 140),
                     (0, 30), (30, 30), 3)
    pygame.draw.rect(add_action_button, (250, 250, 230),
                     (10, 18, 40, 25), 0)
    pygame.draw.rect(add_action_button, (20, 20, 20), (10, 18, 40, 25), 2)
    add_action_button.blit(self.def_font.render(
        'Q0', True, (0, 0, 0)), (18, 25))
    self.side_menu_group.add(Button_UI((80, 150), add_action_button,
                                       self.cursor.save_object_to_create, (Action_item, (60, 60)), "Action", "unique"))

    add_conector_button = pygame.surface.Surface(
        (60, 60), pygame.SRCALPHA, 32)
    pygame.draw.line(add_conector_button, (140, 140, 140),
                     (30, 0), (30, 60), 3)
    self.side_menu_group.add(Button_UI((10, 220), add_conector_button,
                                       self.cursor.save_object_to_create, (Conector, [(0, 0)]), "Conector", "unique"))

    add_condition_button = pygame.surface.Surface(
        (60, 60), pygame.SRCALPHA, 32)
    pygame.draw.line(add_condition_button,
                     (140, 140, 140), (30, 0), (30, 60), 3)
    pygame.draw.line(add_condition_button,
                     (140, 140, 140), (23, 30), (37, 30), 5)
    add_condition_button.blit(self.def_font.render(
        'I0', True, (0, 0, 0)), (35, 35))
    self.side_menu_group.add(Button_UI((80, 220), add_condition_button,
                                       self.cursor.save_object_to_create, (Condition, [(0, 0)]), "Condition", "unique"))

    add_text_button = pygame.surface.Surface((60, 60), pygame.SRCALPHA, 32)
    add_text_button.blit(self.def_font.render(
        'TEXT', True, (0, 0, 0)), (15, 25))
    self.side_menu_group.add(Button_UI((80, 290), add_text_button,
                                       self.cursor.save_object_to_create, (Text_item, (60, 60)), "Text", "unique"))

    cuad = Grid_diagram(self.diagram_group.surface.get_size(), 30)
    self.diagram_group.add(cuad)

    hide_button = pygame.surface.Surface((30, 30), pygame.SRCALPHA, 32)
    pygame.draw.line(hide_button, (20, 20, 20), (5, 15), (15, 5), 2)
    pygame.draw.line(hide_button, (20, 20, 20), (15, 5), (25, 15), 2)
    pygame.draw.line(hide_button, (20, 20, 20), (25, 15), (15, 25), 2)
    pygame.draw.line(hide_button, (20, 20, 20), (15, 25), (5, 15), 2)
    self.action_menu_group.add(Button_UI((10, 10), hide_button,
                                         self.side_menu_group.toggle_hide_surface, (0, 0), "Hide selection menu"))

    toggle_grid_button = pygame.surface.Surface(
        (30, 30), pygame.SRCALPHA, 32)
    pygame.draw.rect(toggle_grid_button, (250, 20, 20), (5, 5, 10, 10), 1)
    pygame.draw.rect(toggle_grid_button, (250, 20, 20), (14, 5, 10, 10), 1)
    pygame.draw.rect(toggle_grid_button, (250, 20, 20), (5, 14, 10, 10), 1)
    pygame.draw.rect(toggle_grid_button, (250, 20, 20),
                     (14, 14, 10, 10), 1)
    grid_button = Button_UI((160, 10), toggle_grid_button,
                            cuad.cuadricula, (0, 0), "Toggle grid")
    self.action_menu_group.add(grid_button)
    grid_button.on_press(self.cursor, self)

    simulate_button = pygame.surface.Surface((30, 30), pygame.SRCALPHA, 32)
    pygame.draw.line(simulate_button, (20, 20, 20), (5, 5), (25, 15), 2)
    pygame.draw.line(simulate_button, (20, 20, 20), (5, 25), (25, 15), 2)
    pygame.draw.line(simulate_button, (20, 20, 20), (5, 5), (5, 25), 2)
    self.action_menu_group.add(Button_UI(((self.resolution[0])/2, 10), simulate_button,
                                         self.toggle_play, (0, 0), "Toggle simulation"))

    add_input_button = pygame.surface.Surface((30, 30), pygame.SRCALPHA, 32)
    add_input_button.blit(self.def_font.render('+IN', True, (0, 0, 0)), (3, 9))
    self.action_menu_group.add(Button_UI((self.resolution[0] - 120, 10), add_input_button,
                                         add_input_indicator, (0, 0), "Add input", "press"))

    add_output_button = pygame.surface.Surface((30, 30), pygame.SRCALPHA, 32)
    add_output_button.blit(self.def_font.render(
        '+OUT', True, (0, 0, 0)), (3, 9))
    self.action_menu_group.add(Button_UI((self.resolution[0] - 60, 10), add_output_button,
                                         add_output_indicator, (0, 0), "Add output", "press"))

    back_button = pygame.surface.Surface((30, 30), pygame.SRCALPHA, 32)
    pygame.draw.line(back_button, (20, 20, 20), (25, 5), (5, 15), 2)
    pygame.draw.line(back_button, (20, 20, 20), (25, 25), (5, 15), 2)
    pygame.draw.line(back_button, (20, 20, 20), (25, 5), (25, 25), 2)
    self.action_menu_group.add(Button_UI((10, self.resolution[1] - 40), back_button,
                                         self.modification_back, (0, 0), "Undo", "press"))

    save_image_button = pygame.surface.Surface((30, 30), pygame.SRCALPHA, 32)
    pygame.draw.rect(save_image_button, (20, 20, 20), (5, 5, 20, 20), 1)
    pygame.draw.line(save_image_button, (20, 20, 20), (5, 5), (25, 5), 1)
    pygame.draw.line(save_image_button, (20, 20, 20), (5, 5), (15, 15), 1)
    pygame.draw.line(save_image_button, (20, 20, 20), (25, 5), (15, 15), 1)

    self.action_menu_group.add(Button_UI((self.resolution[0] - 40, self.resolution[1] - 40), save_image_button,
                                         save_surface_as_image, (self.path, "image saved.png"), "Save as image", "press"))

    self.indicator_group.add(self.cursor)

    self.io_menu_group.add(On_indiactor_UI(
        (10, 60), "I0", (20, 0), input_binding_key, "0", "IN", 0))
    self.io_menu_group.add(On_indiactor_UI(
        (80, 60), "Q0", (20, 0), output_action_on, (self.diagram_group, 0), "OUT", 0))


def create_object(self):
    if self.cursor.crear[0] and self.cursor.event == 2:
        if self.cursor.crear[0] == Conector:
            for figura in cursor_group_collide(self.cursor, self.diagram_group):
                if figura.__class__.__name__ not in ["Conector", "Condition", "Text_item", "Action_item"] and not self.cursor.subject:
                    self.cursor.subject = Conector(
                        figura, figura.rect.center)
                    self.diagram_group.add(self.cursor.subject)
                    self.cursor.event = 0
                    self.modification_safe(
                        [("add", self.cursor.subject, "")])
                    return
        if self.cursor.crear[0] == Condition:
            for figura in cursor_group_collide(self.cursor, self.diagram_group):
                if figura.__class__.__name__ not in ["Conector", "Condition", "Text_item", "Action_item"] and not self.cursor.subject:
                    conditions = 1
                    for item in self.diagram_group:
                        if item.__class__.__name__ == "Condition":
                            conditions += 1
                    self.cursor.subject = Condition(
                        figura, figura.rect.center, "Condition " + str(conditions), (20, 0), active_condition, "I0")
                    self.diagram_group.add(self.cursor.subject)
                    self.cursor.event = 0
                    self.modification_safe(
                        [("add", self.cursor.subject, "")])
                    return
        if self.cursor.crear[0] == Start_item:
            self.cursor.subject = Start_item(cursor_group_relative_pos(
                self.cursor, self.diagram_group), self.cursor.crear[1], "Start")
            self.diagram_group.add(self.cursor.subject)
            self.modification_safe([("add", self.cursor.subject, "")])
            self.cursor.event, self.cursor.subject = 0, False
            return
        if self.cursor.crear[0] == Stage_item:
            etapas = 1
            for item in self.diagram_group:
                if item.__class__.__name__ == "Stage_item":
                    etapas += 1
            self.cursor.subject = Stage_item(
                cursor_group_relative_pos(self.cursor, self.diagram_group), self.cursor.crear[1], "Stage " + str(etapas), etapas)
            self.diagram_group.add(self.cursor.subject)
            self.modification_safe([("add", self.cursor.subject, "")])
            self.cursor.event, self.cursor.subject = 0, False
            return
        if self.cursor.crear[0] == Action_item:
            output_index = 0
            for item in self.diagram_group:
                if item.__class__.__name__ == "Action_item":
                    output_index += 1
            self.cursor.subject = Action_item(
                cursor_group_relative_pos(self.cursor, self.diagram_group), self.cursor.crear[1], "Action "+str(output_index), output_index)
            self.diagram_group.add(self.cursor.subject)
            output_indicator = On_indiactor_UI((80, 60+40*output_index), "Q"+str(
                output_index), (20, 0), output_action_on, (self.diagram_group, output_index), "OUT", output_index)
            self.io_menu_group.add(output_indicator)
            self.modification_safe(
                [("add", self.cursor.subject, ""), ("add", output_indicator, "")])
            self.cursor.event, self.cursor.subject = 0, False
            return
        if self.cursor.crear[0] == Text_item:
            self.cursor.subject = Text_item(
                cursor_group_relative_pos(self.cursor, self.diagram_group), self.cursor.crear[1], "Text")
            self.diagram_group.add(self.cursor.subject)
            self.modification_safe([("add", self.cursor.subject, "")])
            self.cursor.event, self.cursor.subject = 0, False
            return


def io_indicators_state(self):
    self.input_list = []
    self.output_list = []
    for io in self.io_menu_group:
        if io.__class__.__name__ == "On_indiactor_UI":
            condition = io.condition_func(*[self]+list(io.params))
            io.on = condition if type(condition) == bool else io.on
            if io.on:
                if io.tipe == "IN":
                    self.input_list.append(io.number)
                if io.tipe == "OUT":
                    self.output_list.append(io.number)


def active_condition(self, item, params, *args):
    return input_condition(params, self.input_list, self.output_list)


def add_input_indicator(self, *args):
    input_index = 0
    for item in self.io_menu_group:
        if item.__class__.__name__ == "On_indiactor_UI" and item.tipe == "IN":
            input_index += 1
    input_indicator = On_indiactor_UI((10, 60+40*input_index), "I"+str(
        input_index), (20, 0), input_binding_key, str(input_index), "IN", input_index)
    self.io_menu_group.add(input_indicator)
    self.modification_safe([["add", input_indicator, ""]])


def add_output_indicator(self, *args):
    output_index = 0
    for item in self.io_menu_group:
        if item.__class__.__name__ == "On_indiactor_UI" and item.tipe == "OUT":
            output_index += 1
    output_indicator = On_indiactor_UI((80, 60+40*output_index), "Q"+str(output_index),
                                       (20, 0), output_action_on, (self.diagram_group, output_index), "OUT", output_index)
    self.io_menu_group.add(output_indicator)
    self.modification_safe([["add", output_indicator, ""]])
