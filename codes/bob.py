from pyfirmata import Arduino
import time


board = Arduino('COM3')
LED = board.get_pin('d:13:o')
DURATION = 0.01 # length of one bit in seconds
PAUSE = DURATION/10  # length of pause to ensure uniformity


def one_bit(LED, bit):
    print("1" if bit else "0", end = "")
    n = int (DURATION // PAUSE) + 1
    arr =  [1] * (3*n//4) + [0] * (n//4 + 1) if bit else [1] * (n//4 + 1) + [0] * (3*n//4)
    for i in arr:
        LED.write(i)
        time.sleep(PAUSE)
        
def string_to_binary(input_string):
    binary_string = "00001"
    for char in input_string:
        # Convert the character to its ASCII value and then to an 8-bit binary string
        binary_char = format(ord(char), '08b')
        binary_string += binary_char
    return binary_string

def send(string):
    for char in string:
        one_bit(LED, char == "1")

while True:
    text = input("\nEnter text to send: ")
    binary = string_to_binary(text)
    to = time.time()
    send(binary)
    print(f"\nTime taken: {(time.time() - to):.2f} s")