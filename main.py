import struct

import serial

# ser = serial.Serial('/dev/ttyTHS1', 38400, timeout=0.050)  # open serial port
ser = serial.Serial('COM12', 38400, timeout=0.050)  # open serial port

is_break = True


def rotate(speed):
    start = 0xABCD
    steer = 0
    checksum = start ^ steer ^ speed
    command = (start, steer, speed, checksum)
    command_bytes = struct.pack('<HhhH', start, steer, speed, checksum)
    ser.write(command_bytes)


while is_break:
    rotate(60)
    start_byte = ser.read()
    if start_byte[0] != 0xCD:
        continue

    s = ser.read(21)
    #   typedef struct{
    #    uint16_t start;
    #    int16_t 	cmd1;
    #    int16_t 	cmd2;
    #    int16_t 	speedR_meas;
    #    int16_t 	speedL_meas;
    #    int16_t 	errorR;
    #    int16_t 	errorL;
    #    int16_t 	batVoltage;
    #    int16_t 	boardTemp;
    #    uint16_t cmdLed;
    #    uint16_t checksum;
    # } SerialFeedback;
    feedback = struct.unpack('<BhhhhhhhhHH', s)
    cmd1 = feedback[1]
    cmd2 = feedback[2]
    speedR_meas = feedback[3]
    speedL_meas = feedback[4]
    errorR = feedback[5]
    errorL = feedback[6]
    batVoltage = feedback[7]
    cmdLed = feedback[8]
    print(
        'cmd1 : ', speedR_meas,
        'cmd2 : ', speedR_meas,
        'speedR_meas : ', speedR_meas,
        'errorR : ', errorR,
        'speedL_meas : ', speedL_meas,
        'errorL : ', errorL,
        'batVoltage : ', batVoltage)

ser.close()
