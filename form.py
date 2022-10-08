from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, IntegerField, SelectField, \
        StringField, TextAreaField, SubmitField, DateField, EmailField, TimeField
from wtforms import validators

class Option(Form):
    day = DateField(
        'Day',
        validators=[validators.InputRequired()]
    )
    mode = SelectField(
        'Mode',
        choices=["Whole day", "Hourly range", "Concrete time"]
    )
    time1 = TimeField('time1')
    time2 = TimeField('time2')

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
            if option.mode.data == "Hourly range":
                if (option.time1.data is None or option.time2.data is None):
                    self.error_message = "Please fill in time field."
                    return False
                if (option.time1.data > option.time2.data):
                    self.error_message = "Times in hourly range must be in consecutive order."
                    return False
            if option.mode.data == "Concrete time" and option.time1.data is None:
                self.error_message = "Please fill in time field."
                return False

        value = super().validate_on_submit(*args, **kwargs)
        self.error_message = self.errors
        return value
