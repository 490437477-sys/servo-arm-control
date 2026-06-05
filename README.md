# Servo Arm Control System

User Manual for Arduino & Python GUI

## 1. Product Overview

This software controls a 5-servo robotic arm using joysticks or serial commands. Compatible with Arduino UNO and similar boards.

## 2. Safety Warning

### Power Supply
- After uploading code, switch from USB to external power supply
- Use 5V 1A or higher power adapter
- This ensures stable operation for board and servos

### Overload Protection
- Do not apply excessive force when grasping objects
- If servo stalls, current increases sharply
- Overcurrent will trigger board protection and restart

## 3. Pin Definition

### Joystick Pins
| Control | Pin | Description |
|---------|-----|-------------|
| Joystick 1 X-axis | A0 | Analog Pin 0 |
| Joystick 1 Y-axis | A1 | Analog Pin 1 |
| Joystick 1 Button | D2 | Digital Pin 2 |
| Joystick 2 X-axis | A3 | Analog Pin 3 |
| Joystick 2 Y-axis | A2 | Analog Pin 2 |
| Joystick 2 Button | D4 | Digital Pin 4 |

### Servo Pins
| Servo | Pin | Description |
|-------|-----|-------------|
| Servo 0 | D5 | Digital Pin 5 |
| Servo 1 | D9 | Digital Pin 9 |
| Servo 2 | D10 | Digital Pin 10 |
| Servo 3 | D11 | Digital Pin 11 |
| Servo 4 | D7 | Digital Pin 7 |
| LED | D3 | Digital Pin 3 |

## 4. Control Logic

| Control | Pin | Servo | Range |
|---------|-----|-------|-------|
| Joystick 1 X | A0 | Servo 0 | 0-180 deg |
| Joystick 1 Y | A1 | Servo 1 | 0-180 deg |
| Joystick 1 Button | D2 | Servo 4 | 0-90 deg |
| Joystick 2 X | A3 | Servo 2 | 0-180 deg |
| Joystick 2 Y | A2 | Servo 3 | 0-180 deg |
| Joystick 2 Button | D4 | Servo 4 | 0-90 deg |

### Button Control
- Joystick 1 Button: Servo 4 +2 deg per press (max 90 deg)
- Joystick 2 Button: Servo 4 -2 deg per press (min 0 deg)

## 5. Arduino Setup

1. Open `servo_control.ino` in Arduino IDE
2. Select your board (Arduino UNO/Nano)
3. Select correct port
4. Upload the sketch
5. Open Serial Monitor (9600 baud)

## 6. Serial Commands

| Command | Description |
|---------|-------------|
| `0 90` | Set Servo0 to 90 degrees (0-180) |
| `1 45` | Set Servo1 to 45 degrees (0-180) |
| `2 180` | Set Servo2 to 180 degrees (0-180) |
| `3 90` | Set Servo3 to 90 degrees (0-180) |
| `4 60` | Set Servo4 to 60 degrees (0-90) |
| `90` | Set ALL servos to 90 degrees |
| `90 90 90 90 90` | Batch set all servos |

### Example
```
> 0 90
S0:90
```

## 7. Python GUI Setup

1. Install Python 3.x
2. Install pyserial: `pip install pyserial`
3. Run: `python servo_control.py`
4. Select COM port and click Connect
5. Use sliders or enter values to control servos

## 8. Support

GitHub: https://github.com/490437477-sys/servo-arm-control
