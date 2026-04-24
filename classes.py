import math
from abc import ABC, abstractmethod
from pge import BORDER_WIDTH, COLOR_BORDER, COLOR_DOT, DOT_RADIUS

class Drawable(ABC):
    @abstractmethod
    def draw(self, renderer):
        pass

class Point(Drawable):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.autoclean = False

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
    
    def __div__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Point(self.x / scalar, self.y / scalar)
        return NotImplemented
    
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Point(self.x * scalar, self.y * scalar)
        return NotImplemented
    
    def __le__(self, other):
        if isinstance(other, Point):
            return self.x <= other.x and self.y <= other.y
        return NotImplemented
    
    def __ge__(self, other):
        if isinstance(other, Point):
            return self.x >= other.x and self.y >= other.y
        return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, Point):
            return self.x < other.x and self.y < other.y
        return NotImplemented
    
    def __gt__(self, other):
        if isinstance(other, Point):
            return self.x > other.x and self.y > other.y
        return NotImplemented

    def draw(self, renderer):
        renderer.draw_point(self.x, self.y)

class Vector(Point):
    def __init__(self, p1, p2):
        if isinstance(p1, Point) and isinstance(p2, Point):
            super().__init__(p2.x - p1.x, p2.y - p1.y)
        else:
            super().__init__(p1, p2)

    def __str__(self):
        return f"<{self.x}, {self.y}>"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        return NotImplemented

class Line(Drawable):
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.autoclean = False

    def __str__(self):
        return f"Line({self.start}, {self.end})"

    def draw(self, renderer):
        renderer.draw_line(self.start.x, self.start.y, self.end.x, self.end.y)
        
    def __len__(self):
        return self.get_length()
    
    def get_length(self):
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
        
        ix = p1.x + t * dx1
        iy = p1.y + t * dy1
        if 0 <= t <= 1 and 0 <= u <= 1:            
            return Point(ix, iy)
        return None
    
    def intersects(self, other):
        return self.intersection(other) is not None
    
    def get_pp(self, p: Point):
        x, y = p.x, p.y
        x1, y1 = self.start.x, self.start.y
        x2, y2 = self.end.x, self.end.y
        return ((x2- x1) * (y - y1) - (y2 - y1) * (x - x1))
    
    def project_point(self, p: Point):
        x1, y1 = self.start.x, self.start.y
        x2, y2 = self.end.x, self.end.y
        dx = x2 - x1
        dy = y2 - y1
        denom = dx * dx + dy * dy
        if denom == 0:
            return Point(x1, y1)
        t = ((p.x - x1) * dx + (p.y - y1) * dy) / denom
        if t <= 0:
            return Point(x1, y1)
        if t >= 1:
            return Point(x2, y2)
        return Point(x1 + dx * t, y1 + dy * t)

    
class Polygon(Drawable):
    def __init__(self, vertices):
        self.vertices = vertices
        self.autoclean = False

    def __str__(self):
        return f"Polygon({self.vertices})"

    def draw(self, renderer):
        if len(self.vertices) < 2:
            return
        vertices = [(v.x, v.y) for v in self.vertices]
        renderer.draw_polygon(vertices)

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

    def get_normals(self):
        n = len(self.vertices)
        if n < 2:
            return []
        area = 0
        for i in range(n):
            p = self.vertices[i]
            q = self.vertices[(i + 1) % n]
            area += p.x * q.y - q.x * p.y
        ccw = area > 0
        normals = []
        for edge in self.edges():
            dx = edge.end.x - edge.start.x
            dy = edge.end.y - edge.start.y
            if ccw:
                normals.append(Vector(-dy, dx))
            else:
                normals.append(Vector(dy, -dx))
        return normals

class Angle(Drawable):
    def __init__(self, vertex: Point, p1: Point, p2: Point):
        self.vertex = vertex
        self.p1 = Line(vertex, p1)
        self.p2 = Line(vertex, p2)
        self.autoclean = True

    def __str__(self):
        return f"Angle({self.vertex}, {self.p1}, {self.p2})"

    def draw(self, renderer):
        renderer.draw_tmp_polygon([(self.vertex.x, self.vertex.y), (self.p1.end.x, self.p1.end.y), (self.p2.end.x, self.p2.end.y)], fill_color=(95, 129, 199, 50), show=False)
        renderer.draw_line(self.vertex.x, self.vertex.y, self.p1.end.x, self.p1.end.y, color=(95, 129, 199, 150))
        renderer.draw_line(self.vertex.x, self.vertex.y, self.p2.end.x, self.p2.end.y, color=(95, 129, 199, 150))
        renderer.draw_tmp_text(f"{math.degrees(math.atan2(self.p1.end.y - self.vertex.y, self.p1.end.x - self.vertex.x) - 
                                            math.atan2(self.p2.end.y - self.vertex.y, self.p2.end.x - self.vertex.x)):.2f}°",
                                            (self.vertex.x + self.p1.end.x*2 + self.p2.end.x*2) / 5, (self.vertex.y + self.p1.end.y*2 + self.p2.end.y*2) / 5, color=(235, 220, 255), type="RT")

class World:
    def __init__(self, renderer):
        self.objects = []
        self.renderer = renderer
        self.screen_width = renderer.width
        self.screen_height = renderer.height

    def add_object(self, obj):
        self.objects.append(obj)

    def draw(self):
        for obj in self.objects:
            obj.draw(self.renderer)
        self.objects = [obj for obj in self.objects if not obj.autoclean]

    def update(self):
        return self.renderer.finish_update()

    def tmp_draw_line(self, x1, y1, x2, y2, color=COLOR_BORDER, width=BORDER_WIDTH):
        self.renderer.draw_tmp_line(x1, y1, x2, y2, color, width)

    def tmp_draw_point(self, x, y, color=COLOR_DOT, radius=DOT_RADIUS):
        self.renderer.draw_tmp_point(x, y, color, radius)
    
    def tmp_draw_polygon(self, vertices, fill_color=COLOR_BORDER):
        self.renderer.draw_tmp_polygon(vertices, fill_color)

class CheckContainingMethods:
    def even_odd_rule(polygon: Polygon, point: Point, world: World, direction: int) -> bool:
        line = None
        if direction == 0:
            line = Line(point, Point(world.screen_width, point.y))
        elif direction == 1:
            line = Line(point, Point(point.x, world.screen_height))
        elif direction == 2:
            line = Line(point, Point(0, point.y))
        elif direction == 3:
            line = Line(point, Point(point.x, 0))
        world.tmp_draw_polygon([(v.x, v.y) for v in polygon.vertices], fill_color=(48, 38, 28))
        world.tmp_draw_line(line.start.x, line.start.y, line.end.x, line.end.y, color=(110, 90, 150), width=3)
        count = 0
        intersection = None
        pt_to_draw = []
        for edge in polygon.edges():
            if edge.intersects(line):
                pt = edge.intersection(line)
                pt_to_draw.append(pt)
                if pt.x != edge.start.x or pt.y != edge.start.y:
                    count += 1
                if intersection is None:
                    intersection = pt
                elif intersection >= edge.intersection(line):
                    intersection = pt
        verdict = (count % 2 == 1)
        if verdict:
            world.tmp_draw_polygon([(v.x, v.y) for v in polygon.vertices], fill_color=(168, 120, 86, 80))
        if intersection is not None:
            world.tmp_draw_line(point.x, point.y, intersection.x, intersection.y, color=(224, 175, 104), width=3)
        for i in pt_to_draw:
            world.tmp_draw_point(i.x, i.y, color=(187, 154, 247))
        pgw = world.renderer
        pgw.textRB = [f"{'Inside' if verdict else 'Outside'}", f"Count: {count}", f"[Even-Odd Rule] {['R', 'D', 'L', 'U'][direction]}"]
        return verdict
    
    def sum_of_angles(polygon: Polygon, point: Point, world: World) -> bool:
        total_angle = 0
        for edge in polygon.edges():
            v1 = Point(edge.start.x - point.x, edge.start.y - point.y)
            v2 = Point(edge.end.x - point.x, edge.end.y - point.y)
            angle = math.atan2(v1.x * v2.y - v1.y * v2.x, v1.x * v2.x + v1.y * v2.y)
            total_angle += angle
            q = Angle(point, edge.start, edge.end)
            world.add_object(q)
        total_angle = math.degrees(total_angle)
        verdict = abs(total_angle) > 1e-5
        pgw = world.renderer
        pgw.textRB = [f"{'Inside' if verdict else 'Outside'}", f"Total Angle: {total_angle:.2f}", "[Sum of Angles]"]
        if verdict:
            world.tmp_draw_polygon([(v.x, v.y) for v in polygon.vertices], fill_color=(168, 120, 86, 80))
        return verdict
    
    def half_plane_method(polygon: Polygon, point: Point, world: World) -> bool:
        world.tmp_draw_polygon([(v.x, v.y) for v in polygon.vertices], fill_color=(48, 38, 28))
        pgw = world.renderer
        verdict = True
        dolater = []
        for edge in polygon.edges():
            if edge.get_pp(point) <= 0:
                verdict = False
                dolater.append(lambda e=edge: world.tmp_draw_line(e.start.x, e.start.y, e.end.x, e.end.y, color=(255, 100, 100), width=3))
            else:
                dolater.append(lambda e=edge: world.tmp_draw_line(e.start.x, e.start.y, e.end.x, e.end.y, color=(100, 255, 100), width=3))
        pgw.textRB = [f"{'Inside' if verdict else 'Outside'}", "[Half-Plane Method]"]
        if verdict:
            world.tmp_draw_polygon([(v.x, v.y) for v in polygon.vertices], fill_color=(168, 120, 86, 80))
        for func in dolater:
            func()
        return verdict
    
    def closest_point_on_boundary(polygon: Polygon, point: Point, world: World) -> Point:
        closest_point = None
        min_distance, min_index = float('inf'), -1
        for i, edge in enumerate(polygon.edges()):
            proj = edge.project_point(point)
            dist = Line(point, proj).get_length()
            if dist < min_distance:
                min_distance = dist
                closest_point = proj
                min_index = i
        world.tmp_draw_line(point.x, point.y, closest_point.x, closest_point.y, color=(255, 255, 100), width=3)
        world.tmp_draw_point(closest_point.x, closest_point.y, color=(255, 255, 100))
        norms = polygon.get_normals()
        e = polygon.edges()[min_index]
        if closest_point.x == e.start.x and closest_point.y == e.start.y:
            n = (norms[(min_index - 1) % len(norms)] + norms[min_index]) * 0.5
        elif closest_point.x == e.end.x and closest_point.y == e.end.y:
            n = (norms[min_index] + norms[(min_index + 1) % len(norms)]) * 0.5
        else:
            n = norms[min_index]
        world.tmp_draw_line(polygon.vertices[min_index].x, polygon.vertices[min_index].y,
                            polygon.vertices[min_index].x + n.x, polygon.vertices[min_index].y + n.y, color=(255, 0, 0), width=3)
        q = Vector(closest_point, point)
        d = Vector(n.x, n.y) * q
        pgw = world.renderer
        pgw.textRB = [f"{'Inside' if d > 0 else 'Outside'}", f"{d:.2f}", f"q: ({q.x:.2f}, {q.y:.2f})", f"n: ({n.x:.2f}, {n.y:.2f})", f"Closest Point: ({closest_point.x:.2f}, {closest_point.y:.2f})", f"Distance: {min_distance:.2f}", "[Closest Point on Boundary]"]
        return d > 0