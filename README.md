# ESG Activity API Submitter

A flexible Python script designed to automate the submission of data to the ESG Activity Store API. It supports generating multiple entries for a single activity over a specified date range (e.g., daily or weekly).

## Prerequisites
* Python 3.x
* `requests` library

You can install the required library using pip:
`pip install requests`

## How It Works
The script uses a `base_payload` template. It loops through your specified date range, dynamically injects the correct date into the payload, and sends a POST request to the API. 

This makes it completely agnostic to the type of activity. You just define the fields required for your specific form, and the script handles the looping and submission.

## Configuration

1. **Set your API Key:**
   Replace `your_api_key_here` in the script with your actual key generated from *Settings → API Keys*.

2. **Define your Payload Template:**
   Update the `ACTIVITY_PAYLOAD_TEMPLATE` dictionary. You will need:
   * `question_id`: The ID of the activity form.
   * `facility_id`: Your location ID (*Settings → Locations*).
   * `reporting_cycle_id`: The ID for your reporting period (*Settings → Financial Year*).
   * `fields`: A key-value map of the exact form questions and your answers.

3. **Set your Execution Parameters:**
   Modify the arguments passed to `submit_activity_entries()` at the bottom of the script:
   * `frequency`: Set to `'daily'`, `'weekly'`, or `'cycle'` (single entry).
   * `start_date_str`: The beginning of your reporting loop (Format: `YYYY-MM-DD`).
   * `end_date_str`: The end of your reporting loop (Format: `YYYY-MM-DD`).

## Execution
Run the script from your terminal:
`python main.py`

## Example Use Cases
* **Waste Tracking:** Set frequency to `'daily'` and add your daily waste output values to the `fields`.
* **Supplier Logs:** Set frequency to `'weekly'` to push supplier purchase logs once a week.
* **Annual Audits:** Set frequency to `'cycle'` to submit a single, one-off payload for the current reporting cycle.
