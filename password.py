import os
import json
from argon2 import PasswordHasher
from getpass import getpass
import time

MASTER_FILE='master.json'

ph=PasswordHasher()


def setup_master_password():
    if not os.path.exists(MASTER_FILE):
        print("🔒 First-time setup : Create a master password.")
        master_password=getpass("Enter a master password  :")
        hashed_password=ph.hash(master_password)
        try:
            data={
                'master_password':hashed_password
            }
            
            with open(MASTER_FILE,'w') as file:
                json.dump(data,file,indent=4)
            
            print("\n✅ Master Password set successfully")
        except Exception as e:
            print(f"Error occured : {e}")
    else:
        verify_master_password()



def verify_master_password():
    try:
        with open(MASTER_FILE,'r') as file:
            data=json.load(file)
            stored_password=data['master_password']
    except Exception as e:
        print(f"Error occured {e}")
        
    while True:
        entered_password=getpass("🔑 Enter the Master Password : ")
        try:
            if ph.verify(stored_password,entered_password):
                print("✅ Access Granted.")
        except Exception as e:
            print("❌ Password is incorrect! Please try again.")


    