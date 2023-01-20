import crypt
import itertools

ZERO = 0
START_LENGTH = 1
MAX_CHAR_LENGTH = 9999


def brute_force(salt, user_hash):
    print("[+] Now launching a Brute Force Attack. Please wait...")
    attempts = ZERO

    characters_map = ('!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', "'\'", '/', '.',
                      ',', '<', '>', ':', ':', '{', '}', '[', ']', '|', '"', '\'', '?', '~', '`',
                      '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f',
                      'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                      'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
                      'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                      'W', 'X', 'Y', 'Z', ' ')

    for length in range(START_LENGTH, MAX_CHAR_LENGTH):
        for guess in itertools.product(characters_map, repeat=length):
            attempts += 1
            password = ''.join(guess)

            if crypt.crypt(password, salt) == user_hash:
                print(f"[+] CRACK COMPLETE: Password has been found!")
                return password, attempts

            # print(f"[+] Attempt {attempts}: {password}")


# SOURCE USED: https://stackoverflow.com/questions/40269605/how-to-create-a-brute-force-password-cracker-for-alphabetical-and-alphanumerical