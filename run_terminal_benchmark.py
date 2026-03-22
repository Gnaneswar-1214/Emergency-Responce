import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.benchmarking.metrics import Benchmarker

def run_terminal_output():
    sizes = [1000, 5000, 10000]
    print("=" * 60)
    print(f"Running Benchmarks on CSV Dataset for sizes: {sizes}")
    print("=" * 60 + "\n")
    
    # Run the benchmark engine directly
    results = Benchmarker.run_all_benchmarks(sizes, "CSV Dataset")
    
    for structure_name, metrics_list in results.items():
        print(f"[{structure_name.upper()}]")
        for m in metrics_list:
            print(f"  -> Size: {m['size']:<6} | "
                  f"Insert: {m['insert_time_ms']:>7.3f} ms | "
                  f"Extract Max: {m.get('extract_time_ms', 0):>7.3f} ms | "
                  f"Top-K: {m.get('top_k_time_ms', 0):>7.3f} ms | "
                  f"Memory: {m.get('memory_bytes', 0):>7} bytes")
        print("-" * 60)

if __name__ == "__main__":
    run_terminal_output()
