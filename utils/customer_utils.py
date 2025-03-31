import random

def generate_post_code():
    return ''.join(random.choices('0123456789', k=10))

def post_code_to_first_name(post_code):
    letters = []
    for digit in post_code:
        letter_index = int(digit) % 26
        letters.append(chr(letter_index + ord('a')))
    return ''.join(letters)