import datetime


class GlobalVariables:
    # Global variable
    variables = {
        "current_date": datetime.datetime.now(),
        "positives": [],
        "negatives": [],
        "score": 0,
    }

    @classmethod
    def update_var(cls, variable_name, variable_value):
        # Use the global keyword to modify the class-level variable
        cls.variables[variable_name] = variable_value

    @classmethod
    def return_var(cls, variable_name):
        # Use the global keyword to return the class-level variable
        return cls.variables[variable_name]
