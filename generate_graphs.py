import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
from backend.benchmarking.metrics import Benchmarker

def generate_graphs():
    sizes = [5000, 10000, 20000]
    print(f"Running benchmarks for sizes: {sizes}")
    results = Benchmarker.run_all_benchmarks(sizes, "CSV Dataset")
    
    metrics = {
        "insert_time_ms": "Insert Time vs Input Size (ms)",
        "extract_time_ms": "Extract Max Time vs Input Size (ms)",
        "update_time_ms": "Update Severity Time vs Input Size (ms)",
        "delete_time_ms": "Delete Time vs Input Size (ms)",
        "top_k_time_ms": "Top-K Time vs Input Size (ms)",
        "memory_bytes": "Memory Usage vs Input Size (Bytes)"
    }
    
    colors = {
        "Heap": "blue",
        "Sorted Array": "red",
        "Hash Map": "orange",
        "Balanced BST": "green"
    }
    
    for metric_key, metric_title in metrics.items():
        plt.figure(figsize=(8, 5))
        for struct_name, struct_data in results.items():
            x = [d["size"] for d in struct_data]
            y = [d.get(metric_key, 0) for d in struct_data]
            plt.plot(x, y, marker='o', label=struct_name, color=colors.get(struct_name, "black"))
        
        plt.title(metric_title)
        plt.xlabel("Dataset Size (N)")
        plt.ylabel(metric_title.split(" vs ")[0])
        plt.legend()
        plt.grid(True)
        filename = f"{metric_key}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Generated {filename}")

if __name__ == "__main__":
    generate_graphs()
