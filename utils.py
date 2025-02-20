import json
import os

PASSWORD_FILE='password.json'

def read_data():
    try:
        with open(PASSWORD_FILE,'r') as file:
            data=json.load(file)
    except Exception as e:
        return []

    return data

def write_data(data):
     with open(PASSWORD_FILE,'w') as file:
        json.dump(data,file,indent=4)

             