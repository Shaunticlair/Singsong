from datetime import datetime, timedelta
import json

from song_class import Song
from record_class import Record

def export_data(record):
        """
        Export songs to the desired json file, for permanent storage.
        """
        exportdict={}
        
        """Fill export dictionary with data from record """
    
    
        with open('songs2.json', 'w') as json_file:
            json.dump(exportdict, json_file)

