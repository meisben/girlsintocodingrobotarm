from microbit import *
import math
import music

class KitronikRoboticsBoard:
    PRESCALE_REG = 0xFE
    MODE_1_REG = 0x00
    SRV_REG_BASE = 0x08
    MOT_REG_BASE = 0x28
    REG_OFFSET = 4

    chipAddress = 0x6C
    initialised = False
    stepStage = 1
    stepCounter = 0
    stepperSteps = 2000

    def __init(self):
        buf = bytearray(2)

        buf[0] = self.PRESCALE_REG
        buf[1] = 0x85
        i2c.write(self.chipAddress, buf, False)
        
        for blockReg in range(0xFA, 0xFE, 1):
            buf[0] = blockReg
            buf[1] = 0x00
            i2c.write(self.chipAddress, buf, False)

        buf[0] = self.MODE_1_REG
        buf[1] = 0x01
        i2c.write(self.chipAddress, buf, False)
        self.initialised = True

    def motorOn(self, motor, direction, speed):
        if self.initialised is False:
            self.__init(self)
        buf = bytearray(2)
        motorReg = self.MOT_REG_BASE + (2 * (motor - 1) * self.REG_OFFSET)
        HighByte = False
        OutputVal = speed * 40
        
        if direction == "forward":
            if OutputVal > 0xFF:
                HighByte = True
                HighOutputVal = int(OutputVal/256)
            buf[0] = motorReg
            buf[1] = int(OutputVal)
            i2c.write(self.chipAddress, buf, False)
            buf[0] = motorReg + 1
            if HighByte:
                buf[1] = HighOutputVal
            else:
                buf[1] = 0x00
            i2c.write(self.chipAddress, buf, False)
            
            for offset in range(4, 6, 1):
                buf[0] = motorReg + offset
                buf[1] = 0x00
                i2c.write(self.chipAddress, buf, False)
            
        elif direction == "reverse":
            if OutputVal > 0xFF:
                HighByte = True
                HighOutputVal = int(OutputVal/256)
            buf[0] = motorReg + 4
            buf[1] = int(OutputVal)
            i2c.write(self.chipAddress, buf, False)
            buf[0] = motorReg + 5
            if HighByte:
                buf[1] = HighOutputVal
            else:
                buf[1] = 0x00
            i2c.write(self.chipAddress, buf, False)
            
            for offset2 in range(0, 2, 1):
                buf[0] = motorReg + offset2
                buf[1] = 0x00
                i2c.write(self.chipAddress, buf, False)

    def stepperMotorTurnAngle(self, stepper, angle):
        angleToSteps = 0

        if self.initialised is False: 
            self.__init(self)
        
        if angle < 0:
            direction = "reverse"
        else:
            direction = "forward"
        
        angleToSteps = int(((abs(angle) - 1) * (self.stepperSteps - 1)) / (360 - 1) + 1)

        self._turnStepperMotor(self, stepper, direction, angleToSteps)

    def stepperMotorTurnSteps(self, stepper, direction, stepperSteps):
        if self.initialised is False: 
            self.__init(self)

        self._turnStepperMotor(self, stepper, direction, stepperSteps)

    def _turnStepperMotor(self, stepper, direction, steps):
        stepCounter = 0

        while stepCounter < steps:
            if self.stepStage == 1 or self.stepStage == 3:
                if stepper == 0:
                    currentMotor = 1
                else:
                    currentMotor = 3
            else:
                if stepper == 0:
                    currentMotor = 2
                else:
                    currentMotor = 4

            if self.stepStage == 1 or self.stepStage == 4:
                 currentDirection = "forward"
            else:
                currentDirection = "reverse"

            self.motorOn(self, currentMotor, currentDirection, 100)
            sleep(50)

            if direction == "forward":
                if self.stepStage == 4: 
                    self.stepStage = 1
                else:
                    self.stepStage += 1
            elif direction == "reverse":
                if self.stepStage == 1: 
                    self.stepStage = 4
                else:
                    self.stepStage -= 1
            
            stepCounter += 1

def get_turn_angle(current, target, limit):
        diff = target - current
        if abs(diff) > (limit/2):
            return "over limit"
        else: 
            return diff

x = 10
y = 10
current_theta_1 = 0
current_theta_2 = 0
len_1 = 9
len_2 = 9

set_volume(100)

while True:
    theBoard = KitronikRoboticsBoard

    if pin_logo.is_touched():
        music.pitch(200, duration=150, wait=True)
        if math.sqrt(x**2+y**2) > (len_1 + len_2):
            display.scroll("Coord out of range", delay=120, wait=True, loop=False)
        else:
            theta_2 = math.acos((x**2 + y**2 - len_1**2 - len_2**2)/(2*len_1*len_2))
            theta_1 = math.atan2(y,x) - math.atan2((len_2*math.sin(theta_2)),(len_1+len_2*math.cos(theta_2)))
            t_ang_1 = get_turn_angle(current_theta_1, theta_1, math.pi)
            t_ang_2 = get_turn_angle(current_theta_2, theta_2, math.pi*1.5)

            if t_ang_1 == "over limit" or t_ang_2 == "over limit":
                display.scroll("Joint angle limit error", delay=120, wait=True, loop=False)
            else:
                current_theta_1 = theta_1
                current_theta_2 = theta_2
                #display.scroll("%d,%d"%(math.degrees(current_theta_1),math.degrees(current_theta_2)), delay=120, wait=True, loop=False)
                theBoard.stepperMotorTurnAngle(theBoard, 0, math.degrees(t_ang_1))
                theBoard.stepperMotorTurnAngle(theBoard, 1, math.degrees(t_ang_2))
    else:
        if button_a.is_pressed():
            music.pitch(200, duration=150, wait=True)
            y += 1
            if y > 18:
                y = 1
            display.scroll("x=%d,y=%d"%(x,y), delay=100, wait=False, loop=False)
            sleep(350)
        elif button_b.is_pressed():
            music.pitch(200, duration=150, wait=True)
            x += 1
            if x > 18:
                x = 1
            display.scroll("x=%d,y=%d"%(x,y), delay=100, wait=False, loop=False)
            sleep(350)

