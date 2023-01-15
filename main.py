import crypt
import getopt
import os
import sys
import Algorithms

WELCOME_MSG = "Welcome to a basic single-threaded password cracker program!"
WELCOME_DECORATION = "=============================================================================================" \
                     "=============="
ZERO = 0
TWO = 2
BACK_TO_START = 0


def check_if_root_user():
    if not os.geteuid() == 0:
        sys.exit("[+] ERROR: Only the 'root' user can run this script "
                 "[Please run this script again using sudo command].")


def parse_arguments():
    cleansed_user_list_args = []

    # Remove file name from argument list
    arguments = sys.argv[1:]

    # Getting the file directory from (-f flag) and users (as args)
    opts, user_list_args = getopt.getopt(arguments, 'f:')

    # Check if users are passed in
    check_user_parameters(user_list_args)

    # Check for duplicate users in arguments (prevent cracking duplicate users)
    remove_duplicate_users(cleansed_user_list_args, user_list_args)

    # Get file directory
    for opt, argument in opts:
        if opt == '-f':
            file_directory = argument
            return file_directory, cleansed_user_list_args


def check_user_parameters(user_list):
    if len(user_list) == ZERO:
        sys.exit("[+] No users were passed in as arguments!")


def remove_duplicate_users(cleansed_user_list_args, orig_user_list_args):
    for user in orig_user_list_args:
        if user not in cleansed_user_list_args:
            cleansed_user_list_args.append(user)

    print(f"[+] The following users are to have their passwords cracked: {cleansed_user_list_args}")


def check_if_file_exists(file_dir):
    try:
        if not os.path.exists(file_dir):
            sys.exit("[+] ERROR: File Doesn't Exist or Invalid Argument!")
        else:
            print(f"[+] Now reading the {file_dir} file...")
    except FileNotFoundError:
        sys.exit("[+] ERROR: File Doesn't Exist!")


def display_welcome_msg():
    print(WELCOME_MSG)
    print(WELCOME_DECORATION)


def user_not_found_check():
    if len(selected_user_info) is ZERO and len(user_list_args) >= TWO:
        print(f"\n[+] ERROR: {user} has not been found in {file_directory}! "
              f"Now moving on to the next user...")
    elif len(selected_user_info) is ZERO and len(user_list_args) < TWO:
        print(f"\n[+] ERROR: The last user: '{user}' has not been found in {file_directory}!")


def algorithm_not_found():
    print("[+] ERROR: This algorithm type is not supported!")
    print("[+] Now checking for next user...")


# Main Driver
if __name__ == "__main__":
    display_welcome_msg()
    # check_if_root_user()
    file_directory, user_list_args = parse_arguments()
    check_if_file_exists(file_directory)

    # Reading contents of the file and check if users exist
    file = open(file_directory, 'r')

    # Check if users exist
    for user in user_list_args:
        selected_user_info = ""
        file.seek(BACK_TO_START)
        for entry in file:
            if user == entry.split(':')[0]:
                print(f"\n[+] {user} has been found! Now attempting to determine a suitable hashing algorithm...")
                selected_user_info = entry.split('$')

                # Determine the type of algorithm for user and extract salt
                algorithm = Algorithms.Algorithm()
                if algorithm.algorithm_checker(selected_user_info) == Algorithms.Algorithm.ERROR_CODE:
                    algorithm_not_found()
                    break
                salt = algorithm.extract_salt(selected_user_info[1], entry)
                print(salt)

                # Generate the hash and compare
                password = crypt.crypt("Finalfantasy14-", salt)
                print(f"The hash for '{user}' is {password}")
                break

        user_not_found_check()
        user_list_args = user_list_args[1:]


# Yescrypt Implementation (if "$y$)
# password_hash = crypt.crypt("Finalfantasy14-", salt="$y$j9T$1CfDFTUXt5jy5XeLb/zFq0")

# SHA-256 Hash Implementation - No rounds specified (if "$5$")
# password_hash = crypt.crypt("Finalfantasy14-", salt="$5$JpMWTLY2641Zvdo5")

# SHA-256 w/ specified rounds (if "$5$")
# password_hash = crypt.crypt("Finalfantasy14-", salt="$5$rounds=65536$faeBDKH6Gn6FBdTv")

# SHA-512 Hash Implementation w/ specified rounds (if "$6$)
# password_hash = crypt.crypt("Finalfantasy14-", salt="$6$rounds=65536$9eXQ8Y1U74Zf8ATv")

# SHA-512 (no rounds specified - difference is in the number of $)
# password_hash = crypt.crypt("Finalfantasy14-", salt="$6$vnFrIUOz/grJYx2U")

# MD5 Hash Implementation (if "$1$")
# password_hash = crypt.crypt("Finalfantasy14-", salt="$1$kLZY44Dg")

# BCrypt Hash Implementation (if "$2a$ or $2b$ or $2y$")
# password_hash = crypt.crypt("Finalfantasy14-", salt="$2b$05$7xIm.bug.dew9oh40baZxu8QyOd")
# print(f"Secret Password: {password_hash}\n")




