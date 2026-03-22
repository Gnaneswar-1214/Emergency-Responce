#include "data_structures.hpp"
#include "benchmarker.hpp"
#include "json.hpp"
#undef max
#undef min
#include "crow_all.h"

using json = nlohmann::json;

int main() {
    crow::SimpleApp app;

    // Static Routing mimicking FastAPI
    CROW_ROUTE(app, "/")([](const crow::request& req, crow::response& res){
        res.set_static_file_info("frontend/index.html");
        res.end();
    });

    CROW_ROUTE(app, "/static/styles.css")([](const crow::request& req, crow::response& res){
        res.set_static_file_info("frontend/styles.css");
        res.end();
    });

    CROW_ROUTE(app, "/static/app.js")([](const crow::request& req, crow::response& res){
        res.set_static_file_info("frontend/app.js");
        res.end();
    });

    // Core Benchmark API Gateway
    auto benchmark_handler = [](const crow::request& req) {
        auto x = crow::json::load(req.body);
        if (!x) return crow::response(400);

        std::string distribution = x["distribution"].s();
        std::vector<int> sizes;
        for (const auto& item : x["sizes"]) {
            sizes.push_back(item.i());
        }

        std::vector<EmergencyCall> dataset;
        // Cap local sizes for synchronous latency limits
        if (distribution == "CSV Dataset") {
            dataset = WorkloadGenerator::generate_from_csv("emergency_calls_80000.csv", 20000);
        } else {
            for(int i=0; i<20000; i++) dataset.push_back({rand()%10 + 1, "C" + std::to_string(i)});
        }

        json final_response;
        
        MaxHeapTracker heap;
        final_response["Priority Queue (Heap)"] = MetricsBenchmarker::run_benchmarks(&heap, dataset);
        
        SortedArrayTracker arr;
        final_response["Sorted Array"] = MetricsBenchmarker::run_benchmarks(&arr, dataset);
        
        HashMapTracker map;
        final_response["Hash Map"] = MetricsBenchmarker::run_benchmarks(&map, dataset);
        
        AVLTreeTracker avl;
        final_response["Balanced BST"] = MetricsBenchmarker::run_benchmarks(&avl, dataset);

        json payload;
        payload["status"] = "success";
        payload["data"] = final_response;

        crow::response res;
        res.body = payload.dump();
        res.add_header("Content-Type", "application/json");
        return res;
    };

    CROW_ROUTE(app, "/api/benchmark").methods(crow::HTTPMethod::POST)(benchmark_handler);
    CROW_ROUTE(app, "/benchmark").methods(crow::HTTPMethod::POST)(benchmark_handler);

    std::cout << "Starting C++ High-Performance Dispatch Server on port 10000...\n";
    app.port(10000).multithreaded().run();
}
