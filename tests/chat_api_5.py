# //////////////////////
# Run codeproduces by Bard
# \\\\\\\\\\\\\\\\\\\\\\


from bardapi import Bard
import requests
import os
token='fAjTeQk3nqTxCtqrj2o7c2KYy7H_kUXYNbNqOERnykbY1FXUFbGvJ5unR-EA3LLNwtwfNw.'
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

  
bard = Bard(token=token, session=session, run_code=True)
bard.get_answer("code a two variable wich produce the addition of two integers of your choise and print the finela result")