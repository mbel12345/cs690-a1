def is_palindrome_normalized(text):
    normalized = [
        character.lower()
        for character in text
        if ("A" <= character <= "Z") or ("a" <= character <= "z") or ("0" <= character <= "9")
    ]
    return normalized == normalized[::-1]
