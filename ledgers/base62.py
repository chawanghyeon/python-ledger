BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base62_encode(number: int) -> str:
    if number == 0:
        return "0"

    base62 = []
    while number > 0:
        number, remainder = divmod(number, 62)
        base62.append(BASE62_ALPHABET[remainder])

    return "".join(reversed(base62))


def base62_decode(base62_string: str) -> int:
    number = 0
    for char in base62_string:
        number = number * 62 + BASE62_ALPHABET.index(char)

    return number
