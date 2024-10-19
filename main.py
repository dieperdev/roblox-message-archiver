import os

from verify_roblosecurity import verify_cookie
from dotenv import load_dotenv

load_dotenv()

roblosecurity = os.environ.get('ROBLOSECURITY')

def main():
    pass

if __name__ == '__main__':
    if not roblosecurity:
        print('A ROBLOSECURITY cookie is required to continue.')

        exit(1)

    cookie_verified = verify_cookie(roblosecurity)

    if not cookie_verified:
        print('You need a valid ROBLOSECURITY cookie to continue.')

        exit(1)

    main()