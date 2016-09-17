#!/usr/bin/env python

from bluepy.btle import UUID, DefaultDelegate, Peripheral, BTLEException
import itertools
import serial
import struct
import sys
import time
if sys.version_info >= (3, 0):
    from functools import reduce

ser = serial.Serial()
ser.port = "/dev/ttyUSB0"
ser.baudrate = 9600
ser.open()

#set initial value for number trackers
zone = 1
source = 1
power = 1
volume = 1
z = 1
s = 1
p = 1
v = 1

class NuimoDelegate(DefaultDelegate):

    def __init__(self, nuimo):
        DefaultDelegate.__init__(self)
        self.nuimo = nuimo

    def handleNotification(self, cHandle, data):
        global power, zone, source, volume, z, s, p, v
        if int(cHandle) == self.nuimo.characteristicValueHandles['BATTERY']:
            print('BATTERY', ord(data[0]))

        elif int(cHandle) == self.nuimo.characteristicValueHandles['FLY']:
            print('FLY', ord(data[0]), ord(data[1]))

        elif int(cHandle) == self.nuimo.characteristicValueHandles['SWIPE']:
            #print('SWIPE', ord(data[0]))
            if ord(data[0]) == 0:
                zone += 1
                z = (zone%6)+1
                print "zone: %d" % (z)
                displayInfo("z%d" % (z))
            if ord(data[0]) == 1:
                zone -= 1
                z = (zone%6)+1
                print "zone: %d" % (z)
                displayInfo("z%d" % (z))

            if ord(data[0]) == 2:
                source -= 1
                s = (source%6)+1
                print "source: %d" % (s)
                displayInfo("s%d" % (s))
                sendSerial("<1%sCH0%s\r\n" % (z, s))

            if ord(data[0]) == 3:
                source += 1
                s = (source%6)+1
                print "source: %d" % (s)
                displayInfo("s%d" % (s))
                sendSerial("<1%sCH0%s\r\n" % (z, s))

        elif int(cHandle) == self.nuimo.characteristicValueHandles['ROTATION']:
            value = ord(data[0]) + (ord(data[1]) << 8)
            if value >= 1 << 15:
                value = value - (1 << 16)
            #print('ROTATION', value)
            if value < 0:
                #print "volDown: %d" % (value)
                if volume > 0:
                    volume -= 1
                    print "volume %d" % (volume)
                    displayInfo("vD")
                    sendSerial("<1%sVO0%s\r\n" % (z, volume))
            if value > 0:
                #print "volUp: %d" % (value)
                if volume < 9:
                    volume += 1
                    print "volume %d" % (volume)
                    displayInfo("vU")
                    sendSerial("<1%sVO0%s\r\n" % (z, volume))

        elif int(cHandle) == self.nuimo.characteristicValueHandles['BUTTON']:
            print('BUTTON', ord(data[0]))
            if ord(data[0]) == 0:
                power += 1
                p = (power%2)
                sendSerial("<1%sPR0%s\r\n" % (z, p))
                if p == 0:
                    print "power off"
                    displayInfo("pOff")
                elif p == 1:
                    print "power on"
                    displayInfo("pOn")

def sendSerial(str):
    #this function will send a command over the serial connection
    print str
    ser.write(str)

def displayInfo(str):
    # zones
    if str == "z1":
        nuimo.displayLedMatrix(
            "         " +
            "         " +
            " *** **  " +
            "   *  *  " +
            "  *   *  " +
            " *    *  " +
            " *** *** " +
            "         " +
            "         ", 2.0)
    if str == "z2":
        nuimo.displayLedMatrix(
            "         " +
            "         " +
            " *** *** " +
            "   *   * " +
            "  *  *** " +
            " *   *   " +
            " *** *** " +
            "         " +
            "         ", 2.0)
    if str == "z3":
        nuimo.displayLedMatrix(
            "         " +
            "         " +
            " *** *** " +
            "   *   * " +
            "  *   ** " +
            " *     * " +
            " *** *** " +
            "         " +
            "         ", 2.0)
    if str == "z4":
        nuimo.displayLedMatrix(
            "         " +
            "         " +
            " *** * * " +
            "   * * * " +
            "  *  *** " +
            " *     * " +
            " ***   * " +
            "         " +
            "         ", 2.0)
    if str == "z5":
        nuimo.displayLedMatrix(
            "         " +
            "         " +
            " *** *** " +
            "   * *   " +
            "  *  *** " +
            " *     * " +
            " *** *** " +
            "         " +
            "         ", 2.0)
    if str == "z6":
        nuimo.displayLedMatrix(
            "         " +
            "         " +
            " *** *** " +
            "   * *   " +
            "  *  *** " +
            " *   * * " +
            " *** *** " +
            "         " +
            "         ", 2.0)
#sources
    if str == "s1":
        nuimo.displayLedMatrix(
            "         " +
            "         " +
            "  ** **  " +
            " *    *  " +
            " ***  *  " +
            "   *  *  " +
            " **  *** " +
            "         " +
            "         ", 2.0)
    if str == "s2":
        nuimo.displayLedMatrix(
            "         " +
            "         " +
            "  ** *** " +
            " *     * " +
            " *** *** " +
            "   * *   " +
            " **  *** " +
            "         " +
            "         ", 2.0)
    if str == "s3":
        nuimo.displayLedMatrix(
            "         " +
            "         " +
            "  ** *** " +
            " *     * " +
            " ***  ** " +
            "   *   * " +
            " **  *** " +
            "         " +
            "         ", 2.0)
    if str == "s4":
        nuimo.displayLedMatrix(
            "         " +
            "         " +
            "  ** * * " +
            " *   * * " +
            " *** *** " +
            "   *   * " +
            " **    * " +
            "         " +
            "         ", 2.0)
    if str == "s5":
        nuimo.displayLedMatrix(
            "         " +
            "         " +
            "  ** *** " +
            " *   *   " +
            " *** *** " +
            "   *   * " +
            " **  *** " +
            "         " +
            "         ", 2.0)
    if str == "s6":
        nuimo.displayLedMatrix(
            "         " +
            "         " +
            "  ** *** " +
            " *   *   " +
            " *** *** " +
            "   * * * " +
            " **  *** " +
            "         " +
            "         ", 2.0)
#power
    if str == "pOn":
        nuimo.displayLedMatrix(
            "         " +
            "    *    " +
            "  * * *  " +
            " *  *  * " +
            " *  *  * " +
            " *  *  * " +
            "  *   *  " +
            "   ***   " +
            "         ", 2.0)
    if str == "pOff":
        nuimo.displayLedMatrix(
            "         " +
            "    *  * " +
            "  * * *  " +
            " *  ** * " +
            " *  *  * " +
            " * **  * " +
            "  *   *  " +
            " * ***   " +
            "         ", 2.0)
#volume
    if str == "vD":
        nuimo.displayLedMatrix(
            "         " +
            "   **    " +
            "  * *    " +
            " *  *    " +
            " *  * ***" +
            " *  *    " +
            "  * *    " +
            "   **    " +
            "         ", 2.0)
    if str == "vU":
        nuimo.displayLedMatrix(
            "         " +
            "   **    " +
            "  * *    " +
            " *  *  * " +
            " *  * ***" +
            " *  *  * " +
            "  * *    " +
            "   **    " +
            "         ", 2.0)

class Nuimo:

    SERVICE_UUIDS = [
        UUID('0000180f-0000-1000-8000-00805f9b34fb'), # Battery
        UUID('f29b1525-cb19-40f3-be5c-7241ecb82fd2'), # Sensors
        UUID('f29b1523-cb19-40f3-be5c-7241ecb82fd1')  # LED Matrix
    ]

    CHARACTERISTIC_UUIDS = {
        UUID('00002a19-0000-1000-8000-00805f9b34fb') : 'BATTERY',
        UUID('f29b1529-cb19-40f3-be5c-7241ecb82fd2') : 'BUTTON',
        UUID('f29b1528-cb19-40f3-be5c-7241ecb82fd2') : 'ROTATION',
        UUID('f29b1527-cb19-40f3-be5c-7241ecb82fd2') : 'SWIPE',
        UUID('f29b1526-cb19-40f3-be5c-7241ecb82fd2') : 'FLY',
        UUID('f29b1524-cb19-40f3-be5c-7241ecb82fd1') : 'LED_MATRIX'
    }

    NOTIFICATION_CHARACTERISTIC_UUIDS = [
        #'BATTERY', # Uncomment only if you are not using the iOS emulator (iOS does't support battery updates without authentication)
        'BUTTON',
        'ROTATION',
        'SWIPE',
        'FLY']

    # Notification data
    NOTIFICATION_ON  = struct.pack("BB", 0x01, 0x00)
    NOTIFICATION_OFF = struct.pack("BB", 0x00, 0x00)

    def __init__(self, macAddress):
        self.macAddress = macAddress

    def set_delegate(self, delegate):
        self.delegate = delegate

    def connect(self):
        self.peripheral = Peripheral(self.macAddress, addrType='random')
        # Retrieve all characteristics from desires services and map them from their UUID
        characteristics = list(itertools.chain(*[self.peripheral.getServiceByUUID(uuid).getCharacteristics() for uuid in Nuimo.SERVICE_UUIDS]))
        characteristics = dict((c.uuid, c) for c in characteristics)
        # Store each characteristic's value handle for each characteristic name
        self.characteristicValueHandles = dict((name, characteristics[uuid].getHandle()) for uuid, name in Nuimo.CHARACTERISTIC_UUIDS.items())
        # Subscribe for notifications
        for name in Nuimo.NOTIFICATION_CHARACTERISTIC_UUIDS:
            self.peripheral.writeCharacteristic(self.characteristicValueHandles[name] + 1, Nuimo.NOTIFICATION_ON, True)
        self.peripheral.setDelegate(self.delegate)

    def waitForNotifications(self):
        self.peripheral.waitForNotifications(1.0)

    def displayLedMatrix(self, matrix, timeout, brightness = 1.0):
        matrix = '{:<81}'.format(matrix[:81])
        bytes = list(map(lambda leds: reduce(lambda acc, led: acc + (1 << led if leds[led] not in [' ', '0'] else 0), range(0, len(leds)), 0), [matrix[i:i+8] for i in range(0, len(matrix), 8)]))
        self.peripheral.writeCharacteristic(self.characteristicValueHandles['LED_MATRIX'], struct.pack('BBBBBBBBBBBBB', bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5], bytes[6], bytes[7], bytes[8], bytes[9], bytes[10], max(0, min(255, int(255.0 * brightness))), max(0, min(255, int(timeout * 10.0)))), True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python nuimo.py <Nuimo's MAC address>")
        sys.exit()

    nuimo = Nuimo(sys.argv[1])
    nuimo.set_delegate(NuimoDelegate(nuimo))

    # Connect to Nuimo
    print("Trying to connect to %s. Press Ctrl+C to cancel." % sys.argv[1])
    try:
        nuimo.connect()
    except BTLEException:
        print("Failed to connect to %s. Make sure to:\n  1. Disable the Bluetooth device: hciconfig hci0 down\n  2. Enable the Bluetooth device: hciconfig hci0 up\n  3. Enable BLE: btmgmt le on\n  4. Pass the right MAC address: hcitool lescan | grep Nuimo" % nuimo.macAddress)
        sys.exit()
    print("Connected. Waiting for input events...")

    # Display some LEDs matrices and wait for notifications
    nuimo.displayLedMatrix(
        "         " +
        " ***     " +
        " *  * *  " +
        " *  *    " +
        " ***  *  " +
        " *    *  " +
        " *    *  " +
        " *    *  " +
        "         ", 2.0)
    time.sleep(2)
    nuimo.displayLedMatrix(
        " **   ** " +
        " * * * * " +
        "  *****  " +
        "  *   *  " +
        " * * * * " +
        " *  *  * " +
        " * * * * " +
        "  *   *  " +
        "   ***   ", 20.0)

    try:
        while True:
            nuimo.waitForNotifications()
    except BTLEException as e:
        print("Connection error:", e)
    except KeyboardInterrupt:
        print("Program aborted")
