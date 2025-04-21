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
    ps = study.get("protocolSection", {})
    idmod = ps.get("identificationModule", {})
    statmod = ps.get("statusModule", {})
    descmod = ps.get("descriptionModule", {})
    contactmod = ps.get("contactsLocationsModule", {})
    sponsormod = ps.get("sponsorsModule", {})

    trial = {
        "NCTId": idmod.get("nctId", ""),
        "BriefTitle": idmod.get("briefTitle", ""),
        "OverallStatus": statmod.get("overallStatus", ""),
        "StartDate": statmod.get("startDateStruct", {}).get("date", ""),
        "BriefSummary": descmod.get("briefSummary", ""),
        "LocationCity": "",
        "LocationState": "",
        "LocationCountry": "",
        "Sponsor": sponsormod.get("leadSponsor", {}).get("name", "")
    }

    # ✅ Pull top-level location fields
    locations = contactmod.get("locations", [])
    if locations and isinstance(locations, list):
        first_loc = locations[0]
        trial["LocationCity"] = first_loc.get("city", "")
        trial["LocationState"] = first_loc.get("state", "")
        trial["LocationCountry"] = first_loc.get("country", "")

    trials.append(trial)

# === SAVE ===
with open("angelman-clinical-trials.json", "w") as f:
    json.dump(trials, f, indent=2)

print(f"✅ Exported {len(trials)} trials")
