from time import sleep

from nxt.brick import Brick
from nxt.locator import find_one_brick
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Light, Sound, Touch, Ultrasonic, Color20
from nxt.sensor import PORT_1, PORT_2, PORT_3, PORT_4
from nxt.sensor import Type

class Direction(object):
    def __init__(self, back, left, right):
        self.directions = [back, left, right]

    def get_directions(self):
        return self.directions

fore = Direction(1, -1, -1)
back = Direction(-1, 1, 1)

fore_left = Direction(1, -1, 1)
back_right = Direction(-1, 1, -1)

fore_right = Direction(1, 1, -1)
back_left = Direction(-1, -1, 1)



class Strider(object):

    def __init__(self, brick='NXT'):
        r'''Creates a new Strider controller.
        
            brick
                Either an nxt.brick.Brick object, or an NXT brick's name as a
                string. If omitted, a Brick named 'NXT' is looked up.
        '''
        if isinstance(brick, basestring):
            brick = find_one_brick(name=brick)
    
        self.brick = brick
        self.back_leg = Motor(brick, PORT_B)
        self.left_leg = Motor(brick, PORT_C)
        self.right_leg = Motor(brick, PORT_A)

        #self.touch = Touch(brick, PORT_1)
        #self.sound = Sound(brick, PORT_2)
        #self.light = Light(brick, PORT_3)
        #self.ultrasonic = Ultrasonic(brick, PORT_4)
        self.colour = Color20(brick, PORT_3)

    def walk(self, direction, time = 0):
        [back, left, right] = direction.get_directions()
        self.back_leg.run(back * 80)
        self.left_leg.run(left * 80)
        self.right_leg.run(right * 80)
        if time > 0:
            sleep(time)
            self.stop()
            
        
    def show_colour(self, colour):
        self.colour.set_light_color(colour)

    def colour_display(self):
        for colour in [Type.COLORRED, Type.COLORGREEN, Type.COLORBLUE]:
            self.show_colour(colour)
            sleep(2)
        self.show_colour(Type.COLORNONE)
        

    def stop(self):
        self.back_leg.idle()
        self.left_leg.idle()
        self.right_leg.idle()

    def fire_lasers(self):
        for i in range(0, 5):
            self.brick.play_sound_file(False, '! Laser.rso')

if __name__ == '__main__':
    robot = Strider()
    robot.colour_display()
    robot.walk(fore, 4)
    sleep(1)
    robot.walk(back, 1)
    robot.walk(fore_right, 3)
    robot.walk(fore_left, 3)
    robot.walk(back_right, 3)
    robot.walk(back_left, 3)
    #robot.walk_forward()
    #sleep(4)
    #robot.stop()
    #robot.fire_lasers()
    #sleep(5)
    #robot.walk_backward()
    #sleep(4)
    robot.stop()
