from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/")
async def telemetry(data: dict):
    regions = data.get("regions", [])
    threshold = data.get("threshold_ms", 180)

    # Mock telemetry data for example
    # In real deployment, replace this with your telemetry source
    mock_data = {
        "emea": np.random.randint(100, 200, 50),
        "amer": np.random.randint(150, 250, 50),
        "apac": np.random.randint(120, 220, 50),
    }

    response = {}
    for region in regions:
        latencies = mock_data.get(region, [])
        if len(latencies) == 0:
            continue
        avg_latency = float(np.mean(latencies))
        p95_latency = float(np.percentile(latencies, 95))
        avg_uptime = 100.0  # Assuming uptime is always 100% in mock
        breaches = int(np.sum(np.array(latencies) > threshold))
        response[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches,
        }

    return response