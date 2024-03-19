# //////////////////////
# Archived
# \\\\\\\\\\\\\\\\\\\\\\


from bardapi import Bard
import os
import requests
# from dotenv import load_dotenv()

token="fAjTeT70rx8bVuPYCCbPXE6athMtl_yy010TSmmC7YN5A3P8t4-Do18tL_cbLn0spJIyPA."

# This enables ongoing conversation with Bard in separate queries
session = requests.Session()
session.headers = {
    "Host": "bard.google.com",
    "X-Same-Domain": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://bard.google.com",
    "Referer": "https://bard.google.com/",
}
session.cookies.set("__Secure-1PSID", os.getenv(token)) 
session.cookies.set("__Secure-1PSIDTS", os.getenv("sidts-CjEBPVxjStWvAhyYkv5MgA2mebjsaK1URAYT6hMjBlBg-K2yTFhUgk638cC_kG0yVFA2EAA"))
session.cookies.set("__Secure-1PSIDCC", os.getenv("ABTWhQE4EVm8kWT_U_a2Lj4MVRMp1miMYCyexFjik0X8QpTKdMmhmgoul6s2GTEZFw_IWrdD"))
bard = Bard(token=token, session=session)
response = bard.get_answer("I am from Peru")['content']
# do something with response
# By using the session we continue chatting without passing the chat-log
response = bard.get_answer("What is my last prompt??")['content']
print(response)
print("-------------------------")