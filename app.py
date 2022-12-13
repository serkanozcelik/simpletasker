from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, durationPretty
import datetime
from datetime import date
import json

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///simpletask.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show Tasks by criterias"""
    # Show tasks table, filter by user session data and client criterias.

    if request.args.get("submit") == 'remove' and request.args.get("taskid"):
        sql = db.execute("UPDATE tasks SET status = -1 WHERE userid = ? AND taskid = ?", session["userid"], request.args.get("taskid"))
        if sql > 0:
            flash('Task removed!')
        else:
            flash('Task not removed!', 'error')

    if request.args.get("clientid"):
        tasks = db.execute("SELECT tasks.*, clients.name AS client, jobTypes.name as jobType FROM tasks, clients, jobTypes WHERE clients.clientid = tasks.clientid AND jobTypes.typeid = tasks.jobTypeId AND tasks.status != -1 AND tasks.userid = ? AND tasks.clientid = ? ORDER BY tasks.taskid DESC", session["userid"], request.args.get("clientid"))
    else:
        tasks = db.execute("SELECT tasks.*, clients.name AS client, jobTypes.name as jobType FROM tasks, clients, jobTypes WHERE clients.clientid = tasks.clientid AND jobTypes.typeid = tasks.jobTypeId AND tasks.status != -1  AND tasks.userid = ? ORDER BY tasks.taskid DESC", session["userid"])

    income = 0

    for i, task in enumerate(tasks):
        task["row"] = len(tasks)-i
        task["inDate"] = datetime.datetime.fromtimestamp(task["inDate"]).strftime('%d.%m.%Y')
        task["startDate"] = datetime.datetime.fromtimestamp(task["startDate"]).strftime('%d.%m.%Y')
        task["finishDate"] = datetime.datetime.fromtimestamp(task["finishDate"]).strftime('%d.%m.%Y')
        task["durationPretty"] = durationPretty(task["duration"])
        income += task["income"]

    clients = db.execute("SELECT * FROM clients WHERE status != -1 AND userid = ?", session["userid"])

    return render_template("index.html", tasks = tasks, clients = clients, clientid = request.args.get("clientid"), count = len(tasks), income="{:.2f}".format(income))

@app.route("/clients")
@login_required
def clients():
    """Show Clients by criterias"""
    # Show clients table, filter by user session data.

    if request.args.get("submit") == 'remove' and request.args.get("clientid"):
        sql = db.execute("UPDATE clients SET status = -1 WHERE userid = ? AND clientid = ?", session["userid"], request.args.get("clientid"))
        if sql > 0:
            flash('Client removed!')
        else:
            flash('Client not removed!', 'error')

    clients = db.execute("SELECT * FROM clients WHERE status != -1 AND userid = ?", session["userid"])
    for i, client in enumerate(clients, start = 1):
        client["row"] = i

    return render_template("clients.html", clients = clients, count = len(clients))


@app.route("/addClient", methods=["GET", "POST"])
@login_required
def addClient():
    """Client Operations"""
    # Add new client or editing the previous one.

    if request.method == "POST":

        if not request.form.get("clientid"):

            sql = "INSERT INTO clients (userid, name, email, contact, phone, address) VALUES (?)"
            val = (session["userid"], request.form.get("name"), request.form.get("email"), request.form.get("contact"), request.form.get("phone"), request.form.get("address"))

            db.execute(sql, val)

            flash('Client Added!')

        else:

            db.execute("UPDATE clients SET name = ?, email = ?, contact = ?, phone = ?, address = ? WHERE clientid = ?",
            request.form.get("name"), request.form.get("email"), request.form.get("contact"), request.form.get("phone"), request.form.get("address"), request.form.get("clientid"))

            flash('Client Updated!')

        return redirect("/clients")

    else:

        client = []

        if request.args.get("clientid"):
            client = db.execute("SELECT * FROM clients WHERE clientid = ?", request.args.get("clientid"))[0]

        return render_template("/addClient.html", client = client)


@app.route("/addTask", methods=["GET", "POST"])
@login_required
def addTask():
    """Task Operations"""
    # Add new task or editing the previous one.

    # Form submit events
    if request.method == "POST":
        if not request.form.get("clientid"):
            return apology("Must provide clientid", 400)

        if not request.form.get("taskid"):
            #inDate = int(datetime.datetime.strptime(request.form.get("inDate"), '%Y-%m-%d').strftime("%s"))
            inDate = datetime.datetime.strptime(request.form.get("inDate"), "%Y-%m-%d").timestamp()
            startDate = datetime.datetime.strptime(request.form.get("startDate"), "%Y-%m-%d").timestamp()
            finishDate = datetime.datetime.strptime(request.form.get("finishDate"), "%Y-%m-%d").timestamp()

            sql = "INSERT INTO tasks (userid, clientid, section, page, jobTypeId, brief, inDate, startDate, finishDate, duration, price, income) VALUES (?)"
            val = (session["userid"], request.form.get("clientid"), request.form.get("section"), request.form.get("page"), request.form.get("typeid"), request.form.get("brief"), inDate, startDate, finishDate, request.form.get("duration"), request.form.get("price"), round(int(request.form.get("duration")) * (int(request.form.get("price")) / 60), 2))

            db.execute(sql, val)

            flash('Task Added!')


        else:
            inDate = datetime.datetime.strptime(request.form.get("inDate"), "%Y-%m-%d").timestamp()
            startDate = datetime.datetime.strptime(request.form.get("startDate"), "%Y-%m-%d").timestamp()
            finishDate = datetime.datetime.strptime(request.form.get("finishDate"), "%Y-%m-%d").timestamp()

            db.execute("UPDATE tasks SET section = ?, page = ?, jobTypeId = ?, brief = ?, inDate = ?, startDate = ?, finishDate = ?, duration = ?, price = ?, income = ? WHERE taskid = ?",
            request.form.get("section"), request.form.get("page"), request.form.get("typeid"), request.form.get("brief"), inDate, startDate, finishDate, request.form.get("duration"), request.form.get("price"), round(int(request.form.get("duration")) * (int(request.form.get("price")) / 60), 2), request.form.get("taskid"))

            flash('Task Updated!')

        return redirect("/?clientid=" + request.form.get("clientid"))

    else:

        # Empty form or get record data you want to edit
        if not request.args.get("clientid"):
            return apology("Must provide clientid", 400)

        client = db.execute("SELECT clientid, name FROM clients WHERE userid = ? AND clientid = ?", session["userid"], request.args.get("clientid"))[0]
        jobTypes = db.execute("SELECT * FROM jobTypes WHERE status != -1 AND userid = ?", session["userid"])

        today = date.today()
        today = today.strftime("%Y-%m-%d")

        dates = {}
        dates['inDate'] = dates['startDate'] = dates['finishDate'] = today

        data = db.execute("SELECT DISTINCT section, page FROM tasks")

        inputData = {}
        inputData['sections'] = set()
        inputData['pages'] = set()

        for x in data:
            inputData['sections'].add(x['section'])
            inputData['pages'].add(x['page'])

        inputData['sections'] = json.dumps(list(inputData['sections']))
        inputData['pages'] = json.dumps(list(inputData['pages']))


        task = []
        if request.args.get("taskid"):
            task = db.execute("SELECT tasks.*, jobTypes.price AS defaultPrice FROM tasks, jobTypes WHERE jobTypes.typeid = tasks.jobTypeId AND tasks.taskid = ?", request.args.get("taskid"))[0]

            if len(task) > 0:
                dates["inDate"] = datetime.datetime.fromtimestamp(task["inDate"]).strftime('%Y-%m-%d')
                dates["startDate"] = datetime.datetime.fromtimestamp(task["startDate"]).strftime('%Y-%m-%d')
                dates["finishDate"] = datetime.datetime.fromtimestamp(task["finishDate"]).strftime('%Y-%m-%d')


        return render_template("/addTask.html", client = client, jobTypes = jobTypes, dates = dates, inputData = inputData, task = task)


@app.route("/settings")
@login_required
def jobTypes():
    """Show settings"""
    # Get job types with their prices from jobTypes table

    if request.args.get("submit") == 'remove' and request.args.get("typeid"):
        sql = db.execute("UPDATE jobTypes SET status = -1 WHERE userid = ? AND typeid = ?", session["userid"], request.args.get("typeid"))
        if sql > 0:
            flash('Job Type removed!')
        else:
            flash('Job Type not removed!', 'error')

    jobTypes = db.execute("SELECT * FROM jobTypes WHERE status != -1 AND userid = ?", session["userid"])
    for i, jobType in enumerate(jobTypes, start = 1):
        jobType["row"] = i

    return render_template("/settings.html", jobTypes=jobTypes, count = len(jobTypes))


@app.route("/addJobType", methods=["GET", "POST"])
@login_required
def addJobType():
    """Job Type Operations"""
    # Job types and prices will be arranged from the form on this page.

    if request.method == "POST":

        if not request.form.get("typeid"):
            sql = "INSERT INTO jobTypes (userid, name, price) VALUES (?)"
            val = (session["userid"], request.form.get("name"), request.form.get("price"))
            db.execute(sql, val)

            flash('Job Type Added!')

        else:

            db.execute("UPDATE jobTypes SET name = ?, price = ? WHERE typeid = ?", request.form.get("name"), request.form.get("price"), request.form.get("typeid"))

            flash('Client Updated!')

        return redirect("/settings")

    else:

        jobType = []
        if request.args.get("typeid"):
            jobType = db.execute("SELECT * FROM jobTypes WHERE typeid = ?", request.args.get("typeid"))[0]

        return render_template("/addJobType.html", jobType = jobType)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any userid
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Must provide username", 403)
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["userid"] = rows[0]["id"]

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any userid
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("Must provide username", 400)

        if not request.form.get("password"):
            return apology("Must provide password", 400)

        if not request.form.get("confirmation"):
            return apology("Must provide password", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords not match", 400)

        # Ensure username don't already exist
        if db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username")):
            return apology("username already exist", 400)

        # Create new user in table
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        # Query database for user's id
        row = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["userid"] = row[0]["id"]

        flash("Welcome " + request.form.get("username") + ", now you're registered!")

        # Redirect user to login page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")