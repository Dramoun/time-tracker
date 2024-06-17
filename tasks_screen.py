from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen


class TasksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(TasksContent())


class TasksContent(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        # Set up the background color for NavBarButtons
        with self.canvas.before:
            Color(0.1, 0.2, 0.9, 0.5)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Update the position and size of the background rectangle on size/position change
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
