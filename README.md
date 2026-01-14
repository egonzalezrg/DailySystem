# DailySystem 

Daily System is a flexible personal system for tracking habits, routines, and daily behaviors over time that support self-imporvement.

The goal of the project is to move away from motivation-based tracking and toward consistent, system-driven progress.

This repository represents the foundation of a larger personal system that will continue to expand with additional tracking features and a future mobile app.

# Features (current)

- Create and manage habits (build or eliminate behaviors)
- Track habits on a weekly, date-based view
- Navigate between past and future weeks
- Persist habit history using a local database
- Delete habits cleanly along with their history
- Simple, distraction-free UI focused on consistency

The system uses real calendar dates, allowing progress to be tracked reliably across weeks, months, and years.

# The Why? for this project

Many productivity tools rely on motivation or streak pressure.
This project is built around the idea that systems and a strategic plan will do a better job at targetting consistency and accountability.

By keeping the interface simple and focusing on daily consistency, the app encourages sustainable habit-building rather than short-term intensity.

# Tech Stack

- # Python (Flask)
- # SQLite (date-based persistence)
- # HTML / CSS
- # Jinja templates
- # Git / GitHub

The project is intentionally lightweight and beginner-friendly while following clean structure and best practices.

# Requirements for Running the project lgood?ocally

Python 3.10+ recommended
Flask

Setup & Run on Windows (local)
  pytohn -m venv venv
  venv\Scripts\activate
  pip install flask
  python app.py

Setup & Run on macOS / Linux (local)
  python3 -m venv venv
  source venv/bin/activate
  pip install flask
  python app.py

Then open your browser and go to:
http://127.0.0.1:5000 

# Project structure currently
.
├── app.py
├── schema.sql
├── static/
│   └── styles.css
├── templates/
│   ├── index.html
│   ├── system.html
│   ├── habits.html
│   └── table.html
└── README.md

# Future plans

This project is just getting started. Planned expansions include:
- Additional self-improvement tracking (e.g. nutrition, workouts, focus)
- More flexible tracking types (counts, metrics, trends)
- Data insights and summaries
- Improved UI and UX
- A dedicated mobile app experience

The current codebase is designed to scale as these features are added incrementally.

# Status

This is an active personal project and will continue to evolve over time.
The current version represents a stable foundation that future features will build upon.
