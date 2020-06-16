from datetime import datetime, timedelta
import json

#Local file imports
from song_class import Song



def load_song_data(file):
    """
    Load song data from file.json.
    """
    filename = file + '.json'
    try: #Try to load json file
        with open(filename) as json_file:
            loaded_song_data= json.load(json_file)
    except: #If it fails, load an empty file.
        loaded_song_data={}
        
    return loaded_song_data

def parse_song_data(data):
    """
    Convert song data from dictionaries to the Song class.
    """
    parsed_song_data = {} 
    
    for song_name in data: #View each song
        songdict = data[song_name] #Get that song's dictionary
        
        song = Song(songdict) #Use dictionary to create Song object
        parsed_song_data[song_name] = song #Add song object
        
    return parsed_song_data #Return song object

"""Edit file name if you would like to rename your json file. Do not add a .json suffix."""
file = 'saved_songs'

loaded_song_data = load_song_data(file) #Load data

song_data = parse_song_data(loaded_song_data) #Convert to proper form
    