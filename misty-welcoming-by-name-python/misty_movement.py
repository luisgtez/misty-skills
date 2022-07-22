from shutil import move
from mistyPy.Robot import Robot
from mistyPy.Events import Events   
from curtsies import Input

def movement():
    with Input(keynames='curses') as input_generator:
        for e in input_generator:
            print(e)
            misty.MoveHead(0,0,0)
            if e == 'w':
                misty.Drive(50,0)
            if e == 's':
                misty.Drive(q0,0)
            if e == 'e':
                misty.Drive(0,-100)
            if e == 'q':
                misty.Drive(0,100)
            if e=='KEY_SPACE':
                misty.Drive(0,0)
                


ip_address = '192.168.128.86'
misty = Robot(ip_address)

movement()