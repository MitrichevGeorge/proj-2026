import math
import pygame as pg
from abc import ABC, abstractmethod
from themes import tokyonight as theme

RENDER_SCALE = 2
DOT_RADIUS = 5
BORDER_WIDTH = 2

COLOR_FILL, COLOR_BG, COLOR_DOT, COLOR_BORDER = theme

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

class Point(Drawable):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __le__(self, other):
        if isinstance(other, Point):
            return self.x <= other.x and self.y <= other.y
        return NotImplemented
    
    def __ge__(self, other):
        if isinstance(other, Point):
            return self.x >= other.x and self.y >= other.y
        return NotImplemented
    
    def draw(self, surface, color=COLOR_DOT, radius=DOT_RADIUS):
        pg.draw.circle(surface, color, (int(self.x)*RENDER_SCALE, int(self.y)*RENDER_SCALE), radius*RENDER_SCALE)

class Line(Drawable):
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __str__(self):
        return f"Line({self.start}, {self.end})"

    def draw(self, surface, color=COLOR_BORDER):
        pg.draw.line(surface, color, (int(self.start.x)*RENDER_SCALE, int(self.start.y)*RENDER_SCALE), 
                     (int(self.end.x)*RENDER_SCALE, int(self.end.y)*RENDER_SCALE), width=BORDER_WIDTH*RENDER_SCALE)
        
    def __len__(self):
        return math.sqrt((self.end.x - self.start.x) ** 2 + (self.end.y - self.start.y) ** 2)
    
    def __add__(self, other):
        if isinstance(other, Line):
            return Line(self.start + other.start, self.end + other.end)
        return NotImplemented
    
    def intersection(self, other):
        p1 = self.start
        q1 = self.end
        p2 = other.start
        q2 = other.end
        
        dx1 = q1.x - p1.x
        dy1 = q1.y - p1.y
        dx2 = q2.x - p2.x
        dy2 = q2.y - p2.y
        
        denom = dx1 * dy2 - dy1 * dx2
        if denom == 0:
            return None
        
        t = ((p2.x - p1.x) * dy2 - (p2.y - p1.y) * dx2) / denom
        u = ((p2.x - p1.x) * dy1 - (p2.y - p1.y) * dx1) / denom
        
        if 0 <= t <= 1 and 0 <= u <= 1:
            ix = p1.x + t * dx1
            iy = p1.y + t * dy1
            return Point(ix, iy)
        return None
    
    def intersects(self, other):
        return self.intersection(other) is not None

    
class Polygon(Drawable):
    def __init__(self, vertices):
        self.vertices = vertices

    def __str__(self):
        return f"Polygon({self.vertices})"

    def draw(self, surface, color=COLOR_FILL):
        if len(self.vertices) < 2:
            return
        points = [(int(p.x)*RENDER_SCALE, int(p.y)*RENDER_SCALE) for p in self.vertices]
        pg.draw.polygon(surface, color, points)
        pg.draw.polygon(surface, COLOR_BORDER, points, width=BORDER_WIDTH*RENDER_SCALE)
        for vertex in self.vertices:
            vertex.draw(surface, color=COLOR_DOT, radius=DOT_RADIUS)

    def perimeter(self):
        n = len(self.vertices)
        if n < 2:
            return 0
        return sum(((self.vertices[i].x - self.vertices[(i + 1) % n].x) ** 2 + 
                    (self.vertices[i].y - self.vertices[(i + 1) % n].y) ** 2) ** 0.5 for i in range(n))
    
    def edges(self):
        n = len(self.vertices)
        return [Line(self.vertices[i], self.vertices[(i + 1) % n]) for i in range(n)]
    
    def add_vertex(self, point):
        self.vertices.append(point)
    
class World:
    def __init__(self):
        self.objects = []
        self.screen_width = 1200
        self.screen_height = 800

    def initpg(self):
        pg.init()
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pg.time.Clock()
        self.render_scale = RENDER_SCALE
        self.render_surface = pg.Surface(
            (self.screen_width * self.render_scale, self.screen_height * self.render_scale),
            pg.SRCALPHA
        )
        self.tmp_surface = pg.Surface(
            (self.screen_width * self.render_scale, self.screen_height * self.render_scale),
            pg.SRCALPHA
        )
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))

    def add_object(self, obj):
        self.objects.append(obj)

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

    def update(self):
        self.clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
        self.render_surface.fill((0, 0, 0))
        self.draw(self.render_surface)
        scaled = pg.transform.smoothscale(self.render_surface, (self.screen_width, self.screen_height))
        tmp_scaled = pg.transform.smoothscale(self.tmp_surface, (self.screen_width, self.screen_height))
        self.tmp_surface.fill((0, 0, 0, 0))
        self.screen.blit(scaled, (0, 0))
        self.screen.blit(tmp_scaled, (0, 0))
        pg.display.flip()
        return True
    
    def tmp_draw_line(self, arg1, arg2=None, color=COLOR_BORDER):
        if isinstance(arg1, Line):
            p1 = arg1.start
            p2 = arg1.end
        else:
            p1 = arg1
            p2 = arg2
        pg.draw.line(self.tmp_surface, color, (int(p1.x)*RENDER_SCALE, int(p1.y)*RENDER_SCALE), 
                     (int(p2.x)*RENDER_SCALE, int(p2.y)*RENDER_SCALE), width=BORDER_WIDTH*RENDER_SCALE)

class CheckContainingMethods:
    def even_odd_rule(polygon: Polygon, point: Point, world: World) -> bool:
        line = Line(point, Point(world.screen_width, point.y))
        world.tmp_draw_line(line, color=(255, 0, 0))
        count = 0
        intersection = None
        for edge in polygon.edges():
            if edge.intersects(line):
                count += 1
                if intersection is None:
                    intersection = edge.intersection(line)
                elif intersection >= edge.intersection(line):
                    intersection = edge.intersection(line)
        if intersection is not None:
            world.tmp_draw_line(Line(point, intersection), color=(0, 255, 0))
        return count % 2 == 1

def main():
    pg.init()
    world = World()
    world.initpg()

    triangle = Polygon([Point(100, 100), Point(150, 50), Point(200, 100)])
    square = Polygon([Point(300, 300), Point(350, 300), Point(350, 350), Point(300, 350)])
    point = Point(120, 80)
    
    world.add_object(triangle)
    world.add_object(square)
    world.add_object(point)

    while world.update():
        point.x, point.y = pg.mouse.get_pos()
        CheckContainingMethods.even_odd_rule(triangle, point, world)
        pass

    pg.quit()

if __name__ == "__main__": main()