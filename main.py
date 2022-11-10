from datetime import date, time
from flask import Flask, render_template, redirect, request
from werkzeug.exceptions import abort
from urllib.parse import unquote
from constants import MODES

from form import CreationForm, PollForm, EditForm, CloseForm
from db import make_poll, poll_exists, read_poll, user_filled_poll, write_poll, delete_user_from_poll, edit_poll_db, close_poll_db
from poll import gen_new_options, gen_edit_options

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sosecret'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_poll', methods=['GET', 'POST'])
def new_poll():
    form = CreationForm()
    if form.validate_on_submit():
        poll_name = form.poll_title.data
        description = form.description.data
        poll_options = gen_new_options(form.options.data)
        secret = make_poll(poll_name, description, poll_options)
        return redirect(f'/poll/{secret}')

    return render_template('new_poll.html', form=form, errors=form.error_message)


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
    closeForm = CloseForm()
    if len(form.options) == 0:
        for option in poll.options:
            form.options.append_entry()
    
    for option in poll.options:
        closeForm.options.choices.append(option.text)

    errors = ""

    # poll closed / closing
    if closeForm.validate_on_submit():
        close_poll_db(poll_id, closeForm.options.data)
        poll = read_poll(poll_id)
    if poll.closed == 'TRUE':
        return closed_poll(poll_id, poll)

    # editing poll
    query = request.query_string.decode('utf-8').split("=", 1)
    if query[0] == "edit":
        return edit_poll(poll_id, poll)

    # edditing / deleting users
    if query[0] == "edituser":
        user = unquote(query[1])
        if not user_filled_poll(poll_id, user):
            return abort(400)
        else:
            if form.validate_on_submit():
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
        user = unquote(query[1])
        if not user_filled_poll(poll_id, user):
            return abort(400)
        else:
            delete_user_from_poll(poll_id, user)
            return redirect(".")

    if form.validate_on_submit():
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

    return render_template('poll.html', poll=poll, form=form, close_form=closeForm, errors=errors, modes=MODES)

def edit_poll(poll_id, poll):
    form = EditForm(description=poll.description)
    form.error_message = ""
    if len(form.options) == 0:
        for option in poll.options:
            option = str(option).split(" ")
            day1 = date.fromisoformat(option[0])
            time1 = time.fromisoformat(option[1]) if len(option) > 1 else None
            form.options.append_entry({"day": day1, "time": time1})

    errors = ""
    if request.method == "POST":
        if form.validate_on_submit():
            edit_poll_db(poll_id, form.description.data, gen_edit_options(form.options.data))
            return redirect(".")
        else:
            errors = form.errors

    return render_template("edit_poll.html", form=form, errors=errors)

def closed_poll(poll_id, poll):
    return render_template("closed_poll.html", poll=poll)

app.run(debug=True, use_debugger=False, use_reloader=True)
