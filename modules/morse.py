morse_codes = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    " ": "/"
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
        try:
            output=""
            for c in self.data_income:
                output += morse_codes[c.title()]
                output += " "
            return output
        except:
            return None


    def decipher(self):
        try:
            output = ""
            words = self.data_income.split("/")
            for word in words:
                letters = word.split()
                for letter in letters:
                    deciphered = reversed_morse_codes[letter]
                    output += deciphered
                output += " "
            return output
        except:
            return None