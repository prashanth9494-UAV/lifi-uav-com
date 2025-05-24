from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from aes_utils import decrypt
import cv2
import numpy as np

class ReceiverApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.password_input = TextInput(hint_text='Enter Password', password=True)
        self.layout.add_widget(Label(text='Password:'))
        self.layout.add_widget(self.password_input)

        receive_btn = Button(text='Start Receiving')
        receive_btn.bind(on_press=self.on_receive)
        self.layout.add_widget(receive_btn)

        self.output_label = Label(size_hint_y=None, text='', halign='left', valign='top')
        self.output_label.bind(texture_size=self.update_height)

        scroll = ScrollView()
        scroll.add_widget(self.output_label)
        self.layout.add_widget(scroll)

        return self.layout

    def update_height(self, instance, value):
        self.output_label.height = self.output_label.texture_size[1]

    def on_receive(self, instance):
        cap = cv2.VideoCapture(0)
        binary_data = ""
        for _ in range(160):
            ret, frame = cap.read()
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            luminance = np.mean(gray)
            binary_data += "1" if luminance > 120 else "0"
            cv2.waitKey(50)
        cap.release()
        chars = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]
        encrypted = ''.join(chars).rstrip('\x00')
        try:
            decrypted = decrypt(encrypted, self.password_input.text)
            self.output_label.text = decrypted
        except Exception as e:
            self.output_label.text = f"Decryption failed: {e}"

if __name__ == '__main__':
    ReceiverApp().run()
