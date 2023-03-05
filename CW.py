import serial
from serial import Serial
import time

# Set the COM port and baud rate for the USB to CI-V interface
com_port = 'COM3'
baud_rate = 9600

# Set the Morse code dictionary
morse_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..',
    "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.',
    '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
    ' ': ' '
}

def morse_encode(text):
    morse_code = ''
    for char in text:
        if char.upper() in morse_dict:
            morse_code += morse_dict[char.upper()] + ' '
    return morse_code.strip()

def morse_decode(morse_code):
    text = ''
    for code in morse_code.split():
        for k, v in morse_dict.items():
            if v == code:
                text += k
                break
        else:
            text += '?'
    return text

# Connect to the USB to CI-V interface
ser = Serial(com_port, baud_rate)

# Set the CI-V address of the radio
address = '01'

# Set the delay between characters (in seconds)
delay = 0.1

while True:
    # Get input from the user
    input_text = input('Enter text to send as Morse code: ')

    # Encode the input text as Morse code
    morse_code = morse_encode(input_text)

    # Send the Morse code to the radio
    for code in morse_code:
        if code == '.':
            ser.write(bytes.fromhex(f'{address} 8E'))
        elif code == '-':
            ser.write(bytes.fromhex(f'{address} 8F'))
        else:
            time.sleep(delay)

    # Wait for the transmission to finish
    time.sleep(delay)

    # Receive Morse code from the radio
morse_rx = ''
while True:
    # Read the next character from the radio
    char = ser.read()

    # Check if the character is the end of message character
    if char == b'\xFE':
        break

    # Decode the character as Morse code
    if char == b'\x8E':
        morse_rx += '.'
    elif char == b'\x8F':
        morse_rx += '-'
    else:
        # Ignore any other characters
        pass

# Decode the received Morse code
rx_text = morse_decode(morse_rx)

# Print the decoded text
print(f'Received text: {rx_text}')
