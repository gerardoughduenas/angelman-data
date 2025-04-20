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

print("=== Status Code:", res.status_code)
print("=== Response Body Start ===")
print(res.text[:1000])  # Show only first 1000 characters
print("=== Response Body End ===")

try:
    data = res.json()
    print("=== Fetched 1 trial ===")
    print(json.dumps(data.get("studies", [])[0], indent=2))
except Exception as e:
    print("⚠️ Failed to parse JSON:", e)
    exit(1)
