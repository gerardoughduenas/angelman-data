import requests
import json

url = "https://clinicaltrials.gov/api/v1/studies"
params = {
    "query": "Angelman Syndrome",
    "fields": "NCTId,BriefTitle,OverallStatus,StartDateStruct,BriefSummary,Locations",
    "limit": 1
}
headers = {
    "Accept": "application/json"
}

res = requests.get(url, params=params, headers=headers)
data = res.json()

print("=== Fetched 1 trial ===")
print(json.dumps(data.get("studies", [])[0], indent=2))
