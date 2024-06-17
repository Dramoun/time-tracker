import json
import os
import shutil

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView

from datetime import datetime

from kivy.uix.stacklayout import StackLayout


class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(CalendarContent())


class CalendarContent(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Define the main layout for the screen
        self.orientation = 'lr-tb'

        # Load tasks from JSON
        self.task_list = self.load_tasks_from_json()

        # Add date display layout
        self.add_date_display()

        # Display today's date and tasks
        self.display_date_and_tasks()

    def add_date_display(self):
        # Date display layout
        date_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)

        # Get current date
        now = datetime.now()

        # Create buttons for year, month, day
        year_btn = Button(text=str(now.year))
        month_btn = Button(text=now.strftime('%B') + f'({now.strftime('%m')})')
        day_btn = Button(text=str(now.day))

        # Add buttons to date layout
        date_layout.add_widget(year_btn)
        date_layout.add_widget(month_btn)
        date_layout.add_widget(day_btn)

        # Add date layout to main layout
        self.add_widget(date_layout)

    def load_tasks_from_json(self):
        file_path = App.get_running_app().user_data_dir + '/daily_template.json'
        print(file_path)
        local_file_path = 'data/daily_template.json'  # Replace with your actual local path

        # Check if the file exists in the running app directory
        if not os.path.exists(file_path):
            # If not, copy the local file to the running app directory
            try:
                shutil.copy(local_file_path, file_path)
            except FileNotFoundError:
                return []  # Return an empty list if the local file doesn't exist

        # Now, try to load the tasks from the copied or existing file
        try:
            with open(file_path) as f:
                data = json.load(f)
                return data['tasks']
        except FileNotFoundError:
            return []  # Return an empty list if there's still no file

    def save_tasks_to_json(self):
        file_path = App.get_running_app().user_data_dir + '/daily_template.json'
        with open(file_path, 'w') as f:
            json.dump({'tasks': self.task_list}, f)

    def display_date_and_tasks(self):
        def update_label_height(instance, value):
            instance.height = instance.texture_size[1]

        # Sort the tasks by start time
        sorted_tasks = sorted(self.task_list, key=lambda x: x.get('start_time', '23:59'))

        # Create a layout for the tasks
        tasks_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        tasks_layout.spacing = 15  # Adjust the value as needed
        # This line ensures that the layout will grow with its content
        tasks_layout.bind(minimum_height=tasks_layout.setter('height'))

        for task in sorted_tasks:
            # Create a horizontal layout for each task
            task_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None)
            # Set the height dynamically based on the content
            task_layout.bind(minimum_height=task_layout.setter('height'))

            # Create widgets for the task properties
            time_label = Label(text=task.get('start_time', 'No time'), size_hint_x=None, width=50)
            name_label = Label(
                text=task['name'],
                size_hint_y=None,
                text_size=(self.width + 120, None)
            )
            name_label.bind(texture_size=update_label_height)
            value_label = Label(text='+' + str(task.get('value', 0)), size_hint_x=None, width=20)
            checkbox = CheckBox(active=task.get('checked', False), size_hint_x=None, width=40)

            # Add widgets to the task layout
            task_layout.add_widget(time_label)
            task_layout.add_widget(name_label)
            task_layout.add_widget(value_label)
            task_layout.add_widget(checkbox)

            # Add the task layout to the tasks layout
            tasks_layout.add_widget(task_layout)

        # Create a ScrollView for the tasks
        tasks_scroll_view = ScrollView(size_hint=(1, 1))
        tasks_scroll_view.add_widget(tasks_layout)  # Add tasks_layout to ScrollView

        # Add the ScrollView to the main layout instead of tasks_layout
        self.add_widget(tasks_scroll_view)

    def on_stop(self):
        # Save tasks to JSON when the app is closed
        self.save_tasks_to_json()
