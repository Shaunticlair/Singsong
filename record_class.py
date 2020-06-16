



class Record():
    """
    Records is the main object that stores songs and handles modifications to those objects.
    """
    
    def __init__(self):
        
    pass



        
        
class Records():
    """
    Records is the main object that stores songs and handles modifications to those objects.
    """
    def __init__(self):
        
        #Obtain data
        self.load_songs() #Load songs from json file
        self.parse_songs() #Convert songs from dictionary to 
        
        #Convert to page form
        self.get_pages(self.songsperpage)
        self.songsperpage = 8
        self.pick_page(1)
        self.edits=[]

    def load_songs(self):
        """
        Load songs from json.
        """
        try: #If data exists, then load it
            with open('songs2.json') as json_file: #Open file
                loaded_song_data= json.load(json_file) #Store data in a variable
        except: #If no data exists, assume an empty file
            loaded_song_data={} 
        self.loaded_songs=loaded_song_data #Save song as loaded
        
    def parse_songs(self):
        """
        self.loaded_songs: Songs as dictionaries loaded from json
        self.songs: Songs converted from dictionaries to Song objects.
        """
        converted_song_data={}
        for song in self.lsongs:
            songdict = self.lsongs[song]
            converted_song_data[song] = Song(songdict)
        self.songs = converted_song_data

    def export_songs(self):
        """
        Export songs to the desired json file, for permanent storage.
        """
        exportdict={}
        consongs=self.csongs
        for song in consongs:
            currsong=consongs[song]
            currsong.check_streak()
            currsong.check_level()
            exportdict[currsong.song_name]=currsong.get_song()
        with open('songs2.json', 'w') as json_file:
            json.dump(exportdict, json_file)
            
            
    def get_personal_xp(self):
        """
        Get xp of player based on the level of all songs.
        """
        self.player_xp = 0
        #Effective hours= self.player_xp*4/60
        self.lifetime_xp = 0
        
        for song in self.csongs:
            
            currsong = self.csongs[song]
            
            self.player_xp += total_xp_dict[currsong.current_level] + currsong.xp
            self.lifetime_xp += currsong.how_many_times
        
    
    
#Edit songs
    def new_song(self,name,newsongdict={}):
        """
        Add a new song to the list of songs.
        """
        newsongdict['song_name']=name
        self.csongs[name]=Song(newsongdict)
    
    def remove_song(self,name):
        """
        Remove a song from the list of songs.
        """
        try:
            del self.csongs[name]
        except:
            print("Error! Song may no longer exist.")

    def print_songs(self):
        """
        Prints current songs.
        """
        for song in self.csongs:
            print(song)
            
    def song_attr(self,song,attr,val):
        """
        Define a song attribute
        """
        if song not in self.csongs:
            print('Song not found!')
            return None
        mod_song=self.csongs[song]
        mod_song.modify(attr,val)
        self.csongs[song]=mod_song
        
    def temp_song(self,song):
        """
        Save that you plan on changing a song.
        """
        if song not in self.csongs:
            print('Song not found!')
            return None
        mod_song=self.csongs[song]
        modification=mod_song.temp_mod()
        if modification!=None:
            self.edits+=[modification]
        
    def show_edits(self):
        """
        Shows pending edits to songs in the database.
        """
        editbles=self.edits
        print('Here are the pending edits:')
        for edit_num in range(len(editbles)):
            edit=editbles[edit_num]
            operation=edit[1]
            song_name=edit[0]
            try:
                attr=songattrs[edit[2]]
                oldval=self.csongs[song_name].__dict__[edit[2]]
                newval=edit[3]
                print(str(edit_num)+':',operation,C('B'),song_name,C('N'),': change',\
                      C('G'),attr,C('N'),'from',C('R'),oldval,C('N'),\
                      'to',C('R'),newval,C('N'))
            except IndexError:
                print(str(edit_num)+':',C('R')+operation,C('B'),song_name,C('N'))
                
    def new_edit(self,song,edit_type):
        """
        Create new edit
        """
        try:
            self.edits+=[(song,edit_type)]
        except:
            print('Something went wrong!')
            
#Printing songs
    def print_song_data(self):
        """
        Prints songs with data.
        """
        consongs=self.csongs
        for song in consongs:
            print(consongs[song])
        
    def song_list(self):
        """
        List all songs.
        """
        consongs=self.csongs
        for song in consongs:
            consongs[song].list_item()
            
#Pages
    def get_pages(self, songperpage=8):
        """
        Get pages for songs, n songs each page.
        """
        (newlist,songpages,consongs)=([],[],self.csongs)
        
        ###Sort csongs by most recent
        song_iterable= iter( zip(consongs.keys(), consongs.values() ))
        songs = [ (name, song_data) for name, song_data in song_iterable ] #Dict to tuple
        songs= sorted(songs, key=lambda song: song[1].days_since_last())
        
        #Iterate through songs, add them to page if appropriate *or* open new page
        for song in songs:
            if len(newlist)<songperpage:
                newlist.append((song[0],song[1]))
            else:
                songpages+=[newlist]
                newlist=[ (song[0],song[1]) ] #Add new song
        if newlist!=[]:
            songpages+=[newlist]
        self.songpages=songpages
        
    def pick_page(self,page):
        """
        Pick current viewing page
        """
        self.page=page-1
        if self.page in range(0,len(self.songpages)):
            self.pagedict=dict(self.songpages[self.page])
        elif len(self.songpages)==0:
            print("No pages available!")
            self.page=0
            self.pagedict={}
        else:
            print("Page not found!")
            self.page=0
            self.pagedict=dict(self.songpages[self.page])
            
        
    def print_page(self,xp_show=False):
        """
        Print the page currently saved.
        """
        songpages=self.songpages
        page=self.page
        
        try:
            print('Page ',str(page+1)+'/'+str(len(self.songpages))+'\n')
            self.get_personal_xp()
            
            
            print("Player Level: "+ str(self.player_xp//45))
            print("Player XP: "+str(self.player_xp ) +'\n')
            
            
            
            for sheet in songpages[page]:
                sheet[1].list_item(xp_show) #Printing pages
            print('\n')
        except:
            raise
            print('\nNo songs found!\n')
            
    def select_songsperpage(self):
        """Change songs per page."""
        
        try:
            songsperpage = int( input("How many songs per page would you like? ") )
            
            print("Set number of songs per page to "+str(songsperpage))
            self.songsperpage = songsperpage
            self.page = 1
            self.refresh()
            
        except:
            print("Something went wrong...")
            
    def find(self):
        """
        Find what page contains a given song.
        """
        pass
            
            
#Cleanup    
    def interpret(self,string=''):
        """
        Interpret part of a song name as the first matching full name.
        """
        if string=='':
            query=input(string)
        else:
            query=string
        if query.lower() in {'end','none','never mind'}:
            return None
        for song in self.pagedict: #Exact match
            if query==song:
                return song
        for song in self.pagedict: #Partial match
            if query in song:
                did_they_mean = did_you_mean(song)
                
                if did_they_mean==None: #Cancel the attempt
                    return None
                elif did_they_mean:
                    return song
        print('Song not found')
        return None
    
    def refresh(self):
        """
        Refresh your song list.
        """
        self.export_songs()
        self.load_songs()
        self.get_pages(self.songsperpage)
        self.pick_page(1)
        print('All data has been refreshed.')
    
    def cancel(self):
        """
        Cancel a planned edit.
        """
        print("Which edit do you want to cancel?")
        self.show_edits()
        choice=input('')
        if not int(choice) in range(len(self.edits)):
            print("That's not an available number.")
            return None
        print("You're choosing to undo edit"+C('R'),choice,C('N'))
        dummy=input("Are you sure? ")
        if not dummy in confirmdict:
            return None
        self.edits=self.edits[:int(choice)]+self.edits[int(choice)+1:]
        print('Edit removed')
        
    def confirm(self):
        """
        Confirm all changes.
        """
        self.show_edits()
        print("Are you sure you want to confirm these edits? ")
        choice=input('')
        if not choice in confirmdict:
            return False
        else:
            pass
            for edit in self.edits:
                song_name=edit[0]
                
                try:
                    song=self.csongs[song_name]
                except:
                    pass
                
                if edit[1]=='Modify':
                    attr=edit[2]
                    val=edit[3]
                    song.modify(attr,val)
                    self.csongs[song_name]=song
                    print('Edited',CC('B',song_name))
                elif edit[1]=='Add':
                    self.new_song(song_name) #Song is a string!
                    print( C('R')+'Added',CC('B',song_name) )
                elif edit[1]=='Remove':
                    self.remove_song(song_name)
                    print(C('R')+'Removed',CC('B',song_name))
                elif edit[1]=='Sang':
                    song.sang_today()
                    print(C('R')+'You sang',CC('B',song_name),'today!')
                else:
                    print('HELP')
                    
        self.edits=[]
        self.refresh()
        return True

