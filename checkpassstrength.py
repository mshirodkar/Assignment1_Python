import re

def check_password_strength(password):
    """
    Check if the given password meets the security criteria:
    - At least 8 characters long
    - Contains both uppercase and lowercase letters
    - Contains at least one digit
    - Contains at least one special character
    Returns True if all conditions are met, otherwise False.
    """
    if len(password) < 8:
        return False

    if not re.search(r'[A-Z]', password):
        return False

    if not re.search(r'[a-z]', password):
        return False

    if not re.search(r'\d', password):
        return False

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True


# --- Main script ---
def main():
    password = input("Enter your password to check its strength: ")

    if check_password_strength(password):
        print("Your password is strong.")
    else:
        print("Your password is weak. Make sure it meets the following criteria:")
        print("   - At least 8 characters long")
        print("   - Contains both uppercase and lowercase letters")
        print("   - Contains at least one digit (0-9)")
        print("   - Contains at least one special character (e.g., !, @, #, $)")

if __name__ == "__main__":
    main()
