import os
from Reader import Reader
import requests

#------------------------------------------------------------------------------------------
# Edit these for your task!

# path to your authentication
AUTH_FILE = "/home/marcus/grive/codedungeon/diurnalis/auth.txt"

# your beeminder details (other than authentication)
USERNAME = "jmbhughes"
GOAL_SLUG = "journal"

# path to your journal 
JOURNAL_PATH =  "/home/marcus/grive/journal/journal.tex"

#Nothing below this line needs updating.
#------------------------------------------------------------------------------------------
GOAL_URL="https://www.beeminder.com/api/v1/users/{}/goals/{}/datapoints.json".format(USERNAME, GOAL_SLUG)

def get_auth_token(auth_file=AUTH_FILE):
    ''' Loads the authorization token from a local file'''
    with open(auth_file, "r") as f:
        l = f.readlines()
    return l[1][:-1]

class BeeminderAPI:
    def __init__(self, goal_url, auth_token):
        self.goal_url = goal_url
        self.auth_token = auth_token
        self.datapoints = self._get_datapoints()

    def _datapoint_exists(self, timestamp):
        return timestamp in self.datapoints    

    def post_datapoint(self, value, timestamp=None):
        ''' Post a new data point with a request '''
        if timestamp:
            data = {'value':value,
                    'auth_token':self.auth_token,
                    'timestamp':timestamp}
        else:
            data = {'value':value,
                    'auth_token':self.auth_token}
        requests.post(self.goal_url, data=data)
        
    def update_datapoint(self, timestamp, value):
        ''' Update an existing data point with a request, 
        assumes that the user has already checked for existence
        '''
        id = self.datapoints[timestamp]['id']
        data = {'value':value,
                'auth_token':self.auth_token,
                'timestamp':timestamp}
        datapoint_url = self.goal_url.replace(".json","/{}.json".format(id))
        requests.put(datapoint_url, data=data)
        
    def _get_datapoints(self):
        datapoints = requests.get(self.goal_url,
                                  data={'auth_token':self.auth_token}).json()
        return {dp['timestamp']:dp for dp in datapoints}
    
class JournalBeeminderUpdater(BeeminderAPI):
    def __init__(self, goal_url, auth_token, journal):
        BeeminderAPI.__init__(self, goal_url, auth_token)
        self.journal = journal

    def update(self, n=10):
        ''' update the n most recent data points '''
        for entry in self.journal.get_most_recent_entry(n=n):
            if self._datapoint_exists(entry.date.timestamp()):
                self.update_datapoint(entry.date.timestamp(), len(entry))
            else:
                self.post_datapoint(len(entry), timestamp=entry.date.timestamp())        
        
if __name__ == "__main__":
    # get authorization token
    auth_token = get_auth_token()

    # Load and process the journal, getting the most recent entry
    journal_path = JOURNAL_PATH
    journal = Reader(journal_path)

    # Interface with Beeminder and make update
    beeminder = JournalBeeminderUpdater(GOAL_URL, auth_token, journal)
    beeminder.update()
