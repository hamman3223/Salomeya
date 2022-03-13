from cryptography.fernet import Fernet
import winreg
import base64

class hideKey():

    def __init__(self, adj_key: list):
        self.adj_key = adj_key
        self.REG_PATH = r'Conrol Panel\Keyboard'
        self.run()

    @staticmethod
    def set_reg(name, value, REG_PATH):
        try:

            winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)

            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
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

        for num in range(5):

            print(base64.b64encode(num))
            print(self.adj_key[num])
            # hideKey.set_reg(
            #     name=base64.b64encode(num),
            #     value=self.adj_key[num],
            #     REG_PATH=self.REG_PATH,
            # )

class keyGenerator():

    def __init__(self) -> None:
        self.key = keyGenerator.gen_key()
        self.adj_key = keyGenerator.adj_key(keyGenerator.gen_key().decode())

    @staticmethod
    def gen_key() -> str:
        return Fernet.generate_key()

    @staticmethod
    def adj_key(key) -> list:

        _adj_key = []
        key = keyGenerator.gen_key()
        n = 4
        lenght = len(key)
        chars = int(lenght/n)

        if (lenght % n != 0):
            print("Sorry this string cannot be diveded into" + str(n) + " equal parts.")
        else:
            for i in range(0,lenght, chars):
                _adj_key.append(key[i:i+chars])

        return _adj_key

print(hideKey(adj_key=keyGenerator().adj_key).run())
print()
