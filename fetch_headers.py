import urllib.request
import json
import os
import certifi
import ssl

context = ssl.create_default_context(cafile=certifi.where())
os.makedirs('cpp_target/include', exist_ok=True)

# Fetch Crow direct
crow_url = "https://github.com/CrowCpp/Crow/releases/download/v1.2.0/crow_all.h"
req1 = urllib.request.Request(crow_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req1, context=context) as r, open('cpp_target/include/crow_all.h', 'wb') as f:
        f.write(r.read())
    print("Crow Downloaded successfully")
except Exception as e:
    print("Failed Crow Download:", e)

# Fetch Json direct
json_url = "https://github.com/nlohmann/json/releases/download/v3.11.3/json.hpp"
req2 = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req2, context=context) as r, open('cpp_target/include/json.hpp', 'wb') as f:
        f.write(r.read())
    print("JSON Downloaded successfully")
except Exception as e:
    print("Failed JSON Download:", e)
