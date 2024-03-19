# //////////////////////
# Maintain a chat
# \\\\\\\\\\\\\\\\\\\\\\


from bardapi import Bard
import requests
import os
import re

import json
import sys

# Config
token = "a000fwjTecdyaxI645qqoBEBqf9CI-y1c59Ihp0OhnJFubGNIjcORSUHM8QSrz6Ouv9WE8ToIQACgYKAccSAQASFQHGX2MiN4prc_YG6CSsEaE78OGKHxoVAUF8yKq4awqKb0tdHQtWOOleE3EO0076." #__Secure-1PSID

os.environ["_BARD_API_KEY"] = token
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

bard = Bard(token=token, session=session, timeout=30)

def get_description(item):
    with open('tests/descriptions.json', 'r') as file:
        descriptions = json.load(file)
    return descriptions[item]

def get_response(promt):
    response = bard.get_answer(promt)["content"]
    return response


# patient_input = input("Describe your helath state and your symptoms: ")
patient_input = get_description(int(sys.argv[1]))

promt = f"""You are a medical advisor. You have knowledge about types of doctors, health symptoms, and other relevant information. Always answer with the goal of suggest a relevant medical specialist related to the symptoms described. The answer should be no more than 100 words.
Respond to the following:

"{patient_input}" """

print(f'\U0001F4E3 You: {promt}')
print('-'*100, "\n")

response = get_response(promt)
print(f'\U0001F4E5 Bot: {response}')
print('-'*100, "\n")

response_doctor = get_response("Return the type of doctor suggested, no more words. If more than one return them separated by coma.")
print(f'\U0001F4E5 Bot: {response_doctor}')

response_tips = get_response("Give some tips for preparing before the appointment. The answer should be no more than 100 words.")
print(f'\U0001F4E5 Bot: {response_tips}')
