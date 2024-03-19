# //////////////////////
# Archived
# \\\\\\\\\\\\\\\\\\\\\\


from bardapi import Bard
import os
import time

import requests
from bardapi.constants import SESSION_HEADERS

import re
# config
# The key is the value from __Secure-1PSID from the cookies
os.environ[
    "_BARD_API_KEY"
] = "fAjTecXgT0QO2HNyBIqs618KiDkUoE8Pv11cpwUbyEM99dMjSvudt9vKwdD6C82JhZHBJg."

# Extract attempt 1st
def search_doctor(response):
    """Search the docotr from the text"""
    # Define the regex pattern
    pattern = r"\*\*(.*?)\*\*"

    # Use re.search() to find the first occurrence of the pattern
    match = re.search(pattern, response)

    if match:
        word = match.group(1) # Extract the matched group
        print(f"The word between the asterisks is: {word}")
    else:
        print("There is no word between asterisks in the text.")

# Try 1
"""
input = "I feel a mild pain on my chest, it feels like its coming from my stomach, I dont have a lot of appetite. What doctor should I consult?"
print(Bard().get_answer(input)["content"])
"""


# Try 2
# patient_input=input("Describe your helath state and your symptoms: ")

# promt = f""" Your task is to act as medical advisor.
#     You will get a description of a patient on its general health and any syptoms the patient has.
#     And your job is to give advise on which doctor the patient should make an appointment, also you will  provide a few tips for getting the best possible care.
#     Start your reply with the following sentence: The recommended doctor for you to consult is: <category of doctor>. Then give the tips.
#     ```{patient_input}```
#     """

# def get_completitoin(promt):
#     response = Bard().get_answer(promt)["content"]
#     return response

# response= get_completitoin(promt)
# print(response)
# search_doctor(response)


# Try 3
# try:
while True:
    user_input=input('\U0001F4E3 You: ')
    print('')
    print('\U0001F4E5 Bot: ', Bard().get_answer(user_input.strip())["content"])
    print('-'*100, "\n")
# except KeyboardInterrupt:
#     print('Ended Chat!')
# except:
#     print('Ended Chat!')
