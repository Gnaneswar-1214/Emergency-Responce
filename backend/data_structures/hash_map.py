from typing import List, Optional
from .call import EmergencyCall

class HashMapDispatch:
    def __init__(self):
        self.map = {}

    def insert(self, call: EmergencyCall):
        self.map[call.id] = call

    def extract_max(self) -> Optional[EmergencyCall]:
        if not self.map:
            return None
        
        # O(N) extraction
        max_call = min(self.map.values()) # min because our __lt__ returns True for max priority
        del self.map[max_call.id]
        return max_call

    def update_severity(self, call_id: str, new_severity: int):
        if call_id in self.map:
            call = self.map[call_id]
            self.map[call_id] = EmergencyCall(call_id, new_severity, call.timestamp)

    def delete(self, call_id: str):
        if call_id in self.map:
            del self.map[call_id]

    def top_k(self, k: int) -> List[EmergencyCall]:
        # O(N log N) since we sort all
        sorted_calls = sorted(self.map.values()) # uses custom __lt__
        return sorted_calls[:k]
