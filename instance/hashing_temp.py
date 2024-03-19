from werkzeug.security import generate_password_hash

passwords = ["chloe123", "eric456", "lisa789", "ryan123", "zoe456"]
# passwords = ["alice123", "bob456", "emma789", "max123", "sara456", "marina90"]

for index, password in enumerate(passwords):
    hashed = generate_password_hash(password)
    print(f"{index}, Initial password: {password} hashed to: {hashed}")