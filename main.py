import crypt
import getopt
import os
import sys
import Algorithms

WELCOME_MSG = "A basic single-threaded password cracker program (v1.0) \nJohnny Hui (A00973103)"
WELCOME_DECORATION = "=============================================================================================" \
                     "=============="
ZERO = 0
TWO = 2
BACK_TO_START = 0
PROGRAM_TERMINATE_MSG_1 = "[+] All users have been processed!"
PROGRAM_TERMINATE_MSG_2 = "[+] PROGRAM EXIT: Now terminating program..."

def algorithm_not_found():
    print("[+] ALGORITHM_NOT_FOUND_ERROR: This algorithm type is not supported!")
    print("[+] Now checking for next user...")


def check_if_file_exists(file_dir):
    try:
        if not os.path.exists(file_dir):
            sys.exit("[+] ERROR: File Doesn't Exist or Invalid Argument!")
        else:
            print(f"[+] Now reading the {file_dir} file...")
    except FileNotFoundError:
        sys.exit("[+] ERROR: File Doesn't Exist!")


def check_if_root_user():
    if not os.geteuid() == 0:
        sys.exit("[+] ERROR: Only the 'root' user can run this script "
                 "[Please run this script again using sudo command].")


def check_user_parameters(user_list):
    if len(user_list) == ZERO:
        sys.exit("[+] No users were passed in as arguments!")


def check_valid_user(file_entry, user_name, user_list):
    if '$' not in file_entry and len(user_list) >= TWO:
        print(f"[+] INVALID USER: {user_name} is a service, utility, or process and cannot be cracked!")
        print("[+] Now moving on to the next user...")
        return False
    elif '$' not in file_entry and len(user_list) < TWO:
        print(f"[+] INVALID USER: {user_name} is a service, utility, or process and cannot be cracked!")
        return False
    else:
        return True


def display_welcome_msg():
    print(WELCOME_MSG)
    print(WELCOME_DECORATION)


def find_password(file_directory, input_hash, input_salt, max_attempt):
    attempt = ZERO
    if max_attempt == ZERO:
        try:
            password_file = open(file_directory, 'r')

            for line in password_file:
                if crypt.crypt(line.strip(), input_salt) == input_hash:
                    print(f"[+] CRACK COMPLETE: Password has been found!")
                    print(f"[+] Number of Attempts Made: {attempt}")
                    print(f"[+] The password is {line}")
                    return None
                else:
                    attempt += 1

            print(f"[+] Number of Attempts Made: {attempt}")
            print(f"[+] CRACK FAILED: Password isn't present in the file provided!")
        except IOError:
            sys.exit(f"[+] IOError: Cannot open the following password file: {file_directory}!")
    else:
        try:
            password_file = open(file_directory, 'r')

            for line in password_file:
                if crypt.crypt(line.strip(), input_salt) == input_hash:
                    print(f"[+] CRACK COMPLETE: Password has been found!")
                    print(f"[+] The password is {line}")
                    return None
                elif attempt == max_attempt:
                    print(f"[+] CRACK FAILED: Max attempts of {attempt} has been reached!")
                    print("[+] Now moving on to the next user...")
                    return None
                else:
                    attempt += 1

            print(f"[+] Number of Attempts Made: {attempt}")
            print(f"[+] CRACK FAILED: Password isn't present in the file provided!")
        except IOError:
            sys.exit(f"[+] IOError: Cannot open the following password file: {file_directory}!")


def open_shadow_file(file_dir):
    try:
        file = open(file_dir, 'r')
        return file
    except IOError:
        sys.exit(f"[+] IOError: Cannot open the following file: {file_dir}")


def parse_arguments():
    cleansed_user_list_args = []
    file_directory = ""
    password_list = ""
    max_attempts = 0

    # Remove file name from argument list
    arguments = sys.argv[1:]

    # Getting the file directory from (-f flag) and users (as args)
    opts, user_list_args = getopt.getopt(arguments, 'f:l:a:')

    # Check if empty parameters
    check_args(opts)

    # Check if users are passed in
    check_user_parameters(user_list_args)

    # Check for duplicate users in arguments (prevent cracking duplicate users)
    remove_duplicate_users(cleansed_user_list_args, user_list_args)

    # Get file directory
    for opt, argument in opts:
        if opt == '-f':
            file_directory = argument
        if opt == '-l':
            password_list = argument
        if opt == '-a':
            max_attempts = argument

    return file_directory, cleansed_user_list_args, password_list, int(max_attempts)


def check_args(opts):
    if len(opts) == ZERO:
        sys.exit("[+] NO_ARG_ERROR: No arguments were passed in!")


def remove_duplicate_users(cleansed_user_list_args, orig_user_list_args):
    for user in orig_user_list_args:
        if user not in cleansed_user_list_args:
            cleansed_user_list_args.append(user)

    print(f"[+] The following users are to have their passwords cracked: {cleansed_user_list_args}")


def remove_user_from_list(user_list):
    return user_list[1:]


def user_not_found_check(user_info, user_list, user_name, file_dir):
    if len(user_info) is ZERO and len(user_list) >= TWO:
        print(f"[+] ERROR: {user_name} has not been found in {file_dir}! "
              f"Now moving on to the next user...\n")
    elif len(selected_user_info) is ZERO and len(user_list) < TWO:
        print(f"\n[+] ERROR: The last user: '{user_name}' has not been found in {file_dir}!")


def print_end():
    print(f"\n{WELCOME_DECORATION}")
    print(PROGRAM_TERMINATE_MSG_1)
    print(PROGRAM_TERMINATE_MSG_2)


# Main Program
if __name__ == "__main__":
    display_welcome_msg()
    # check_if_root_user()
    file_directory, user_list_args, password_list_dir, max_attempts = parse_arguments()
    check_if_file_exists(file_directory)

    # Read contents of the /etc/shadow
    shadow_file = open_shadow_file(file_directory)

    # Check if users exist and handle each
    for user in user_list_args:
        selected_user_info = ""
        shadow_file.seek(BACK_TO_START)

        for entry in shadow_file:
            if user == entry.split(':')[0]:
                print(f"\n[+] {user} has been found! Now attempting to determine a suitable hashing algorithm...")
                selected_user_info = entry.split('$')

                # Check if user is valid (and not a service/process/utility)
                if check_valid_user(entry, user, user_list_args) is False:
                    break

                # Determine the type of algorithm for user and extract salt
                algorithm = Algorithms.Algorithm()
                if algorithm.algorithm_checker(selected_user_info) == Algorithms.Algorithm.ERROR_CODE:
                    algorithm_not_found()
                    break

                print("[+] Now beginning the cracking process...")

                # Retrieve the Hash
                user_hash = entry.split(':')[1]

                # Retrieve the salt
                salt = algorithm.extract_salt(selected_user_info[1], entry)

                # Find the password from dictionary
                find_password(password_list_dir, user_hash, salt, max_attempts)

        user_not_found_check(selected_user_info, user_list_args, user, file_directory)
        user_list_args = remove_user_from_list(user_list_args)

    # Program Terminate
    print_end()
