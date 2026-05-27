import requests
import pandas as pd
import time
import os
import math

API_KEY = os.getenv('TESE_API_KEY', 'tese_2353c2b9b1a63a279cdb917fa6f46a565f65256906e59d8b1c895c7868c06fe6')

def get_reporting_cycle_id(date_string):
    """Maps the start date to the correct Q1-Q4 Reporting Cycle ID."""
    month = pd.to_datetime(date_string).month
    if 1 <= month <= 3: return "6a0497deb0c370a9b8e58abf"  # Q1
    elif 4 <= month <= 6: return "6a0497deb0c370a9b8e58abb"  # Q2
    elif 7 <= month <= 9: return "6a0497deb0c370a9b8e58ac1"  # Q3
    else: return "6a0497deb0c370a9b8e58abd"  # Q4

def is_valid(value):
    """Helper to check if a pandas dataframe value is empty/NaN."""
    if pd.isna(value) or value == "":
        return False
    return True

def submit_production_ready_activities(file_path):
    # Load file
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Use .csv or .xlsx")

    url = 'https://stage-api.tese.io/api/v3/external/esg/activity-store'
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }

    success_count = 0
    error_count = 0

    for index, row in df.iterrows():
        try:
            frequency = str(row['Frequency']).strip().lower()
            start_date = pd.to_datetime(row['Start Date']).strftime('%Y-%m-%d')
            cycle_id = get_reporting_cycle_id(start_date)
            
            payload = {
                "question_id": "Q_ACTIVITY_1774263214927_HOLHYH",
                "facility_id": "6a03512fb0c370a9b8e4ee06",
                "reporting_cycle_id": cycle_id,
                "fields": {
                    "Enter the supplier name exactly the same way every time — inconsistent spelling creates duplicate entries.": row.get('Supplier Name', 'CoopeAgri Costa Rica'),
                    "Does this supplier provide agricultural food, feed, or biofuel ingredients? Packaging suppliers should not be included.": True,
                    "Does this supplier currently hold a recognised GFSI food safety certification?": True,
                    "Shown when GFSI-certified = Yes. Which GFSI-recognised programme is the supplier certified under?": {
                        "label": "BRCGS", "value": "BRCGS", "_id": "69c24bc06fb663108dc9486f"
                    },
                    "How much did you spend with this supplier on agricultural products during the reporting period?": float(row['Spend']),
                    "System-populated. SUM of spend across all agricultural supplier records.": str(row['Total Spend']),
                    "System-populated. SUM of spend where GFSI certified = Yes.": str(row['Total Spend GFSI'])
                },
                "source": "api",
                "needs_approval": True,
            }

        
            if frequency == 'daily':
                payload["date"] = start_date
                payload["metadata"] = {"notes": f"Automated Daily entry for {start_date}"}
                log_context = start_date
            else:
                if not is_valid(row.get('End Date')):
                    raise ValueError(f"End Date is required for {frequency} frequency.")
                
                end_date = pd.to_datetime(row['End Date']).strftime('%Y-%m-%d')
                payload["start_date"] = start_date
                payload["end_date"] = end_date
                payload["metadata"] = {"notes": f"Automated {frequency.capitalize()} entry: {start_date} to {end_date}"}
                log_context = f"{start_date} to {end_date}"


            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code in [200, 201]:
                print(f"[SUCCESS] Row {index + 1} ({log_context}): Uploaded to Cycle {cycle_id}")
                success_count += 1
            else:
                print(f"[FAILED] Row {index + 1} ({log_context}): API returned {response.status_code} - {response.text}")
                error_count += 1

            time.sleep(0.5)

        except Exception as e:
            print(f"[ERROR] Row {index + 1} failed during processing. Reason: {e}")
            error_count += 1
            continue 

    print(f"\n--- Upload Complete ---")
    print(f"Successfully processed: {success_count}")
    print(f"Failed/Errors: {error_count}")

# Execute the script
submit_production_ready_activities('supplier_data_sample.xlsx')
