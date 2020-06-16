#Default data

"""This dictionary contains the default values for every song attribute."""

default_song_dict={'song_name': 'N/A',         'last_sung': None ,    'how_many_times': 0,
                   'dates_sung':[],            'current_streak': 0,   'current_level': 0,
                   'artist':'N/A',             'longest_streak': 0,   'max_level': 0, 
                   'levelfreeze':False,        'xp':0,                'last_demoted': None}

"""This dictionary converts the attribute names to their representations when displayed."""

attr_to_string={'song_name': 'Song name',           'last_sung': 'Last sung',              'how_many_times': 'How many times',
                'dates_sung': 'Dates sung',         'current_streak': 'Current streak',    'current_level': 'Current level',
                'artist': 'Artist',                 'longest_streak': 'Longest streak',    'max_level': 'Max level achieved',  
                'levelfreeze':'Level Frozen',       'xp':'XP',                             'last_demoted':'Last demoted'}

"""This dictionary converts the representations of attributes to their names inside the Song class."""

string_to_attr={ attr_to_string[key] : key for key in attr_to_string} #Reverse dictionary

"""This dictionary identifies the type available to this attribute."""

attr_types = {'song_name': str,                   'last_sung': 'date_string',               'how_many_times': int,
              'dates_sung': 'list:date_string',   'current_streak': int,                    'current_level': int,
              'artist': str,                      'longest_streak': int,                    'max_level': str,
              'levelfreeze':bool,                 'xp':'XP',                                'last_demoted':'date_string'}

"""This dictionary contains values that can be interpreted to mean "yes" by the code."""

confirmdict={'yes','true','mhm','yeah','yep','ye','y', 'confirm'} #Different ways to say "yes"


##Leveldict stores { level: ( minimum_xp_to_reach_level , required_max_streak_length_to_reach_level, days_to_lose_level ) }

"""This dictionary stores the data for each level as a tuple: minimum xp to reach this level, required max streak to reach this 
level, and the number of days to lose a level."""

leveldata = { 0: (0, 0, 0),      1: ( 1, 1, 2),    2: (3, 2, 2),     3: (5, 3, 4),     4: (7, 4, 7),
              5: (9, 5, 14),     6: (11, 6, 24),   7: (13, 7, 37),   8: (15, 8, 53),   9: (17, 9, 66),
              10: (19, 10, 76), 11: (21, 11, 83), 12: (23, 12, 86), 13: (25, 13, 88), 14: (27, 14, 89),
              15: (29, 15, 90), 16: (31, 16, 90), 17: (33, 17, 90), 18: (35, 18, 90), 19: (37, 19, 90),
              20: (39, 20, 90)}

"""This dictionary resembles leveldata, but has been converted for greater readability."""

leveldict =  { level: {'req_xp': leveldata[level][0], 
                       'req_streak': leveldata[level][1], 
                       'days_to_lose': leveldata[level][2]}
                        for level in leveldata }

"""This dictionary gets the total xp to reach a certain level by adding up all the xp for each lower level."""

total_xp = lambda total_level:  sum ( [      leveldict[level]['req_xp']     for level in range(total_level+1)     ] 
                            #Add up xp        #Get xp for a given level       #Select a level