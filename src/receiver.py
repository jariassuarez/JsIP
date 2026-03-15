import struct
import threading
import socket

from mappings import DS4_BUTTONS, DS4_AXES, DS4_BUTTON_CODES, DS4_AXIS_CODES
from virtual import VirtualDS4

PACKET_FORMAT = '=HIhBB'
PACKET_SIZE = struct.calcsize(PACKET_FORMAT)

JS_EVENT_BUTTON = 0x01
JS_EVENT_AXIS   = 0x02
JS_EVENT_INIT   = 0x80


class JoystickReceiver:
    def __init__(self, host, port, virtual_device):
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.virt = virtual_device

    def start(self):
        self.sock.bind(self.addr)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.sock.close()
        self.thread.join()

    def _on_event(self, seq, time, value, type_, number):
        is_init = bool(type_ & JS_EVENT_INIT)  # check BEFORE masking
        type_ &= ~JS_EVENT_INIT

        if type_ == JS_EVENT_BUTTON:
            self._on_button(seq, time, number, pressed=bool(value), init=is_init)
        elif type_ == JS_EVENT_AXIS:
            self._on_axis(seq, time, number, value, init=is_init)

    def _on_button(self, seq, time, number, pressed, init):
        name = DS4_BUTTONS.get(number)
        if name and name in DS4_BUTTON_CODES:
            self.virt.send_button(name, pressed)
        else:
            print(f"[warn] unmapped button number: {number}")

    def _on_axis(self, seq, time, number, raw, init):
        name = DS4_AXES.get(number)
        if name and name in DS4_AXIS_CODES:
            self.virt.send_axis(name, raw)
        else:
            print(f"[warn] unmapped axis number: {number}")

    def _run(self):
        while not self.stop_event.is_set():
            try:
                data, _ = self.sock.recvfrom(PACKET_SIZE)
                if len(data) < PACKET_SIZE:
                    continue
                seq, time, value, type_, number = struct.unpack(PACKET_FORMAT, data)
                self._on_event(seq, time, value, type_, number)
            except OSError:
                break  # socket was closed

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


if __name__ == '__main__':
    with VirtualDS4() as virt:
        with JoystickReceiver('127.0.0.1', 5005, virt) as receiver:
            input("Listening... press Enter to stop.\n")