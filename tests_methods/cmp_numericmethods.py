#!/usr/bin/python

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import time
import sys
import inspect, os
import random

tmpdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory)
sys.path.append("%s/../simulation" % tmpdir)
sys.path.append("%s/../" % tmpdir)

from conf.settings import appsettings
from simulation.system.spacesystem import SpaceObject
from simulation.system.spacesystem import SpaceSystem
Width = 1200
Height = 1200
class SpaceObjectTest(SpaceObject):

    def draw(self,draw, width, height, r):
        draw.ellipse((int(self.x-r), int(self.y-r), int(self.x+r), int(self.y+r)), fill=self.color)
        # print("pos %s vel %s" % (self.position, self.velocity))

def test_fun(methods,num_obj, num_iter, dt):
    summary_d = {}
    lines = ""
    for method in methods:
        print("Start for %s %s %s" % (method, num_iter, dt))
        savefile_name = "testdraw/{}dt{}obj{}numiter{}".format(method, dt, num_obj, num_iter)
        savefile = open(str(savefile_name)+".csv", "w")
        appsettings['numericmethod'] = method
        appsettings['dt_in_numericmethod'] = dt
        savefile.write("numericmethods = %s, dt = %s, iteracji = %s \n" % (method, dt, num_iter))
        system = test_add_object(num_obj)
        image = Image.new("RGB", (Width, Height), "white")
        draw = ImageDraw.Draw(image)
        draw.line((0, Height/2, Width, Height/2), "black")
        start_time = time.time()
        sumx = sumy = 0
        for i in range(0, num_iter):
            tmp_time = time.time()
            for item in system:
                if item.spaceid == 0:
                    savefile.write("%s;%s;\n" % (item.x, item.y))
                    sumx += item.x
                    sumy += item.y
                if item.position > [Width, Height]:
                    break
                item.draw(draw, 0, 0, 2)
            end_tmp_time = time.time()
            start_time -= end_tmp_time - tmp_time
            system.update()
        time_cal = time.time() - start_time
        lines += "%s;%s;%s;%s;%s;%s;%s;" % (method,  dt, num_iter, time_cal, num_obj,sumx, sumy)
        font = ImageFont.truetype("spinwerad.ttf", 18)
        draw.line((Height/2, 0, Height/2, Width), "black")
        draw.text((10, 10),"numericmethods = %s, dt = %s, iteracji = %s num_ob = %s" % (method, dt, num_iter, num_obj), font=font, fill="black")
        draw.text((30, 30),"time= %s" % (time_cal), font=font, fill="black")
        summary_txt = "numericmethods = %s; dt = %s; iteracji = %s; time = %s; num_obj = %s\n" % (method, dt, num_iter, time_cal, num_obj)
        print(summary_txt)
        image.save("%s.png" %(savefile_name))
        image = draw = None
        system.clear()
        savefile.close()

    print(lines)
    summary = open("wynik.csv", "a")
    summary.write(lines + "\n")
    summary.close()
def test_add_object(num_obj):
    system = SpaceSystem()
    testobj = SpaceObjectTest(pos=(50, 50))
    testobj.velocity_x = 1.9
    testobj.velocity_y = -0.14
    testobj.color = (200, 215,255)
    testobj.spaceid = 0
    system.append(testobj)
    for i in range(1, num_obj):
        testobj2 = SpaceObjectTest(pos=(10 * i + i+10+ Width/2, 11 * i + Height/2))
        testobj2.mass = 180
        testobj2.color = (10*i+10, 150, 50)
        testobj2.velocity_x = 1.9 * i
        testobj2.velocity_y = -0.14
        system.append(testobj2)
    return system

if __name__ == '__main__':
    methods = ["VerletVelocity", "Euler", "RungeKutta"]
    # for num in range(, 28, 5):
    for dt in np.arange(0.1, 0.7, 0.1):
        for iteracji in range(1000,10000,1500):
            test_fun(methods,2, iteracji, dt)

