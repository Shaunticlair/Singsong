
Created in: July 2019

Last Updated: 3/20/20

Original Version of interface. Given basic functionality, some bugs remain. Was not modularized into different documents. 

    This program creates a text interface for recording the dates upon which songs are practiced by the user.
    In order to encourage to user to practice more, mechanics of "experience points", "levels", and "streaks" are used to make the 
    experience more like a game. 
    
    Song data is stored in a json file, and will be retrieved and edited upon each running of the main.py file. 
    
    
    
###Workflow
    
    Singers.py:
        
        Classes:
        the Song class, which represents songs sung, 
        the Record class, which represents the interface itself, 
        the Date class, which represents dates differently.
        
        Permanent data:
        the dictionaries containing parameters for leveling up and how to represent data, 
        the interactive element which allows the user to use the program easily.
        
        Editable data:
        the data imported from songs2.json
    
    
    songs2.json:
    
        Stores every single song with its many parameters.