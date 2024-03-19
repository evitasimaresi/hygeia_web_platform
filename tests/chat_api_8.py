# //////////////////////
# Archived
# \\\\\\\\\\\\\\\\\\\\\\
#  Isude run:  export $(dbus-launch) before run the script


import requests
import browser_cookie3
from http.cookiejar import MozillaCookieJar

# Specify the profile
cookie_file = '/mnt/c/Users/evita/AppData/Local/Google/Chrome/User Data/Default/Network/Cookies'

url = 'https://bard.google.com/'
print(url)

# Get cookies for a specific domain
cj = browser_cookie3.chrome(domain_name='bard.google.com', cookie_file=cookie_file)

# Print all cookies
for cookie in cj:
    print(f"-------- cj: {cj} --------")


