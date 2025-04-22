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
    sponsormod = ps.get("sponsorCollaboratorsModule", {})
    eligmod = ps.get("eligibilityModule", {})

    # === Collect all locations as array of dicts ===
    all_locations = []
    for loc in contactmod.get("locations", []):
        facility = loc.get("locationFacility", {})
        loc_data = {
            "city": facility.get("city", ""),
            "state": facility.get("state", ""),
            "country": facility.get("country", "")
        }
        if any(loc_data.values()):
            all_locations.append(loc_data)

    # === Extract age data ===
    min_age = eligmod.get("minimumAge", "")
    max_age = eligmod.get("maximumAge", "")
    age_groups = eligmod.get("ageGroups", [])

    trial = {
        "NCTId": idmod.get("nctId", ""),
        "BriefTitle": idmod.get("briefTitle", ""),
        "OverallStatus": statmod.get("overallStatus", ""),
        "StartDate": statmod.get("startDateStruct", {}).get("date", ""),
        "BriefSummary": descmod.get("briefSummary", ""),
        "LocationCity": "",
        "LocationState": "",
        "LocationCountry": "",
        "Sponsor": sponsormod.get("leadSponsor", {}).get("name", ""),
        "AllLocations": all_locations,
        "MinimumAge": min_age,
        "MaximumAge": max_age,
        "AgeGroups": age_groups
    }

    # Fallback to first location for legacy display
    if all_locations:
        trial["LocationCity"] = all_locations[0]["city"]
        trial["LocationState"] = all_locations[0]["state"]
        trial["LocationCountry"] = all_locations[0]["country"]

    trials.append(trial)

# === SAVE ===
with open("angelman-clinical-trials.json", "w") as f:
    json.dump(trials, f, indent=2)

print(f"✅ Exported {len(trials)} trials")
