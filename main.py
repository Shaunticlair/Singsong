"""All necessary imports for this program to run"""
import json
from datetime import datetime, timedelta

"""Import relevant classes """
from song_class import Song
from record_class import Record
from ui_class import UI

"""Import data from JSON"""
from loader import song_data

"""Feed data into the Record object, which will hold all songs"""
recorder = Record(song_data)

"""Give the Record object to the UI, which will mediate between the Record object and the user."""
interface = UI(recorder)

"""Begin interfacing with the user."""
interface.start_program() 

"""Exporting data occurs within interface."""



