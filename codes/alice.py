from pyfirmata import Arduino, util
# import time

board = Arduino('COM7')
it = util.Iterator(board)
it.start()

PIN = board.get_pin('a:0:i')
LED = board.get_pin('d:13:o')
THRESHOLD = 4/1024
bitsRecieved = 0
startedRecording = False
currentValue = False
prevValue = False
MAXVALUES = 3000
bits = []

def bits_to_string(bits):
    return ''.join(map(lambda x: "1" if x else "0", bits))

while True:
    val = PIN.read()
    currentValue = val > THRESHOLD
    if currentValue and not prevValue:

        if startedRecording:
            bitsRecieved += 1
            print(bitsRecieved)
            bits.append(onesRead > valuesRead/2)
            if bitsRecieved == MAXVALUES:
                print(bits_to_string(bits))
                completed = True
                break

        startedRecording = True
        LED.write(1)
        valuesRead = 0
        onesRead = 0

    if startedRecording:
        valuesRead += 1
        if currentValue:
            onesRead += 1
