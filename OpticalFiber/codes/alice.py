from pyfirmata import Arduino, util
import time
import numpy as np

board = Arduino('COM14')
it = util.Iterator(board)
it.start()

def binary_to_string(binary_string):
    # Initialize an empty string to store the result
    result_string = ""

    # Iterate through the binary string in 8-character chunks
    for i in range(0, len(binary_string), 8):
        # Extract each 8-character chunk
        binary_char = binary_string[i:i + 8]

        # Convert the binary chunk to an integer
        char_code = int(binary_char, 2)

        # Convert the integer to its ASCII character and append it to the result string
        result_string += chr(char_code)

    return result_string

def check1(strings, min_length):
    merged_strings = []
    i = 0
    while i < len(strings) - 1:
        # print(i)
        current_string = strings[i]
        if len(current_string) < min_length:
            if current_string.startswith("0"):  # add with previous
                # print("add with previous")
                merged_strings[-1] += current_string
            else:  # add with next
                # print("add with next")
                merged_strings.append(current_string + strings[i + 1])
                i += 1
        else:
            merged_strings.append(current_string)
        i += 1
    return merged_strings


PIN = board.get_pin('a:0:i')
LED = board.get_pin('d:13:o')
THRESHOLD = 4/1024
stop_n = 10_000
bits = ""
PAUSE = 0
started_reading = False

while PIN.read() is None: continue
print("Ready")


# Reading values
while True:
    val = PIN.read()
    currentValue = val > THRESHOLD
    if currentValue and not started_reading:
        started_reading = True
        print("\nStarted Recieving!\n") 
    this_bit = "1" if currentValue else "0"
    print(this_bit, end="", flush=True)
    bits += this_bit
    time.sleep(PAUSE)
    if started_reading and bits[-stop_n:] == "0" * stop_n:
        print("\nCompleted Recieving!\n")
        break

bits = bits[:-stop_n]
reading = bits.split("0011")[1:]
lengths = list(map(len, reading))
mean_length = sum(lengths) / len(lengths)
print("Mean length:", mean_length)
# fill last bit with zeros if it is too short
reading[-1] += "0" * (int(mean_length) - len(reading[-1]))
print(*reading, sep="\n")

# if len(reading) % 8:  # if not divisible by 8
#     print("Error: Not divisible by 8... trying to fix")
#     reading = check1(reading, int(mean_length)-8)
#     if len(reading) % 8:
#         print("could not fix")
#     else:
#         print("fixed")
    

interprets = ""
for reading in reading:
    ones = reading.count("1")
    if ones > len(reading) / 2:
        interprets += "1"
    else:
        interprets += "0"
print("\n")

interprets = interprets.lstrip("0")[1:]

if len(interprets) % 8 == 7:  # if one bit short
    print("Error: One bit short... trying to fix")
    interprets = interprets + "0"




print(interprets)
# interprets = "0110011101100001011011100110010001110101"
print(binary_to_string(interprets))





# int val;
# int threshold = 4;

# void setup() {
#   // put your setup code here, to run once:
#   pinMode(A0, INPUT);
#   Serial.begin(9600);
# }

# void loop() {
#   // put your main code here, to run repeatedly:
#   if (analogRead(A0) >= threshold){
#     Serial.println(1);
#   }else{
#     Serial.println(0);
#   }
#   delay(10);
# }

# 1111111100000000000000000000000000000000
# 1111111111111111111111111110000000000000
# 1111111111111111111111111110000000000000
# 1111111111110000000000000000000000000000
# 1111111111110000000000000000000000000000
# 1111111111110000000000000000000000000000
# 1111111111110000000000000000000000000000
# 1111111111111111111111111110000000000000

# 01100001