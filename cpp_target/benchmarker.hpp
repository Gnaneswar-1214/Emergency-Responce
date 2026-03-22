#pragma once

#include "data_structures.hpp"
#include <chrono>
#include <fstream>
#include <sstream>
#include <iostream>
#include <random>

class WorkloadGenerator {
public:
    static std::vector<EmergencyCall> generate_from_csv(const std::string& filepath, int max_lines = 50000) {
        std::vector<EmergencyCall> calls;
        std::ifstream file(filepath);
        if (!file.is_open()) return calls;

        std::string line, word;
        std::getline(file, line); // header

        int line_count = 0;
        while (std::getline(file, line) && line_count < max_lines) {
            std::stringstream s(line);
            std::string id_str, sev_str;
            
            std::getline(s, id_str, ',');
            std::getline(s, word, ','); // TS
            std::getline(s, word, ','); // Loc
            std::getline(s, word, ','); // Type
            std::getline(s, sev_str, ','); // Sev
            
            try {
                int sev = std::stoi(sev_str);
                calls.push_back({sev, id_str});
                line_count++;
            } catch (...) {}
        }
        return calls;
    }
};

class MetricsBenchmarker {
public:
    static std::vector<std::unordered_map<std::string, double>> run_benchmarks(BaseStructure* ds, const std::vector<EmergencyCall>& initial_calls) {
        std::vector<std::unordered_map<std::string, double>> results;
        std::vector<int> sizes = {1000, 5000, 10000};
        
        for (int size : sizes) {
            if (size > initial_calls.size()) break;
            
            double insert_time = 0;
            auto start = std::chrono::high_resolution_clock::now();
            for (int i = 0; i < size; ++i) ds->insert(initial_calls[i]);
            auto end = std::chrono::high_resolution_clock::now();
            insert_time = std::chrono::duration<double, std::milli>(end - start).count();
            
            double extract_time = 0;
            int queries = size / 10;
            start = std::chrono::high_resolution_clock::now();
            for (int i = 0; i < queries; ++i) ds->extract_max();
            end = std::chrono::high_resolution_clock::now();
            extract_time = std::chrono::duration<double, std::milli>(end - start).count();
            
            for (int i = 0; i < queries; ++i) ds->insert(initial_calls[i]);
            
            double update_time = 0;
            start = std::chrono::high_resolution_clock::now();
            for (int i = 0; i < queries; ++i) ds->update_severity(initial_calls[i].call_id, 10);
            end = std::chrono::high_resolution_clock::now();
            update_time = std::chrono::duration<double, std::milli>(end - start).count();
            
            double delete_time = 0;
            start = std::chrono::high_resolution_clock::now();
            for (int i = 0; i < queries; ++i) ds->delete_call(initial_calls[i].call_id);
            end = std::chrono::high_resolution_clock::now();
            delete_time = std::chrono::duration<double, std::milli>(end - start).count();

            for (int i = 0; i < queries; ++i) ds->insert(initial_calls[i]);

            double topk_time = 0;
            start = std::chrono::high_resolution_clock::now();
            for (int i = 0; i < queries; ++i) ds->get_top_k(10);
            end = std::chrono::high_resolution_clock::now();
            topk_time = std::chrono::duration<double, std::milli>(end - start).count();

            std::unordered_map<std::string, double> payload;
            payload["size"] = size;
            payload["insert_time_ms"] = insert_time;
            payload["extract_time_ms"] = extract_time;
            payload["update_time_ms"] = update_time;
            payload["delete_time_ms"] = delete_time;
            payload["top_k_time_ms"] = topk_time;
            payload["memory_bytes"] = size * 48; // Baseline overhead estimation
            
            results.push_back(payload);
        }
        return results;
    }
};
