'''
struct js_event {
        __u32 time;     /* event timestamp in milliseconds */
        __s16 value;    /* value */
        __u8 type;      /* event type */
        __u8 number;    /* axis/button number */
};

js file has this format according to https://www.kernel.org/doc/html/latest/input/joydev/joystick-api.html
uint32, int16, uint8, uint8 = 8 bytes

#define JS_EVENT_BUTTON         0x01    /* button pressed/released */
#define JS_EVENT_AXIS           0x02    /* joystick moved */
#define JS_EVENT_INIT           0x80    /* initial state of device */

'''

import struct
import threading
import socket

JS_EVENT_FORMAT = '=IhBB'
JS_EVENT_SIZE = struct.calcsize(JS_EVENT_FORMAT)

PACKET_FORMAT = '=HIhBB'

class JoystickSender:
    def __init__(self, device, host, port):
        self.device = device
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self._seq = 0

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def _next_seq(self):
        seq = self._seq
        self._seq = (self._seq + 1) % 65536
        return seq

    def _run(self):
        with open(self.device, 'rb') as js:
            while not self.stop_event.is_set():
                data = js.read(JS_EVENT_SIZE)
                if len(data) < JS_EVENT_SIZE:
                    break
                time, value, type_, number = struct.unpack(JS_EVENT_FORMAT, data)
                packet = struct.pack(PACKET_FORMAT, self._next_seq(), time, value, type_, number)
                self.sock.sendto(packet, self.addr)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()
        self.sock.close()

if __name__ == '__main__':
    # As a context manager (recommended)
    with JoystickSender('/dev/input/js0', '127.0.0.1', 5005) as sender:
        input("Press Enter to stop...\n")