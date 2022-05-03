import copy
import math

import pygame, gui, main, sys, pugixor, os
from zipfile import ZipFile

theme = main.rreg.getObject("windows_sys")[0][1]
theme_rreg = pugixor.XorDocumentRead("gui/images/"+theme+"/settings.xor")
font = theme_rreg.getObject("font")[0][1]
sysfont = int(theme_rreg.getObject("font")[1][1])
antialias = int(theme_rreg.getObject("font")[2][1])
font_size = int(theme_rreg.getObject("font")[3][1])
font_color = theme_rreg.getObject("font")[4][1]
button_font_color = theme_rreg.getObject("font")[5][1]
link_font_color = theme_rreg.getObject("font")[6][1]
menu_font_color = theme_rreg.getObject("font")[7][1]
menu_font = theme_rreg.getObject("font")[8][1]
menu_sysfont = int(theme_rreg.getObject("font")[9][1])
menu_antialias = int(theme_rreg.getObject("font")[10][1])
start_font_color = theme_rreg.getObject("font")[11][1]
start_font = theme_rreg.getObject("font")[12][1]
start_sysfont = int(theme_rreg.getObject("font")[13][1])
start_antialias = int(theme_rreg.getObject("font")[14][1])
start_font_size = int(theme_rreg.getObject("font")[15][1])
start_text = theme_rreg.getObject("font")[16][1]
bg_color = theme_rreg.getObject("windows_sys")[0][1]

theme_man_func = """
theme_rreg = pugixor.XorDocumentRead("gui/images/"+"{theme}"+"/settings.xor")

try:
    atum_ver = theme_rreg.getObject("windows_sys")[2][1]
except:
    atum_ver = '?'

try:
    atum_ver_int = int(atum_ver)
except:
    try:
        atum_ver_int = float(''.join(atum_ver.split("Beta ")))/10
    except:
        atum_ver_int = None

if not atum_ver_int == None:
    if atum_ver_int >= main.version:
        print(main.rreg.text)
        self.userdata = '{theme}'
        main.theme_change = 1
        main.rreg.text[1] = 'theme={theme};'
        rreg_write = pugixor.XorDocumentWrite('rreg.xor')
        rreg_write.clear()
        for obj_name in main.rreg.getAllObjectNames():
            obj = main.rreg.getObject(obj_name)
            if obj_name == 'windows_sys' and obj[0][0] == 'theme':
                obj[0][1] = '{theme}'
            obj2 = []
            for str in obj:
                obj2.append('='.join(str))
            rreg_write.createObject(obj_name, obj2)
        rreg_write.close()"""

icon_man_func = """
print(main.rreg.text)
main.rreg.text[5] = 'user_pic=user/pics/{icon};'
rreg_write = pugixor.XorDocumentWrite('rreg.xor')
rreg_write.clear()
for obj_name in main.rreg.getAllObjectNames():
    obj = main.rreg.getObject(obj_name)
    if obj_name == 'user' and obj[0][0] == 'user_pic':
        obj[0][1] = '{icon}'
    obj2 = []
    for str in obj:
        obj2.append('='.join(str))
    rreg_write.createObject(obj_name, obj2)
rreg_write.close()"""

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, title, command):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.title_str = title
        self.command = command
        self.customtheme = 0
        self.hover = False
        self.alpha = 25
        self.collide_rect_y = 0

        self.load_theme(theme, font, sysfont, antialias, font_size, button_font_color)

    def load_theme(self, theme, font, sysfont, antialias, font_size, font_color):
        self.theme = theme
        self.font = font

        self.button_left_top = pygame.image.load("gui/images/"+self.theme+'/'+"button.png").subsurface((1, 0, 3, 3))
        self.button_center_top = pygame.transform.scale(pygame.image.load("gui/images/"+self.theme+'/'+"button.png").subsurface((4, 0, 5, 1)), (self.rect.w - 2, 2))
        self.button_right_top = pygame.image.load("gui/images/"+self.theme+'/'+"button.png").subsurface((23, 0, 3, 3))

        self.button_left_center = pygame.transform.scale(pygame.image.load("gui/images/"+self.theme+'/'+"button.png").subsurface((1, 3, 2, 21)), (3, self.rect.h))
        self.button_center_center = pygame.transform.scale(pygame.image.load("gui/images/"+self.theme+'/'+"button.png").subsurface((3, 3, 20, 20)), (self.rect.w - 2, self.rect.h - 4))
        self.button_right_center = pygame.transform.flip(self.button_left_center, 1, 0)

        self.button_left_bottom = pygame.transform.flip(self.button_left_top, 0, 1)
        self.button_center_bottom = pygame.transform.flip(self.button_center_top, 0, 1)
        self.button_right_bottom = pygame.transform.flip(self.button_right_top, 1, 1)

        self.button_left_top_hover = pygame.image.load("gui/images/"+self.theme+'/'+"button-active.png").subsurface((1, 0, 3, 3))
        self.button_center_top_hover = pygame.transform.scale(pygame.image.load("gui/images/"+self.theme+'/'+"button-active.png").subsurface((4, 0, 20, 1)), (self.rect.w - 2, 2))
        self.button_right_top_hover = pygame.image.load("gui/images/"+self.theme+'/'+"button-active.png").subsurface((23, 0, 3, 3))

        self.button_left_center_hover = pygame.transform.scale(pygame.image.load("gui/images/"+self.theme+'/'+"button-active.png").subsurface((1, 3, 2, 21)), (3, self.rect.h))
        self.button_center_center_hover = pygame.transform.scale(pygame.image.load("gui/images/"+self.theme+'/'+"button-active.png").subsurface((2, 3, 20, 20)), (self.rect.w - 2, self.rect.h - 4))
        self.button_right_center_hover = pygame.transform.flip(self.button_left_center_hover, 1, 0)

        self.button_left_bottom_hover = pygame.transform.flip(self.button_left_top_hover, 0, 1)
        self.button_center_bottom_hover = pygame.transform.flip(self.button_center_top_hover, 0, 1)
        self.button_right_bottom_hover = pygame.transform.flip(self.button_left_top_hover, 1, 1)

        if sysfont:
            self.title_font_rendered = pygame.font.SysFont(self.font, font_size, 0, 0)
        else:
            self.title_font_rendered = pygame.font.Font(self.font, font_size)

        try:
            font_color = pygame.color.Color(
                (int(font_color.split(',')[0]), int(font_color.split(',')[1]),
                 int(font_color.split(',')[2])))
        except:
            font_color = pygame.color.Color(font_color)

        self.title_txt = self.title_font_rendered.render(self.title_str, antialias, font_color)

    def draw_normal(self):
        self.image.blit(self.button_left_top, (0, 0))
        self.image.blit(self.button_center_top, (2, 0))
        self.image.blit(self.button_right_top, (self.rect.w - 2, 0))

        self.image.blit(self.button_left_center, (0, 2))
        self.image.blit(self.button_center_center, (2, 2))
        self.image.blit(self.button_right_center, (self.rect.w - 3, 2))

        self.image.blit(self.button_left_bottom, (0, self.rect.h - 2))
        self.image.blit(self.button_center_bottom, (2, self.rect.h - 2))
        self.image.blit(self.button_right_bottom, (self.rect.w - 2, self.rect.h - 2))

    def draw_hover(self):
        self.image.blit(self.button_left_top_hover, (0, 0))
        self.image.blit(self.button_center_top_hover, (2, 0))
        self.image.blit(self.button_right_top_hover, (self.rect.w - 2, 0))

        self.image.blit(self.button_left_center_hover, (0, 2))
        self.image.blit(self.button_center_center_hover, (2, 2))
        self.image.blit(self.button_right_center_hover, (self.rect.w - 3, 2))

        self.image.blit(self.button_left_bottom_hover, (0, self.rect.h - 2))
        self.image.blit(self.button_center_bottom_hover, (2, self.rect.h - 2))
        self.image.blit(self.button_right_bottom_hover, (self.rect.w - 2, self.rect.h - 2))

    def customize_check(self):
        if main.theme_change:
            if self.customtheme == 0:
                theme = main.rreg.getObject("windows_sys")[0][1]
                theme_rreg = pugixor.XorDocumentRead("gui/images/" + theme + "/settings.xor")
                font = theme_rreg.getObject("font")[0][1]
                sysfont = int(theme_rreg.getObject("font")[1][1])
                antialias = int(theme_rreg.getObject("font")[2][1])
                font_size = int(theme_rreg.getObject("font")[3][1])
                button_font_color = theme_rreg.getObject("font")[5][1]
                self.load_theme(theme, font, sysfont, antialias, font_size, button_font_color)

    def update(self, x, y, window):
        global theme, font, sysfont, antialias, font_size
        self.customize_check()

        self.image.fill((0, 0, 0, 0))
        self.image.set_alpha((self.alpha))

        self.collide_rect = self.image.get_rect(topleft=(x, y+self.collide_rect_y))
        if self.collide_rect.w > window.rect.w:
            self.collide_rect.w = window.rect.w - self.x
        if self.collide_rect.w + self.x > window.rect.w:
            self.collide_rect.w = self.collide_rect.w + (window.rect.w - (self.collide_rect.w + self.x))
        if self.collide_rect.x < 0:
            self.collide_rect.x = window.rect.x
            self.collide_rect.w += self.x

        if not self.collide_rect.collidepoint(pygame.mouse.get_pos()):
            self.draw_normal()
            self.hover = False
        else:
            self.draw_hover()
            self.hover = True
            if main.mouse_pressed:
                exec(self.command)

        self.image.blit(self.title_txt, self.title_txt.get_rect(center=(self.rect.w/2, self.rect.h/2)))

    def draw(self, window):
        self.update(self.x+window.rect.x, self.y+window.rect.y+30, window)
        window.display.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(main.sc, (255, 255, 0), (self.x+window.rect.x, self.y+window.rect.y+30, self.rect.w, self.rect.h), 5)

class ImageButton(Button):
    def __init__(self, x, y, command, image, image_hover):
        Button.__init__(self, x, y, 5, 5, '', command)
        self.load_image(image, image_hover)
        self.image = pygame.Surface((self.image_normal.get_width(), self.image_normal.get_height()), pygame.SRCALPHA)
        # self.customtheme = 1

    def load_image(self, image, image_hover):
        self.image_normal = pygame.image.load(image)
        self.image_hover = pygame.image.load(image_hover)

    def draw_normal(self):
        self.image.blit(self.image_normal, (0, 0))

    def draw_hover(self):
        self.image.blit(self.image_hover, (0, 0))

class DrgableY(Button):
    def __init__(self, x, y, w, h, slide_min, slide_max):
        Button.__init__(self, x, y, w, h, '', '')
        self.mouse_count = 0
        self.mouse_can = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.slide_min = slide_min
        self.slide_max = slide_max

        self.moving = 0

    def update(self, x, y, window):
        global theme, font, sysfont, antialias, font_size
        self.customize_check()

        self.collide_rect = self.image.get_rect(topleft=(x, y))
        mouse_pressed = pygame.mouse.get_pressed()

        if not self.collide_rect.collidepoint(pygame.mouse.get_pos()):
            self.draw_normal()
            self.hover = False
        else:
            self.draw_hover()
            self.hover = True
            if mouse_pressed[0] and self.mouse_count == 0:
                movings = 0
                for window in main.windows.spritedict:
                    if window.mouse_can and window.close == 0:
                        movings += 1
                if movings == 0:
                    self.mouse_count += 1
                    self.mouse_can = 1
                    self.mouse_x = pygame.mouse.get_pos()[0] - self.x
                    self.mouse_y = pygame.mouse.get_pos()[1] - self.y
                    self.moving = 1

        if not mouse_pressed[0]:
            self.mouse_count = 0
            self.mouse_can = 0
            self.moving = 0

        if mouse_pressed[0] and self.mouse_count == 1 and self.mouse_can:
            if self.y <= self.slide_min:
                self.collide_rect.y += 5
                self.y += 5
                self.mouse_can = 0
                self.moving = 0
            elif self.y+self.rect.h >= self.slide_max:
                self.collide_rect.y -= 5
                self.y -= 5
                self.mouse_can = 0
                self.moving = 0
            else:
                self.y = pygame.mouse.get_pos()[1] - self.mouse_y
                self.moving = 1

class Link(pygame.sprite.Sprite):
    def __init__(self, x, y, title, command, image, _font_size=font_size):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.load_image(image)
        self.title_str = title
        self.command = command
        self.customtheme = 0

        self.load_theme(theme, font, sysfont, antialias, _font_size, link_font_color)
        self.title_rect = self.title_txt.get_rect(center=(self.rect.x+self.rect.w/2, self.rect.y+self.rect.h-27-(font_size-_font_size)))

    def load_theme(self, theme, font, sysfont, antialias, font_size, font_color):
        self.theme = theme
        self.font = font
        self.font_size = font_size

        if sysfont:
            self.title_font_rendered = pygame.font.SysFont(self.font, font_size, 0, 0)
        else:
            self.title_font_rendered = pygame.font.Font(self.font, font_size)

        try:
            font_color = pygame.color.Color(
                (int(font_color.split(',')[0]), int(font_color.split(',')[1]),
                 int(font_color.split(',')[2])))
        except:
            font_color = pygame.color.Color(font_color)

        if not font_size == gui.font_size:
            self.customtheme = 1

        self.title_txt = self.title_font_rendered.render(self.title_str, antialias, font_color)
        self.title_lines = []
        self.title_lines_rects = []
        self.title_id = 0
        for line in self.title_str.split('\n'):
            self.title_lines.append(self.title_font_rendered.render(line, antialias, font_color))
            self.title_lines_rects.append(self.title_lines[self.title_id].get_rect(center=(self.rect.x+self.rect.w/2, self.rect.y+self.rect.h-27-(gui.font_size-self.font_size)+self.title_id*self.font_size+40)))
            self.title_id += 1

    def load_image(self, image):
        self.image_codename = image
        icons = main.rreg.getObject("icons")
        theme = pugixor.XorDocumentRead("rreg.xor").getObject("windows_sys")[0][1]
        for icon in icons:
            if icon[0] == self.image_codename:
                try:
                    self.image_normal = pygame.image.load("gui/images/"+theme+"/icons/"+icon[1]+".png")
                    self.image_hover = pygame.image.load("gui/images/"+theme+"/icons/"+icon[1]+"_hover.png")
                except:
                    self.image_normal = pygame.image.load("gui/icons/"+icon[1]+".png")
                    self.image_hover = pygame.image.load("gui/icons/"+icon[1]+"_hover.png")

        self.image = pygame.Surface((self.image_normal.get_width(), self.image_normal.get_height()+40), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect.h -= 40

    def draw_normal(self):
        self.image.blit(self.image_normal, (0, 0))

    def draw_hover(self):
        self.image.blit(self.image_hover, (0, 0))

    def draw_any(self, sc):
        for x in range(0, len(self.title_lines)):
            txt = self.title_lines[x]
            sc.blit(txt, self.title_lines_rects[x])

    def update(self, sc):
        global link_font_color
        if main.theme_change:
            theme = main.rreg.getObject("windows_sys")[0][1]
            theme_rreg = pugixor.XorDocumentRead("gui/images/" + theme + "/settings.xor")
            link_font_color = theme_rreg.getObject("font")[6][1]
            self.load_image(self.image_codename)
            if self.customtheme:
                self.load_theme(theme, font, sysfont, antialias, self.font_size, link_font_color)
            else:
                self.load_theme(theme, font, sysfont, antialias, font_size, link_font_color)

        self.image.fill((0, 0, 0, 0))
        mouse = pygame.mouse.get_pos()
        if not self.rect.collidepoint(mouse):
            self.draw_normal()
        else:
            self.draw_hover()
            if main.mouse_pressed:
                exec(self.command)

        self.draw_any(sc)

        sc.blit(self.image, self.rect)

class Window(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, title="Window"):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

        self.image = pygame.Surface((w, h+30), pygame.SRCALPHA)
        self.display = pygame.Surface((w, h), pygame.SRCALPHA)
        self.title = pygame.Surface((w, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.fill_rect = self.image.get_rect(topleft=(0, 30))
        self.fill_rect.height -= 30
        self.close = False

        self.close_button = 1
        self.title_moving = 1
        self.title_bar_life = 1

        self.title_rect = self.title.get_rect(topleft=(x, y))
        self.title_str = title

        gui.theme = main.rreg.getObject("windows_sys")[0][1]
        gui.theme_rreg = pugixor.XorDocumentRead("gui/images/" + theme + "/settings.xor")
        gui.font = theme_rreg.getObject("font")[0][1]
        gui.sysfont = int(theme_rreg.getObject("font")[1][1])
        gui.antialias = int(theme_rreg.getObject("font")[2][1])
        gui.font_size = int(theme_rreg.getObject("font")[3][1])
        gui.bg_color = theme_rreg.getObject("windows_sys")[0][1]
        gui.font_color = theme_rreg.getObject("font")[4][1]
        self.load_theme(gui.theme, gui.font, gui.sysfont, gui.antialias, gui.font_size, gui.bg_color, gui.font_color)
        self.customtheme = 0

        self.close_rect = self.close_normal.get_rect(topleft=(x+self.rect.w-32, y-1))
        self.close_blit_rect = self.close_normal.get_rect(topleft=(self.rect.w - 32, -1))

        self.mouse_count = 0
        self.mouse_can = 0
        self.mouse_x = 0
        self.mouse_y = 0

    def load_theme(self, theme, font, sysfont, antialias, font_size, bg_color, font_color):
        self.theme = theme
        self.font = font
        try:
            self.bg_color = pygame.color.Color((int(bg_color.split(',')[0]), int(bg_color.split(',')[1]), int(bg_color.split(',')[2])))
        except:
            self.bg_color = pygame.color.Color(bg_color)

        try:
            font_color = pygame.color.Color(
                (int(font_color.split(',')[0]), int(font_color.split(',')[1]),
                 int(font_color.split(',')[2])))
        except:
            font_color = pygame.color.Color(font_color)

        self.title_left = pygame.image.load("gui/images/"+self.theme+'/'+"title_left.png")
        self.title_center = pygame.transform.scale(pygame.image.load("gui/images/"+self.theme+'/'+"title_center.png"), (self.rect.w-30*2, 30))
        #self.title_right = pygame.image.load("gui/images/"+self.theme+'/'+"title_right.png")
        self.title_right = pygame.transform.flip(self.title_left, 1, 0)
        if sysfont:
            self.title_font_rendered = pygame.font.SysFont(self.font, font_size, 0, 0)
        else:
            self.title_font_rendered = pygame.font.Font(self.font, font_size)

        self.title_txt = self.title_font_rendered.render(self.title_str, antialias, font_color)
        self.close_normal = pygame.image.load("gui/images/"+theme+'/'+"titlebutton-close@2.png")
        self.close_hover = pygame.image.load("gui/images/"+theme+'/'+"titlebutton-close-hover@2.png")

    def title_update(self):
        mouse_pressed = pygame.mouse.get_pressed()

        self.title.fill((0, 0, 0, 0))
        self.title.set_alpha(25)
        self.title.blit(self.title_left, (0, 0))
        self.title.blit(self.title_center, (30, 0))
        self.title.blit(self.title_right, (self.rect.w-30, 0))
        self.title.blit(self.title_txt, (5, 5))

        if self.close_button:
            if self.close_rect.collidepoint(pygame.mouse.get_pos()):
                self.title.blit(self.close_hover, self.close_blit_rect)
                if main.mouse_pressed:
                    self.mouse_can = 0
                    self.close = 1
            else:
                self.title.blit(self.close_normal, self.close_blit_rect)

        if self.title_rect.collidepoint(pygame.mouse.get_pos()):
            if mouse_pressed[0] and self.mouse_count == 0 and self.title_moving:
                movings = 0
                for window in main.windows.spritedict:
                    if window.mouse_can and window.close == 0:
                        movings += 1
                if movings == 0:
                    self.mouse_count += 1
                    self.mouse_can = 1
                    self.mouse_x = pygame.mouse.get_pos()[0] - self.x
                    self.mouse_y = pygame.mouse.get_pos()[1] - self.y

        if not mouse_pressed[0]:
            self.mouse_count = 0
            self.mouse_can = 0

        if mouse_pressed[0] and self.mouse_count == 1 and self.mouse_can and self.title_moving:
            self.x = pygame.mouse.get_pos()[0] - self.mouse_x
            self.y = pygame.mouse.get_pos()[1] - self.mouse_y

            self.title_rect = self.title.get_rect(topleft=(self.x, self.y))
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
            if self.close_button:
                self.close_rect = self.close_normal.get_rect(topleft=(self.x+self.rect.w - 32, self.y-1))

    def logic(self):
        pass

    def update(self):
        global theme, theme_rreg, font, sysfont, antialias, font_size, bg_color, button_font_color, link_font_color, menu_font, menu_sysfont, menu_antialias, menu_font_color
        if main.theme_change:
            if self.customtheme == 0:
                theme = main.rreg.getObject("windows_sys")[0][1]
                theme_rreg = pugixor.XorDocumentRead("gui/images/" + theme + "/settings.xor")
                font = theme_rreg.getObject("font")[0][1]
                sysfont = int(theme_rreg.getObject("font")[1][1])
                antialias = int(theme_rreg.getObject("font")[2][1])
                font_size = int(theme_rreg.getObject("font")[3][1])
                bg_color = theme_rreg.getObject("windows_sys")[0][1]
                font_color = theme_rreg.getObject("font")[4][1]
                button_font_color = theme_rreg.getObject("font")[5][1]
                link_font_color = theme_rreg.getObject("font")[6][1]
                menu_font = theme_rreg.getObject("font")[8][1]
                menu_sysfont = int(theme_rreg.getObject("font")[9][1])
                menu_antialias = int(theme_rreg.getObject("font")[10][1])
                menu_font_color = theme_rreg.getObject("font")[7][1]
                self.load_theme(theme, font, sysfont, antialias, font_size, bg_color, font_color)

        self.image.fill(self.bg_color, self.fill_rect)
        if self.title_bar_life:
            self.title_update()
            self.image.blit(self.title, (0, 0))
        self.image.fill(self.bg_color, self.fill_rect)
        self.logic()
        if self.title_bar_life:
            self.image.blit(self.display, (0, 30))
        else:
            self.image.blit(self.display, (0, 0))

class StartMenu(Window):
    def __init__(self):
        Window.__init__(self, 0, main.SCREEN_HEIGHT-430-30, 350, 430, '')
        self.close_button = 0
        self.title_moving = 0
        self.title_bar_life = 0
        self.rama_radius = 4
        self.start_y = 70
        self.button_start_y = 72
        self.buttons = []
        self.buttons.append(Button(5, self.button_start_y, self.rect.w-5*2-2, 30, "Менеджер Програм Modern", "main.windows.add(ProgramManModern(100, 100))"))
        self.load_res(theme, menu_font, menu_sysfont, menu_antialias, menu_font_color)

        for btn in self.buttons:
            btn.alpha = 255
            btn.collide_rect_y = -30

    def load_res(self, theme, font, sysfont, antialias, font_color):
        self.title_img = pygame.image.load("gui/images/"+theme+'/'+"menu-bg.png")

        self.title2_left = self.title_img.subsurface((0, 0, 105, 70))
        self.title2_center = pygame.transform.scale(self.title_img.subsurface((106, 0, 1, 70)), (self.rect.w-116, 70))
        self.title2_right = self.title_img.subsurface((self.title_img.get_width()-13, 0, 13, 70))

        self.title3_left = pygame.transform.scale(self.title_img.subsurface(
            (0, 70, 105, self.title_img.get_height()-71)),
            (105, self.rect.h-30-70))
        self.title3_center = pygame.transform.scale(
            self.title_img.subsurface((106, 70, 1, self.title_img.get_height()-71)),
            (self.rect.w - 116, self.rect.h-30-70))
        self.title3_right = pygame.transform.scale(self.title_img.subsurface(
            ((self.title_img.get_width()-13, 70, 13, self.title_img.get_height()-71))),
            (13, self.rect.h-30-70))

        self.user_pic = pygame.transform.scale(pygame.image.load(main.rreg.getObject("user")[1][1]), (48, 48))

        try:
            font_color = pygame.color.Color(
                (int(font_color.split(',')[0]), int(font_color.split(',')[1]),
                 int(font_color.split(',')[2])))
        except:
            font_color = pygame.color.Color(font_color)

        if sysfont:
            self.title_font_rendered = pygame.font.SysFont(font, 24, 0, 0)
        else:
            self.title_font_rendered = pygame.font.Font(font, 24)

        self.user_name = self.title_font_rendered.render(main.rreg.getObject("user")[0][1], antialias, font_color)

    def logic(self):
        global theme, menu_font, menu_sysfont, menu_antialias, menu_font_color
        self.image.fill((0, 0, 0, 0))
        self.display.blit(self.title2_left, (0, 0))
        self.display.blit(self.title2_center, (105, 0))
        self.display.blit(self.title2_right, (self.rect.w-14, 0))

        self.display.blit(self.title3_left, (0, self.start_y))
        self.display.blit(self.title3_center, (105, self.start_y))
        self.display.blit(self.title3_right, (self.rect.w-14, self.start_y))

        pygame.draw.rect(self.display, (255, 255, 255), (7, 7, 52, 52), self.rama_radius, self.rama_radius, self.rama_radius, self.rama_radius)
        self.display.blit(self.user_pic, (9, 9))
        self.display.blit(self.user_name, (67, 20))

        pygame.draw.rect(self.display, (255, 255, 255), (2, self.button_start_y-3, self.rect.w-5, self.display.get_height()-self.button_start_y-3-40-2))
        for btn in self.buttons:
            btn.draw(self)

        if main.mouse_pressed:
            if not self.rect.collidepoint(pygame.mouse.get_pos()):
                self.close = 1

        if main.theme_change:
            theme = main.rreg.getObject("windows_sys")[0][1]
            theme_rreg = pugixor.XorDocumentRead("gui/images/" + theme + "/settings.xor")
            menu_font = theme_rreg.getObject("font")[8][1]
            menu_sysfont = int(theme_rreg.getObject("font")[9][1])
            menu_antialias = int(theme_rreg.getObject("font")[10][1])
            menu_font_color = theme_rreg.getObject("font")[7][1]
            self.load_res(theme, menu_font, menu_sysfont, menu_antialias, menu_font_color)

class Panel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_res()

    def load_res(self):
        self.image = pygame.Surface((main.SCREEN_WIDTH, 30))
        self.panel = pygame.transform.scale(pygame.image.load("gui/images/"+theme+"/panel.png"), (main.SCREEN_WIDTH, 30))
        self.rect = self.panel.get_rect(topleft=(0, main.SCREEN_HEIGHT-30))
        self.zero_rect = self.panel.get_rect()

        self.btn_normal = pygame.image.load("gui/images/"+theme+"/start-button.png")
        self.btn_hover = pygame.image.load("gui/images/"+theme+"/start-button-hover.png")
        self.btn_image = pygame.image.load("gui/images/"+theme+"/menu.png")
        self.btn_image_rect = self.btn_image.get_rect(midleft=(4, 30/2))
        self.btn_rect = self.btn_normal.get_rect(topleft=(0, main.SCREEN_HEIGHT - 30))

        self.theme = theme
        self.font = start_font

        try:
            start_font_color = pygame.color.Color(
                (int(gui.start_font_color.split(',')[0]), int(gui.start_font_color.split(',')[1]),
                 int(gui.start_font_color.split(',')[2])))
        except:
            start_font_color = pygame.color.Color(gui.start_font_color)

        if sysfont:
            self.title_font_rendered = pygame.font.SysFont(self.font, start_font_size, 0, 0)
        else:
            self.title_font_rendered = pygame.font.Font(self.font, start_font_size)

        self.title_txt = self.title_font_rendered.render(start_text, start_antialias, start_font_color)
        self.title_txt_rect = self.title_txt.get_rect(midleft=(self.btn_image_rect.bottomright[0]+3, 30/2))

    def update(self):
        global start_font_color, start_font, start_sysfont, start_antialias, start_font_size, start_text
        if main.theme_change:
            start_font_color = theme_rreg.getObject("font")[11][1]
            start_font = theme_rreg.getObject("font")[12][1]
            start_sysfont = int(theme_rreg.getObject("font")[13][1])
            start_antialias = int(theme_rreg.getObject("font")[14][1])
            start_font_size = int(theme_rreg.getObject("font")[15][1])
            start_text = theme_rreg.getObject("font")[16][1]
            self.load_res()

        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.panel, self.zero_rect)
        if not self.btn_rect.collidepoint(pygame.mouse.get_pos()):
            self.image.blit(self.btn_normal, self.zero_rect)
        else:
            self.image.blit(self.btn_hover, self.zero_rect)
            if main.mouse_pressed:
                main.windows.add(StartMenu())

        self.image.blit(self.btn_image, self.btn_image_rect)
        self.image.blit(self.title_txt, self.title_txt_rect)

class Package(Window):
    def __init__(self, title, title2, file):
        Window.__init__(self, 150, 150, 150, 150-30, title)
        self.image_codename = "exe"
        try:
            self.image_normal = pygame.image.load(title2)

            self.icon_image = pygame.Surface((self.image_normal.get_width(), self.image_normal.get_height()),
                                             pygame.SRCALPHA)
            self.icon_rect = self.icon_image.get_rect(topleft=(10, 10))
        except:
            self.load_image()

        self.button = Button(10, self.rect.h-30-30-10, self.rect.w-10*2, 30, "Відкрити", "exec(open('"+file+"', encoding='UTF-8').read())")

    def load_image(self):
        icons = main.rreg.getObject("icons")
        theme = pugixor.XorDocumentRead("rreg.xor").getObject("windows_sys")[0][1]
        for icon in icons:
            if icon[0] == self.image_codename:
                try:
                    self.image_normal = pygame.image.load("gui/images/" + theme + "/icons/" + icon[1] + ".png")
                    self.image_hover = pygame.image.load("gui/images/" + theme + "/icons/" + icon[1] + "_hover.png")
                except:
                    self.image_normal = pygame.image.load("gui/icons/" + icon[1] + ".png")
                    self.image_hover = pygame.image.load("gui/icons/" + icon[1] + "_hover.png")

        self.icon_image = pygame.Surface((self.image_normal.get_width(), self.image_normal.get_height()),
                                    pygame.SRCALPHA)
        self.icon_rect = self.icon_image.get_rect(topleft=(10, 10))

    def logic(self):
        self.display.fill(self.bg_color)
        self.display.blit(self.image_normal, self.icon_rect)

        self.button.alpha = 255
        self.button.draw(self)

        if main.theme_change:
            self.load_image()

class PackageAutoTheme(Window):
    def __init__(self, title, title2, theme):
        Window.__init__(self, 150, 150, 150, 150-30, title)
        self.image_codename = "exe"
        try:
            self.image_normal = pygame.image.load(title2)

            self.icon_image = pygame.Surface((self.image_normal.get_width(), self.image_normal.get_height()),
                                             pygame.SRCALPHA)
            self.icon_rect = self.icon_image.get_rect(topleft=(10, 10))
        except:
            self.load_image()

        self.button = Button(10, self.rect.h-30-30-10, self.rect.w-10*2, 30, "Встановити", theme_man_func.format(theme=theme))

    def load_image(self):
        icons = main.rreg.getObject("icons")
        theme = pugixor.XorDocumentRead("rreg.xor").getObject("windows_sys")[0][1]
        for icon in icons:
            if icon[0] == self.image_codename:
                try:
                    self.image_normal = pygame.image.load("gui/images/" + theme + "/icons/" + icon[1] + ".png")
                    self.image_hover = pygame.image.load("gui/images/" + theme + "/icons/" + icon[1] + "_hover.png")
                except:
                    self.image_normal = pygame.image.load("gui/icons/" + icon[1] + ".png")
                    self.image_hover = pygame.image.load("gui/icons/" + icon[1] + "_hover.png")

        self.icon_image = pygame.Surface((self.image_normal.get_width(), self.image_normal.get_height()),
                                    pygame.SRCALPHA)
        self.icon_rect = self.icon_image.get_rect(topleft=(10, 10))

    def logic(self):
        self.display.fill(self.bg_color)
        self.display.blit(self.image_normal, self.icon_rect)

        self.button.alpha = 255
        self.button.draw(self)

        if main.theme_change:
            self.load_image()

class Base(Window):
    def __init__(self, x, y, theme="Mint-Y-Aqua"):
        gui.Window.__init__(self, x, y, 450, 300, ":)")
        self.load_theme(theme, font, sysfont, antialias, font_size, (255, 255, 150), font_color)
        self.customtheme = 1
        # self.bg_color = (166, 255, 108)
        self.button = Button(30, 30, 100, 30, "Вийти", "window.close = 1")
        self.button.load_theme("Mint-Y", font, 0, 1, 19, (0, 0, 0))
        self.button.customtheme = 1

    def logic(self):
        self.button.draw(self)

class ThemeMan(Window):
    def __init__(self, x, y):
        gui.Window.__init__(self, x, y, 450, 290, "Менеджер Тем")
        # # self.bg_color = (166, 255, 108)
        # self.bg_color = (255, 255, 150)
        self.buttons = []
        self.themes = os.listdir("gui/images")
        y = 0
        x = 0
        for count in range(0, len(self.themes)):
            theme = self.themes[x+y*4]
            func = theme_man_func.format(theme=theme)
            self.buttons.append(Button(10+x*110, 10+y*40, 100, 30, theme, func))
            x += 1
            if x == 4:
                x = 0
                y += 1

    def logic(self):
        for button in self.buttons:
            button.draw(self)

class ThemeManModern(Window):
    def __init__(self, x, y):
        gui.Window.__init__(self, x, y, 450, 290, "Менеджер Тем Modern")
        self.buttons = []
        self.themes = os.listdir("gui/images")

        self.thumbnail_theme = gui.theme
        self.thumbnail_x = 0
        self.thumbnail_y = 12
        self.thumbnail_w = 154
        self.thumbnail_h = 60
        self.thumbnail_stroke = 2
        #self.thumbnail_stroke_color = (255, 255, 255)
        self.thumbnail_stroke_color = (0, 0, 0)

        self.thumbnail_pic = pygame.Surface((self.thumbnail_w, self.thumbnail_h))

        self.margin = 2
        self.margin2 = 2
        self.button_slide = 0
        self.button_slide_max = 9

        self.slider = DrgableY(self.rect.w-self.margin-17+self.margin/2, 4, 16, (self.rect.h-self.thumbnail_h-43)-(len(self.themes)-self.button_slide_max)*30-10, 3, self.rect.h-self.thumbnail_h-43)
        self.slide = (self.slider.y+self.slider.rect.h-self.rect.y-5*1.5)-28

        self.timer = 0
        self.alpha = 25

        for x in range(0, len(self.themes)):
            theme = self.themes[x]
            theme_rreg = pugixor.XorDocumentRead("gui/images/"+theme+"/settings.xor")
            try:
                theme_name = theme_rreg.getObject("windows_sys")[1][1]
            except:
                theme_name = theme

            func = theme_man_func.format(theme=theme)
            self.buttons.append(Button(self.margin2, self.margin2+x*(30+self.margin2), ((self.rect.w-self.margin*2-17-self.margin2*2)-abs(25+self.margin*2))/3*2, 30, theme_name, func))
            self.buttons[-1].userdata = theme

        self.render(self.thumbnail_theme)

    def render(self, theme):
        self.thumbnail_pic.fill((0, 0, 0, 0))
        self.thumbnail_pic.set_alpha(self.alpha)
        self.thumbnail_pic.fill(main.BG_COLOR)

        self.thumbnail_title_right = pygame.transform.flip(pygame.image.load("gui/images/"+theme+'/'+"title_left.png"), 1, 0)
        self.thumbnail_title_center = pygame.transform.scale(pygame.image.load("gui/images/"+theme+'/'+"title_center.png"), (self.thumbnail_w-28+self.thumbnail_stroke, 30))
        self.thumbnail_title_close = pygame.image.load("gui/images/"+theme+'/'+"titlebutton-close@2.png")

        theme_rreg = pugixor.XorDocumentRead("gui/images/" + theme + "/settings.xor")
        bg_color = theme_rreg.getObject("windows_sys")[0][1]

        font = theme_rreg.getObject("font")[0][1]
        sysfont = int(theme_rreg.getObject("font")[1][1])
        antialias = int(theme_rreg.getObject("font")[2][1])
        font_size = int(theme_rreg.getObject("font")[3][1])
        font_color = theme_rreg.getObject("font")[4][1]
        try:
            atum_ver = theme_rreg.getObject("windows_sys")[2][1]
        except:
            atum_ver = '?'

        try:
            atum_ver_int = int(atum_ver)
        except:
            try:
                atum_ver_int = float(''.join(atum_ver.split('Beta ')))/10
            except:
                atum_ver_int = None

        try:
            font_color = pygame.color.Color(
                (int(font_color.split(',')[0]), int(font_color.split(',')[1]),
                 int(font_color.split(',')[2])))
        except:
            font_color = pygame.color.Color(font_color)

        try:
            font_color2 = pygame.color.Color(
                (int(gui.button_font_color.split(',')[0]), int(gui.button_font_color.split(',')[1]),
                 int(gui.button_font_color.split(',')[2])))
        except:
            font_color2 = pygame.color.Color(gui.button_font_color)

        try:
            self.thumbnail_bg_color = pygame.color.Color((int(bg_color.split(',')[0]), int(bg_color.split(',')[1]), int(bg_color.split(',')[2])))
        except:
            self.thumbnail_bg_color = pygame.color.Color(bg_color)

        if sysfont:
            self.thumbnail_title_font_rendered = pygame.font.SysFont(font, font_size, 0, 0)
        else:
            self.thumbnail_title_font_rendered = pygame.font.Font(font, font_size)

        self.thumbnail_title_txt = self.thumbnail_title_font_rendered.render("Test Тест ії ІЇ", antialias, font_color)
        self.options_txts = []
        font_name = font.split('/')[-1]
        font_name = '.'.join(font_name.split('.')[:-1])
        text = "Кодове Ім'я:\n{code_name}\n\nВерсія Atum:\n{atum_ver}".format(code_name=theme, atum_ver=atum_ver)
        for txt in text.split('\n'):
            self.options_txts.append(self.title_font_rendered.render(txt, gui.antialias, font_color2))

        pygame.draw.rect(self.thumbnail_pic, self.thumbnail_bg_color, (0, self.thumbnail_y+30-self.thumbnail_x, self.thumbnail_w-self.thumbnail_x, self.thumbnail_h))
        self.thumbnail_pic.blit(self.thumbnail_title_center, (self.thumbnail_w-30-self.thumbnail_title_center.get_width()-self.thumbnail_x, self.thumbnail_y))
        self.thumbnail_pic.blit(self.thumbnail_title_right, (self.thumbnail_w-30-self.thumbnail_x, self.thumbnail_y))
        self.thumbnail_pic.blit(self.thumbnail_title_close, (self.thumbnail_w-32-self.thumbnail_x, self.thumbnail_y-1))
        self.thumbnail_pic.blit(self.thumbnail_title_txt, (5, self.thumbnail_y+5))

    def logic(self):
        formula = len(self.themes)-8

        if self.slider.moving:
            pygame.draw.rect(self.display, self.bg_color, self.display.get_rect(topleft=(0, 0)))
            self.render(self.thumbnail_theme)

        for button in self.buttons[self.button_slide:self.button_slide_max+self.button_slide]:
            btn = copy.copy(button)
            btn.y -= self.slide-20+(self.button_slide_max-6)*30-10-(30*((2*(self.button_slide_max-6))-formula))
            if self.slider.moving:
                self.alpha = 255
            else:
                self.alpha = 25

            btn.alpha = self.alpha
            btn.draw(self)
            if btn.hover:
                self.thumbnail_theme = btn.userdata
                self.render(self.thumbnail_theme)

        for button in self.buttons:
            button.customize_check()

        pygame.draw.rect(self.display, self.bg_color, (self.rect.w - self.thumbnail_w - self.thumbnail_stroke - 25, 10+self.thumbnail_h, self.rect.w, self.rect.h))
        pygame.draw.rect(self.display, self.thumbnail_stroke_color, (self.rect.w - self.thumbnail_w - self.thumbnail_stroke - 25,
                                                     10,
                                                     self.thumbnail_w + self.thumbnail_stroke * 2,
                                                     self.thumbnail_h + self.thumbnail_stroke),
                         self.thumbnail_stroke)

        pygame.draw.rect(self.display, (55, 55, 55), (self.display.get_width()-25+self.margin*2.5, 0, 25+self.margin*2, self.display.get_height()-self.thumbnail_h-10))
        self.slider.draw(self)

        self.slide = self.slider.y-self.y+self.y+self.slider.rect.h-21-100
        self.button_slide = math.floor(self.slide/30)-(self.button_slide_max-(5+formula))

        self.display.blit(self.thumbnail_pic, (self.rect.w-self.thumbnail_w - 25, 10))

        id = 0
        for txt in self.options_txts:
            self.display.blit(txt, (self.rect.w-self.thumbnail_w - 25, (10*2 + self.thumbnail_h) + gui.font_size*id))
            id += 1

        if main.theme_change:
            self.timer += 1
        if self.timer == 25:
            self.timer = 0
            pygame.draw.rect(self.display, self.bg_color, self.display.get_rect(topleft=(0, 0)))
        if self.timer > 0:
            self.timer += 1

class ProgramMan(Window):
    def __init__(self, x, y):
        gui.Window.__init__(self, x, y, 450, 290, "Менеджер Програм")
        self.buttons = []
        self.apps = []

        self.margin = 2
        self.margin2 = 2
        self.button_slide = 0
        self.button_slide_max = 9

        self.alpha = 255
        self.timer = 0

        for app in os.listdir("apps"):
            result = []
            result.append(open("apps/" + app, encoding="UTF-8").read().split('\n')[0][3:-3])
            result.append("apps/" + app)
            self.apps.append(result)

        self.slider = DrgableY(self.rect.w-self.margin-17+self.margin/2, 4, 16, (self.rect.h-43)-(len(self.apps)-self.button_slide_max)*30, -1, self.rect.h-43)
        self.slide = (self.slider.y+self.slider.rect.h-self.rect.y-5*1.5)-28

        for y in range(0, len(self.apps)):
            app = self.apps[y]
            func = """exec(open('''{app}''', encoding="UTF-8").read())""".format(app=app[1])
            self.buttons.append(Button(self.margin, self.margin2+y*(30+self.margin2), self.rect.w-self.margin*2-17-2*2, 30, app[0], func))

    def logic(self):
        if self.slider.moving:
            pygame.draw.rect(self.display, self.bg_color, self.display.get_rect(topleft=(0, 0)))

        for button in self.buttons[self.button_slide:self.button_slide_max+self.button_slide]:
            btn = copy.copy(button)
            btn.y -= self.slide - 20 + (len(self.apps) - 6) * 30-10-(30*2)
            if self.slider.moving:
                self.alpha = 255
            else:
                self.alpha = 25

            btn.alpha = self.alpha
            btn.draw(self)

        for button in self.buttons:
            button.customize_check()

        pygame.draw.rect(self.display, (55, 55, 55), (self.display.get_width()-25+self.margin*2.5, 0, 25+self.margin*2, self.display.get_height()))
        self.slider.draw(self)

        self.slide = self.slider.y-self.y+abs(100-self.y)+self.slider.rect.h-21
        self.button_slide = math.floor(self.slide/30)-(self.button_slide_max-5)

        if main.theme_change:
            self.timer += 1
        if self.timer == 25:
            self.timer = 0
            pygame.draw.rect(self.display, self.bg_color, self.display.get_rect(topleft=(0, 0)))
        if self.timer > 0:
            self.timer += 1

class ProgramManModern(Window):
    def __init__(self, x, y):
        gui.Window.__init__(self, x, y, 450, 290, "Менеджер Програм Modern")
        self.buttons = []
        self.themes = []
        for app in os.listdir("apps"):
            if os.path.isfile("apps/" + app) and app.split('.')[-1] == "py":
                result = []
                result.append(open("apps/" + app, encoding="UTF-8").read().split('\n')[0][3:-3])
                result.append("""exec(open("apps/{app}", encoding="UTF-8").read())""".format(app=app))
                self.themes.append(result)
            elif os.path.isfile("apps/" + app) and app.split('.')[-1] == "xor":
                pkg_rreg = pugixor.XorDocumentRead("apps/" + app)
                pkg_name = pkg_rreg.getObject("params")[0][1]
                pkg_file = pkg_rreg.getObject("params")[1][1]
                pkg_icon = pkg_rreg.getObject("params")[2][1]
                pkg_mode = pkg_rreg.getObject("params")[3][1]
                code = """
with ZipFile("apps/{app}.mpkg") as zipObj:
    zipObj.extractall('')
if int("{pkg_mode}") == 0:
    main.windows.add(Package("{pkg_name}", "{pkg_icon}", "{pkg_file}"))
if int("{pkg_mode}") == 1:
    main.windows.add(PackageAutoTheme("{pkg_name}", "{pkg_icon}", "{pkg_file}"))""".format(app='.'.join(app.split('.')[:-1]), pkg_name=pkg_name, pkg_file=pkg_file, pkg_icon=pkg_icon, pkg_mode=pkg_mode)
                result = []
                result.append(pkg_name)
                result.append(code)
                self.themes.append(result)

        self.thumbnail_theme = gui.theme
        self.thumbnail_h = 60

        self.margin = 2
        self.margin2 = 2
        self.button_slide = 0
        self.button_slide_max = 9

        self.slider = DrgableY(self.rect.w-self.margin-17+self.margin/2, 4, 16, (self.rect.h-self.thumbnail_h-43)-(len(self.themes)-self.button_slide_max)*30-10, -1, self.rect.h-self.thumbnail_h-43)
        self.slide = (self.slider.y+self.slider.rect.h-self.rect.y-5*1.5)-28

        self.timer = 0
        self.alpha = 25

        for x in range(0, len(self.themes)):
            app = self.themes[x]
            try:
                theme_name = pugixor.XorDocumentRead("gui/images/"+theme+"/settings.xor").getObject("windows_sys")[1][1]
            except:
                theme_name = theme

            print(app[1])
            func = app[1]
            self.buttons.append(Button(self.margin, self.margin2+x*(30+self.margin2), self.rect.w-self.margin*2-17-2*2, 30, app[0], func))

    def logic(self):
        formula = len(self.themes)-8

        if self.slider.moving:
            pygame.draw.rect(self.display, self.bg_color, self.display.get_rect(topleft=(0, 0)))

        for button in self.buttons[self.button_slide:self.button_slide_max+self.button_slide]:
            btn = copy.copy(button)
            btn.y -= self.slide-20+(self.button_slide_max-6)*30-10-(30*(6-formula))
            if self.slider.moving:
                self.alpha = 255
            else:
                self.alpha = 25

            btn.alpha = self.alpha
            btn.draw(self)

        for button in self.buttons:
            button.customize_check()

        pygame.draw.rect(self.display, (55, 55, 55), (self.display.get_width()-25+self.margin*2.5, 0, 25+self.margin*2, self.display.get_height()-self.thumbnail_h-10))
        self.slider.draw(self)

        self.slide = self.slider.y-self.y+self.y+self.slider.rect.h-21-100
        self.button_slide = math.floor(self.slide/30)-(self.button_slide_max-(5+formula))

        if main.theme_change:
            self.timer += 1
        if self.timer == 25:
            self.timer = 0
            pygame.draw.rect(self.display, self.bg_color, self.display.get_rect(topleft=(0, 0)))
        if self.timer > 0:
            self.timer += 1

class UserPicMan(Window):
    def __init__(self, x, y):
        gui.Window.__init__(self, x, y, 450, 290, "Менеджер Аватарок Користувача")
        self.buttons = []
        self.themes = []
        self.path = "user/pics"
        for icon in os.listdir(self.path):
            if os.path.isfile(self.path + '/' + icon) and not icon.split('.')[-1] == "psd":
                result = []
                result.append('.'.join(icon.split('.')[:-1]))
                result.append(icon_man_func.format(icon=icon))
                self.themes.append(result)

        self.thumbnail_theme = gui.theme
        self.thumbnail_h = 60

        self.margin = 2
        self.margin2 = 2
        self.button_slide = 0
        self.button_slide_max = 9

        self.slider = DrgableY(self.rect.w - self.margin - 17 + self.margin / 2, 4, 16, (self.rect.h - self.thumbnail_h - 43 - 5*2)/(len(self.themes)-self.button_slide_max+1), -1, self.rect.h - self.thumbnail_h - 43)
        self.slide = (self.slider.y+self.slider.rect.h-self.rect.y-5*1.5)-28

        self.timer = 0
        self.alpha = 25

        for x in range(0, len(self.themes)):
            app = self.themes[x]

            func = app[1]
            self.buttons.append(Button(self.margin, self.margin2+x*(30+self.margin2), self.rect.w-self.margin*2-17-2*2, 30, app[0], func))

    def logic(self):
        formula = len(self.themes)-16

        if self.slider.moving:
            pygame.draw.rect(self.display, self.bg_color, self.display.get_rect(topleft=(0, 0)))

        for button in self.buttons[self.button_slide:self.button_slide_max+self.button_slide]:
            btn = copy.copy(button)
            btn.y -= (self.slide-20+(self.button_slide_max-7)*30-10-(30*(10-formula))-10)+90
            if self.slider.moving:
                self.alpha = 255
            else:
                self.alpha = 25

            btn.alpha = self.alpha
            btn.draw(self)

        for button in self.buttons:
            button.customize_check()

        pygame.draw.rect(self.display, (55, 55, 55), (self.display.get_width()-25+self.margin*2.5, 0, 25+self.margin*2, self.display.get_height()-self.thumbnail_h-10))
        self.slider.draw(self)

        self.divize = (len(self.themes)-25)
        if self.divize <= 0:
            self.divize = 1
        self.slide = ((self.slider.y-self.y+self.y+self.slider.rect.h-27-100)*3)+240-(len(self.themes)-26/self.divize)*(13-(len(self.themes)-25)*5)
        self.button_slide = math.floor(self.slide/30)-(self.button_slide_max-(3+formula))

        if main.theme_change:
            self.timer += 1
        if self.timer == 25:
            self.timer = 0
            pygame.draw.rect(self.display, self.bg_color, self.display.get_rect(topleft=(0, 0)))
        if self.timer > 0:
            self.timer += 1