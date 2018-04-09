import os
from Reader import Reader
import requests
import argparse
import json

class BeeminderAPI:
    ''' A simple python interface for the Beeminder API '''
    def __init__(self, goal_url, auth_token):
        self.goal_url = goal_url
        self.auth_token = auth_token
        self.datapoints = self._get_datapoints()

    def _datapoint_exists(self, timestamp):
        ''' determines if a datapoint already exists for that timestamp '''
        return timestamp in self.datapoints    

    def post_datapoint(self, value, timestamp=None):
        ''' Post a new data point with a request 
        @param value : the value being updated
        @param timestamp : the standard datetime timestamp
        '''
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
    ''' a customized API interface for the journal activities ''' 
    def __init__(self, goal_url, auth_token, journal):
        BeeminderAPI.__init__(self, goal_url, auth_token)
        self.journal = journal

    def update(self, n=10):
        ''' update datapoints for n most recent journal entries '''
        for entry in self.journal.get_most_recent_entry(n=n):
            if self._datapoint_exists(entry.date.timestamp()):
                self.update_datapoint(entry.date.timestamp(), len(entry))
            else:
                self.post_datapoint(len(entry), timestamp=entry.date.timestamp())        
        
if __name__ == "__main__":
    # get the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("configuration", help="path to a json configuration file")
    args = vars(parser.parse_args())
    with open(args['configuration'], 'r') as f:
        args = json.load(f)
        
    # set up parameters
    journal = Reader(args["LOCAL"]["JOURNAL_PATH"])
    username = args["BEEMINDER"]["USERNAME"]
    goal_slug = args["BEEMINDER"]["GOAL_SLUG"]
    goal_url="https://www.beeminder.com/api/v1/users/{}/goals/{}/datapoints.json".format(username, goal_slug)
    
    # Interface with Beeminder and make update
    beeminder = JournalBeeminderUpdater(goal_url,
                                        args["BEEMINDER"]["AUTH_TOKEN"],
                                        journal)
    beeminder.update()
