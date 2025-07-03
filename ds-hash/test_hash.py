from consistent_hash import ConsistentHashing

ch = ConsistentHashing()

# Add 3 servers
ch.add_server(1)
ch.add_server(2)
ch.add_server(3)

# Simulate request distribution
for i in range(10):
    server = ch.get_server(i)
    print(f"Request {i} → Server {server}")
