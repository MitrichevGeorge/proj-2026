import os
import math
import pygame as pg
from themes import tokyonight as theme

RENDER_SCALE = 2
DOT_RADIUS = 5
BORDER_WIDTH = 2

COLOR_FILL, COLOR_BG, COLOR_DOT, COLOR_BORDER, COLOR_TEXT = theme

class pge:
    def __init__(self, render_scale=RENDER_SCALE):
        pg.init()
        w, h = pg.display.Info().current_w, pg.display.Info().current_h
        w, h = int(w * 0.8), int(h * 0.8)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.width = w
        self.height = h
        self.screen = pg.display.set_mode((w,h), pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.font = pg.font.Font("HurmitNerdFontMono-Regular.otf", 16)

        self.render_scale = render_scale
        self.render_surface = pg.Surface((w * render_scale, h * render_scale), pg.SRCALPHA)
        self.tmp_surface = pg.Surface((w * render_scale, h * render_scale), pg.SRCALPHA)
        self.tmp2_surface = pg.Surface((w * render_scale, h * render_scale), pg.SRCALPHA)

        self.textLB = ["Hello, World!"]
        self.textLT = [""]
        self.textRB = [""]
        self.textRT = [""]

        self.fsarr = 0
        self.fszx = 0
        self.fscd = 0

    def start_update(self):
        self.clock.tick(144)
        self.render_surface.fill((22, 24, 36))

    def finish_update(self):
        self.screen.fill((0, 0, 0))
        scaled_surface = pg.transform.smoothscale(self.render_surface, (self.width, self.height))
        self.screen.blit(scaled_surface, (0, 0))
        tmp_scaled = pg.transform.smoothscale(self.tmp_surface, (self.width, self.height))
        self.tmp_surface.fill((0, 0, 0, 0))
        self.screen.blit(tmp_scaled, (0, 0))
        tmp2_scaled = pg.transform.smoothscale(self.tmp2_surface, (self.width, self.height))
        self.tmp2_surface.fill((0, 0, 0, 0))
        self.screen.blit(tmp2_scaled, (0, 0))
        self.update_text()
        pg.display.flip()

        self.fsarr = 0
        self.fszx = 0
        self.fscd = 0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    self.fscd = 1
                elif event.key == pg.K_d:
                    self.fscd = -1
                elif event.key == pg.K_z:
                    self.fszx = -1
                elif event.key == pg.K_x:
                    self.fszx = 1
                elif event.key == pg.K_LEFT:
                    self.fsarr = -1
                elif event.key == pg.K_RIGHT:
                    self.fsarr = 1
        return True
    
    def update_text(self):
        self.set_text(f"FPS: {self.clock.get_fps():.2f}", 0, type="LT")
        self.draw_batch_text(self.textLB, 10, self.screen.get_height() - 10, -30, color=COLOR_TEXT, type="LB")
        self.draw_batch_text(self.textLT, 10, 10, color=COLOR_TEXT, type="LT")
        self.draw_batch_text(self.textRB, self.screen.get_width() - 10, self.screen.get_height() - 10, -30, color=COLOR_TEXT, type="RB")
        self.draw_batch_text(self.textRT, self.screen.get_width() - 10, 10, color=COLOR_TEXT, type="RT")

    def set_text(self, text, line_index, type="LB"):
        if type == "LB":
            if line_index >= len(self.textLB):
                self.textLB.append(text)
            self.textLB[line_index] = text
        elif type == "LT":
            if line_index >= len(self.textLT):
                self.textLT.append(text)
            self.textLT[line_index] = text
        elif type == "RB":
            if line_index >= len(self.textRB):
                self.textRB.append(text)
            self.textRB[line_index] = text
        elif type == "RT":
            if line_index >= len(self.textRT):
                self.textRT.append(text)
            self.textRT[line_index] = text

    def draw_point(self, x, y, color=COLOR_DOT, radius=DOT_RADIUS):
        pg.draw.circle(self.render_surface, color, 
                      (int(x) * self.render_scale, int(y) * self.render_scale), 
                      radius * self.render_scale)

    def draw_line(self, x1, y1, x2, y2, color=COLOR_BORDER):
        pg.draw.line(self.render_surface, color,
                    (int(x1) * self.render_scale, int(y1) * self.render_scale),
                    (int(x2) * self.render_scale, int(y2) * self.render_scale),
                    width=BORDER_WIDTH * self.render_scale)

    def draw_polygon(self, vertices, fill_color=COLOR_FILL, show=True):
        if len(vertices) < 2:
            return
        points = [(int(v[0]) * self.render_scale, int(v[1]) * self.render_scale) 
                 for v in vertices]
        pg.draw.polygon(self.render_surface, fill_color, points)
        if show:
            pg.draw.polygon(self.render_surface, COLOR_BORDER, points, 
                       width=BORDER_WIDTH * self.render_scale)
            for point in points:
                pg.draw.circle(self.render_surface, COLOR_DOT, point, DOT_RADIUS * self.render_scale)

    def draw_tmp_line(self, x1, y1, x2, y2, color=COLOR_BORDER, width=BORDER_WIDTH):
        pg.draw.line(self.tmp_surface, color,
                    (int(x1) * self.render_scale, int(y1) * self.render_scale),
                    (int(x2) * self.render_scale, int(y2) * self.render_scale),
                    width=width * self.render_scale)
        
    def draw_tmp_point(self, x, y, color=COLOR_DOT, radius=DOT_RADIUS):
        pg.draw.circle(self.tmp_surface, color, 
                      (int(x) * self.render_scale, int(y) * self.render_scale), 
                      radius * self.render_scale)
        
    def draw_tmp_polygon(self, vertices, fill_color=COLOR_FILL, show=True):
        if len(vertices) < 2:
            return
        points = [(int(v[0]) * self.render_scale, int(v[1]) * self.render_scale) 
                 for v in vertices]
        pg.draw.polygon(self.tmp_surface, fill_color, points)
        if show:
            pg.draw.polygon(self.tmp_surface, COLOR_BORDER, points, 
                           width=BORDER_WIDTH * self.render_scale)
            for point in points:
                pg.draw.circle(self.tmp_surface, COLOR_DOT, point, DOT_RADIUS * self.render_scale)
        
    def draw_text(self, text, x, y, color=COLOR_TEXT, type="LB"):
        text_surface = self.font.render(text, True, color)
        rect = text_surface.get_rect()
        if type == "LB":
            rect.bottomleft = (x, y)
        elif type == "LT":
            rect.topleft = (x, y)
        elif type == "RB":
            rect.bottomright = (x, y)
        elif type == "RT":
            rect.topright = (x, y)
        self.screen.blit(text_surface, rect)

    def draw_tmp_text(self, text, x, y, color=COLOR_TEXT, type="LB"):
        text_surface = self.font.render(text, True, color)
        x,y = int(x) * self.render_scale, int(y) * self.render_scale
        rect = text_surface.get_rect()
        if type == "LB":
            rect.bottomleft = (x, y)
        elif type == "LT":
            rect.topleft = (x, y)
        elif type == "RB":
            rect.bottomright = (x, y)
        elif type == "RT":
            rect.topright = (x, y)
        elif type == "CT":
            rect.center = (x, y)
        self.tmp2_surface.blit(text_surface, rect)

    def draw_batch_text(self, text_list, x, y, step = 30, color=COLOR_TEXT, type="LB"):
        for i, text in enumerate(text_list):
            self.draw_text(text, x, y + i * step, color, type)

def main():
    _pge = pge()
    while True:
        _pge.start_update()
        if not _pge.finish_update():
            break

if __name__ == "__main__": main()