from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from aes_utils import encrypt
import time

class TransmitterApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.message_input = TextInput(hint_text='Enter Message')
        self.layout.add_widget(Label(text='Message:'))
        self.layout.add_widget(self.message_input)

        self.password_input = TextInput(hint_text='Enter Password', password=True)
        self.layout.add_widget(Label(text='Password:'))
        self.layout.add_widget(self.password_input)

        send_btn = Button(text='Send')
        send_btn.bind(on_press=self.on_send)
        self.layout.add_widget(send_btn)

        return self.layout

    def transmit_binary(self, binary_data):
        for bit in binary_data:
            print("Light ON" if bit == "1" else "Light OFF")
            time.sleep(0.3)

    def on_send(self, instance):
        message = self.message_input.text
        password = self.password_input.text
        if message and password:
            encrypted = encrypt(message, password)
            binary = ''.join(format(ord(i), '08b') for i in encrypted)
            self.transmit_binary(binary)

if __name__ == '__main__':
    TransmitterApp().run()
