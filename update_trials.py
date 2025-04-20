import requests
import json

url = "https://clinicaltrials.gov/api/v1/studies"
params = {
    "query": "Angelman Syndrome",
    "fields": "NCTId,BriefTitle,OverallStatus,StartDateStruct,BriefSummary,Locations",
    "limit": 1000
}

response = requests.get(url, params=params)
data = response.json()

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

with open("angelman-clinical-trials.json", "w") as f:
    json.dump(trials, f, indent=2)
