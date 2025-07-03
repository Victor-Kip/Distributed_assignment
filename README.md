# 🧠 Distributed Systems Load Balancer – Hackathon Project

This project implements a simple yet powerful load balancer using *consistent hashing* to route HTTP requests across multiple containerized backend servers. It supports *dynamic scaling, **heartbeat monitoring, and **auto-recovery* of failed servers.

---

## 📦 Project Structure

ds-assignment/
├── ds-server/ # Flask server container
│ └── server.py
├── ds-loadbalancer/ # Flask load balancer container
│ ├── balancer.py
│ ├── consistent_hash.py
│ └── Dockerfile
├── ds-simulation/ # Request simulator + visualizer
│ └── simulate_requests.py


## 🚀 Features

- ⚖️ Load balancing via **consistent hashing**
- 🔁 **Heartbeat monitoring** (every 5 seconds)
- 🛠️ **Auto-restarts** failed servers on crash
- 📊 Python script to simulate requests and visualize server load
- 🔧 Built using **Flask**, **Docker**, and **Matplotlib**

## 🛠 Setup Instructions

### 1. Build Docker Images


Build server image
cd ds-server
docker build -t ds-server .

# Build load balancer image
cd ../ds-loadbalancer
docker build -t ds-loadbalancer .

2. Create Docker Network
docker network create ds_net

4. Run Load Balancer
docker run -it -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock --network ds_net ds-loadbalancer

➕ Adding Servers
In another terminal:
curl.exe -X POST http://localhost:5000/add
curl.exe -X POST http://localhost:5000/add
curl.exe -X POST http://localhost:5000/add

🧪 Testing with Requests
curl.exe "http://localhost:5000/home?id=12"
Returns:
{
  "message": "Hello from Server: 1",
  "status": "successful"
}

💥 Simulate Server Crash
docker stop server-2
Your load balancer will log:
[!] Server 2 failed heartbeat. Restarting...
[+] Server 2 restarted

📈 Request Simulation (A-1 / A-2)
Simulate 100 random requests and visualize server usage:
cd ds-simulation
python simulate_requests.py
Generates a chart like:
[Screenshot 2025-07-03 213244](https://github.com/user-attachments/assets/c7639ce3-15e5-49ba-a028-7982340aa859)

