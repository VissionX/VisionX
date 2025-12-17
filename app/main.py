from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatIconButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.core.window import Window
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.supervisor import VisionSupervisor
from infra.config import Config

class VisionXApp(MDApp):
    """Main VisionX application"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.supervisor = None
        self.app_config = Config()  # Renamed from self.config to avoid Kivy conflict
        
    def build(self):
        """Build the UI"""
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        
        # Main screen
        screen = MDScreen()
        
        # Status label
        self.status_label = MDLabel(
            text="VisionX - Initializing...",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            font_style="H5"
        )
        screen.add_widget(self.status_label)
        
        # Microphone button (centered, large)
        self.mic_button = MDFillRoundFlatIconButton(
            icon="microphone",
            text="Listening",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            size_hint=(None, None),
            size=("200dp", "200dp"),
            font_size="24sp",
            disabled=True
        )
        screen.add_widget(self.mic_button)
        
        # Info label
        self.info_label = MDLabel(
            text='Say "start" to detect objects',
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            font_style="Body1"
        )
        screen.add_widget(self.info_label)
        
        # Exit button
        exit_btn = MDIconButton(
            icon="close",
            pos_hint={"right": 0.98, "top": 0.98},
            on_release=self.stop_app
        )
        screen.add_widget(exit_btn)
        
        # Schedule initialization
        Clock.schedule_once(self._initialize_app, 1)
        
        return screen
    
    def _initialize_app(self, dt):
        """Initialize the supervisor"""
        try:
            print("Creating VisionSupervisor...")
            # Create supervisor
            self.supervisor = VisionSupervisor(self.app_config)  # Use app_config
            print("VisionSupervisor created successfully")
            
            # Initialize in background thread
            import threading
            init_thread = threading.Thread(target=self._init_worker, daemon=True)
            init_thread.start()
            print("Initialization thread started")
            
        except Exception as e:
            import traceback
            error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            self.update_status(f"Error: {str(e)}")
    
    def _init_worker(self):
        """Worker thread for initialization"""
        try:
            print("Starting supervisor initialization...")
            self.supervisor.initialize()
            print("Supervisor initialized successfully")
            
            # Schedule UI update on main thread
            Clock.schedule_once(lambda dt: self._start_listening(), 0)
            
        except Exception as e:
            import traceback
            error_msg = f"Init error: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            Clock.schedule_once(lambda dt: self.update_status(f"Init error: {str(e)}"), 0)
    
    def _start_listening(self):
        """Start listening for commands"""
        self.supervisor.start(status_callback=self.update_status)
        self.mic_button.disabled = False
        self.update_status("Listening for voice commands...")
    
    def update_status(self, status):
        """Update status label"""
        def _update(dt):
            self.status_label.text = status
            
            # Update button state
            if "Detecting" in status:
                self.mic_button.icon = "camera"
                self.mic_button.text = "Detecting"
            else:
                self.mic_button.icon = "microphone"
                self.mic_button.text = "Listening"
        
        Clock.schedule_once(_update, 0)
    
    def stop_app(self, *args):
        """Stop the application"""
        print("Stopping application...")
        if self.supervisor:
            self.supervisor.stop()
        self.stop()
    
    def on_stop(self):
        """Cleanup on app stop"""
        print("App on_stop called")
        if self.supervisor:
            try:
                self.supervisor.stop()
            except Exception as e:
                print(f"Error during cleanup: {e}")

def main():
    """Entry point"""
    # Set window size
    Window.size = (400, 600)
    
    # Run app
    app = VisionXApp()
    app.run()

if __name__ == "__main__":
    main()
