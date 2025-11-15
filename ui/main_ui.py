from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

class MainUI(MDApp):
    def build(self):
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        start_btn = MDRaisedButton(
            text="start",
            pos_hint={"center_x": 0.5},
            on_release=self.on_start_pressed
        )
        layout.add_widget(start_btn)
        return layout

    def on_start_pressed(self, instance):
        print("Start button pressed! Voice Trigger will run here.")

if __name__ == "__main__":
    MainUI().run()

