# 🙋‍♂️ RaiseHand Lite

A **real-time student-teacher interaction tool** built with Django Channels and WebSockets. This project demonstrates how to build instant, bi-directional communication in a classroom setting.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2+-green?logo=django)
![WebSocket](https://img.shields.io/badge/WebSocket-Enabled-orange)
![Redis](https://img.shields.io/badge/Redis-7.0-red?logo=redis)

---

## ✨ Features

- **Real-time Hand Raising**: Students can raise/lower hands instantly
- **Live Teacher Dashboard**: Teachers see raised hands in real-time
- **Instant Acknowledgment**: Teachers can dismiss hands with one click
- **Multiple Rooms**: Support for multiple concurrent classrooms
- **Beautiful UI**: Modern dark theme with glassmorphism effects
- **Sound Notifications**: Audio alert when students raise hands
- **Connection Status**: Visual indicator for WebSocket connection
- **Session Tracking**: Timer and acknowledgment counter

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Django 4.2** | Web framework |
| **Django Channels** | WebSocket support |
| **Redis** | Channel layer backend |
| **Daphne** | ASGI server |
| **Tailwind CSS** | Styling (via CDN) |
| **Vanilla JavaScript** | WebSocket client |

---

## 📁 Project Structure

```
raisehand lite/
├── raisehand_project/          # Django project configuration
│   ├── settings.py             # Django + Channels config
│   ├── asgi.py                 # ASGI entry point
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI fallback
├── classroom/                  # Main application
│   ├── consumers.py            # WebSocket consumer logic
│   ├── routing.py              # WebSocket URL routing
│   ├── views.py                # HTTP views
│   ├── urls.py                 # App URLs
│   └── templates/classroom/
│       ├── base.html           # Base template
│       ├── index.html          # Landing page
│       ├── student.html        # Student interface
│       └── teacher.html        # Teacher dashboard
├── manage.py
├── requirements.txt
├── docker-compose.yml          # Redis container
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Step 1: Clone & Setup Virtual Environment

```bash
cd "d:\Teaching Role\Projects\raisehand lite"

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run Migrations

```bash
python manage.py migrate
```

### Step 4: Start the Server

```bash
# Start Django development server
python manage.py runserver 8000
```

### Step 5: Open in Browser

1. **Landing Page**: http://localhost:8000/
2. **Student View**: http://localhost:8000/student/room1/?name=YourName
3. **Teacher View**: http://localhost:8000/teacher/room1/?name=Teacher

> **Note:** By default, the app uses `InMemoryChannelLayer` which works perfectly for development and demos. For production, you can switch to Redis by updating `settings.py`.


---

## 🎮 How to Use

### As a Student
1. Go to the landing page
2. Enter your name and room code
3. Click "Student" to join
4. Click the big hand button to raise your hand
5. Wait for teacher acknowledgment

### As a Teacher
1. Go to the landing page
2. Enter your name and same room code
3. Click "Teacher" to join
4. See students who raise hands in real-time
5. Click "Acknowledge" to dismiss a hand

---

## 🔧 Configuration

### Settings Overview (`raisehand_project/settings.py`)

```python
# ASGI application for WebSocket support
ASGI_APPLICATION = 'raisehand_project.asgi.application'

# Redis channel layer configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
```

### Environment Variables (Production)

```bash
export SECRET_KEY="your-production-secret-key"
export DEBUG=False
export REDIS_URL="redis://your-redis-host:6379"
```

---

## 🧪 Testing

### Manual Testing Flow
1. Open two browser windows
2. Join as Student in one, Teacher in another
3. Use the same room code (e.g., "room1")
4. Raise hand as student → Should appear on teacher dashboard
5. Acknowledge as teacher → Student gets notified

### Test Multiple Students
Open multiple incognito windows with different student names to test concurrent functionality.

---

## 🏗️ Architecture

### WebSocket Message Flow

```
Student                    Server (Django Channels)              Teacher
   │                              │                                 │
   │──── Connect ─────────────────│                                 │
   │                              │                                 │
   │                              │◄───────── Connect ──────────────│
   │                              │                                 │
   │── {"type": "raise_hand"} ───►│                                 │
   │                              │── Broadcast to group ──────────►│
   │                              │                                 │
   │                              │◄── {"type": "acknowledge"} ─────│
   │◄─── Broadcast ───────────────│                                 │
   │                              │                                 │
```

### Key Components

1. **ASGI Router** (`asgi.py`): Routes HTTP and WebSocket traffic
2. **Consumer** (`consumers.py`): Handles WebSocket events
3. **Channel Groups**: Allow broadcasting to multiple users
4. **Redis**: Stores channel layer state for message passing

---

## 💼 Interview Talking Points

### Why Django Channels?
> "I used Django Channels because traditional HTTP is request-response based and too slow for real-time interaction. Channels provides WebSocket support through ASGI, allowing persistent connections."

### Why AsyncWebsocketConsumer?
> "AsyncWebsocketConsumer uses Python's async/await pattern, allowing the server to handle thousands of concurrent connections without blocking. This is essential for real-time applications."

### Why Redis for Channel Layers?
> "Redis serves as the backing store for channel layers, enabling message passing between different consumers. It's fast, reliable, and supports pub/sub patterns needed for broadcasting."

### Scalability Considerations
> "This architecture scales horizontally. Multiple Daphne workers can share the same Redis instance, allowing the application to handle more concurrent users across multiple server instances."

### Alternative Approaches
> "I could have used polling (HTTP requests every few seconds) but that's inefficient. WebSockets maintain a single TCP connection, reducing latency and server load."

---

## 📦 Production Deployment

### Using Daphne + Nginx

```nginx
# nginx.conf
upstream channels-backend {
    server localhost:8000;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://channels-backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "raisehand_project.asgi:application"]
```

---

## 🎨 UI Screenshots

The application features a modern, dark-themed UI with:
- Glassmorphism card effects
- Gradient backgrounds and buttons
- Smooth animations and transitions
- Responsive design for all screen sizes

---

## 📚 Learning Resources

- [Django Channels Documentation](https://channels.readthedocs.io/)
- [WebSocket API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Redis Pub/Sub](https://redis.io/topics/pubsub)
- [ASGI Specification](https://asgi.readthedocs.io/)

---

## 📝 License

MIT License - Feel free to use this project for learning and portfolio purposes.

---

## 👨‍💻 Author

Built with ❤️ for interview preparation.

> "This project demonstrates my understanding of real-time web technologies, async programming, and modern full-stack development with Django."
#   R a i s e H a n d s  
 