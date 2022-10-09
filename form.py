from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, IntegerField, SelectField, \
        StringField, TextAreaField, SubmitField, DateField, EmailField, TimeField
from wtforms import validators

class Option(Form):
    day_mode = SelectField(
        'DayMode',
        choices=["One day", "Range of days"]
    )
    day1 = DateField(
        'Day1',
        validators=[validators.InputRequired()]
    )
    day2 = DateField(
        'Day2',
        validators=[validators.Optional()]
    )
    day_increment = IntegerField(
        'DayIncrement',
        validators=[validators.Optional()]
    )

    time_mode = SelectField(
        'TimeMode',
        choices=["Whole day", "Hourly range", "Various times"]
    )
    time1 = TimeField(
        'time1',
        validators=[validators.Optional()]
    )
    time2 = TimeField(
        'time2',
        validators=[validators.Optional()]
    )
    time3 = TimeField(
        'time3',
        validators=[validators.Optional()]
    )
    time_increment = IntegerField(
        'TimeIncrement',
        validators=[validators.Optional()]
    )

class PollForm(FlaskForm):
    poll_title = StringField(
        'Poll title',
        validators=[validators.InputRequired(), validators.Length(max=100)]
    )

    options = FieldList(
        FormField(Option),
        'Options',
        min_entries=1,
        max_entries=100
    )

    def validate_on_submit(self, *args, **kwargs):
        self.error_message = ""
        for option in self.options:
            if option.day_mode.data == "Range of days":
                if option.day2.data is None:
                    self.error_message = "Please fill in 'to day' field."
                    return False
                elif option.day1.data > option.day2.data:
                    self.error_message = "'From day' must be earlier than 'to day'."
                    return False
                elif option.day_increment.data is None:
                    self.error_message = "Please fill in 'every x days' field."
                    return False
                elif option.day_increment.data <= 0:
                    self.error_message = "'Every x days' field must contain positive number."
                    return False

            if option.time_mode.data == "Hourly range":
                if option.time1.data is None:
                    self.error_message = "Please fill in 'from time' field."
                    return False
                elif option.time2.data is None:
                    self.error_message = "Please fill in 'to time' field."
                    return False
                elif option.time1.data > option.time2.data:
                    self.error_message = "'From time' must be earlier than 'to time'."
                    return False
                elif option.time_increment.data is None:
                    self.error_message = "Please fill in 'every x minutes' field."
                    return False
                elif option.time_increment.data <= 0:
                    self.error_message = "'Every x minutes' field must contain positive number."
                    return False
        
            elif option.time_mode.data == "Various times":
                if option.time1.data is None and option.time2.data is None and option.time3.data is None:
                    self.error_message = "Please fill in at least one time field."
                    return False
        
        value = super().validate_on_submit(*args, **kwargs)
        self.error_message = self.errors
        print("Here", value)
        return value
