from cryptography.fernet import Fernet


class Decryptor():

    def __init__(self, filename: str, key: str):

        self.__fernet_class = Fernet(key.encode())
        self.filename = filename

    def run(self):

        with open(self.filename, 'rb') as file:

            enc_d = file.read()
            dec_d = self.__fernet_class.decrypt(enc_d)

        with open(self.filename, 'wb') as file:

            file.write(dec_d)


Decryptor(
    filename="fin_acc.xlsx",
    key=input("Enter your key: ").encode()
).run()