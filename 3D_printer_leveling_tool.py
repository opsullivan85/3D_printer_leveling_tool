import serial
import json
from rich.console import Console


class Printer3D:
    def __init__(self, ser: serial, positions: list[int]):
        self.ser = ser
        self.positions = positions
        self.position = -1

    def next(self):
        self.position = (self.position + 1) % len(self.positions)
        new_position = self.positions[self.position]

        self.ser.write(f'G0 X{new_position[0]} Y{new_position[1]}')

    def home(self):
        self.ser.write('G28')


def main():
    console = Console()

    try:
        com, baud, positions = json.load(open('config.json', 'r'))  # load points
        ser = serial.Serial(com, baud)

    except json.decoder.JSONDecodeError:
        console.print('Cannot parse config file.\n'
                      'Ensure it is formatted correctly.',
                      style='bold red')
        console.print('Press \[enter] to close this window')
        input()
        return

    except serial.serialutil.SerialException:
        console.print('Cannot connect to 3D printer.\n'
                      'Ensure it is powered on, connected, and the COM port is set correctly in config.json.',
                      style='bold red')
        console.print('Press \[enter] to close this window')
        input()
        return

    printer3D = Printer3D(ser, positions)

    printer3D.home()
    printer3D.next()  # go to first position

    print('press [enter] for next position.')

    while True:
        input('>>> ')
        printer3D.next()


if __name__ == '__main__':
    main()
