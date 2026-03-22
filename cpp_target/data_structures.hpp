#pragma once

#include <string>
#include <vector>
#include <unordered_map>
#include <queue>
#include <algorithm>
#include <memory>
#include <iostream>
#include <map>

struct EmergencyCall {
    int severity;
    std::string call_id;

    bool operator<(const EmergencyCall& other) const {
        return severity < other.severity;
    }
};

class BaseStructure {
public:
    virtual void insert(const EmergencyCall& call) = 0;
    virtual EmergencyCall extract_max() = 0;
    virtual void update_severity(const std::string& call_id, int new_severity) = 0;
    virtual void delete_call(const std::string& call_id) = 0;
    virtual std::vector<EmergencyCall> get_top_k(int k) = 0;
    virtual ~BaseStructure() = default;
};

// 1. Priority Queue (Heap)
class MaxHeapTracker : public BaseStructure {
private:
    std::vector<EmergencyCall> heap;
    std::unordered_map<std::string, int> index_map;
    
    void sift_up(int idx) {
        while (idx > 0) {
            int p = (idx - 1) / 2;
            if (heap[p].severity < heap[idx].severity) {
                std::swap(heap[p], heap[idx]);
                index_map[heap[p].call_id] = p;
                index_map[heap[idx].call_id] = idx;
                idx = p;
            } else break;
        }
    }

    void sift_down(int idx) {
        int n = heap.size();
        while (true) {
            int left = 2 * idx + 1;
            int right = 2 * idx + 2;
            int largest = idx;
            
            if (left < n && heap[left].severity > heap[largest].severity) largest = left;
            if (right < n && heap[right].severity > heap[largest].severity) largest = right;
            
            if (largest != idx) {
                std::swap(heap[idx], heap[largest]);
                index_map[heap[idx].call_id] = idx;
                index_map[heap[largest].call_id] = largest;
                idx = largest;
            } else break;
        }
    }

public:
    void insert(const EmergencyCall& call) override {
        heap.push_back(call);
        int idx = heap.size() - 1;
        index_map[call.call_id] = idx;
        sift_up(idx);
    }

    EmergencyCall extract_max() override {
        if (heap.empty()) return {-1, ""};
        EmergencyCall max_val = heap[0];
        EmergencyCall last_val = heap.back();
        heap.pop_back();
        index_map.erase(max_val.call_id);
        
        if (!heap.empty()) {
            heap[0] = last_val;
            index_map[last_val.call_id] = 0;
            sift_down(0);
        }
        return max_val;
    }

    void update_severity(const std::string& call_id, int new_severity) override {
        if (index_map.find(call_id) == index_map.end()) return;
        int idx = index_map[call_id];
        int old_sev = heap[idx].severity;
        heap[idx].severity = new_severity;
        if (new_severity > old_sev) sift_up(idx);
        else sift_down(idx);
    }

    void delete_call(const std::string& call_id) override {
        if (index_map.find(call_id) == index_map.end()) return;
        int idx = index_map[call_id];
        EmergencyCall last_val = heap.back();
        heap.pop_back();
        index_map.erase(call_id);
        
        if (idx < heap.size()) {
            int old_sev = heap[idx].severity;
            heap[idx] = last_val;
            index_map[last_val.call_id] = idx;
            if (last_val.severity > old_sev) sift_up(idx);
            else sift_down(idx);
        }
    }

    std::vector<EmergencyCall> get_top_k(int k) override {
        std::vector<EmergencyCall> result;
        std::priority_queue<EmergencyCall> temp_q(heap.begin(), heap.end());
        int count = 0;
        while (!temp_q.empty() && count < k) {
            result.push_back(temp_q.top());
            temp_q.pop();
            count++;
        }
        return result;
    }
};

// 2. Sorted Array
class SortedArrayTracker : public BaseStructure {
private:
    std::vector<EmergencyCall> arr;

public:
    void insert(const EmergencyCall& call) override {
        auto it = std::upper_bound(arr.begin(), arr.end(), call, [](const EmergencyCall& a, const EmergencyCall& b){
            return a.severity < b.severity;
        });
        arr.insert(it, call);
    }

    EmergencyCall extract_max() override {
        if (arr.empty()) return {-1, ""};
        EmergencyCall max_val = arr.back();
        arr.pop_back();
        return max_val;
    }

    void update_severity(const std::string& call_id, int new_severity) override {
        for (auto it = arr.begin(); it != arr.end(); ++it) {
            if (it->call_id == call_id) {
                arr.erase(it);
                break;
            }
        }
        insert({new_severity, call_id});
    }

    void delete_call(const std::string& call_id) override {
        for (auto it = arr.begin(); it != arr.end(); ++it) {
            if (it->call_id == call_id) {
                arr.erase(it);
                break;
            }
        }
    }

    std::vector<EmergencyCall> get_top_k(int k) override {
        std::vector<EmergencyCall> result;
        int n = arr.size();
        for (int i = 0; i < std::min(k, n); ++i) {
            result.push_back(arr[n - 1 - i]);
        }
        return result;
    }
};

// 3. Hash Map
class HashMapTracker : public BaseStructure {
private:
    std::unordered_map<std::string, int> map;

public:
    void insert(const EmergencyCall& call) override {
        map[call.call_id] = call.severity;
    }

    EmergencyCall extract_max() override {
        if (map.empty()) return {-1, ""};
        std::string max_id;
        int max_sev = -1;
        for (const auto& pair : map) {
            if (pair.second > max_sev) {
                max_sev = pair.second;
                max_id = pair.first;
            }
        }
        map.erase(max_id);
        return {max_sev, max_id};
    }

    void update_severity(const std::string& call_id, int new_severity) override {
        if (map.count(call_id)) {
            map[call_id] = new_severity;
        }
    }

    void delete_call(const std::string& call_id) override {
        map.erase(call_id);
    }

    std::vector<EmergencyCall> get_top_k(int k) override {
        std::vector<EmergencyCall> all_calls;
        for (const auto& pair : map) {
            all_calls.push_back({pair.second, pair.first});
        }
        std::sort(all_calls.begin(), all_calls.end(), [](const EmergencyCall& a, const EmergencyCall& b){
            return a.severity > b.severity;
        });
        std::vector<EmergencyCall> result;
        for (int i = 0; i < std::min(k, (int)all_calls.size()); ++i) {
            result.push_back(all_calls[i]);
        }
        return result;
    }
};

// 4. Balanced BST (Wraps std::multimap which is a Red-Black Tree native to C++)
class AVLTreeTracker : public BaseStructure {
private:
    std::multimap<int, std::string> tree;
    std::unordered_map<std::string, std::multimap<int, std::string>::iterator> lookup;

public:
    void insert(const EmergencyCall& call) override {
        auto it = tree.insert({call.severity, call.call_id});
        lookup[call.call_id] = it;
    }

    EmergencyCall extract_max() override {
        if (tree.empty()) return {-1, ""};
        auto it = std::prev(tree.end());
        EmergencyCall max_val = {it->first, it->second};
        lookup.erase(it->second);
        tree.erase(it);
        return max_val;
    }

    void update_severity(const std::string& call_id, int new_severity) override {
        if (lookup.count(call_id)) {
            tree.erase(lookup[call_id]);
            auto it = tree.insert({new_severity, call_id});
            lookup[call_id] = it;
        }
    }

    void delete_call(const std::string& call_id) override {
        if (lookup.count(call_id)) {
            tree.erase(lookup[call_id]);
            lookup.erase(call_id);
        }
    }

    std::vector<EmergencyCall> get_top_k(int k) override {
        std::vector<EmergencyCall> result;
        auto it = tree.rbegin();
        int count = 0;
        while (it != tree.rend() && count < k) {
            result.push_back({it->first, it->second});
            ++it;
            count++;
        }
        return result;
    }
};
