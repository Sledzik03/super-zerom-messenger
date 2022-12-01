msg = "teksgfgjghkfhjkt"


def encrypt(plaintext):
    cipher_text = ""

    for letter in plaintext:
        letter_code = ord(letter)
        new_letter_code = letter_code + 3000
        new_letter = chr(new_letter_code)
        cipher_text += new_letter
    return cipher_text


def decrypt(plaintext):
    cipher_text = ""

    for letter in plaintext:
        letter_code = ord(letter)
        new_letter_code = letter_code - 3000
        new_letter = chr(new_letter_code)
        cipher_text += new_letter
    return cipher_text


print(encrypt(msg))
read = encrypt(msg)
print("")
print(decrypt(read))
