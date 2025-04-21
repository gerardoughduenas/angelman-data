import requests
import json

# === CONFIG ===
API_URL = "https://clinicaltrials.gov/api/v2/studies"
QUERY = "Angelman Syndrome"
FIELDS = [
    "nctId", "briefTitle", "overallStatus", "startDate", "briefSummary",
    "locations.city", "locations.state", "locations.country"
]
LIMIT = 1000

params = {
    "query.term": QUERY,
    "fields": ",".join(FIELDS),
    "pageSize": LIMIT,
    "format": "json"
}

# === FETCH + VALIDATE ===
response = requests.get(API_URL, params=params)
print("STATUS CODE:", response.status_code)

if response.status_code != 200:
    print("❌ Non-200 response received. Aborting.")
    print("RESPONSE TEXT:")
    print(response.text[:1000])
    exit(1)

try:
    data = response.json()
except Exception as e:
    print("❌ Failed to parse JSON:", e)
    print("RESPONSE TEXT:")
    print(response.text[:1000])
    exit(1)

# === EXTRACT DATA ===
studies = data.get("studies", [])
output = []

for study in studies:
    loc = study.get("locations", [{}])[0] if study.get("locations") else {}
    output.append({
        "NCTId": study.get("nctId", ""),
        "BriefTitle": study.get("briefTitle", ""),
        "OverallStatus": study.get("overallStatus", ""),
        "StartDate": study.get("startDate", ""),
        "BriefSummary": study.get("briefSummary", ""),
        "LocationCity": loc.get("city", ""),
        "LocationState": loc.get("state", ""),
        "LocationCountry": loc.get("country", "")
    })

# === SAVE ===
with open("angelman-clinical-trials.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"✅ Exported {len(output)} trials")
