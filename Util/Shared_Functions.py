import pygame
import math
import re


def save_surface_as_image(ui, path, filename="output.png", *args):
    if not ui.diagram_group.surface:
        return
    pygame.image.save(ui.diagram_group.surface, path + "/" + filename)


def get_nested_attr(obj, attr_path):
    for attr in attr_path.split('.'):
        obj = getattr(obj, attr)
    return obj


def set_nested_attr(obj, attr_path, value):
    attrs = attr_path.split('.')
    for attr in attrs[:-1]:
        obj = getattr(obj, attr)
    setattr(obj, attrs[-1], value)


def input_binding_key(ui, key, *args):
    for event in ui.pygame_events:
        if event.type == pygame.KEYDOWN:
            if event.unicode == key:
                return True
        if event.type == pygame.KEYUP:
            if event.unicode == key:
                return False
    return None


def output_action_on(ui, group, output_index, *args):
    for item in group:
        if item.__class__.__name__ == "Action_item":
            if item.output_index == output_index and item.on:
                return True
    return False


def apply_zoom(surface, zoom, offset, mouse_pos, zoom_factor, *args):
    rel_mouse_x = (mouse_pos[0] - offset[0]) / zoom
    rel_mouse_y = (mouse_pos[1] - offset[1]) / zoom
    zoom *= zoom_factor
    offset[0] = mouse_pos[0] - rel_mouse_x * zoom
    offset[1] = mouse_pos[1] - rel_mouse_y * zoom
    return zoom, offset


def cursor_group_relative_pos(cursor, group, *args):
    return [cursor.rect[0]/group.zoom-group.pos[0]/group.zoom, cursor.rect[1]/group.zoom-group.pos[1]/group.zoom]


def cursor_item_collide(cursor, item=pygame.sprite.Sprite, *args):
    try:
        group = item.groups()[0]
    except:
        return False
    cursor_rect = pygame.Surface([10, 10]).get_rect(center=[
        cursor.rect[0]/group.zoom-group.pos[0]/group.zoom, cursor.rect[1]/group.zoom-group.pos[1]/group.zoom])
    if cursor_rect.colliderect(item):
        return True
    return False


def cursor_group_collide(cursor, group, *args):
    collide_list = []
    cursor_rect = pygame.Surface([10, 10]).get_rect(center=[
        cursor.rect[0]/group.zoom-group.pos[0]/group.zoom, cursor.rect[1]/group.zoom-group.pos[1]/group.zoom])
    for item in group:
        if cursor_rect.colliderect(item):
            collide_list.append(item)
    return collide_list


def delete_object(object_to_delete=pygame.sprite.Sprite, ui=object, *args):
    ui.modification_safe([["kill", object_to_delete, ""]])
    ui.cursor.event = 0
    group = object_to_delete.groups()
    if not len(object_to_delete.groups()):
        return
    for con in group[0]:
        try:
            if con.first_object == object_to_delete or con.last_object == object_to_delete:
                con.kill()
        except:
            pass
    if object_to_delete.__class__.__name__ == "Action_item":
        for on_indicator in ui.io_menu_group:
            if on_indicator.tipe == "OUT" and on_indicator.number == object_to_delete.output_index:
                on_indicator.kill()
    object_to_delete.kill()


def rename_object(object_to_rename=pygame.sprite.Sprite, ui=object, *args):
    ui.modification_safe([("mod", object_to_rename, "last_name"), ("mod", object_to_rename, "name"), (
        "mod", object_to_rename, "name_label_surface"), ("mod", object_to_rename, "name_label_rect")])
    ui.cursor.event = 0
    object_to_rename.changing_name = True
    ui.input_text = object_to_rename.name
    ui.pendant_input_text = get_name_label, [object_to_rename]


def change_params_object(object_to_rename=pygame.sprite.Sprite, ui=object, *args):
    ui.modification_safe([("mod", object_to_rename, "last_params"), ("mod", object_to_rename, "params"), (
        "mod", object_to_rename, "params_label_surface"), ("mod", object_to_rename, "params_label_rect")])
    ui.cursor.event = 0
    object_to_rename.changing_params = True
    ui.input_text = object_to_rename.params
    ui.pendant_input_text = get_params_label, [object_to_rename]


def hold_on_state(object_to_hold_state=pygame.sprite.Sprite, ui=object, *args):
    ui.modification_safe([("mod", object_to_hold_state, "hold_on")])
    object_to_hold_state.hold_on = True


def not_hold_on_state(object_to_hold_state=pygame.sprite.Sprite, ui=object, *args):
    ui.modification_safe([("mod", object_to_hold_state, "hold_on"), (
        "mod", object_to_hold_state, "was_on"), ("mod", object_to_hold_state, "turned_on_by")])
    object_to_hold_state.hold_on = False
    object_to_hold_state.was_on = False
    object_to_hold_state.turned_on_by = False


def input_condition(inputs: str, active_inputs: list[int], active_outputs: list[int], *args) -> bool:
    def replace(match):
        token = match.group(0)
        not_op = token.startswith('!')
        symbol = token[1] if not_op else token[0]
        index = int(re.search(r'\d+', token).group())
        if symbol == 'I' or symbol == 'i':
            state = index in active_inputs
        elif symbol == 'Q' or symbol == 'q':
            state = index in active_outputs
        else:
            return "False"
        return str(not state if not_op else state)
    expression = inputs.replace("&", " and ").replace("|", " or ")
    expression = re.sub(r'!?[IQ]\d+', replace, expression)
    try:
        return eval(expression)
    except:
        return False


def filter_point_list(points):
    if len(points) < 3:
        return points[:]
    result = [points[0]]
    for i in range(1, len(points)-1):
        prev = points[i-1]
        curr = points[i]
        next = points[i+1]
        if curr == prev:
            continue
        dx1 = curr[0] - prev[0]
        dy1 = curr[1] - prev[1]
        dx2 = next[0] - curr[0]
        dy2 = next[1] - curr[1]
        mag1 = math.hypot(dx1, dy1)
        mag2 = math.hypot(dx2, dy2)
        if mag1 == 0 or mag2 == 0:
            continue
        ux1, uy1 = dx1 / mag1, dy1 / mag1
        ux2, uy2 = dx2 / mag2, dy2 / mag2
        dot = ux1 * ux2 + uy1 * uy2
        if dot > -0.99:
            result.append(curr)
    result.append(points[-1])
    return result


def points_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def interpolar(p1, p2, t):
    return (
        p1[0] + (p2[0] - p1[0]) * t,
        p1[1] + (p2[1] - p1[1]) * t
    )


def marker_on_line(self, line_length, points, progress):
    try:
        distance_covered = int((progress if progress > 0 else 0)
                               if progress < line_length else line_length)
        for i in range(len(points) - 1):
            seg_dist = points_distance(points[i], points[i + 1])
            if distance_covered <= seg_dist:
                t = distance_covered / seg_dist
                p1, p2 = points[i], points[i + 1]
                dx, dy = p2[0] - p1[0], p2[1] - p1[1]

                if abs(dx) > abs(dy):
                    direction = 'right' if dx > 0 else 'left'
                elif abs(dy) > abs(dx):
                    direction = 'down' if dy > 0 else 'up'
                else:
                    direction = 'diagonal'

                return interpolar(p1, p2, t), direction
            distance_covered -= seg_dist
        return points[-1], 'None'
    except:
        self.kill()


def get_name_label(self, name="", *args):
    self.last_name = name
    self.name = name
    self.name_label_surface = self.font.render(
        str(self.name), True, (0, 0, 0))
    self.name_label_rect = self.name_label_surface.get_rect()
    self.changing_name = False
    self.changing_name_timer = 10


def get_params_label(self, params="", *args):
    self.last_params = params
    self.params = params
    self.params_label_surface = self.params_font.render(
        str(self.params), True, (0, 0, 0))
    self.params_label_rect = self.params_label_surface.get_rect()
    self.changing_params = False
    self.changing_params_timer = 10


def name_label_logic(self, cursor=object, ui=object, *args):
    if self.changing_name:
        self.changing_name_timer -= 1 if self.changing_name_timer else -20
        self.name_label_surface = self.font.render(
            str(ui.input_text) + ("|" if self.changing_name_timer > 10 else " "), True, (220, 20, 20))
        self.name_label_rect = self.name_label_surface.get_rect()
        if ui.pendant_input_text == None:
            get_name_label(self, self.last_name)
        if cursor.event == 2:
            # cursor.event = 0
            get_name_label(self, ui.input_text)
            ui.input_text = ""
            ui.pendant_input_text = None


def param_label_logic(self, cursor=object, ui=object, *args):
    if self.changing_params:
        self.changing_params_timer -= 1 if self.changing_params_timer else -20
        self.params_label_surface = self.font.render(
            str(ui.input_text) + ("|" if self.changing_params_timer > 10 else " "), True, (220, 20, 20))
        self.params_label_rect = self.params_label_surface.get_rect()
        if ui.pendant_input_text == None:
            get_params_label(self, self.last_params)
        if cursor.event == 2:
            # cursor.event = 0
            get_params_label(self, ui.input_text)
            ui.input_text = ""
            ui.pendant_input_text = None


def name_label_render(self, screen=pygame.Surface, aline="center"):
    screen.blit(self.name_label_surface, (self.rect.centerx - (round(self.name_label_rect[2]/2) if aline == "center" else 0) +
                                          self.name_pos[0], self.rect.centery - round(self.name_label_rect[3]/2) + self.name_pos[1]))


def params_label_render(self, screen=pygame.Surface, aline="center"):
    screen.blit(self.params_label_surface, (self.rect.centerx - (round(self.params_label_rect[2]/2) if aline == "center" else 0) +
                                            self.params_pos[0], self.rect.centery - round(self.params_label_rect[3]/2) + self.params_pos[1]))


def item_state_logic(self, cursor=object, ui=object, *args):
    self.turned_on_by = False
    cursor_pos = cursor_group_relative_pos(cursor, self.groups()[0])
    if self.state == 0 and cursor_item_collide(cursor, self):
        if cursor.crear[0] != False:
            if cursor.event == 2 and cursor.crear[0].__name__ != "Conector" and cursor.crear[0].__name__ != "Condition":
                mod_list = [("mod", self, "rect.center")]
                for item in self.groups()[0]:
                    if (item.__class__.__name__ == "Conector" or item.__class__.__name__ == "Condition") and (item.first_object == self or item.last_object == self):
                        mod_list += [("mod", item, "point_list"), ("mod", item, "nofijo"),
                                     ("mod", item, "line_lenght"), ("mod",
                                                                    item, "position"),
                                     ("mod", item, "last_moved")]
                ui.modification_safe(mod_list)
                cursor.offset = [self.rect.left -
                                 cursor_pos[0], self.rect.top-cursor_pos[1]]
                self.state = 1
                cursor.event = 0
            if cursor.event == 3:
                cursor.inter_click_menu = "Menu", (self.options, self)
                cursor.event = 0
    elif self.state == 1:
        self.rect.topleft = round((cursor_pos[0]+cursor.offset[0])/30
                                  )*30, round((cursor_pos[1]+cursor.offset[1])/30)*30
        if cursor.current_press[0] == 0:
            self.state = 0


def conector_line_logic(self, cursor=object, ui=object, *args):
    if self.state == 0:
        if cursor_item_collide(cursor, self):
            if cursor.event == 3:
                cursor.inter_click_menu = "Menu", (self.options, self)
                cursor.event = 0
    if self.last_object != None:
        if self.last_object.turned_on_by:
            self.last_object.on = True
        else:
            self.last_object.on = False
    real_cursor_pos = cursor_group_relative_pos(cursor, self.groups()[0])
    cursor_pos = [round((real_cursor_pos[0])/30
                        )*30, round((real_cursor_pos[1])/30)*30]
    if self.state == 0:
        if ((self.first_object.state == 1 and self.last_moved == "last") or (self.last_object.state == 1 and self.last_moved == "first")):
            self.point_list.reverse()
        if self.first_object.state == 1:
            cursor_pos = self.first_object.rect.center
        if self.last_object.state == 1:
            cursor_pos = self.last_object.rect.center
    self.position = cursor_pos
    if self.state == 1 or (self.state == 0 and (self.first_object.state == 1 or self.last_object.state == 1)):
        if self.state == 0:
            self.last_moved = "first" if self.first_object.state == 1 else "last" if self.last_object.state == 1 else self.last_moved
        if math.sqrt((self.point_list[-1][0]-cursor_pos[0])**2+(
                self.point_list[-1][1]-cursor_pos[1])**2) > self.dist and self.dist < 20:
            if (abs(self.point_list[-1][0]-self.position[0])
                    >= abs(self.point_list[-1][1]-self.position[1])):
                self.dire = 0
            else:
                self.dire = 1
        if self.dire == 1:
            self.nofijo[0] = (self.point_list[-1][0], self.position[1])
        else:
            self.nofijo[0] = (self.position[0], self.point_list[-1][1])
        self.nofijo[1] = self.position
    if cursor.event == 2:
        coll = False
        for figura in cursor_group_collide(cursor, self.groups()[0]):
            if cursor.subject == self:
                self.state, self.last_object = 0, figura
                cursor.event, cursor.subject = 0, False
                conector_new_line(self)
                coll = True
                break
        if coll == False:
            conector_new_line(self)
    if (cursor.current_press[0] == 0 and self.state == 0 and (self.first_object.state == 0 or self.last_object.state == 0)):
        conector_new_line(self)
    self.dist = math.sqrt(
        (self.point_list[-1][0]-cursor_pos[0])**2+(self.point_list[-1][1]-cursor_pos[1])**2)
    self.on_dir_indicator += (3 if self.point_list[0] == self.first_object.rect.center else -
                              3)if self.on_dir_indicator < self.line_lenght else -self.line_lenght


def conector_new_line(self, *args):
    self.point_list = filter_point_list(
        self.point_list+self.nofijo)
    self.line_lenght = sum(points_distance(
        self.point_list[i], self.point_list[i+1]) for i in range(len(self.point_list)-1))
    self.condition_point, self.condition_dir = marker_on_line(self,
                                                              self.line_lenght, self.point_list, round(self.line_lenght/2))
    self.rect.center = self.condition_point


def conector_line_render(self, screen=pygame.Surface):
    point_list = filter_point_list(self.point_list+self.nofijo)
    if self.state == 1 or (self.state == 0 and (self.first_object.state == 1 or self.last_object.state == 1)):
        pygame.draw.lines(screen, (255, 40, 40), 0,
                          point_list+[(point_list[-1])], 2)
    if not (self.state == 0 and (self.first_object.state == 1 or self.last_object.state == 1)):
        pygame.draw.lines(screen, self.color, 0,
                          self.point_list+[(self.point_list[-1])], 2)
    if self.on:
        for on_dir_ind in range(1 + int(self.line_lenght/100)):
            pos_marcador, dir = marker_on_line(self, self.line_lenght, self.point_list, (self.on_dir_indicator + (100 * on_dir_ind if (
                self.on_dir_indicator + 100 * on_dir_ind) <= self.line_lenght else -self.line_lenght+100 * on_dir_ind)))
            pygame.draw.rect(screen, (255, 0, 0),
                             (pos_marcador[0]-2, pos_marcador[1]-2, 6, 6))
