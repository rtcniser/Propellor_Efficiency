from pyfirmata import Arduino
import time

board = Arduino('COM7')
LED = board.get_pin('d:13:o')
DURATION = 2  # length of one bit in seconds
PAUSE = 0.2  # length of pause to ensure uniformity


def one_bit(LED, bit):
    n = DURATION // PAUSE
    arr =  [1] * (3*n//4) + [0] * (n//4 + 1) if bit else [1] * (n//4 + 1) + [0] * (3*n//4)
    for i in arr:
        LED.write(i)
        time.sleep(PAUSE)
        
def string_to_binary(input_string):
    binary_string = ""
    for char in input_string:
        # Convert the character to its ASCII value and then to an 8-bit binary string
        binary_char = format(ord(char), '08b')
        binary_string += binary_char
    return binary_string

def send(string):
    for char in string:
        one_bit(LED, char == "1")

while True:
    text = input("Enter text to send: ")
    binary = string_to_binary(text)
    send(binary)