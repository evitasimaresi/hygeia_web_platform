# //////////////////////
# Archived
# \\\\\\\\\\\\\\\\\\\\\\


from bardapi import Bard
import os
import requests

session = requests.Session()

# os.environ["_BARD_API_KEY"] = "fAjTefHhasd9eHbHNRi0jnxW5zWfbFV6sOdZPjNmqb8Ro1xmfG29pQKv0YuKRo-McgX7IA."
# session.cookies.set("__Secure-1PSID", "fAjTeRE2aWXTYERiRSHMgvwpMliAEkdc6qasPZx1ASFeI6y9VE7X4fv0zwEabL2JeMwZKw.")

bard = Bard(token_from_browser=True, session=session)

res1 = bard.get_answer("Do you like cookies?")
print(res1['content'])

res2 = bard.get_answer("Can you give your faveorte cookie recipe?")
print(res2['content'])