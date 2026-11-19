
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

# Read the notification topic from the environment
topic = os.environ.get("NTFY_TOPIC", "").strip()

if not topic:
    raise SystemExit("Set NTFY_TOPIC in .env or the environment before running this script.")

# Step 1: Retrieve live ISS data
api_url = "https://api.wheretheiss.at/v1/satellites/25544"

request = Request(
    api_url,
    headers={"User-Agent": "merci-iss-demo/1.0"}
)

with urlopen(request, timeout=15) as response:
    iss = json.load(response)

lat = iss["latitude"]
lon = iss["longitude"]
alt = iss["altitude"]
speed = iss["velocity"]

map_url = (
    f"https://www.openstreetmap.org/"
    f"?mlat={lat:.4f}&mlon={lon:.4f}"
    f"#map=4/{lat:.4f}/{lon:.4f}"
)

# Step 2: Send a notification via ntfy
message = (
    f"ISS position: {lat:.2f}, {lon:.2f}\n"
    f"Altitude: {alt:.0f} km\n"
    f"Speed: {speed:.0f} km/h\n"
    f"Map: {map_url}"
)

notification = Request(
    f"https://ntfy.sh/{topic}",
    data=message.encode("utf-8"),
    headers={
        "Title": "ISS tracked by Raspberry Pi merci",
        "Click": map_url,
        "Content-Type": "text/plain; charset=utf-8"
    },
    method="POST"
)

with urlopen(notification, timeout=15) as response:
    print(f"Notification sent: HTTP {response.status}")

print(f"Latitude: {lat:.4f}")
print(f"Longitude: {lon:.4f}")
print("ISS Tracker - Release 2.0")
