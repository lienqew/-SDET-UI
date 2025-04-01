import random
import string


class CustomerDataGenerator:
    @staticmethod
    def generate_post_code(length=10):
        return ''.join(random.choices(string.digits, k=length))

    @staticmethod
    def generate_first_name(post_code):
        return ''.join(chr(int(digit) + ord('a')) for digit in post_code)

    @staticmethod
    def generate_customer_data():
        post_code = CustomerDataGenerator.generate_post_code()
        first_name = CustomerDataGenerator.generate_first_name(post_code)
        return first_name, "Autotest", post_code
