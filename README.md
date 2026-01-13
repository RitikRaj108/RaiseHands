# RaiseHands

Project README
**RaiseHands**

A minimal Django + Channels application that provides a realtime "raise hand" classroom feature so teachers and students can interact during live sessions.

**Features**

- Realtime raise-hand notifications using Django Channels and WebSockets.

- Separate teacher and student views.

- Simple routing and consumer structure for easy extension.

**Tech Stack**

- Python 3.8+ (or compatible)

- Django

- Django Channels (ASGI)

- Redis (optional, recommended for production / channel layer)

**Repository layout**

- `manage.py` — Django management entrypoint

- `requirements.txt` — Python dependencies

- `docker-compose.yml` — optional Docker services (e.g., Redis + app)

- `raisehand_project/` — Django project (ASGI, settings, urls)

- `classroom/` — app containing views, consumers, templates and routing

Requirements
-----------

Install Python dependencies (recommended in a virtual environment):

```powershell

python -m venv venv

.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

Or on macOS / Linux:

```bash

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

Local development (Django runserver)
----------------------------------

1. Apply migrations and create a superuser:

```powershell

python manage.py migrate

python manage.py createsuperuser

2. Run the development server (ASGI server enabled via `asgi.py`):

```powershell

python manage.py runserver

```

3. Open a browser at `http://127.0.0.1:8000/` to view the app.

Using Docker (optional)
-----------------------

If you prefer Docker and `docker-compose`, start the services with:

```powershell

docker-compose up --build

```

This will start the application and any configured services (for example, Redis). Adjust your `docker-compose.yml` and settings as needed for production.

Notes on Channels / Production
------------------------------

- For production use, configure a persistent channel layer (Redis) and run an ASGI server such as Daphne or Uvicorn with workers.

- Ensure static files are collected and served (e.g., via WhiteNoise or a dedicated static server) and DEBUG=False in production settings.

Development tips
----------------

- Templates are in `classroom/templates/classroom/` (teacher, student, index pages).

- WebSocket consumers are in `classroom/consumers.py` and routing is in `classroom/routing.py` and `raisehand_project/asgi.py`.

- To add new realtime features, extend the consumer methods and update the frontend JS to send/receive JSON messages.

Contributing
------------

1. Fork the repo and create a feature branch.

2. Run the app locally and add tests where appropriate.

3. Open a pull request describing the change.

License
-------

This project is provided as-is; add an appropriate LICENSE file if you plan to reuse or distribute it.

Questions
---------
If you want, I can: run the project locally, add a Dockerfile, wire Redis in `docker-compose.yml`, or add a short quickstart script. Tell me which you'd like next.
# 🙋‍♂️ RaiseHand Lite

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django Channels](https://img.shields.io/badge/Django%20Channels-WebSocket-006d5b?style=for-the-badge&logo=django&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

> **A real-time student-teacher interaction tool built to demonstrate the power of WebSockets, Async Python, and Django Channels.**

---

## 📖 Project Overview
**RaiseHand Lite** solves the problem of laggy classroom interactions. Unlike traditional web apps that require page refreshes, this project uses **WebSockets** to maintain a persistent, bi-directional connection. 

It allows students to "raise their hand" virtually, sending an instant signal to the teacher's dashboard using the **ASGI (Asynchronous Server Gateway Interface)** protocol.

---

## ✨ Features

- **🖐️ Real-time Hand Raising:** Instant updates using WebSocket frames. No polling or refreshing required.
- **👨‍🏫 Live Teacher Dashboard:** Teachers see an auto-updating queue of students who need attention.
- **⚡ Instant Acknowledgment:** One-click dismissal of raised hands, syncing state across all connected clients instantly.
- **🔔 Audio Notifications:** Custom JavaScript triggers sound alerts when a new hand is raised.
- **🎨 Modern UI:** Glassmorphism design system using Tailwind CSS with dark mode.
- **🔌 Connection Health:** Visual indicators showing real-time WebSocket connection status (Connected/Disconnected).
- **🔄 Session Tracking:** Handles multiple rooms and concurrent sessions via Redis Channel Layers.

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Django 4.2** | The core backend web framework. |
| **Django Channels** | Extends Django to handle WebSockets and Async protocols. |
| **Redis** | The backing store for Channel Layers (handles message passing). |
| **Daphne** | Production-grade ASGI server for handling async connections. |
| **Vanilla JavaScript** | Client-side WebSocket management (`ReconnectingWebSocket`). |
| **Tailwind CSS** | Utility-first CSS for rapid styling. |

---

## 🏗️ Architecture & Data Flow

This project moves away from the standard WSGI (Request-Response) cycle to an ASGI (Event-Driven) cycle.

```mermaid
sequenceDiagram
    participant S as Student
    participant SRV as Django ASGI (Daphne)
    participant R as Redis Channel Layer
    participant T as Teacher

    Note over S, T: WebSocket Handshake (ws://)
    
    S->>SRV: JSON: {"type": "raise_hand", "name": "Ritik"}
    Note right of S: Student clicks "Raise Hand"
    
    SRV->>R: Group Send ("room_1", event)
    Note right of SRV: Consumer processes message
    
    R->>SRV: Broadcast to Group
    
    SRV-->>T: Push Event (Update DOM & Play Sound)
    Note right of T: Teacher sees alert instantly
    
    T->>SRV: JSON: {"type": "acknowledge", "id": 1}
    SRV->>R: Group Send ("room_1", ack_event)
    R->>SRV: Broadcast to Group
    SRV-->>S: Push Event (Hand Lowered)


raisehand lite/
├── raisehand_project/      # Project Configuration
│   ├── asgi.py             # Entry point for ASGI (Crucial for Channels)
│   ├── settings.py         # Config including CHANNEL_LAYERS
│   └── urls.py             # Main routing
├── classroom/              # Core Application
│   ├── consumers.py        # WebSocket logic (Handle connections/messages)
│   ├── routing.py          # WebSocket URL routing (ws://path)
│   ├── views.py            # Standard HTTP Views
│   └── templates/          # HTML Interfaces
│       ├── base.html
│       ├── student.html
│       └── teacher.html
├── manage.py
├── requirements.txt
└── docker-compose.yml      # Redis configuration


# Clone the repository
git clone [https://github.com/yourusername/raisehand-lite.git](https://github.com/yourusername/raisehand-lite.git)
cd "raisehand lite"

# Create Virtual Environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

python manage.py migrate

# Start the Daphne/Django development server
python manage.py runserver
