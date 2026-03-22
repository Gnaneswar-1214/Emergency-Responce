import random
import time
from backend.data_structures.call import EmergencyCall
from typing import List

class WorkloadGenerator:
    @staticmethod
    def generate_random(n: int) -> List[EmergencyCall]:
        # severity 1 to 10
        return [EmergencyCall(f"C{i}", random.randint(1, 10), time.time() + i*0.001) for i in range(n)]

    @staticmethod
    def generate_skewed(n: int) -> List[EmergencyCall]:
        # mostly severity 1 and 2, but a few 9 and 10
        calls = []
        for i in range(n):
            if random.random() < 0.9:
                sev = random.randint(1, 3)
            else:
                sev = random.randint(8, 10)
            calls.append(EmergencyCall(f"C_{i}", sev, time.time() + i*0.001))
        return calls

    @staticmethod
    def generate_sorted(n: int) -> List[EmergencyCall]:
        # Already sorted by priority: high severity to low severity
        # meaning it gets inserted in decreasing priority order
        calls = []
        for i in range(n):
            sev = 10 - int((i/n)*10)
            sev = max(1, sev)
            calls.append(EmergencyCall(f"S_{i}", sev, time.time() + i*0.001))
        return calls

    @staticmethod
    def generate_reverse_sorted(n: int) -> List[EmergencyCall]:
        # Inserted in increasing priority order (low severity -> high severity)
        calls = []
        for i in range(n):
            sev = int((i/n)*10) + 1
            calls.append(EmergencyCall(f"R_{i}", sev, time.time() + i*0.001))
        return calls

    @staticmethod
    def generate_from_csv(n: int, csv_path: str = "emergency_calls_80000.csv") -> List[EmergencyCall]:
        import csv
        import os
        calls = []
        if not os.path.exists(csv_path):
            print(f"Warning: {csv_path} not found. Falling back to random dataset.")
            return WorkloadGenerator.generate_random(n)
            
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= n:
                    break
                try:
                    sev = int(row['SeverityLevel'])
                except (ValueError, KeyError):
                    sev = 5
                calls.append(EmergencyCall(row.get('CallID', f"C_{i}"), sev, time.time() + i*0.001))
        return calls
