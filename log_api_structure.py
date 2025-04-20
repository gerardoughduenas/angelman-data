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

try:
    res = requests.get(url, params=params, headers=headers)
    print("=== Status Code:", res.status_code)
    print("=== Response Headers ===")
    print(res.headers)
    print("=== Response Text Preview ===")
    print(res.text[:1000])
    print("=== End Response Preview ===")

    if res.status_code != 200:
        print("⚠️ Request failed with status:", res.status_code)
        exit(1)

    try:
        data = res.json()
        print("=== Fetched 1 trial ===")
        print(json.dumps(data.get("studies", [])[0], indent=2))
    except Exception as e:
        print("⚠️ Failed to parse JSON:", e)
        print("Full raw text:")
        print(res.text)
        exit(1)

except Exception as outer_e:
    print("🚨 Outer exception caught:", outer_e)
    exit(1)
