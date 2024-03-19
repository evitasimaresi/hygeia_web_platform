# //////////////////////
# Maintain a chat
# \\\\\\\\\\\\\\\\\\\\\\


from bardapi import Bard
import requests
import os
token='fAjTeQAJyBwq2lyGTW3-7jpXvtOysSb8DAeIq20eq418E0fID6E1RYRsVUkRIS9VfS5xgA.'
os.environ['_BARD_API_KEY'] = token

session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY")) 
# session.cookies.set("__Secure-1PSID", token) 

bard = Bard(token=token, session=session, timeout=30)
response1 = bard.get_answer("Do you like cookies?")['content']
print(response1)
# Continued conversation without set new session
response2 = bard.get_answer("Giveme you best recipy")['content']
print(response2)