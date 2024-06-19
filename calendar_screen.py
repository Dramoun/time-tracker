import json
import os
import shutil
from calendar import monthrange, isleap

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView

from datetime import datetime, timedelta

from kivy.uix.stacklayout import StackLayout

from globals import GlobalVariables


class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calendar_content = CalendarContent()
        self.add_widget(self.calendar_content)

    def closing(self):
        self.calendar_content.closing()


class CalendarContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Define the main layout for the screen
        self.orientation = 'vertical'

        # Global variables
        self.current_date_name = 'current_date'
        self.current_date = GlobalVariables.return_var(self.current_date_name)

        self.score_name = 'score'
        self.score = GlobalVariables.return_var(self.score_name)

        self.positives_name = 'positives'
        self.positives = GlobalVariables.return_var(self.positives_name)

        self.negatives_name = 'negatives'
        self.negatives = GlobalVariables.return_var(self.negatives_name)

        self.current_task_data = []
        self.load_tasks_from_json()

        # Instantiate the DateDisplay class
        date_display = DateDisplay(reload_tasks=self.load_different_day_tasks)
        # Add the DateDisplay instance to your main layout
        self.add_widget(date_display)

        # Display today's date and tasks
        self.task_display = TaskScheduleManager(tasks_list=self.current_task_data)
        # Add the DateDisplay instance to your main layout
        self.add_widget(self.task_display)

    def closing(self):
        self.save_tasks_to_json()

    def load_different_day_tasks(self):
        self.save_tasks_to_json()
        self.load_tasks_from_json()
        self.task_display.update_tasks(current_task_data=self.current_task_data)

    def load_tasks_from_json(self):
        # Format self.current_date into 'YYYY-MM-DD' string format
        self.current_date = GlobalVariables.return_var(variable_name=self.current_date_name)
        date_str = self.current_date.strftime('%Y-%m-%d')
        daily_file_path = os.path.join(App.get_running_app().user_data_dir, f'{date_str}.json')
        print(daily_file_path)
        template_file_path = os.path.join(App.get_running_app().user_data_dir, 'daily_template.json')
        local_template_path = 'data/daily_template.json'  # Replace with your actual local path

        # Check if the daily file for the current date exists
        if os.path.exists(daily_file_path):
            with open(daily_file_path) as f:
                data = json.load(f)
                self.score = data['score']
                GlobalVariables.update_var(variable_name=self.score_name, variable_value=self.score)

                self.positives = data['positives']
                GlobalVariables.update_var(variable_name=self.positives_name, variable_value=self.positives)

                self.negatives = data['negatives']
                GlobalVariables.update_var(variable_name=self.negatives_name, variable_value=self.negatives)
                self.current_task_data = data['tasks']
        else:
            # If not, check if the template file exists in the running app directory
            if not os.path.exists(template_file_path):
                # If not, copy the local template to the running app directory
                try:
                    shutil.copy(local_template_path, template_file_path)
                except FileNotFoundError:
                    self.score = None
                    self.positives = []
                    self.negatives = []
                    self.current_task_data = []  # Return an empty list if the local template doesn't exist

            # Now, try to load the tasks from the template
            with open(template_file_path) as f:
                data = json.load(f)
                # Create a new daily file with the current date and template data
                with open(daily_file_path, 'w') as daily_f:
                    json.dump(data, daily_f)

                self.score = data['score']
                GlobalVariables.update_var(variable_name=self.score_name, variable_value=self.score)

                self.positives = data['positives']
                GlobalVariables.update_var(variable_name=self.positives_name, variable_value=self.positives)

                self.negatives = data['negatives']
                GlobalVariables.update_var(variable_name=self.negatives_name, variable_value=self.negatives)

                self.current_task_data = data['tasks']

    def save_tasks_to_json(self):
        date_str = self.current_date.strftime('%Y-%m-%d')
        daily_file_path = os.path.join(App.get_running_app().user_data_dir, f'{date_str}.json')

        with open(daily_file_path, 'w') as daily_f:
            output = {
                "score": GlobalVariables.return_var(self.score_name),
                "positives": GlobalVariables.return_var(self.positives_name),
                "negatives": GlobalVariables.return_var(self.negatives_name),
                "tasks": self.current_task_data
            }
            json.dump(output, daily_f)

    def on_stop(self):
        self.save_tasks_to_json()


class DateDisplay(StackLayout):
    def __init__(self, reload_tasks, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'lr-tb'
        self.current_date_name = 'current_date'
        self.current_date = GlobalVariables.return_var(self.current_date_name)

        # Create the first horizontal BoxLayout and add widgets
        self.first_line_layout = BoxLayout(orientation='horizontal')
        self.first_line_layout.size_hint_y = None
        self.first_line_layout.height = 40

        # Create the second horizontal BoxLayout and add widgets
        self.second_line_layout = BoxLayout(orientation='horizontal')
        self.second_line_layout.size_hint_y = None
        self.second_line_layout.height = 40
        self.weekday_buttons = []

        # Add the horizontal BoxLayouts to the main vertical BoxLayout
        self.add_widget(self.first_line_layout)
        self.add_widget(self.second_line_layout)

        self.create_date_display()
        self.create_weekday_display()

        self.reload_tasks_data = reload_tasks

    def update_date_buttons(self):
        GlobalVariables.update_var(variable_name=self.current_date_name, variable_value=self.current_date)

        self.year_btn.text = str(self.current_date.year)
        self.month_btn.text = str(self.current_date.strftime('%B')) + f' {self.current_date.strftime('%m')}'
        self.day_btn.text = str(self.current_date.day)
        self.update_weekday_highlighting()  # Call this method after updating current_date
        self.reload_tasks_data()

    def update_weekday_highlighting(self):
        today = self.current_date.weekday()  # Get the current weekday based on the current date
        for i, btn in enumerate(self.weekday_buttons):
            if i == today:
                btn.background_color = (0.5, 0.5, 0.5, 1)  # Highlight today's button in gray
            else:
                btn.background_color = (1, 1, 1, 1)  # Reset other buttons to default color

    def update_current_date(self, year: int = None, month: int = None, day: int = None, weekday: int = None):
        # Update year if provided
        if year is not None:
            # If the current date is Feb 29 and the new year is not a leap year, set day to Feb 28
            if self.current_date.month == 2 and self.current_date.day == 29 and not isleap(year):
                self.current_date = self.current_date.replace(year=year, day=28)
            else:
                self.current_date = self.current_date.replace(year=year)
            self.year_popup.dismiss()

        # Update month if provided
        if month is not None:
            # Check for day validity in the new month and adjust if necessary
            max_day = monthrange(self.current_date.year, month)[1]
            new_day = min(self.current_date.day, max_day)
            self.current_date = self.current_date.replace(month=month, day=new_day)
            self.month_popup.dismiss()

        # Update day if provided and it's a valid date
        if day is not None:
            try:
                self.current_date = self.current_date.replace(day=day)
            except ValueError:
                # If the day is invalid for the current month, set it to the last valid day
                max_day = monthrange(self.current_date.year, self.current_date.month)[1]
                self.current_date = self.current_date.replace(day=max_day)
            self.day_popup.dismiss()

        # Update weekday if provided
        if weekday is not None:
            # Calculate the difference between the current weekday and the new weekday
            current_weekday = self.current_date.weekday()
            delta_days = (weekday - current_weekday)
            self.current_date += timedelta(days=delta_days)

        # Call method to update UI elements like date buttons
        self.update_date_buttons()

    def create_date_display(self):
        # Create buttons for year, month, day
        self.year_btn = Button(text=str(self.current_date.year))
        self.month_btn = Button(text=self.current_date.strftime('%B') + f' {self.current_date.strftime('%m')}')
        self.day_btn = Button(text=str(self.current_date.day))

        # Bind buttons to their callbacks
        self.year_btn.bind(on_release=self.show_year_options)
        self.month_btn.bind(on_release=self.show_month_options)
        self.day_btn.bind(on_release=self.show_day_options)

        # Add buttons to layout
        self.first_line_layout.add_widget(self.year_btn)
        self.first_line_layout.add_widget(self.month_btn)
        self.first_line_layout.add_widget(self.day_btn)

    def create_weekday_display(self):
        layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        today = datetime.today().weekday()  # Monday is 0 and Sunday is 6

        for i, day in enumerate(days):
            btn = Button(text=day, on_release=lambda x, wd=i: self.update_current_date(weekday=wd))
            if i == today:
                btn.background_color = (0.5, 0.5, 0.5, 1)  # Highlight today's button in gray
            layout.add_widget(btn)
            self.weekday_buttons.append(btn)

        # Add date layout to main layout
        self.second_line_layout.add_widget(layout)

    def show_year_options(self, instance):
        # Create a popup with buttons for the last 2 years, current year, and next 2 years
        content = GridLayout(cols=3, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is room for all buttons
        content.bind(minimum_height=content.setter('height'))

        # Start from 2 years ago to 3 years in the future
        for i in range(-2, 4):
            year = self.current_date.year + i
            btn = Button(text=str(year), size_hint_y=None, height=40)
            btn.bind(on_release=lambda x, y=year: self.update_current_date(year=y))
            # Check if this button represents the current year
            if year == self.current_date.year:
                btn.background_color = (0.5, 0.5, 0.5, 1)  # Blue color for the current year
                btn.color = (1, 1, 1, 1)  # White text color
            else:
                btn.background_color = (1, 1, 1, 1)  # Default color for other years
                btn.color = (0, 0, 0, 1)  # Black text color
            content.add_widget(btn)

        # Set a fixed size for the popup that can contain all buttons
        self.year_popup = Popup(title='Select Year', content=content,
                                size_hint=(None, None), size=(300, 170),
                                pos_hint={'top': .86})
        self.year_popup.open()

    def show_month_options(self, instance):
        # Create a popup with buttons for all months in a year
        content = GridLayout(cols=3, spacing=5, size_hint_y=None)
        # Make sure the height is such that there is room for all buttons
        content.bind(minimum_height=content.setter('height'))

        # List of month names
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']

        # Create buttons for each month
        for i, month_name in enumerate(months, start=1):
            btn = Button(text=month_name + f' {months.index(month_name) + 1}', size_hint_y=None, height=40)
            btn.bind(on_release=lambda x, m=i: self.update_current_date(month=m))
            # Check if this button represents the current month
            if i == self.current_date.month:
                btn.background_color = (0.5, 0.5, 0.5, 1)  # Grey color for the current month
                btn.color = (1, 1, 1, 1)  # White text color
            else:
                btn.background_color = (1, 1, 1, 1)  # Default color for other months
                btn.color = (0, 0, 0, 1)  # Black text color
            content.add_widget(btn)

        # Set a fixed size for the popup that can contain all buttons
        self.month_popup = Popup(title='Select a month', content=content,
                                 size_hint=(None, None), size=(350, 250),
                                 pos_hint={'top': .86})
        self.month_popup.open()

    def show_day_options(self, instance):
        # Create a popup with buttons for all days in the selected month
        content = GridLayout(cols=7, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is room for all buttons
        content.bind(minimum_height=content.setter('height'))

        # Get the number of days in the selected month
        year = self.current_date.year
        month = self.current_date.month
        num_days = monthrange(year, month)[1]

        # Create buttons for each day
        for day in range(1, num_days + 1):
            btn = Button(text=str(day), size_hint_y=None, height=40)
            btn.bind(on_release=lambda x, d=day: self.update_current_date(day=d))
            # Check if this button represents the current day
            if day == self.current_date.day:
                btn.background_color = (0.5, 0.5, 0.5, 1)  # Grey color for the current day
                btn.color = (1, 1, 1, 1)  # White text color
            else:
                btn.background_color = (1, 1, 1, 1)  # Default color for other days
                btn.color = (0, 0, 0, 1)  # Black text color
            content.add_widget(btn)

        # Set a fixed size for the popup that can contain all buttons
        self.day_popup = Popup(title='Select Day', content=content,
                               size_hint=(None, None), size=(300, 320),
                               pos_hint={'top': .86})
        self.day_popup.open()


class TaskScheduleManager(BoxLayout):
    def __init__(self, tasks_list, **kwargs):
        super(TaskScheduleManager, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.current_task_data = tasks_list
        self.display_tasks()

    def update_tasks(self, current_task_data):
        self.scroll_view.clear_widgets()
        # Create a BoxLayout to hold the tasks
        tasks_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        tasks_layout.bind(minimum_height=tasks_layout.setter('height'))

        # Add TaskWidgets to the tasks_layout for each task
        for task in current_task_data:
            task_widget = TaskWidget(task)
            tasks_layout.add_widget(task_widget)

        # Add the tasks_layout to the ScrollView
        self.scroll_view.add_widget(tasks_layout)

    def display_tasks(self):
        # Get today's date in the format Year-Month-Day
        today_date = datetime.now().strftime('%Y-%m-%d')
        # Create a Label with today's date as its text
        date_label = Label(text=f"Today's Date: {today_date}", padding=[0, 0, 0, 60])
        self.add_widget(date_label)

        header_box = BoxLayout(orientation='horizontal', padding=[0, 0, 0, 10])
        header_time = Label(text='Time', size_hint_x=0.25)
        header_desc = Label(text='Description')
        header_point = Label(text='+', size_hint_x=0.15)
        header_status = Label(text='?', size_hint_x=0.15)

        header_box.add_widget(header_time)
        header_box.add_widget(header_desc)
        header_box.add_widget(header_point)
        header_box.add_widget(header_status)

        self.add_widget(header_box)

        # Create a ScrollView
        self.scroll_view = ScrollView(size_hint=(1, None),
                                      size=(Window.width, Window.height - 220))

        self.update_tasks(current_task_data=self.current_task_data)
        # Add the ScrollView to the main layout
        self.add_widget(self.scroll_view)

    def save_schedule(self):
        # Save the current state of the schedule to a JSON file
        pass


class LargeCheckBox(CheckBox):
    pass


Builder.load_string('''
<LargeCheckBox@CheckBox>:
    canvas.before:
        PushMatrix
        Scale:
            # Scale of 1.5 means 50% larger than normal
            origin: self.center
            x: 1.2 if self.state == 'down' else 1.3
            y: 1.2 if self.state == 'down' else 1.3
    canvas.after:
        PopMatrix
''')


class TaskWidget(BoxLayout):
    def __init__(self, task_data, **kwargs):
        super(TaskWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 40

        # Create the start time label
        self.start_time_label = Label(text=task_data['start_time'], size_hint_x=0.25)
        self.add_widget(self.start_time_label)

        # Create the task name label with text wrapping
        self.name_label = Label(text=task_data['name'])
        self.name_label.bind(width=lambda *x: setattr(self.name_label, 'text_size', (self.name_label.width, None)))
        self.name_label.bind(texture_size=self.update_height)
        self.add_widget(self.name_label)

        # Create the value label
        self.value_label = Label(text=str(task_data['value']), size_hint_x=0.15)
        self.add_widget(self.value_label)

        def on_checkbox_active(checkbox, value):
            score = GlobalVariables.return_var(variable_name='score')
            print('score before: ', score)
            if value:
                GlobalVariables.update_var(variable_name='score', variable_value=score+task_data['value'])
                task_data['status'] = True
            else:
                GlobalVariables.update_var(variable_name='score', variable_value=score-task_data['value'])
                task_data['status'] = False

            score = GlobalVariables.return_var(variable_name='score')
            print(f"Score after: {score}")

        # Create the status checkbox
        self.status_checkbox = LargeCheckBox(active=task_data['status'], size_hint_x=0.15)
        self.status_checkbox.bind(active=on_checkbox_active)
        self.add_widget(self.status_checkbox)

    def update_height(self, instance, value):
        # Calculate the new height with a scaling factor
        scaling_factor = 0.45  # Adjust this value as needed
        new_height = value[1] * scaling_factor
        if new_height > self.height:
            self.height = new_height
