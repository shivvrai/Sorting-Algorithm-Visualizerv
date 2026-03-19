# 🔄 Sorting & Graph Algorithm Visualizer

An interactive, educational web app to **visualize sorting and graph algorithms step-by-step**, with detailed explanations, time trials, code snippets, and educational resources.

> **Live demo & learning tool** — built with FastAPI + Vanilla JS

---

## ✨ Features

| Feature                     | Description                                                |
| --------------------------- | ---------------------------------------------------------- |
| **7 Sorting Algorithms**    | Bubble, Selection, Insertion, Merge, Quick, Heap, Counting |
| **5 Graph Algorithms**      | BFS, DFS, Dijkstra, Prim, Kruskal                          |
| **Step-by-step Animations** | Pause, play, step forward/backward                         |
| **Time Trial Mode**         | Race all sorting algorithms on the same data               |
| **Education Panel**         | How it works, when to use, real-world uses, code snippets  |
| **Graph Builder**           | Interactive canvas — add nodes, edges, weights             |
| **Export Results**          | JSON or CSV export                                         |

---

## 📁 Project Structure

```
sorting-visualizer/
├── app/                        # Backend (FastAPI)
│   ├── __init__.py             # App factory (CORS, routers, logging)
│   ├── config.py               # Settings from .env
│   ├── main.py                 # Entry point (uvicorn)
│   ├── algorithms/
│   │   ├── sorting.py          # 7 sorting algorithms + registry
│   │   └── graph.py            # 5 graph algorithms + registry
│   ├── data/
│   │   ├── sorting_metadata.py # Educational info for sorting
│   │   ├── sorting_code.py     # Code snippets (Python, JS)
│   │   └── graph_metadata.py   # Educational info + code for graphs
│   ├── models/
│   │   └── schemas.py          # Pydantic request validation
│   └── routes/
│       ├── sorting.py          # /api/sort, /api/time-trial, etc.
│       ├── graph.py            # /api/graph-solve, etc.
│       └── health.py           # /api/health
├── static/                     # Frontend
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── tests/
│   ├── test_sorting.py
│   └── test_graph.py
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/sorting-visualizer.git
cd sorting-visualizer

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env if you need to change PORT, CORS, etc.
```

### 3. Run

```bash
python -m app.main
```

Open **http://localhost:8000** in your browser.

### 4. Run Tests

```bash
pip install pytest httpx
python -m pytest tests/ -v
```

---

## 🐳 Docker Deployment

### Build & Run Locally

```bash
docker build -t sorting-visualizer .
docker run -p 8000:8000 sorting-visualizer
```

### Or with Docker Compose

```bash
docker compose up -d
```

Open **http://localhost:8000**.

---

## ☁️ AWS Free Tier Deployment (EC2 + Docker)

> **Cost: Free** — using EC2 t2.micro (750 hrs/month for 12 months)

### Step 1: Launch EC2

1. Sign in to [AWS Console](https://console.aws.amazon.com)
2. Go to **EC2 → Launch Instance**
3. Configure:
   - **Name**: `sorting-visualizer`
   - **AMI**: Amazon Linux 2023 (free tier eligible)
   - **Instance type**: `t2.micro` (free tier)
   - **Key pair**: Create new or select existing (download `.pem` file!)
   - **Security Group**: Allow:
     - SSH (port 22) — your IP only
     - HTTP (port 80) — anywhere
     - Custom TCP (port 8000) — anywhere
4. Click **Launch Instance**

### Step 2: Connect via SSH

```bash
# Make key readable (Mac/Linux)
chmod 400 your-key.pem

# Connect
ssh -i your-key.pem ec2-user@<YOUR_EC2_PUBLIC_IP>
```

On Windows, use PuTTY or:

```powershell
ssh -i your-key.pem ec2-user@<YOUR_EC2_PUBLIC_IP>
```

### Step 3: Install Docker on EC2

```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Log out and back in for group changes
exit
# SSH back in
ssh -i your-key.pem ec2-user@<YOUR_EC2_PUBLIC_IP>
```

### Step 4: Deploy the App

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/sorting-visualizer.git
cd sorting-visualizer

# Create .env
cp .env.example .env

# Build and run
docker compose up -d --build
```

### Step 5: Access the App

Open in browser:

```
http://<YOUR_EC2_PUBLIC_IP>:8000
```

### Step 6 (Optional): Use Port 80 with Nginx

```bash
# Install Nginx
sudo yum install -y nginx

# Configure reverse proxy
sudo tee /etc/nginx/conf.d/visualizer.conf << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

Now access at: `http://<YOUR_EC2_PUBLIC_IP>` (no port needed!)

### Step 7 (Optional): Free SSL with Let's Encrypt

```bash
# Install certbot
sudo yum install -y certbot python3-certbot-nginx

# Get certificate (need a domain pointing to your EC2 IP)
sudo certbot --nginx -d your-domain.com

# Auto-renew
sudo systemctl enable certbot-renew.timer
```

---

## 🔧 API Endpoints

| Method | Endpoint                           | Description                         |
| ------ | ---------------------------------- | ----------------------------------- |
| `POST` | `/api/sort`                        | Sort array with step-by-step output |
| `POST` | `/api/time-trial`                  | Race all algorithms                 |
| `GET`  | `/api/algorithm-info/{name}`       | Educational metadata                |
| `GET`  | `/api/algorithm-code/{name}`       | Code snippets                       |
| `POST` | `/api/graph-solve`                 | Run graph algorithm                 |
| `GET`  | `/api/graph-algorithm-info/{name}` | Graph algo metadata                 |
| `GET`  | `/api/health`                      | Health check                        |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Frontend**: Vanilla HTML/CSS/JS, Canvas API
- **Containerization**: Docker, Docker Compose
- **Deployment**: AWS EC2 (free tier) + Nginx

---

## 📄 License

MIT
