import struct
import time

import serial

# ser = serial.Serial('/dev/ttyTHS1', 38400, timeout=0.050)  # open serial port
ser = serial.Serial('COM12', 115200, timeout=0.05)  # open serial port
ser.set_buffer_size(rx_size = 100, tx_size = 20)

is_break = True


def hw2complement(numbers):
    mask = 0x8000
    return (
        ((mask&(~numbers))>>15)*(numbers&(~mask)) +
        ((mask&numbers)>>15)*(~(numbers&(~mask))+1)
    )

def rotate(speed):
    start = 0xABCD
    steer = 0
    checksum = start ^ steer ^ speed
    command = (start, steer, speed, checksum)
    command_bytes = struct.pack('<HhhH', start, steer, speed, checksum)
    ser.write(command_bytes)


while is_break:
    #rotate(2)
    #time.sleep(0.001)
    start_byte = ser.read()
    if start_byte:
        if start_byte[0] != 0xCD:
            continue

        s = ser.read(29)
    #   typedef struct{
    #    uint16_t start;
    #    1 int16_t 	cmd1;
    #    2 int16_t 	cmd2;
    #    3 int16_t 	speedR_meas;
    #    4 int16_t 	speedL_meas;
    #    5 int16_t 	batVoltage;
    #    6 int16_t 	boardTemp;
    #    7 uint16_t cmdLed;
    #    uint16_t checksum;
    # } SerialFeedback;
        try:
            feedback = struct.unpack('<BhhhhhhHhhiiH', s)
            cmd1 = feedback[1]
            cmd2 = feedback[2]
            speedR_meas = feedback[3]
            speedL_meas = feedback[4]
            batVoltage = feedback[5]
            boardTemp = feedback[6]
            cmdLed = feedback[7]
            errorR = feedback[8]
            errorL = feedback[9]
            pulseR = feedback[10]
            pulseL = feedback[11]
            chcksum = feedback[12]
            print(
                'cmd1 : ', speedR_meas,
                'cmd2 : ', speedR_meas,
                'speedR_meas : ', speedR_meas,
                #'errorR : ', errorR,
                'speedL_meas : ', speedL_meas,
                #'errorL : ', errorL,
                'batVoltage : ', batVoltage,
                'boardTemp : ', boardTemp,
                'errorR : ', errorL,
                'errorL : ', errorR,
                'pulseR : ', pulseR,
                'pulseL : ', pulseL,
                'chcksum : ', chcksum
            )
        finally:
            pass

ser.close()
