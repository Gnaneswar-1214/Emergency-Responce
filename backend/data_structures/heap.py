import heapq
from typing import List, Optional
from .call import EmergencyCall

class PriorityQueueHeap:
    def __init__(self):
        self.heap = []
        self.call_map = {} # For O(1) access to update/delete
        # Metrics
        self.comparisons = 0
        self.swaps = 0

    def insert(self, call: EmergencyCall):
        self.call_map[call.id] = call
        heapq.heappush(self.heap, call)
        # Note: heapq doesn't easily expose swaps/comparisons, we approximate metrics
        # for a heap insertion in a perfectly balanced tree it's log(N) comparisons/swaps
        import math
        n = len(self.heap)
        if n > 0:
            h = int(math.log2(n))
            self.swaps += h // 2
            self.comparisons += h

    def extract_max(self) -> Optional[EmergencyCall]:
        while self.heap:
            call = heapq.heappop(self.heap)
            if call.id in self.call_map and self.call_map[call.id] == call:
                del self.call_map[call.id]
                import math
                n = len(self.heap)
                if n > 0:
                    h = int(math.log2(n))
                    self.swaps += h
                    self.comparisons += h * 2
                return call
        return None

    def update_severity(self, call_id: str, new_severity: int):
        if call_id in self.call_map:
            call = self.call_map[call_id]
            # Since heapq doesn't support decrease-key efficiently O(log N), 
            # we mark as deleted (remove from map) and insert a new object
            del self.call_map[call_id]
            new_call = EmergencyCall(call_id, new_severity, call.timestamp)
            self.insert(new_call)

    def delete(self, call_id: str):
        if call_id in self.call_map:
            del self.call_map[call_id]
            # It will be lazily removed from heap during extract_max

    def top_k(self, k: int) -> List[EmergencyCall]:
        # To not modify the actual heap, we can nlargest
        # However, our __lt__ makes the "max" elements the strictly smaller ones according to Python
        # Because we defined __lt__ to return True for HIGHER priority (greater severity)
        # So we actually need nsmallest to get the highest priority ones!
        # heapq is a min-heap. Top priorities are at the top (idx 0)
        
        # We must filter out "deleted" calls
        valid_calls = [c for c in self.heap if c.id in self.call_map and self.call_map[c.id] == c]
        return heapq.nsmallest(k, valid_calls)

    def get_height(self):
        import math
        n = len([c for c in self.heap if c.id in self.call_map])
        if n == 0:
            return 0
        return int(math.log2(n))
