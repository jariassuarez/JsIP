import struct
import os
import time as _tm

# Format: uint32, int16, uint8, uint8 = 8 bytes
EVENT_FORMAT = 'IhBB'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)  # = 8

JS_EVENT_BUTTON = 0x01
JS_EVENT_AXIS   = 0x02
JS_EVENT_INIT   = 0x80



def read_joystick(device='/dev/input/js0'):
    with open(device, 'rb') as js:
        while True:
            data = js.read(EVENT_SIZE)
            if len(data) < EVENT_SIZE:
                break

            time, value, type_, number = struct.unpack(EVENT_FORMAT, data)

            # Mask out the init flag
            is_init = bool(type_ & JS_EVENT_INIT)
            type_ &= ~JS_EVENT_INIT

            if type_ == JS_EVENT_BUTTON:
                print(f"Button {number}: {'pressed' if value else 'released'}"
                      f"{' (init)' if is_init else ''}")
            elif type_ == JS_EVENT_AXIS:
                print(f"Axis   {number}: {value:+6d}"
                      f"{' (init)' if is_init else ''}")
                

read_joystick()