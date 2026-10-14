hereimport requests

def email_lookup(email):
    print(f"\n[+] Email Lookup: {email}\n")
    print(f"Checking: {email}")
    print(f"Gravatar: https://www.gravatar.com/avatar/{email}")
    print(f"Domain: {email.split('@')[1]}")
    print(f"\n[INFO] Use haveibeenpwned.com to check leaks")
