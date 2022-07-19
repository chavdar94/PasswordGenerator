from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import string
import random

chars = list(string.ascii_letters + string.digits)


class GeneratePassword(Screen):
    password_length = ObjectProperty(None)
    website = ObjectProperty(None)
    email = ObjectProperty(None)

    def generate_password(self):
        length = int(self.password_length.text)
        password = []
        for i in range(length):
            password.append(random.choice(chars))
        random.shuffle(password)

        pop = Popup(title='Results',
                    content=Label(text=f'{"".join(password)}'),
                    size_hint=(None, None), size=(500, 200))
        pop.open()

        return ''.join(password)

    def write_to_file(self):
        with open("password.txt", "a") as file:
            file.write(f'{self.generate_password()}:{self.website.text}:{self.email.text}')
            file.write('\n')
        self.password_length.text = ''
        self.website.text = ''
        self.email.text = ''


class ReadFile(Screen):
    website = ObjectProperty()
    result = {}

    def read(self):
        with open("password.txt", "r") as file:
            for line in file:
                password, website, email = line.strip().split(':')
                self.result[website] = (password, email)

    def show_result(self):
        website = ''
        password = ''
        email = ''

        for site in self.result:
            if site == self.website.text:
                website = site
                password = self.result[site][0]
                email = self.result[site][1]

        pop = Popup(title='Results',
                    content=Label(text=f'{website} -> {password} -> {email}'),
                    size_hint=(None, None), size=(500, 200))
        pop.open()


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class MyApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyApp().run()
