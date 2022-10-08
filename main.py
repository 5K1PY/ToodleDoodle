import sqlite3
from flask import Flask, render_template, request

from form import PollForm
from db import make_poll

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sosecret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_poll', methods=['GET', 'POST'])
def new_poll():
    form = PollForm()
    if form.validate_on_submit():
        poll_name = form.poll_title.data
        poll_options = []
        for option_create in form.options.data:
            day = option_create['day']
            mode = option_create['mode']
            time1 = option_create['time1']
            time2 = option_create['time2']

            if mode == 'Whole day':
                poll_options.append(f'{day.strftime("%Y-%m-%d")}')
            elif mode == 'Hourly range':
                while time1 <= time2:
                    poll_options.append(f'{day.strftime("%Y-%m-%d")} {time1.strftime("%H:%M")}')
                    time1 = time1.replace(hour=time1.hour+1)
            elif mode == 'Concrete time':
                poll_options.append(f'{day.strftime("%Y-%m-%d")} {time1.strftime("%H:%M")}')
        make_poll(poll_name, poll_options)

    return render_template('new_poll.html', form=form)

app.run(debug=True, use_debugger=False, use_reloader=True)
