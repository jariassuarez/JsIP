DS4_BUTTONS = {
    0:  'cross',
    1:  'circle',
    2:  'triangle',
    3:  'square',
    4:  'L1',
    5:  'R1',
    6:  'L2',          # digital (also analog on axis 2)
    7:  'R2',          # digital (also analog on axis 5)
    8:  'share',
    9:  'options',
    10: 'ps',          # ps button in the center
    11: 'L3',          # left stick click
    12: 'R3',          # right stick click
}

DS4_AXES = {
    0: 'left_x',       # left stick  left=-1, right=+1
    1: 'left_y',       # left stick  up=-1,   down=+1
    2: 'L2',      # right stick left=-1, right=+1
    3: 'right_x',      # right stick left=-1, right=+1
    4: 'right_y',      # right stick up=-1,   down=+1
    5: 'R2',           # analog trigger  unpressed=-1, fully pressed=+1
    6: 'dpad_x',       # D-pad left=-1, right=+1
    7: 'dpad_y',       # D-pad up=-1,   down=+1
}

# DS4 button -> Linux key code mapping
DS4_BUTTON_CODES = {
    'cross':    304,  # BTN_SOUTH
    'circle':   305,  # BTN_EAST
    'triangle': 307,  # BTN_NORTH
    'square':   308,  # BTN_WEST
    'L1':       310,  # BTN_TL
    'R1':       311,  # BTN_TR
    'L2':       312,  # BTN_TL2
    'R2':       313,  # BTN_TR2
    'share':    314,  # BTN_SELECT
    'options':  315,  # BTN_START
    'ps':       316,  # BTN_MODE
    'L3':       317,  # BTN_THUMBL
    'R3':       318,  # BTN_THUMBR
}

# DS4 axis -> Linux ABS code mapping
DS4_AXIS_CODES = {
    'left_x':  0x00,  # ABS_X
    'left_y':  0x01,  # ABS_Y
    'L2':      0x02,  # ABS_Z       trigger, -32767 unpressed, +32767 fully pressed
    'right_x': 0x03,  # ABS_RX
    'right_y': 0x04,  # ABS_RY
    'R2':      0x05,  # ABS_RZ      trigger, -32767 unpressed, +32767 fully pressed
    'dpad_x':  0x10,  # ABS_HAT0X   -1 left, +1 right
    'dpad_y':  0x11,  # ABS_HAT0Y   -1 up,   +1 down
}