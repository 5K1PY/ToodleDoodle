import datetime
from flask import Flask, render_template, redirect
from werkzeug.exceptions import abort

from form import PollForm
from db import make_poll, poll_exists

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
    form = PollForm()
    if form.validate_on_submit():
        poll_name = form.poll_title.data
        poll_options = gen_options(form.options.data)
        print(poll_name, poll_options)

    return render_template('new_poll.html', form=form)

@app.route('/polls/<int:poll_id>')
def get_poll(poll_id):
    if not poll_exists(poll_id):
        abort(404)
    return ""


app.run(debug=True, use_debugger=False, use_reloader=True)
