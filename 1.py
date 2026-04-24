from classes import *
from pge import pge
import pygame as pg

def main():
    renderer = pge()
    world = World(renderer)

    p1 = Polygon([Point(100, 100), Point(150, 50), Point(200, 100), Point(200, 150), Point(150, 200), Point(100, 150)])
    square = Polygon([Point(300, 300), Point(350, 300), Point(350, 350), Point(300, 350)])
    point = Point(120, 80)
    star = Polygon([Point(400, 100), Point(420, 150), Point(470, 150), Point(430, 180), Point(450, 230), Point(400, 200), Point(350, 230), Point(370, 180), Point(330, 150), Point(380, 150)])

    world.add_object(p1)
    world.add_object(square)
    world.add_object(star)

    world.add_object(point)
    renderer.textLB = ["C / D - type", "Z / X - method", "arrows - switch polygon"]
    obj = [p1, square, star]
    sel = 0

    ntt = 0
    tp = 0
    tpc = 3

    while True:
        renderer.start_update()
        world.draw()
        if not world.update():
            break
        sel = (sel + renderer.fsarr) % len(obj)
        ntt += renderer.fscd
        tp = (tp + renderer.fszx) % tpc
        point.x, point.y = pg.mouse.get_pos()
        renderer.textRB = []
        if tp == 0:
            ntt %= 4
            CheckContainingMethods.even_odd_rule(obj[sel], point, world, ntt)
        elif tp == 1:
            CheckContainingMethods.sum_of_angles(obj[sel], point, world)
        elif tp == 2:
            CheckContainingMethods.half_plane_method(obj[sel], point, world)

    pg.quit()

if __name__ == "__main__": main()