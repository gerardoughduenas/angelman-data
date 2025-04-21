import requests  
import json

# === CONFIG ===  
API_URL = "https://classic.clinicaltrials.gov/api/query/study_fields"  
QUERY = "Angelman Syndrome"  
FIELDS = [  
    "NCTId", "BriefTitle", "OverallStatus", "StartDate", "BriefSummary",  
    "LocationCity", "LocationState", "LocationCountry"  
]  
LIMIT = 1000  

params = {  
    "expr": QUERY,  
    "fields": ",".join(FIELDS),  
    "min_rnk": 1,  
    "max_rnk": LIMIT,  
    "fmt": "json"  
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
fields = data.get("StudyFieldsResponse", {}).get("StudyFields", [])  
trials = []

for study in fields:  
    trials.append({  
        "NCTId": study.get("NCTId", [""])[0],  
        "BriefTitle": study.get("BriefTitle", [""])[0],  
        "OverallStatus": study.get("OverallStatus", [""])[0],  
        "StartDate": study.get("StartDate", [""])[0],  
        "BriefSummary": study.get("BriefSummary", [""])[0],  
        "LocationCity": study.get("LocationCity", [""])[0],  
        "LocationState": study.get("LocationState", [""])[0],  
        "LocationCountry": study.get("LocationCountry", [""])[0]  
    })

# === SAVE ===  
with open("angelman-clinical-trials.json", "w") as f:  
    json.dump(trials, f, indent=2)

print(f"✅ Exported {len(trials)} trials")
