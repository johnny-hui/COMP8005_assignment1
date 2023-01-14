class Algorithm:
    YESCRYPT = 'y'
    SHA_256 = '5'
    SHA_512 = '6'
    MD5 = '1'
    BCRYPT_A = "2a"
    BCRYPT_B = "2b"
    BCRYPT_Y = "2y"

    def algorithm_checker(self, prefix):
        match prefix:
            case self.YESCRYPT:
                print("[+] Algorithm Used: YESCRYPT")
            case self.SHA_256:
                print("[+] Algorithm Used: SHA_256")
            case self.SHA_512:
                print("[+] Algorithm Used: SHA_512")
            case self.MD5:
                print("[+] Algorithm Used: MD5")
            case self.BCRYPT_A:
                print("[+] Algorithm Used: bcrypt/blowfish")
            case self.BCRYPT_B:
                print("[+] Algorithm Used: bcrypt/blowfish")
            case self.BCRYPT_Y:
                print("[+] Algorithm Used: bcrypt/blowfish")

    def extract_salt(self, prefix, user_info):
        match prefix:
            case self.YESCRYPT:
                print("[+] Algorithm Used: YESCRYPT")
            case self.SHA_256:
                print("[+] Algorithm Used: SHA_256")
            case self.SHA_512:
                print("[+] Algorithm Used: SHA_512")
            case self.MD5:
                print("[+] Algorithm Used: MD5")
            case self.BCRYPT_A:
                print("[+] Algorithm Used: bcrypt/blowfish")
            case self.BCRYPT_B:
                print("[+] Algorithm Used: bcrypt/blowfish")
            case self.BCRYPT_Y:
                print("[+] Algorithm Used: bcrypt/blowfish")