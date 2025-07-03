import requests
import random
import matplotlib.pyplot as plt

# Number of simulated requests 
NUM_REQUESTS = 100

# IDs to use (e.g., 0 to 99)
request_ids = [random.randint(0, 1000) for _ in range(NUM_REQUESTS)]

# Track which server handled each ID
server_hits = {}

# Send requests to the load balancer
for req_id in request_ids:
    try:
        r = requests.get(f"http://localhost:5000/home", params={"id": req_id}, timeout=3)
        if r.status_code == 200:
            msg = r.json().get("message", "")
            server_id = msg.split(":")[-1].strip()
            server_hits[server_id] = server_hits.get(server_id, 0) + 1
        else:
            print(f"[!] Request ID {req_id} failed with code {r.status_code}")
    except Exception as e:
        print(f"[!] Request ID {req_id} failed:", e)

# Plot results
servers = list(server_hits.keys())
hits = [server_hits[s] for s in servers]

plt.bar(servers, hits, color='skyblue')
plt.xlabel("Server ID")
plt.ylabel("Number of Requests")
plt.title("Request Distribution via Consistent Hashing")
plt.show()
