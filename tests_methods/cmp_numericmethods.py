from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import time

from simulation.system.spacesystem import SpaceObject
from simulation.system.spacesystem import SpaceSystem
from simulation.conf.settings import appsettings
Width = 1200
Height = 1200
class SpaceObjectTest(SpaceObject):

    def draw(self,draw, width, height, r):
        draw.ellipse((int(self.x-r), int(self.y-r), int(self.x+r), int(self.y+r)), fill=self.color)
        # print("pos %s vel %s" % (self.position, self.velocity))

def test_fun(methods,num_iter, dt):
    for method in methods:
        print("Start for %s %s %s" % (method, num_iter, dt))
        appsettings['numericmethod'] = method
        appsettings['dt_in_numericmethod'] = dt
        system = test_add_object(1)
        image = Image.new("RGB", (Width, Height), "white")
        draw = ImageDraw.Draw(image)
        draw.line((0, Height/2, Width, Height/2), "black")
        start_time = time.time()
        for i in range(0, num_iter):
            for item in system:
                if item.position > [Width, Height]:
                    break
                item.draw(draw, 0, 0, 2)
            system.update()
        time_cal = time.time() - start_time
        font = ImageFont.truetype("testdraw/spinwerad.ttf", 18)
        draw.line((Height/2, 0, Height/2, Width), "black")
        draw.text((10, 10),"numericmethods = %s, dt = %s, iteracji = %s" % (method, dt, num_iter), font=font, fill="black")
        draw.text((30, 30),"time= %s" % (time_cal), font=font, fill="black")
        image.save("testdraw/%s_dt%s.png" %(method, dt))
def test_add_object(num_obj):
    system = SpaceSystem()
    testobj = SpaceObjectTest(pos=(50, 50))
    testobj.velocity_x = 1.9
    testobj.velocity_y = -0.14
    testobj.color = (200, 215,255)
    system.append(testobj)
    testobj2 = SpaceObjectTest(pos=(Width/2,Height/2))
    testobj2.mass = 180
    testobj2.color = (100, 150, 50)
    system.append(testobj2)
    return system

if __name__ == '__main__':
    methods = [ "Euler", "VerletVelocity", "RungeKutta"]
    for dt in np.arange(0.5, 2., 0.05):
        test_fun(methods, 10000, dt)

