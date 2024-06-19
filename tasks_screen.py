import json
import os
import shutil

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout

from globals import GlobalVariables


class TasksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        self.clear_widgets()
        self.add_widget(TasksContent())


class TasksContent(StackLayout):
    def __init__(self, **kwargs):
        super(StackLayout, self).__init__(**kwargs)
        self.current_date_name = 'current_date'
        self.current_date = GlobalVariables.return_var(self.current_date_name)

        self.positives = []
        self.positives_name = 'positives'
        self.current_positives = GlobalVariables.return_var(self.positives_name)

        self.negatives = []
        self.negatives_name = 'negatives'
        self.current_negatives = GlobalVariables.return_var(self.negatives_name)

        self.load_optionals()
        self.add_optionals()

        self._time_label = Label(text=str(self.current_date))
        #self.add_widget(self._time_label)

    def add_optionals(self):
        layout = BoxLayout(orientation='horizontal')

        all_items = self.positives + self.negatives
        custom_data = self.current_positives + self.current_negatives
        for item in all_items:
            layout.add_widget(ItemRow(item_data=item, custom_data=custom_data))

        self.add_widget(layout)

    def load_optionals(self):
        # Get the path to the running app directory
        running_dir = App.get_running_app().user_data_dir

        # Check if optionals.json exists in the running directory
        optionals_path = os.path.join(running_dir, 'optionals.json')
        if not os.path.exists(optionals_path):
            # If not, copy the local template to the running directory
            local_template_path = 'data/daily_template.json'  # Replace with your actual local path
            try:
                shutil.copy(local_template_path, optionals_path)
            except FileNotFoundError:
                print('optionals file not found')
                return []

        # Now, always load the optionals.json file
        with open(optionals_path) as f:
            data = json.load(f)
            self.positives = data['positives']
            self.negatives = data['negatives']


class ItemRow(BoxLayout):
    def __init__(self, item_data, custom_data, **kwargs):
        super().__init__(**kwargs)
        self.custom_data = custom_data
        self.orientation = 'horizontal'
        self.item_id = item_data["id"]
        self.total_count = self.custom_data.get(self.item_id, item_data["value"])

        self.item_name = item_data["name"]
        self.value = item_data["value"]

        self.name_label = Label(text=self.item_name)
        self.value_label = Label(text=self.value)
        self.total_label = Label(text=str(self.total_count))
        self.minus_button = Button(text="-", on_press=self.decrement_total)
        self.plus_button = Button(text="+", on_press=self.increment_total)

        self.add_widget(self.name_label)
        self.add_widget(self.value_label)
        self.add_widget(self.minus_button)
        self.add_widget(self.total_label)
        self.add_widget(self.plus_button)

    @staticmethod
    def replace_tuple_value_by_id(my_list, item_id, new_value):
        for i, (id_, value) in enumerate(my_list):
            if id_ == item_id:
                my_list[i] = (id_, new_value)
                break  # Stop searching once the ID is found

        return my_list

    def update_current_id(self):
        if self.item_id[0] == "P":
            list_name = 'positives'
        else:
            list_name = 'negatives'
        current_list = GlobalVariables.return_var(variable_name=list_name)

        if self.item_id not in self.custom_data:
            current_list.append(self.total_count)
        else:
            current_list = self.replace_tuple_value_by_id(my_list=current_list,
                                                          item_id=self.item_id,
                                                          new_value=self.total_count)

        GlobalVariables.update_var(variable_name=list_name, variable_value=current_list)

    def decrement_total(self, instance):
        self.total_count = max(0, self.total_count - 1)
        self.total_label.text = str(self.total_count)
        self.update_current_id()

    def increment_total(self, instance):
        self.total_count += 1
        self.total_label.text = str(self.total_count)
        self.update_current_id()
