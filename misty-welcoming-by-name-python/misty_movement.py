from mistyPy.Robot import Robot
from mistyPy.Events import Events   
from curtsies import Input

def movement():
    with Input(keynames='curses') as input_generator:
        agVel = 0
        linVel = 0
        misty.MoveHead(0,0,0)
        for e in input_generator:
            if e == 'w':
                agVel =0
                linVel = speed
            if e == 'a':
                agVel = speed
                linVel = 0
            if e == 's':
                agVel = 0
                linVel = -speed
            if e == 'd':
                agVel = -speed
                linVel =0
            if e == 'q':
                agVel = speed
                linVel = speed
            if e == 'e':
                agVel = -speed
                linVel = speed
            if e == 'c':
                agVel = 0
                linVel = 0 
            
            misty.Drive(angularVelocity=agVel,linearVelocity=linVel)


ip_address = '192.168.128.86'
misty = Robot(ip_address)
speed = input('Velocidad: ')

movement()