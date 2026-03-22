import time

class EmergencyCall:
    def __init__(self, call_id: str, severity: int, timestamp: float = None):
        self.id = call_id
        self.severity = severity
        self.timestamp = timestamp if timestamp is not None else time.time()
        
    def __lt__(self, other):
        # Higher severity has higher priority
        if self.severity != other.severity:
            return self.severity > other.severity
        # If severity is equal, earlier timestamp has higher priority
        return self.timestamp < other.timestamp
        
    def __eq__(self, other):
        if not isinstance(other, EmergencyCall):
            return False
        return self.id == other.id

    def __repr__(self):
        return f"Call(id={self.id}, sev={self.severity}, ts={self.timestamp})"
