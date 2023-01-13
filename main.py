import crypt
import getopt
import os
import sys
import passlib.hash
from pyescrypt import pyescrypt


def check_if_root_user():
    if not os.geteuid() == 0:
        sys.exit("[+] ERROR: Only the 'root' user can run this script "
                 "(Please run this script with sudo)...\n")


def parse_arguments():
    # Remove file name from argument list
    arguments = sys.argv[1:]

    # Getting the file directory from (-f flag) and users (as args)
    opts, user_list_args = getopt.getopt(arguments, 'f:')

    for opt, argument in opts:
        if opt == '-f':
            file_directory = argument
            print(file_directory)
            return file_directory, user_list_args


def check_if_file_exists():
    # Check if path/file exists
    try:
        if not os.path.exists(file_directory):
            sys.exit("[+] ERROR: File Doesn't Exist!\n")
        else:
            print("File Exists!\n")
    except FileNotFoundError:
        sys.exit("[+] ERROR: File Doesn't Exist!\n")


# Main Driver
if __name__ == "__main__":
    # check_if_root_user()
    file_directory, user_list_args = parse_arguments()
    check_if_file_exists()

    print(user_list_args)

    # Reading contents of the file
    file = open(file_directory, 'r')
    for line in file:
        print(line)

# Yescrypt Implementation (if "$y$)
password_hash = crypt.crypt("Finalfantasy14-", salt="$y$j9T$1CfDFTUXt5jy5XeLb/zFq0")

# SHA-512 Hash Implementation (if "$6$)
# password_hash = crypt.crypt("Finalfantasy14-", salt="$6$rounds=65536$9eXQ8Y1U74Zf8ATv")
print(f"Secret Password: {password_hash}\n")

