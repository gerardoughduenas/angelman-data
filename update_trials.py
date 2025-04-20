import requests
import json

# === CONFIG ===
API_URL = "https://clinicaltrials.gov/api/v1/studies"
QUERY = "Angelman Syndrome"
FIELDS = [
    "protocolSection.identificationModule.nctId",
    "protocolSection.statusModule.overallStatus",
    "protocolSection.statusModule.startDateStruct.date",
    "protocolSection.descriptionModule.briefTitle",
    "protocolSection.descriptionModule.briefSummary",
    "protocolSection.contactsLocationsModule.locations[*].city",
    "protocolSection.contactsLocationsModule.locations[*].state",
    "protocolSection.contactsLocationsModule.locations[*].country"
]
LIMIT = 1000

# === FETCH ===
params = {
    "query": QUERY,
    "fields": ",".join(FIELDS),
    "limit": LIMIT
}
res = requests.get(API_URL, params=params)
data = res.json()

trials = []
for study in data.get("studies", []):
    section = study.get("protocolSection", {})
    id_mod = section.get("identificationModule", {})
    status_mod = section.get("statusModule", {})
    desc_mod = section.get("descriptionModule", {})
    loc_mod = section.get("contactsLocationsModule", {}).get("locations", [])

    city = loc_mod[0].get("city") if loc_mod else ""
    state = loc_mod[0].get("state") if loc_mod else ""
    country = loc_mod[0].get("country") if loc_mod else ""

    trials.append({
        "NCTId": [id_mod.get("nctId", "")],
        "BriefTitle": [desc_mod.get("briefTitle", "")],
        "OverallStatus": [status_mod.get("overallStatus", "")],
        "StartDate": [status_mod.get("startDateStruct", {}).get("date", "")],
        "BriefSummary": [desc_mod.get("briefSummary", "")],
        "LocationCity": [city],
        "LocationState": [state],
        "LocationCountry": [country]
    })

# === OUTPUT ===
with open("angelman-clinical-trials.json", "w") as f:
    json.dump(trials, f, indent=2)

print(f"✅ Exported {len(trials)} trials")
