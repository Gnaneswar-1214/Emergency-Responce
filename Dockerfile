FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Update system and install native compilation tools (CMake, GNU G++, Make, and standalone Asio for Crow networking)
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    make \
    libasio-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the entire working directory
COPY . /app

# Form a build directory, compile the C++ architecture using CMake, and link binaries
RUN mkdir build && cd build && \
    cmake ../cpp_target && \
    make -j$(nproc)

# Expose the standard 10000 web port for Render routing
EXPOSE 10000

# Spin up the high-performance C++ server executable
CMD ["./build/dashboard_server"]
