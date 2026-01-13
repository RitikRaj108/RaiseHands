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
