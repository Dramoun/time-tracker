from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget

from calendar_screen import CalendarScreen, TaskScheduleManager
from tasks_screen import TasksScreen



# Create the main application layout
class MainAppLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.calendar_screen = CalendarScreen(name='Calendar')
        self.tasks_screen = TasksScreen(name='Tasks')

        self.create_top_bar()
        self.create_screen_manager()
        self.create_bottom_nav_bar()

    def closing(self):
        self.calendar_screen.closing()

    def create_top_bar(self):
        self.top_bar = BoxLayout(size_hint_y=None, height=60, orientation='horizontal', padding=10)
        # Replace Button with an ImageButton by setting the background_normal property
        icon_left = Button(size_hint=(None, None), size=(40, 40),
                           background_normal='assets/images/setting_white.png',
                           background_down='assets/images/setting_white_down.png')
        spacer = Widget()
        self.page_name = Label(size_hint=(None, 1), text='Calendar', bold=True)

        self.top_bar.add_widget(icon_left)
        self.top_bar.add_widget(spacer)  # This will push the page name label to the right
        self.top_bar.add_widget(self.page_name)

        self.add_widget(self.top_bar)

    def create_bottom_nav_bar(self):
        self.bottom_nav_bar = BoxLayout(size_hint_y=None, height=30, padding=[0, 10, 0, 10])  # Added bottom padding

        # Spacing and buttons for bottom nav bar
        self.bottom_nav_bar.add_widget(Widget(size_hint_x=0.6))  # Spacer with a width ratio
        daily_btn = Button(size_hint=(None, None), size=(40, 40),
                           background_normal='assets/images/calendar_white.png',
                           background_down='assets/images/calendar_white_down.png')
        self.bottom_nav_bar.add_widget(daily_btn)

        self.bottom_nav_bar.add_widget(Widget(size_hint_x=0.6))  # Larger spacer in the middle

        task_btn = Button(size_hint=(None, None), size=(40, 40),
                          background_normal='assets/images/clipboard_white.png',
                          background_down='assets/images/clipboard_white_down.png')

        daily_btn.bind(on_press=lambda instance: self.change_page('Calendar'))
        task_btn.bind(on_press=lambda instance: self.change_page('Tasks'))

        self.bottom_nav_bar.add_widget(task_btn)

        self.bottom_nav_bar.add_widget(Widget(size_hint_x=0.6))  # Spacer with a width ratio

        self.add_widget(self.bottom_nav_bar)

    def create_screen_manager(self):
        self.screen_manager = ScreenManager()

        # Add screens to the Screen Manager
        self.screen_manager.add_widget(self.calendar_screen)
        self.screen_manager.add_widget(self.tasks_screen)

        self.add_widget(self.screen_manager)

    def change_page(self, screen_name):
        self.screen_manager.current = screen_name
        # Update the top bar page name label
        self.page_name.text = screen_name.replace('_', ' ').title()


# Build the app
class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_app = MainAppLayout()

    def build(self):
        return self.main_app

    def on_stop(self):
        self.main_app.closing()


if __name__ == '__main__':
    MyApp().run()



