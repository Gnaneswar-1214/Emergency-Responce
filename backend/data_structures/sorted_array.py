from typing import List, Optional
from .call import EmergencyCall

class SortedArrayDispatch:
    def __init__(self):
        self.arr = []
        # Metrics
        self.resorts = 0

    def insert(self, call: EmergencyCall):
        self.arr.append(call)
        self._sort()

    def extract_max(self) -> Optional[EmergencyCall]:
        if not self.arr:
            return None
        # Highest priority is at index 0 because our __lt__ places higher priority first
        call = self.arr.pop(0)
        return call

    def update_severity(self, call_id: str, new_severity: int):
        for i, call in enumerate(self.arr):
            if call.id == call_id:
                self.arr[i] = EmergencyCall(call_id, new_severity, call.timestamp)
                self._sort()
                break

    def delete(self, call_id: str):
        for i, call in enumerate(self.arr):
            if call.id == call_id:
                self.arr.pop(i)
                break

    def top_k(self, k: int) -> List[EmergencyCall]:
        return self.arr[:k]

    def _sort(self):
        # We sort the array. Python's timsort is good, but for metrics we count resorts
        self.arr.sort()
        self.resorts += 1
