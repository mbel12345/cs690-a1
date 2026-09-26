def balanced_delimiters(text):
    pairs = {')': '(', ']': '[', '}': '{'}
    openings = set(pairs.values())
    stack = []

    for char in text:
        if char in openings:
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False

    return not stack
