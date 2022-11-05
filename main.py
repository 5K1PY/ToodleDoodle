import datetime
from flask import Flask, render_template, redirect, request
from werkzeug.exceptions import abort
from urllib.parse import unquote
from constants import MODES

from form import CreationForm, PollForm, EditForm
from db import make_poll, poll_exists, read_poll, user_filled_poll, write_poll, delete_user_from_poll

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sosecret'

def gen_options(data):
    poll_options = []
    for option_create in data:
        day_mode = option_create['day_mode']
        day1, day2 = option_create['day1'], option_create['day2']
        day_increment = option_create['day_increment']
        time_mode = option_create['time_mode']
        time1, time2, time3 = option_create['time1'], option_create['time2'], option_create['time3']
        time_increment = option_create['time_increment']

        if day_mode == 'One day':
            day2 = day1
            day_increment = 1

        while day1 <= day2:
            if time_mode == "Whole day":
                poll_options.append(day1.strftime("%Y-%m-%d"))
            elif time_mode == "Various times":
                for time in (time1, time2, time3):
                    if time is not None:
                        poll_options.append(f'{day1.strftime("%Y-%m-%d")} {time.strftime("%H:%M")}')
            elif time_mode == "Hourly range":
                time = time1
                while time <= time2:
                    poll_options.append(f'{day1.strftime("%Y-%m-%d")} {time.strftime("%H:%M")}')
                    hours, minutes = time.hour, time.minute + time_increment
                    hours, minutes = (hours + minutes // 60), (minutes % 60)
                    if hours >= 24:
                        break
                    time = datetime.time(hours, minutes)
            day1 = day1 + datetime.timedelta(days=day_increment)

    poll_options = list(sorted(set(poll_options)))
    return poll_options


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/new_poll', methods=['GET', 'POST'])
def new_poll():
    form = CreationForm()
    if form.validate_on_submit():
        poll_name = form.poll_title.data  
        poll_options = gen_options(form.options.data)
        secret = make_poll(poll_name, poll_options)
        return redirect(f'/poll/{secret}')

    return render_template('new_poll.html', form=form)


def set_form_values(form, name, options):
    form.name.default = name
    form.name.process(name)
    for i in range(len(options)):
        form.options[i].default = options[i]
        form.options[i].process(options[i])

@app.route('/poll/<string:poll_id>/', methods=['GET', 'POST'])
def get_poll(poll_id):
    if not poll_exists(poll_id):
        return abort(404)

    poll = read_poll(poll_id)
    form = PollForm()
    if len(form.options) == 0:
        for i in range(len(poll.options)):
            form.options.append_entry()

    errors = ""
    validated = False

    query = request.query_string.decode('utf-8').split("=", 1)
    if query[0] == "edit":
        form = EditForm()
        for option in poll.options:
            form.options.append_entry(option)
        return render_template("edit_poll.html", form=form)
    if query[0] == "edituser":
        user = unquote(query[1])
        if not user_filled_poll(poll_id, user):
            return abort(400)
        else:
            if form.validate_on_submit():
                validated = True
                delete_user_from_poll(poll_id, user)
                write_poll(
                    form.name.data,
                    map(lambda x: x.option_id, poll.options),
                    form.options.data
                )
                return redirect(".")
            else:
                name, options = poll.remove_row(user)
                set_form_values(form, name, options)

    elif query[0] == "delete":
        user = query[1]
        if not user_filled_poll(poll_id, user):
            return abort(400)
        else:
            delete_user_from_poll(poll_id, user)
            return redirect(".")

    if validated or form.validate_on_submit():
        if user_filled_poll(poll_id, form.name.data):
            errors = "User already filled in the poll."
        else:
            write_poll(
                form.name.data,
                map(lambda x: x.option_id, poll.options),
                form.options.data
            )
            return redirect(".")
    else:
        errors = form.errors

    return render_template('poll.html', poll=poll, form=form, errors=errors, modes=MODES)

app.run(debug=True, use_debugger=False, use_reloader=True)
