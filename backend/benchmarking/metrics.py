import time
import psutil
from typing import Dict, Any, List

from backend.data_structures.heap import PriorityQueueHeap
from backend.data_structures.sorted_array import SortedArrayDispatch
from backend.data_structures.hash_map import HashMapDispatch
from backend.data_structures.bst import AVLTreeDispatch
from backend.benchmarking.workload import WorkloadGenerator

class Benchmarker:
    @staticmethod
    def benchmark_structure(ds_class, dataset, workload_type: str) -> Dict[str, Any]:
        process = psutil.Process()
        ds = ds_class()
        
        mem_before = process.memory_info().rss
        
        # 1. Insert Profile
        start = time.perf_counter()
        for call in dataset:
            ds.insert(call)
        insert_time = time.perf_counter() - start
        
        mem_after = process.memory_info().rss
        memory_used = mem_after - mem_before
        
        # 2. Extract Max Profile (extract 10%)
        num_extracts = max(1, len(dataset) // 10)
        start = time.perf_counter()
        for _ in range(num_extracts):
            ds.extract_max()
        extract_time = time.perf_counter() - start
        
        # 3. Update Severity Profile (update 5%)
        # Ensure we pick calls that trace realistically in the dataset and are still in DS
        # (Though some were extracted. For safety, just re-insert an ad-hoc and update it, to make it fair.)
        sample_call = dataset[-1]
        ds.insert(sample_call)  # ensure it's there
        start = time.perf_counter()
        ds.update_severity(sample_call.id, 10) # increase priority
        update_time = time.perf_counter() - start
        
        # 4. Delete Profile (delete 1 call)
        sample_delete = dataset[-2]
        ds.insert(sample_delete)  # ensure it's there
        start = time.perf_counter()
        ds.delete(sample_delete.id)
        delete_time = time.perf_counter() - start
        
        # 5. Top-K Profile
        start = time.perf_counter()
        ds.top_k(10)
        top_k_time = time.perf_counter() - start
        
        metrics = {
            "insert_time_ms": insert_time * 1000,
            "extract_time_ms": extract_time * 1000,
            "update_time_ms": update_time * 1000,
            "delete_time_ms": delete_time * 1000,
            "top_k_time_ms": top_k_time * 1000,
            "memory_bytes": max(0, memory_used)
        }
        
        # Advanced metrics if supported
        if hasattr(ds, "swaps"): metrics["swaps"] = ds.swaps
        if hasattr(ds, "comparisons"): metrics["comparisons"] = ds.comparisons
        if hasattr(ds, "get_height"): 
            try:
                metrics["height"] = ds.get_height() if callable(ds.get_height) else ds.get_height(ds.root)
            except:
                pass
        if hasattr(ds, "resorts"): metrics["resorts"] = ds.resorts
        if hasattr(ds, "rotations"): metrics["rotations"] = ds.rotations
        
        return metrics

    @staticmethod
    def run_all_benchmarks(sizes: List[int], distribution: str):
        # Maps name to class
        structures = {
            "Heap": PriorityQueueHeap,
            "Sorted Array": SortedArrayDispatch,
            "Hash Map": HashMapDispatch,
            "Balanced BST": AVLTreeDispatch
        }
        
        results = {name: [] for name in structures.keys()}
        
        for size in sizes:
            if distribution == "Random":
                dataset = WorkloadGenerator.generate_random(size)
            elif distribution == "Skewed":
                dataset = WorkloadGenerator.generate_skewed(size)
            elif distribution == "Sorted":
                dataset = WorkloadGenerator.generate_sorted(size)
            elif distribution == "Reverse":
                dataset = WorkloadGenerator.generate_reverse_sorted(size)
            elif distribution == "CSV Dataset":
                dataset = WorkloadGenerator.generate_from_csv(size)
            else:
                dataset = WorkloadGenerator.generate_random(size)
                
            for name, ds_class in structures.items():
                m = Benchmarker.benchmark_structure(ds_class, dataset.copy(), distribution)
                m["size"] = size
                res_entry = {"size": size, **m}
                results[name].append(res_entry)
                
        return results
