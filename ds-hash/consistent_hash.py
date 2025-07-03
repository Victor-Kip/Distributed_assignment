import bisect

class ConsistentHashing:
    def __init__(self, total_slots=512):
        self.total_slots = total_slots
        self.virtual_nodes = {}  # slot → server_id
        self.sorted_slots = []   # sorted list of slots
        self.server_virtuals = {}  # server_id → [slots]

    def _hash_request(self, request_id):
        return (request_id + 2 ** request_id + 17) % self.total_slots

    def _hash_virtual(self, server_id, virtual_index):
        return (server_id ** 2 + virtual_index + 2 ** virtual_index + 25) % self.total_slots

    def add_server(self, server_id):
        self.server_virtuals[server_id] = []
        for j in range(9):  # 9 virtual nodes
            slot = self._hash_virtual(server_id, j)
            while slot in self.virtual_nodes:
                slot = (slot + 1) % self.total_slots
            self.virtual_nodes[slot] = server_id
            self.server_virtuals[server_id].append(slot)
            bisect.insort(self.sorted_slots, slot)

    def remove_server(self, server_id):
        if server_id not in self.server_virtuals:
            return
        for slot in self.server_virtuals[server_id]:
            del self.virtual_nodes[slot]
            self.sorted_slots.remove(slot)
        del self.server_virtuals[server_id]

    def get_server(self, request_id):
        if not self.virtual_nodes:
            return None
        request_slot = self._hash_request(request_id)
        idx = bisect.bisect_left(self.sorted_slots, request_slot)
        if idx == len(self.sorted_slots):
            idx = 0
        slot = self.sorted_slots[idx]
        return self.virtual_nodes[slot]
