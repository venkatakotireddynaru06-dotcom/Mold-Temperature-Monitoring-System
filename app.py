from flask import Flask, render_template
from datetime import datetime
import random
import os

import matplotlib
matplotlib.use("Agg")      # Prevents GUI errors

import matplotlib.pyplot as plt

app = Flask(__name__)

history = []


@app.route("/")
def home():

    temperature = round(random.uniform(28, 60), 1)

    if temperature < 35:
        status = "Low Temperature"
        recommendation = "Increase mold temperature to reach the optimal range."
        color = "blue"

    elif temperature <= 50:
        status = "Optimal Temperature"
        recommendation = "Temperature is stable. Continue production."
        color = "green"

    else:
        status = "High Temperature"
        recommendation = "Increase cooling to avoid product defects."
        color = "red"

    history.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "temp": temperature,
        "status": status
    })

    if len(history) > 10:
        history.pop(0)

    # -----------------------------
    # Temperature Trend Graph
    # -----------------------------

    times = [item["time"] for item in history]
    temps = [item["temp"] for item in history]

    plt.figure(figsize=(8, 3.5))

    plt.plot(
        times,
        temps,
        marker="o",
        linewidth=2
    )

    plt.title("Temperature Trend")

    plt.xlabel("Time")

    plt.ylabel("Temperature (°C)")

    plt.grid(True)

    plt.tight_layout()

    os.makedirs("static", exist_ok=True)

    plt.savefig("static/temperature.png")

    plt.close()

    return render_template(
        "index.html",
        temperature=temperature,
        status=status,
        recommendation=recommendation,
        color=color,
        history=history
    )


if __name__ == "__main__":
    app.run(debug=True)