import bisect

slots = 512
physical_servers = 3
virtual_servers = 9

class ConsistentHashing:
    def __init__(self):
        self.ring = []
        self.nodes = {}

    def _hash(self, value):
        return value % slots

    def virtual_server_hash(self, i, j):
        return self._hash(i**2 + j + 2*j + 25)

    def request_hash(self, request_id):
        return self._hash(request_id**2 + 2*request_id + 17)

    def add_server(self, server_id):
        for j in range(virtual_servers):
            original_slot = self.virtual_server_hash(server_id, j)
            slot = original_slot
            probe_count = 0

            while slot in self.nodes:
                probe_count += 1
                slot = (original_slot + probe_count**2) % slots

            bisect.insort(self.ring, slot)
            self.nodes[slot] = f"Server{server_id} - Virtual{j}"

    def get_server(self, request_id):
        h = self.request_hash(request_id)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0
        slot = self.ring[idx]
        return self.nodes[slot]

if __name__ == "__main__":
    ch = ConsistentHashing()
    for sid in range(1, physical_servers + 1):
        ch.add_server(sid)

    for rid in [132574, 456789, 987654, 111222, 333444, 
        555666, 777888, 999000, 123456, 654321]:
        server = ch.get_server(rid)
        print(f"Request {rid} mapped to: {server}")
    