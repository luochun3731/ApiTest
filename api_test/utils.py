import hashlib
import random
import string


def gen_random_string(str_len):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(str_len)])


def gen_md5(*str_args):
    return hashlib.md5(''.join(str_args).encode('utf-8')).hexdigest()


if __name__ == '__main__':
    print(gen_random_string(8))
