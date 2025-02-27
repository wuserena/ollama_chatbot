from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

class CameraApp(App):
    def __init__(self, response_queue, **kwargs):
        super().__init__(**kwargs)
        self.response_queue = response_queue

    def build(self):
        layout = GridLayout(cols=1)

        self.img = Image(size_hint_y=0.5)  # Kivy Image Widget
        self.capture = cv2.VideoCapture(0)  # OpenCV Camera Capture

        # Label with text wrapping enabled
        self.label = Label(text="Listening...", font_size='20sp', size_hint_y=0.1, halign="center", valign="middle",)
        self.label.bind(size=self.update_text_size)  # Bind to update text wrapping dynamically

        layout.add_widget(self.img)
        layout.add_widget(self.label)

        # Schedule camera updates
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return layout

    def update_text_size(self, instance, value):
        """Ensure text wraps within the available width."""
        instance.text_size = (instance.width, None)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 0)  # Flip for correct orientation in Kivy
            buf = frame.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture

        # Update label text with server response
        if not self.response_queue.empty():
            response_text = self.response_queue.get()
            self.label.text = response_text
            self.label.text_size = (self.label.width, None)  # Ensure text wraps properly


    def on_stop(self):
        self.capture.release()

def start_kivy_app(response_queue):
    """Function to start Kivy app from api_client.py."""
    CameraApp(response_queue).run()
