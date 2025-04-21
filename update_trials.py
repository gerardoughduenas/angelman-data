import requests
import json

# === CONFIG ===
API_URL = "https://clinicaltrials.gov/api/v1/studies"
QUERY = "Angelman Syndrome"
FIELDS = "NCTId,BriefTitle,OverallStatus,StartDateStruct,BriefSummary,Locations"
LIMIT = 1000

params = {
    "query": QUERY,
    "fields": FIELDS,
    "limit": LIMIT
}

headers = {
    "Accept": "application/json"
}

# === FETCH + VALIDATE ===
response = requests.get(API_URL, headers=headers, params=params)
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
trials = []
for study in data.get("studies", []):
    trial = {
        "NCTId": study.get("NCTId", ""),
        "BriefTitle": study.get("BriefTitle", ""),
        "OverallStatus": study.get("OverallStatus", ""),
        "StartDate": study.get("StartDateStruct", {}).get("date", ""),
        "BriefSummary": study.get("BriefSummary", "")
    }

    # Get first location if it exists
    location = study.get("Locations", [{}])[0]
    trial["LocationCity"] = location.get("city", "")
    trial["LocationState"] = location.get("state", "")
    trial["LocationCountry"] = location.get("country", "")

    trials.append(trial)

# === SAVE ===
with open("angelman-clinical-trials.json", "w") as f:
    json.dump(trials, f, indent=2)

print(f"✅ Exported {len(trials)} trials")
