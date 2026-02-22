morse_codes = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    " ": " "
}
reversed_morse_codes = {value: key for key, value in morse_codes.items()}

class MorseConverter:

    def __init__(self, type):
        self.type=type
        self.data_income=""
        self.data_outcome=""

    def operate(self, data):
        self.data_income = data
        if self.type == "cipher":
            self.data_outcome = self.cipher()
        else:
            self.data_outcome = self.decipher()
        return self.data_outcome

    def cipher(self):
        output=""
        for c in self.data_income:
            output += morse_codes[c.title()]
        return output


    def decipher(self):
        output = ""
        data = ""
        for c in self.data_income:
            if not c.isspace():
                data += c
            else:
                print(data)
                output += reversed_morse_codes[data]
                output += " "
                data = ""
        output += reversed_morse_codes[data]
        return output