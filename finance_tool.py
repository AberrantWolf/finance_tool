from datetime import datetime
import json
import requests

import finance_display

base_url = "https://api.airtable.com/v0/{}/{}"
access_id = ""
api_key = ""
headers = ""

# Setup authentication junk
def setup_auth():
    global api_key
    global access_id
    global headers
    f = open("api_key", "rt")
    lines = f.read().splitlines()
    access_id = lines[0]
    api_key = lines[1]
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(api_key)}


# Pull the data from the 'public' API
def get_data(endpoint):
    url = base_url.format(access_id, endpoint)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))['records']
    elif response.status_code == 429:
        print("429 RETURNED: Requesting too fast, you must wait 30 seconds for the next request")
    else:
        print("Response code: {}".format(response.status_code))
        return None


def concat_transactions(into_list, from_list, is_checkpoint=False):
    for xact in from_list:
        fields = xact['fields']
        entry = {'is_checkpoint': is_checkpoint}

        # Due date (optional?) (different values in tables)
        # NOTE: Should be requried for recurring charges?
        # if 'Due Date' in fields:
        #     entry['due_date'] = fields['Due Date'] 
        
        if 'Change Date' in fields:
            entry['date'] = datetime.strptime(
                fields['Change Date'], '%Y-%m-%d')
        
        if 'Date' in fields:
            entry['date'] = datetime.strptime(fields['Date'], '%Y-%m-%d')

        if 'date' not in entry:
            continue # skip entries that haven't been processed
        
        # Amount (required)
        entry['amount'] = fields['Amount']
        
        # Description (optional)
        if 'Description' in fields:
            entry['desc'] = fields['Description']

        # Account (required)
        if 'Account' in fields:
            entry['account'] = fields['AccountName']
        else:
            continue

        into_list.append(entry)


# Start the program!
if __name__ == "__main__":
    setup_auth()

    expenses = get_data('Expenses')
    income = get_data('Income')
    checkpoints = get_data('Checkpoints')

    all_trans = []

    if expenses is not None:
        print("Reading Expenses...")
        concat_transactions(all_trans, expenses)
    else:
        print("No expenses found")

    if income is not None:
        print("Reading Income...")
        concat_transactions(all_trans, income)
    else:
        print("No income found")
    
    if checkpoints is not None:
        print("Reading Checkpoints...")
        concat_transactions(all_trans, checkpoints, True)
    else:
        print("WARNING: Not checkpoints found")

    finance_display.generate_chart(all_trans)
