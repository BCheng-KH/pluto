#!/usr/bin/env python3

import wpilib
#from wpilib import JoystickButton
from wpilib import RobotController
from wpilib.drive import DifferentialDrive
#from buttons import JoystickButton
#from wpilib.robotcontroller import RobotController




import ctre

import networktables
from networktables import NetworkTables
from networktables import NetworkTablesInstance

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        # Robot initialization function

        # VictorSPX = Motor Controllers
        self.frontLeftMotor = ctre.WPI_VictorSPX(0)
        self.rearLeftMotor = ctre.WPI_VictorSPX(1)

        self.frontRightMotor = ctre.WPI_VictorSPX(4)
        self.rearRightMotor = ctre.WPI_VictorSPX(5)

        self.basketMotor = ctre.WPI_VictorSPX(3)
        
        # Digital Inputs (Limit Switch)
        self.basketLimitSwitch = wpilib.DigitalInput(0)

        # Motor controller groups for each side of the robot
        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        # Differential drive with left and right motor controller groups
        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        self.direction = -1

        # Joysticks & Gamepad
        '''self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.gamepad = wpilib.Joystick(2)'''
        self.gamepad = wpilib.Joystick(0)

        # Joystick buttons
        '''self.leftButton1 = JoystickButton(self.leftStick, 1)
        self.rightButton1 = JoystickButton(self.rightStick, 1)
        self.rightButton3 = JoystickButton(self.rightStick, 3)
        self.rightButton4 = JoystickButton(self.rightStick, 4)'''

        # Gamepad buttons
        '''self.gameButton1 = JoystickButton(self.gamepad, 1)
        self.gameButton2 = JoystickButton(self.gamepad, 2)
        self.gameButton3 = JoystickButton(self.gamepad, 3)
        self.gameButton4 = JoystickButton(self.gamepad, 4)
        self.gameButton5 = JoystickButton(self.gamepad, 5)
        self.gameButton6 = JoystickButton(self.gamepad, 6)'''

        # Solenoids
        self.hatchSolenoid = wpilib.DoubleSolenoid(0, 1)
        self.basketSolenoid = wpilib.DoubleSolenoid(2, 3)

        # Compressor
        self.compressor = wpilib.Compressor(0)

        # Camera Server
        wpilib.CameraServer.launch()

    def autonomousInit(self):
        # Executed at the start of autonomous mode
        
        self.myRobot.setSafetyEnabled(False)

        # Start the compressor running in closed loop control mode
        self.compressor.start()

    def autonomousPeriodic(self):
        # Autonomous Mode(Sandstorm = Identical to TeleOp)

        # If rightButton2 is pressed; change the direction to forward
        if self.gamempad.getPOV() == 0:
            self.direction = -1

        # If rightButton3 is pressed; change the direction to backward
        elif self.gamempad.getPOV() == 180:
            self.direction = 1
        # makes robot go faster or slower
        speedMultiplier = 2
        # Tank drive with left and right sticks' Y axis
        if self.gamempad.getRawAxis(2) > 0.5 or self.gamempad.getRawAxis(3) > 0.5:
            # Use full axis value for full speed
            self.myRobot.tankDrive(self.leftStick.getY() * self.direction * speedMultiplier, self.rightStick.getY() * self.direction * speedMultiplier)
        else:
            # Use half of the axis value for decreased speed
            self.myRobot.tankDrive(self.leftStick.getY() * self.direction * speedMultiplier * 0.5, self.rightStick.getY() * self.direction * speedMultiplier * 0.5)

        # If gameButton5 is pressed; lower the basket
        if self.gamempad.getRawButton(5) and not self.gamempad.getRawButton(6):
            if not self.basketLimitSwitch.get():
                self.basketMotor.set(-1)
            else:
                # If basketLimitSwitch is triggered stop the basket
                self.basketMotor.set(0)
        
        # If gameButton6 is pressed; raise the basket
        elif self.gamempad.getRawButton(6) and not self.gamempad.getRawButton(5):
            self.basketMotor.set(1)

        # Else, leave the basket still
        else:
            self.basketMotor.set(0)

        # If gameButton1 is pressed and gameButton2 is not; push the hatch
        if self.gamempad.getRawButton(1) and not(self.gamempad.getRawButton(2)):
            self.hatchSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        # If gameButton2 is pressed and gameButton1 is not; retract the hatch
        elif self.gamempad.getRawButton(2) and not(self.gamempad.getRawButton(1)):
            self.hatchSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

        # If gameButton3 is pressed and gameButton4 is not; push the basket 
        if self.gamempad.getRawButton(3) and not(self.gamempad.getRawButton(4)):
            self.basketSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        # If gameButton4 is pressed and gameButton3 is not; retract the basket 
        if self.gamempad.getRawButton(4) and not(self.gamempad.getRawButton(3)):
            self.basketSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

    def teleopInit(self):
        # Executed at the start of teleop mode
        
        self.myRobot.setSafetyEnabled(False)

        # Start the compressor running in closed loop control mode
        self.compressor.start()

    def teleopPeriodic(self):
        # TeleOperated mode

        # If rightButton2 is pressed; change the direction to forward
        if self.gamempad.getPOV() == 0:
            self.direction = -1

        # If rightButton3 is pressed; change the direction to backward
        elif self.gamempad.getPOV() == 180:
            self.direction = 1
        # makes robot go faster or slower
        speedMultiplier = 2
        # Tank drive with left and right sticks' Y axis
        if self.gamempad.getRawAxis(2) > 0.5 or self.gamempad.getRawAxis(3) > 0.5:
            # Use full axis value for full speed
            self.myRobot.tankDrive(self.leftStick.getY() * self.direction * speedMultiplier, self.rightStick.getY() * self.direction * speedMultiplier)
        else:
            # Use half of the axis value for decreased speed
            self.myRobot.tankDrive(self.leftStick.getY() * self.direction * speedMultiplier * 0.5, self.rightStick.getY() * self.direction * speedMultiplier * 0.5)

        # If gameButton5 is pressed; lower the basket
        if self.gamempad.getRawButton(5) and not self.gamempad.getRawButton(6):
            if not self.basketLimitSwitch.get():
                self.basketMotor.set(-1)
            else:
                # If basketLimitSwitch is triggered stop the basket
                self.basketMotor.set(0)
        
        # If gameButton6 is pressed; raise the basket
        elif self.gamempad.getRawButton(6) and not self.gamempad.getRawButton(5):
            self.basketMotor.set(1)

        # Else, leave the basket still
        else:
            self.basketMotor.set(0)

        # If gameButton1 is pressed and gameButton2 is not; push the hatch
        if self.gamempad.getRawButton(1) and not(self.gamempad.getRawButton(2)):
            self.hatchSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        # If gameButton2 is pressed and gameButton1 is not; retract the hatch
        elif self.gamempad.getRawButton(2) and not(self.gamempad.getRawButton(1)):
            self.hatchSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

        # If gameButton3 is pressed and gameButton4 is not; push the basket 
        if self.gamempad.getRawButton(3) and not(self.gamempad.getRawButton(4)):
            self.basketSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        # If gameButton4 is pressed and gameButton3 is not; retract the basket 
        if self.gamempad.getRawButton(4) and not(self.gamempad.getRawButton(3)):
            self.basketSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

if __name__ == "__main__":
    wpilib.run(MyRobot)