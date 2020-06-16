""" SONG UI """

#UI=Records()
xp_show=False
for song in UI.csongs:
    realsong=UI.csongs[song]
    days_since=realsong.days_since_last()
    if abs(leveldict[realsong.current_level][2]-days_since)<5 and days_since>5 and realsong.current_level > realsong.max_level//2:
        PA(f"'{realsong.song_name}' might be in danger of losing track!")
while True:
    print("")
    UI.print_page(xp_show)
    n_edits=len(UI.edits) #Number of edits
    if n_edits>0:
        print(f"You have {n_edits} pending edit{P(n_edits)}")
    print("What do you want to do?") #Prompt input for operation.
    print("(Type '*' to get a list of options)")
    statement=input("")
    combo=statement.split(' ')+['']
    secondline=combo[1]
    statement=combo[0].lower()
        
#Help
    if statement in {'*','help'}:
        PA("Type 'view' to see the complete data for a song.")
        PA("Type 'sing' to note that you sang a song today.")
        PA("Type 'add' to add a new song.")
        PA("Type 'quick' to quickly add a new song with an artist.")
        PA("Type 'remove' to remove a song.")
        PA("Type 'page' to switch pages.")
        PA("Type 'count' to select the count of songs per page for this session.")
        PA("Type 'edit' to edit an attribute of a song.")
        print("")
        PA("Type 'check' to see which songs might be at risk of losing a level.")
        PA("Type 'xp' to toggle xp showing.")
        PA("Type 'edits' to view pending edits.")
        PA("Type 'confirm' to confirm pending edits.")
        PA("Type 'cancel' to cancel a pending edit.")
        PA("Type 'reload' to reload the data.")
        PA("Type 'end' to close.")
#End
    elif statement in {'end','stop','close','finish','quit'}: #When closed, export
        if edit_check():
            print("Program closing.")
            UI.export_songs()
            break
        else:
            continue
        
#Pick a song
    elif statement in {'pick','view','see','show'}: #If you name a song, list off all attributes.
        if secondline=='':
            print("Which song do you want to view?")
        new_statement=UI.interpret(secondline)
        if new_statement==None:
            pass
        else:
            print(UI.pagedict[new_statement])
            
#Sing today
    elif statement in {'sing', 'sang', 's'}:
        if secondline=='':
            print("What did you sing today?")
        new_statement=UI.interpret(secondline)
        if new_statement==None:
            pass
        else:
            UI.new_edit(new_statement,'Sang')
            print("Added to the edit list.")
            
#Delete song
    elif statement in {'d','del','delete','remove'}:
        if secondline=='':
            print("Which song do you want to remove?")
        new_statement=UI.interpret(secondline)
        if new_statement==None:
            pass
        else:
            UI.new_edit(new_statement,'Remove')
            print('Added to the edit list.')
            
#Flip page
    elif statement in {'page','flip','p'}:
        if secondline=='':
            print("Which page?")
            new_statement=input("")
        else:
            new_statement=secondline
        try:
            UI.pick_page(int(new_statement))
        except:
            print("Not a valid page! Please only enter numbers.")
        
#Set songs per page
    elif statement in {'songcount','count','perpage','songsperpage'}:
        UI.select_songsperpage()
        
#New song
    elif statement in {'new','new song','new_song','create','create_song','add'}:
        if secondline=='':
            print("What's the name of the song?")
            new_statement=input("")
        else:
            new_statement=secondline
        UI.new_edit(new_statement,'Add')
        print('Added to the edit list.')
        
    elif statement in {'quick','make','start'}:
        print("What's the name of the song?")
        new_statement=input("")
        print("Who is the artist?")
        two_statement=input("")
        print(f"You are adding "+CC('B',new_statement)+" by "+CC('R',two_statement)+". Are you sure?")
        red_statement=input("")
        if not red_statement.lower() in confirmdict:
            print('Cancelled.')
            continue
        UI.new_song(new_statement)
        song=UI.csongs[new_statement]
        (attr,val)=('artist',two_statement)
        song.modify(attr,val)
        song.sang_today()
        UI.csongs[new_statement]=song
        print('Song created.')
        UI.refresh()
    
    elif statement in {'edit','change','variable','modify'}:
        if secondline=='':
            print("What song do you want to change?")
        new_statement=UI.interpret(secondline)
        if new_statement==None:
            pass
        else:
            UI.temp_song(new_statement)
            
    elif statement in {'check'}:
        for song in UI.csongs:
            realsong=UI.csongs[song]
            days_since=realsong.days_since_last()
            if abs(leveldict[realsong.current_level][2]-days_since)<5 and days_since>1:
                PA(f"'{realsong.song_name}' might be in danger of losing track!")
                
    elif statement in {'xp'}:
        xp_show=not xp_show
        print("XP showing toggled.")
            
    elif statement in {'edits','queue','pending'}:
        UI.show_edits()
        
    elif statement in {'cancel','undo'}:
        UI.cancel()
        
    elif statement in {'confirm','save'}:
        UI.confirm()
        
    elif statement in {'refresh','reload'}:
        if edit_check():
            UI.refresh()
            
    enter_to_continue()
    
    
#Modify data
            
    def temp_mod(self):
        """
        Prepare to modify an attribute of this song.
        """
        #Prompt the user
        print("Which attribute do you want to edit?")
        
        attr_displays = [string for string in D.string_to_attr.keys() ] #Create an order for the attribute names
        
        for index in range( len( attr_displays ) ): #Get each index
            name = attr_displays [index] #Get each string representation
            
            print( index , ': ' , name ) #Show the index and string representation
            
        #Ensure a valid result was chosen
        try:
            index = int(input('')) #Make sure the result is an integer
            
            attr_name = attr_displays [index] #Make sure the result is a valid index, and get name
            attr = D.string_to_attr [attr_name] #Get relevant attribute
            
        except: #If something went wrong, quit out
            print('Not a valid choice. Must choose by integers given.')
            return None

        #Successful index choice, proceed with another prompt
        print(f"You've chosen {name}.")
        print("What do you want to set this value to?")
        value=input('')

        try:
            converted_value = self.set_type(attr, value) #Convert to the correct type for this value
            
            print("Edit saved.")
            
            return (attr, converted_value) #Return result of this exchange
            
        except Exception as error_message: #If something goes wrong, print what went wrong and proceed
            print("Your edit failed:", error_message)
            return None

        
        
    def set_type(self, attribute, value):
        """
        Check the type of an inputted attribute to ensure that it is reasonable.
        
        attribute: string representing the relevant attribute inside the Song class.
        value: the intended value for that attribute.
        
        returns: the value converted to the correct type.
        
        raises: if the value cannot be converted to the correct type.
        """
        
        allowed_type = D.attr_types[attribute] #Get allowed types
        
        #######################
        if allowed_type == 'date_string': #If the allowed type is date string
            
            if value == 'None': #The value can be None.
                return None
            
            try: #Check if is a valid date
                Date.string_to_date(value) #Will fail if not a valid date
                return value #If valid, return as-is
                
            except:
                raise ValueError("That's not a valid date!")
        
        ######################
        if allowed_type == 'list:date_string': #If the allowed type is a list of dates
            
            try: 
                edited_string = remove_chars( value, '[] ') #Remove ends of the list and spaces
                
                dates = edited_string.split(',') #Split into list of strings
                [ Date.string_to_date(date) for date in dates ] #Check that all dates are valid
                
                return dates #If no issues, return the list of strings
            
            except:
                raise ValueError("That list of dates is invalid!")
                
        else:
            try:
                return allowed_type(value) #Convert to the correct type
            except:
                raise TypeError("Your input could not be converted into the correct type!") #If conversion fails, raise