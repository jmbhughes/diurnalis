import os
from datetime import datetime
from Reader import Reader

def get_auth_token():
    ''' Loads the authorization token from a local file'''
    with open("auth.txt", "r") as f:
        l = f.readlines()
    return l[1][:-1]

def form_curl(value, auth_token, timestamp=None):
    ''' Create a curl request to use as a command '''
    if timestamp:
        return "curl -X POST https://www.beeminder.com/api/v1/users/jmbhughes/goals/journal/datapoints.json -d auth_token={} -d value={} -d timestamp={}".format(auth_token, value, timestamp)
    else:
        return "curl -X POST https://www.beeminder.com/api/v1/users/jmbhughes/goals/journal/datapoints.json -d auth_token={} -d value={}".format(auth_token, value)

if __name__ == "__main__":
    # get authorization token
    auth_token = get_auth_token()

    # Load and process the journal, getting the most recent entry
    journal_path = "/home/marcus/grive/journal/journal.tex"
    reader = Reader(journal_path)
    entry = reader.get_most_recent_entry()

    # If the entry is today, update Beeminder with it otherwise report no writing
    is_today = entry.date.date() == datetime.today().date()
    if is_today:
        cmd = form_curl(len(entry), auth_token)
    else:
        cmd = form_curl(0, auth_token)
    os.system(cmd) # execute command
    
    # Uncomment below to create data points for all entries
    # entries = reader.get_journal_entries()
    # lengths = {int(entry.date.timestamp()):len(entry) for entry in entries}
    # for time, length in lengths.items():
    #     c = form_curl(length, auth_token, time)
    #     os.system(c)

