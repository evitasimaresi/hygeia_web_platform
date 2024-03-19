# //////////////////////
# Archived
# \\\\\\\\\\\\\\\\\\\\\\


from bardapi import Bard
import os
import requests
from urllib.request import urlopen, build_opener, HTTPCookieProcessor
import browser_cookie3
import re
import requests


# os.environ["_BARD_API_KEY"] = "fAjTefHhasd9eHbHNRi0jnxW5zWfbFV6sOdZPjNmqb8Ro1xmfG29pQKv0YuKRo-McgX7IA."
# session.cookies.set("__Secure-1PSID", "fAjTeRE2aWXTYERiRSHMgvwpMliAEkdc6qasPZx1ASFeI6y9VE7X4fv0zwEabL2JeMwZKw.")

# extract the title from a webpage
get_title = lambda html: re.findall('<title>(.*?)</title>', html, flags=re.DOTALL)[0].strip()
print(get_title)

url = 'https://bard.google.com/'
print(url)

cj = browser_cookie3.chrome(domain_name=url)

opener = build_opener(HTTPCookieProcessor(cj))

login_html = opener.open(url).read()

get_title(login_html)

r = requests.get(url, cookies=cj)
print(f"-------- r: {r} --------")






# session = requests.Session()

# bard = Bard(token_from_browser=True, session=session)

