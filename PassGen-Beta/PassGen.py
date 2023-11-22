import webbrowser
import urllib3
import random
import zxcvbn
import customtkinter
import sys
from tkinter import messagebox


def get_latest_version():
    latest_version = urllib3.request(url="https://github.com/gorouflex/passgen/releases/latest", method="GET")
    latest_version = latest_version.geturl()
    return latest_version.split("/")[-1]


def open_github():
    webbrowser.open("https://www.github.com/gorouflex/passgen")


def open_releases():
    webbrowser.open(f"https://github.com/gorouflex/passgen/releases/tag/{get_latest_version()}")


def info_window():
    InfoWindow().mainloop()

def check_for_updates():
    local_version = "1.0.1"
    latest_version = get_latest_version()

    if local_version < latest_version:
        result = messagebox.askquestion(
            "Update Available",
            "A new update has been found! Please use the Updater to install the latest version.\nOtherwise, the app will exit.\nDo you want to visit the GitHub page for more details?",
            icon="warning"
        )
        if result == "yes":
            webbrowser.open("https://github.com/gorouflex/passgen/releases/latest")
        sys.exit()
    elif local_version > latest_version:
        result = messagebox.askquestion(
            "PassGen Beta Program",
            "Welcome to PassGen Beta Program.\nThis build may not be as stable as expected.\nOnly for testing purposes!",
            icon="warning"
        )
        if result == "no":
            sys.exit()
        else:
            pass
    else:
        pass

class InfoWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('About')
        self.title = "About PassGen"
        self.geometry("250x250")
        self.resizable(False, False)

        self.logo_label = customtkinter.CTkLabel(self, text="About PassGen", font=("", 19, "bold"))
        self.logo_label.pack(pady=5)

        self.owner_label = customtkinter.CTkLabel(self, text="Main developer: NotchApple1703", font=("", 15))
        self.owner_label.pack(pady=2)

        self.subdev_label = customtkinter.CTkLabel(self, text="Sub-developer: GorouFlex", font=("", 15))
        self.subdev_label.pack(pady=2)

        self.buttons = [
            ["Open Github", open_github],
            ["Changelog", open_releases],
        ]

        for i in range(2):
            button = customtkinter.CTkButton(self, width=120, height=40, text=self.buttons[i][0], font=("", 16),
                                             corner_radius=5, command=self.buttons[i][1])
            button.pack(pady=5)

        self.version_label = customtkinter.CTkLabel(self, width=200,
                                                    text=f"Latest version on github: {get_latest_version()}",
                                                    font=("", 14))
        self.version_label.pack(pady=5)


class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('PassGen')
        self.geometry("250x350")
        self.resizable(False, False)

        self.logo_label = customtkinter.CTkLabel(self, text="PassGen", font=("", 21, "bold"))
        self.logo_label.pack(pady=10)

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Password", font=("", 15), width=200,
                                                     height=50, border_width=2, corner_radius=10)
        self.password_entry.pack(pady=10)

        self.buttons = [
            ["Generate Pass", self.start_gen],
            ["Save Pass As TXT", self.save_password],
            ["Check Pass", self.start_check],
            ["About", info_window],
        ]
        for i in range(4):
            button = customtkinter.CTkButton(self, width=150, height=40, text=self.buttons[i][0], font=("", 16),
                                             corner_radius=5, command=self.buttons[i][1])
            button.pack(pady=5)

        self.version_label = customtkinter.CTkLabel(self, width=215, text=f"Version 1.0.1", font=("", 14))
        self.version_label.pack(pady=5)

    def start_gen(self):
        password = "".join(map(chr, random.choices(range(33, 127), k=16)))
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

    def save_password(self):
        password = self.password_entry.get()
        with open("password.txt", "a") as f:
            f.write(password + "\n" * bool(password))

    def start_check(self):
        password = self.password_entry.get()
        result = zxcvbn.zxcvbn(password)
        score = result["score"]
        messages = {
            4: ('Password Rating', 'Your password is very strong!', 'info'),
            3: ('Password Rating', 'Your password is strong.', 'info'),
            2: ('Password Rating', 'Your password is moderate.', 'warning'),
            1: ('Password Rating', 'Your password is weak, consider to change your currently password.', 'warning'),
            0: ('Password Rating', 'Your password is very weak,, consider to change your currently password.', 'error')
        }
        title, message, level = messages[score]
        getattr(messagebox, f'show{level}')(title, message)
        

if __name__ == '__main__':
    check_for_updates()
    app = MainWindow()
    app.mainloop()
