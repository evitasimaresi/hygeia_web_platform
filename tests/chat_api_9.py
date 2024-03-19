# //////////////////////
# Archived
# \\\\\\\\\\\\\\\\\\\\\\


"""
from bardapi import Bard
import os
from dotenv  import load_dotenv

load_dotenv()
token = os.getenv("BARD_API_KEY")
print(f"--------------------- token: {token} ---------------------")

bard = Bard(token=token)

result = bard.get_answer("How to say hello formaly?")
print(result)
"""



import requests
"""
r = requests.post('https://bard.google.com/')
for cookie in r.cookies:
    print(cookie.__dict__)
    print(cookie.secure)
"""

session = requests.Session()
response = session.get('https://bard.google.com/')
print(session.cookies)