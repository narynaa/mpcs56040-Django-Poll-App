import json
import pandas as pd
import matplotlib.pyplot as plt

rows = []

with open("spike_results.json", "r") as f:
    for line in f:
        record = json.loads(line)

        if (
            record["type"] == "Point"
            and record["metric"] == "http_req_duration"
        ):
            rows.append(
                {
                    "time": record["data"]["time"],
                    "duration_ms": record["data"]["value"],
                }
            )

df = pd.DataFrame(rows)

df["time"] = pd.to_datetime(df["time"])
df = df.set_index("time").sort_index()

summary = (
    df["duration_ms"]
    .resample("10s")
    .agg(
        average="mean",
        p95=lambda x: x.quantile(0.95),
        p99=lambda x: x.quantile(0.99),
    )
)

plt.figure(figsize=(10, 6))
plt.plot(summary.index, summary["average"], label="Average")
plt.plot(summary.index, summary["p95"], label="p95")
plt.plot(summary.index, summary["p99"], label="p99")

plt.title("Load Test Response Time Graph")
plt.xlabel("Time")
plt.ylabel("Response Time (ms)")
plt.legend()
plt.tight_layout()

plt.savefig("spike_test_response_time_graph.png", dpi=300)
plt.show()
