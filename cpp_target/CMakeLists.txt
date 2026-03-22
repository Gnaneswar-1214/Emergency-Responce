cmake_minimum_required(VERSION 3.15)
project(EmergencyDispatchBackend VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Ensure threading is enabled (required for Crow and Asio)
find_package(Threads REQUIRED)

add_executable(dashboard_server main.cpp)

# Include the headers directory
target_include_directories(dashboard_server PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)

# Link threads
target_link_libraries(dashboard_server PRIVATE Threads::Threads)
