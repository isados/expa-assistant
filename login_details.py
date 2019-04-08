import base64
import json
import os
from getpass import *

secret_file = 'secret.txt'

def _encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string.encode()).decode()

def _decode(key, encoded_string):
    string = base64.urlsafe_b64decode(encoded_string.encode()).decode()
    decoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        decoded_c = chr(ord(string[i]) - ord(key_c) % 256)
        decoded_chars.append(decoded_c)
    decoded_string = "".join(decoded_chars)
    return decoded_string

def read_login_details(passcode, path = secret_file):
    with open(path, 'r') as file:
        loaded_json = json.load(file)
    loaded_json['email_pwd'] = _decode(passcode, loaded_json['email_pwd'])
    loaded_json['expa_pwd'] = _decode(passcode, loaded_json['expa_pwd'])

    return loaded_json

def create_login_file(login_details:dict, key:str, path:str = secret_file):
    login_details['email_pwd'] = _encode(key, login_details['email_pwd'])
    login_details['expa_pwd'] = _encode(key, login_details['expa_pwd'])

    if os.path.exists(path):
        choice = input('Would you like to overwrite the existing login details (y/n):').strip().lower()
        if choice != 'y':
            print('Fine then, goodbye :)')
    else:
        with open(path, 'w') as file:
            json.dump(login_details, file)
        print(f"Login details written to '{path}'")

def verify_passcode_get_details():
    passcode = input('\nEnter your PASSCODE:')
    print()
    details = read_login_details(passcode)
    return details

if __name__ == '__main__':
    pass
    # play_welcome_message()
    # key = 'secret_key'
    # login_details = {
    # 'email': 'isa.aldoseri@aiesec.net',
    # 'email_pwd' : 'nerds100',
    # 'expa_username' : 'isadosry@gmail.com',
    # 'expa_pwd' : 'jij'
    # }
    #
    #
    #
    # create_login_file(login_details, key)
    #
    # loaded = read_login_details(key)
    #
    # print(loaded)
