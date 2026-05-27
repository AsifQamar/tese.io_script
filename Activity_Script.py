import requests
import copy
from datetime import datetime, timedelta

def submit_activity_entries(api_key, frequency, start_date_str, end_date_str, base_payload):
    url = 'https://stage-api.tese.io/api/v3/external/esg/activity-store'
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    current_date = start_date

    while current_date <= end_date:
        # Deep copy to ensure we don't overwrite the original template fields
        payload = copy.deepcopy(base_payload)
        payload["date"] = current_date.strftime("%Y-%m-%d")
        
        # Append frequency context to the metadata notes safely
        if "metadata" not in payload:
            payload["metadata"] = {}
        original_notes = payload["metadata"].get("notes", "API Submission")
        payload["metadata"]["notes"] = f"{original_notes} - {frequency.capitalize()} Entry"

        # Send the API Request
        response = requests.post(url, headers=headers, json=payload)
        print(f"[{payload['date']}] Status: {response.status_code} | Response: {response.text}")

        # Increment date based on desired frequency
        if frequency == 'daily':
            current_date += timedelta(days=1)
        elif frequency == 'weekly':
            current_date += timedelta(days=7)
        else: 
            # If 'cycle' or unrecognized, break after a single entry
            break

# ==========================================
# EXECUTION: Configure for ANY activity here
# ==========================================
if __name__ == "__main__":
    API_KEY = 'your_api_key_here'
    
    # Define your activity-specific structure here
    # You can swap this out depending on the form you are targeting
    ACTIVITY_PAYLOAD_TEMPLATE = {
        "question_id": "YOUR_QUESTION_ID",
        "facility_id": "YOUR_FACILITY_ID",
        "reporting_cycle_id": "YOUR_REPORTING_CYCLE_ID",
        "fields": {
            "Your custom field 1": "Value 1",
            "Your custom boolean field": True,
            "Your custom number field": 150
        },
        "source": "api",
        "needs_approval": True,
        "metadata": {
            "notes": "Custom Activity Log"
        }
    }

    submit_activity_entries(
        api_key=API_KEY,
        frequency='weekly',          # Options: 'daily', 'weekly', 'cycle'
        start_date_str='2026-05-01', 
        end_date_str='2026-05-27',
        base_payload=ACTIVITY_PAYLOAD_TEMPLATE
    )