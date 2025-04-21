import requests
import json

# === CONFIG ===
API_URL = "https://clinicaltrials.gov/api/v2/studies"
QUERY = "Angelman Syndrome"
LIMIT = 1000

params = {
    "query.term": QUERY,
    "pageSize": LIMIT
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

# === EXTRACT STUDY DATA ===
studies = data.get("studies", [])
trials = []

for study in studies:
    trial = {
        "NCTId": study.get("protocolSection", {}).get("identificationModule", {}).get("nctId", ""),
        "BriefTitle": study.get("protocolSection", {}).get("identificationModule", {}).get("briefTitle", ""),
        "OverallStatus": study.get("protocolSection", {}).get("statusModule", {}).get("overallStatus", ""),
        "StartDate": study.get("protocolSection", {}).get("statusModule", {}).get("startDateStruct", {}).get("date", ""),
        "BriefSummary": study.get("protocolSection", {}).get("descriptionModule", {}).get("briefSummary", ""),
        "LocationCity": "",
        "LocationState": "",
        "LocationCountry": ""
    }

    # Add first location details if present
    locations = study.get("protocolSection", {}).get("contactsLocationsModule", {}).get("locations", [])
    if locations:
        loc = locations[0].get("locationFacility", {})
        trial["LocationCity"] = loc.get("city", "")
        trial["LocationState"] = loc.get("state", "")
        trial["LocationCountry"] = loc.get("country", "")

    trials.append(trial)

# === SAVE ===
with open("angelman-clinical-trials.json", "w") as f:
    json.dump(trials, f, indent=2)

print(f"✅ Exported {len(trials)} trials")
