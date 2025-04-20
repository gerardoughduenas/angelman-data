import requests
import json

# === CONFIG ===
API_URL = "https://clinicaltrials.gov/api/v1/studies"
QUERY = "Angelman Syndrome"
FIELDS = "NCTId,BriefTitle,OverallStatus,StartDateStruct,BriefSummary,Locations"
LIMIT = 1000

# === HEADERS (required to avoid 404) ===
headers = {
    "Accept": "application/json"
}

params = {
    "query": QUERY,
    "fields": FIELDS,
    "limit": LIMIT
}

# === REQUEST + LOGGING ===
response = requests.get(API_URL, headers=headers, params=params)

print("STATUS CODE:", response.status_code)
print("RESPONSE TEXT PREVIEW:")
print(response.text[:1000])  # show first 1000 chars

# === FAIL FAST if not 200 or text is empty
if response.status_code != 200:
    print("❌ Non-200 response received. Aborting.")
    exit(1)
if not response.text.strip():
    print("❌ Empty response received. Aborting.")
    exit(1)

# === PARSE JSON ===
try:
    data = response.json()
except Exception as e:
    print("❌ JSON decode failed. Full response below:")
    print(response.text)
    print("Error:", str(e))
    exit(1)

# === PROCESS TRIALS ===
trials = []
for study in data.get("studies", []):
    trial = {
        "NCTId": [study.get("NCTId", "")],
        "BriefTitle": [study.get("BriefTitle", "")],
        "OverallStatus": [study.get("OverallStatus", "")],
        "StartDate": [study.get("StartDateStruct", {}).get("date", "")],
        "BriefSummary": [study.get("BriefSummary", "")]
    }

    location = study.get("Locations", [{}])[0]
    trial["LocationCity"] = [location.get("city", "")]
    trial["LocationState"] = [location.get("state", "")]
    trial["LocationCountry"] = [location.get("country", "")]

    trials.append(trial)

# === OUTPUT ===
with open("angelman-clinical-trials.json", "w") as f:
    json.dump(trials, f, indent=2)

print(f"✅ Exported {len(trials)} trials")
