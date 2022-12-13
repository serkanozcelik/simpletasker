
# simpletasker
### Job tracking web app for freelancers ..


#### Video Demo: https://www.youtube.com/watch?v=SiT9pwRzX9M



[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)


## About:

simpletasker is a simple and user-friendly task tracking application designed for freelance workers. With this web application, you can create a to-do list for your business processes, and you can track your earnings by job type on this list.

It will calculate your earnings based on the hourly rates you set for the tasks and jobs you define. You can also use this to provide your clients with a list of tasks and costs.


## Assets

- Multi-user
- Customers / Clients
- Jobs and tasks
- Job types with definable hourly rates
- Monitoring of earnings $


## Tech Stack

**Frontend:** Html5, Css3, Javascript, Bootstrap

**Backend:** Python, Flask

**Database:** SQLite3

## Installation

To install simpletasker, follow these steps:

```bash
  # Clone this repository
  $ git clone https://github.com/serkanozcelik/simpletasker.git

  # Install requirements:
  $ pip install -r requirements.txt

  # cd simpletasker
  # flask run
```

## Usage

To use simpletasker, run the flask:

```bash
  # cd simpletasker
  # flask run
```
Go to http://127.0.0.1:5000/ to see the app running.

## SQLITE3 table schemas

```bash
CREATE TABLE sqlite_sequence(name,seq)

CREATE TABLE "clients" (
	"clientid"	INTEGER NOT NULL,
	"userid"	INTEGER,
	"name"	TEXT NOT NULL,
	"email"	TEXT,
	"contact"	TEXT,
	"phone"	TEXT,
	"address"	TEXT,
	"status"	INTEGER DEFAULT 1,
	PRIMARY KEY("clientid" AUTOINCREMENT)
)

CREATE TABLE "jobTypes" (
	"typeid"	INTEGER NOT NULL,
	"userid"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"price"	INTEGER NOT NULL DEFAULT 0,
	"status"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("typeid" AUTOINCREMENT)
)

CREATE TABLE "tasks" (
	"taskid"	INTEGER NOT NULL,
	"userid"	INT NOT NULL,
	"jobTypeId"	INTEGER NOT NULL,
	"clientid"	INT NOT NULL,
	"section"	TEXT NOT NULL,
	"page"	TEXT NOT NULL,
	"brief"	TEXT NOT NULL,
	"inDate"	INTEGER,
	"startDate"	INTEGER,
	"finishDate"	INTEGER,
	"duration"	INT,
	"price"	INTEGER NOT NULL DEFAULT 0,
	"revenue"	INTEGER NOT NULL DEFAULT 0,
	"status"	INT DEFAULT 1,
	PRIMARY KEY("taskid" AUTOINCREMENT)
)

CREATE TABLE "users" (
	"id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL,
	"hash"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)
```

## Thanks to ..
I would like to thank the following people:

The Harvard University cs50x team for the libraries and training they provided
The developers who will continue to improve this simple application in the future
Myself for successfully graduating from the Harvard University cs50x program :)

