
Created in: July 2019

Last Updated: 3/20/20

Original Version of interface. Given basic functionality, some bugs remain. Was not modularized into different documents. 

    This program creates a text interface for recording the dates upon which songs are practiced by the user.
    In order to encourage to user to practice more, mechanics of "experience points", "levels", and "streaks" are used to make the 
    experience more like a game. 
    
    Song data is stored in a json file, and will be retrieved and edited upon each running of the main.py file. 
    

Dependencies:
    json
    datetime
    
    
###Workflow

    ###Basics

        main.py: ##################################### COMPLETE
            Imports classes, high-level level view functioning of the program from different files.
            
        loader.py: #################################COMPLETE
            Loads data from json
            
        exporter.py:
            Exports data to json
            
        dictionaries.py: #############################COMPLETE
            Holds dictionaries of parameters.
        
    ###Classes
    
        ui_class.py:
            Contains UI class. Controls user interaction.
            
        record_class.py: ################################ WIP
            Contains Record class. Controls editing of songs.
            
        song_class.py:  ############### COMPLETE
            Contains Song class. Stores data for a single song and its methods.
    
    ###Method specialization
    
        markup.py:############### WIP
            Contains methods for marking up text to be more visually appealing.
            
        date_compute.py: ############### WIP
            Contains methods to convert dates and do computations on them.
        
    ###Data storage
    
        saved_songs.json: #########################COMPLETE
            Contains data on every song sung.
            
            
    ###Test writing
    
        test.py:
            Tests all other modules using unittest.
        