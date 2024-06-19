from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


# Define the default page content
class DefaultPageContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='This is the Default Page'))
        # Add your default page content here


# Define the task page content
class TaskPageContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='This is the Task Page'))
        # Add your task page content here


# Define the default page
class DefaultPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(DefaultPageContent())


# Define the task page
class TaskPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(TaskPageContent())


class IconButton(Button):
    def __init__(self, icon_path, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = icon_path
        self.background_down = icon_path  # You can also set a different image for the pressed state



