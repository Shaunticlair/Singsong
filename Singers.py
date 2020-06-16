import json
from datetime import datetime, timedelta
from math import log
#Default data
defsongdict={'song_name': 'N/A','last_sung': 'N/A','how_many_times': 0,\
 'dates_sung':[],'current_streak': 0,'current_level': 0,\
 'difficulty': 'Unknown','artist':'N/A','longest_streak': 0,'max_level': 0,\
 'levelfreeze':False,'xp':0, 'last_demoted': None}

songattrs={'song_name': 'Song name','last_sung': 'Last sung',\
 'how_many_times': 'How many times','dates_sung': 'Dates sung',\
 'current_streak': 'Current streak','current_level': 'Current level',\
 'difficulty': 'Difficulty','artist': 'Artist','longest_streak': 'Longest streak',\
 'max_level': 'Max level achieved','levelfreeze':'Level Frozen','xp':'XP', 'last_demoted':'Last demoted'}

songinverse=[('Song name', 'song_name'),('Last sung', 'last_sung'),\
 ('How many times', 'how_many_times'),('Dates sung', 'dates_sung'),\
 ('Current streak', 'current_streak'),('Current level', 'current_level'),\
 ('Difficulty', 'difficulty'),('Artist','artist'),('Longest streak', 'longest_streak'),\
 ('Max level achieved', 'max_level'),('Level Frozen', 'levelfreeze'),('XP','xp'), ('Last demoted','last_demoted')]

confirmdict={'yes','true','mhm','yeah','yep','ye','y'}

attr_type= {'song_name': 'Song name','last_sung': 'Last sung',\
 'how_many_times': 'How many times','dates_sung': 'Dates sung',\
 'current_streak': 'Current streak','current_level': 'Current level',\
 'difficulty': 'Difficulty','artist': 'Artist','longest_streak': 'Longest streak',\
 'max_level': 'Max level achieved','levelfreeze':'Level Frozen','xp':'XP', 'last_demoted':'Last demoted'}



##Leveldict stores { level: ( minimum_xp_to_reach_level , required_max_streak_length_to_reach_level, days_to_lose_level ) }

leveldict = { 0: (0, 0, 0),      1: ( 1, 1, 2),    2: (3, 2, 2),     3: (5, 3, 4),     4: (7, 4, 7),
              5: (9, 5, 14),     6: (11, 6, 24),   7: (13, 7, 37),   8: (15, 8, 53),   9: (17, 9, 66),
              10: (19, 10, 76), 11: (21, 11, 83), 12: (23, 12, 86), 13: (25, 13, 88), 14: (27, 14, 89),
              15: (29, 15, 90), 16: (31, 16, 90), 17: (33, 17, 90), 18: (35, 18, 90), 19: (37, 19, 90),
              20: (39, 20, 90)}

colordict={'S':30,'R':31,'G':32,'Y':33,'B':34,'P':35,'C':36,'W':37,'N':0}

xp_up_to_level = lambda level: sum( [leveldict[x][0] for x in range(level+1)] ) #Get total xp to reach a given level

total_xp_dict={ level: xp_up_to_level(level) for level in range(21) } #Get total xp to reach all levels

##Used to compute "xp to next level" and "days to lose level"
#xp_2 = lambda x: round(x**2)
#decay_curve = lambda x: round( 90/( 1+2**(-x+7.5) ) )

#PLAYER LEVEL: XP // 60


"""
Tickets:
    >Fix recommendations to use more than first word
    >Fix highlighting of text
"""

class Records():
    def __init__(self):
        self.songsperpage = 8
        self.load_songs()
        self.parse_songs()
        self.get_pages(self.songsperpage)
        self.pick_page(1)
        self.edits=[]

    def load_songs(self):
        """
        Load songs from json.
        """
        try:
            with open('songs2.json') as json_file:
                loaded_song_data= json.load(json_file)
        except:
            loaded_song_data={}
        self.lsongs=loaded_song_data
        
    def parse_songs(self):
        """
        Take song data and turn it into Songs data type.
        """
        converted_song_data={}
        for song in self.lsongs:
            converted_song_data[song]=Song(self.lsongs[song])
        self.csongs=converted_song_data

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
        
        

#Classes
class Date():
    def __init__(self,month=0,day=0,year=0,date_time=None,events={}):
        try: #If you use datetime object
            self.month=date_time.month
            self.day=date_time.day
            self.year=date_time.year
            self.datetime=date_time
        except: #If you don't use datetime
            (self.month,self.day,self.year)=(month,day,year)
            self.datetime=None
        self.events={}
    
    def __str__(self):
        printable=str(self.month)+'/'+str(self.day)+'/'+str(self.year)
        return printable
    
    def __repr__(self):
        printable=str(self.month)+'/'+str(self.day)+'/'+str(self.year)
        return printable

class Song():
#Basic functionality
    def __init__(self,asongdict=defsongdict):
        """
        Make a new song instance, which stores all the data about the song.
        """
        for attribute in defsongdict:
            try:#If attribute was input
                temp_val=asongdict[attribute]
            except: #Else
                temp_val=defsongdict[attribute]
            self.__dict__[attribute]=temp_val
    
    def __str__(self):
        songdict=self.get_song()
        printable=''
        for song in songdict:
            newprint=str(songattrs[song])+': '+str(songdict[song])+'\n'
            printable+=newprint
        return printable
    
    def __repr__(self):
        printable=self.song_name
        return printable
    

#Useful operations
    def get_song(self):
        """
        Get the dictionary of all song attributes.
        """
        the_song_dict={n:self.__dict__[n] for n in songattrs}
        return the_song_dict
    
    def sang_today(self):
        """
        Indicate that you sang a song today.
        """
        today=str(get_now())
        if today!=self.last_sung:
            self.dates_sung=[today]+self.dates_sung
            self.last_sung=today
        self.how_many_times+=1
        self.xp+=1
        self.check_streak()
        self.check_level()
#Checking data
    def demote(self):
        """
        Demoting this song.
        """
        days_past_deadline = self.days_since_last() - leveldict[self.current_level][2] #Get how many days total could be lost
        new_level = self.current_level + 1 #New level
        xp_to_next_level = leveldict[new_level][0] #XP to level up
        
        if self.last_demoted != None: #If has been demoted previously
            today = get_now().datetime
            last_demotion = parse_day(self.last_demoted).datetime
            days_since_demotion = (today - last_demotion).days
            
            days_to_remove = min([days_since_demotion, days_past_deadline])
                
        else:
            days_to_remove = days_past_deadline
        
        for missing_day in range(days_to_remove): #Remove for each missing day
        
            if self.current_level <= self.max_level//2: #Minimize at half of max level
                return None

            xp_loss = xp_to_next_level//4
            xp_loss = xp_loss if xp_loss>=1 else 1
            self.xp -= xp_loss#Remove a quarter of this level's xp
            
            print(CC('R',self.song_name),'has lost xp.')
            self.last_demoted = str(get_now()) #Set last demotion
            
            
            if self.xp < 0: #If the result is less than zero, then demote level
                new_level = self.current_level #New level
                self.current_level-=1 #Remove level
                print(CC('R',self.song_name),'has lost a level.')
                
                xp_to_past_level = leveldict[new_level][0] #XP to reach old level
                self.xp= int( xp_to_past_level*(3/4) ) #Set xp to 3/4 of what it takes to reach next level
                
        
    def check_level(self):
        """
        Check to see if the level needs to be updated.
        """ 
        current_level=self.current_level
        if current_level==20 or self.levelfreeze: #If you're level 10, or level is frozen, then ignore
            return None
        days_since=self.days_since_last()
        new_level=current_level+1
        xp_to_next_level = leveldict[new_level][0]
        
        days_past_deadline = days_since - leveldict[current_level][2]
        
        if days_past_deadline>0 and self.current_level>0: #If too long, demote
            self.demote()
        
        elif self.longest_streak>=leveldict[new_level][1]:
            #If longest streak is sufficiently long
            if self.xp>=xp_to_next_level:
                #If total singing time is enough
                
                print(CC('G','Level up!'), self.song_name, 'is now level',\
                      CC('R',str(new_level))+'.')
                self.current_level=new_level
                self.xp=0
                
        if self.current_level>self.max_level:
            self.max_level = self.current_level
    
    def check_streak(self):
        """
        Check to see if the current streak needs to be updated. Will also
        update highest streak.
        """
        yesterday=str(get_yesterday())
        
        self.current_streak=0
        days_ago = 1
        dates_sung_ago = 1
        if self.last_sung==yesterday:
            days_ago = 0
        while True:
            days_ago-=1
            dates_sung_ago -=1
            desired_date=get_n_day(get_now(),days_ago)
            try:
                next_date=self.dates_sung[-dates_sung_ago]
            except:
                break
            if str(desired_date)!=str(next_date):
                break
            self.current_streak+=1
        if self.current_streak>self.longest_streak:
            self.longest_streak=self.current_streak
#Listing        
    def list_item(self,xp_show=False):
        """
        Compactly print this song's most important parameters.
        """
        days_since=self.days_since_last()
        
        #Get data
        sn=self.song_name 
        sa=self.artist 
        sl=str(self.last_sung)
        slvl=": L."+str(self.current_level)
        ss='S:'+str(self.current_streak)
        
        #If long enough, don't edit; else, add however many chars are missing
        short_version = lambda v, length: v if (len(v) == length) else (v + ' '*(length-len(v))) 
        
        #Modify data for use by editing length
        short_song = (sn[:13] + '..') if len(sn) > 13 else sn+' '*(15-len(sn))
        short_artist= (sa[:13] + '..') if len(sa) > 13 else sa+' '*(15-len(sa))
        short_last = 'Last: '+ short_version(sl, 10)
        short_level = short_version(slvl, 6)
        short_streak = short_version(ss, 4)
        
        if xp_show: #XP show
            xos= str(self.xp)+'/'+str(leveldict[self.current_level+1][0])
            xp_or_streak = xos if len(xos)==5 else ' '*(5-len(xos)) + xos 
            
        else: #Total singing times
            xos= 'x' + str(self.how_many_times)
            xp_or_streak = xos if len(xos)==3 else ' '*(3-len(xos)) + xos
            
        vertical_bar = CC('R', ' | ')
            
        
        print( short_song + short_level+  (vertical_bar) + short_artist + (vertical_bar)\
              
              +short_streak + ( vertical_bar ) + xp_or_streak + ( vertical_bar )+\
              
              short_last + ( vertical_bar ) +'Days:', days_since)
        
        
#Edit song
    def temp_mod(self):
        """
        Prepare to modify an attribute of this song.
        """
        print("Which attribute do you want to edit?")
        for place in range(len(songinverse)):
            print(place,': ',songinverse[place][0])
        try:
            choice=int(input(''))
            songinverse[choice]
        except:
            print('Not a valid choice. Must choose by integers given.')
            return None
        attribute=songinverse[choice][1]
        visible_attribute=songinverse[choice][0]
        print(f"You've chosen {visible_attribute}.")
        print("What do you want to set this value to?")
        val=input('')
        if attribute in {'current_streak','current_level','longest_streak'\
                           'max_level','levelfreeze','how_many_times'}:
            val=int(val)
        if attribute=='last_sung':
            val=val.replace(' ','')
        if attribute=='dates_sung':
            val=parse_dates_sung(val)
        print('Saved.')
        return((self.song_name, 'Modify', attribute, val))
        
    def modify(self,attr,val):
        """
        Modify an attribute of this song.
        """
        if not attr in self.__dict__:
            print("Attribute doesn't exist")
            return None
        self.__dict__[attr]=val
        
    def days_since_last(self):
        """
        Determine days since last played a song.
        """
        try:
            datedelta=get_now().datetime-parse_day(self.last_sung).datetime
            days_since=datedelta.days
        except:
            days_since=0
        return days_since

def parse_dates_sung(string):
    """
    Convert list/set of dates into list of date strings.
    """
    for char in ' {}[]':
        string=string.replace(char,'')
    string_list=string.split(',')
    return string_list

#Datetime operations
def get_datetime(Date_Instance):
    """
    Checks if Date_Instance is Date or datetime. If it's Date, 
    it returns datetime. Else it does nothing.
    """
    if type(Date_Instance)==type(get_now()): #If type is Date
        return Date_Instance.datetime
    elif type(Date_Instance)==type(get_now().datetime): #If type is datetime
        return Date_Instance
    elif type(Date_Instance)==str:
        return parse_day(Date_Instance)
                
def get_now():
    """
    Returns: DATE object.
    Get the current date.
    """
    time_tuple=datetime.now()
    time_now=Date(date_time=time_tuple)
    return time_now   

def calc_n_day(the_date,n):
    """
    Returns: DATETTIME object.
    Calculate the day that is n days after the_date.
    """
    the_datetime=get_datetime(the_date)
    time_tuple=the_datetime+timedelta(days=n)
    return time_tuple

def get_n_day(the_date,n):
    """
    Returns: DATE object.
    Get the day that is n days after the_date.
    """
    time_tuple=calc_n_day(the_date,n)
    time_n=Date(date_time=time_tuple)
    return time_n

def get_days(the_date,m):
    """
    Returns: LIST object containing DATE objects.
    Get a list of m days from a date to m-1 days later.
    """
    the_datetime=get_datetime(the_date)
    if m>0:
        return [get_n_day(the_datetime,n) for n in range(m)]
    if m<0:
        return [get_n_day(the_datetime,-n) for n in range(-m)]

def get_yesterday():
    """
    Returns: DATE object.
    Get yesterday's date.
    """
    time_tuple=get_n_day(get_now(),-1)
    time_last=Date(date_time=time_tuple)
    return time_last

def parse_day(string):
    """
    Convert string into Date object.
    """
    for char in ' {}[]':
        string=string.replace(char,'')
    try:
        (M,D,Y)=string.split('/')
        gettime=datetime(year=int(Y),month=int(M),day=int(D))
        return Date(date_time=gettime)
    except:
        return None
        
def string_day(Date):
    """
    Convert Date into string object.
    """
    try:
        out="%d/%d/%d" % (Date.month,Date.day,Date.year)
        return out
    except:
        print('Invalid object type.')

#UI
def enter_to_continue():
    """
    Used to create space between inputs.
    """
    inputter=C('S')+"Press ENTER to continue..."+C('N')
    dummy=input(inputter)
    dummy=dummy
    
def did_you_mean(var):
    """
    Asks if the user is certain.
    """
    out=input(f" Did you mean {var}? ")
    if out.lower()=='cancel':
        return None
    if out.lower() in confirmdict:
        out2=input("Are you sure? ")
    else:
        return False
    return out2.lower() in confirmdict

def color(letter):
    color_num=colordict[letter]
    return f"\x1b[{color_num};1;m"
    
def plural(n):
    """
    If n is more than one, give an s.
    """
    if n>1:
        return 's'
    else:
        return ''
    
def replace(string,section, replacement):
    """
    Replace one section of a string with another.
    """
    found_spot=string.find(section)
    dist=len(section)
    newstring=string[:found_spot]+replacement+string[found_spot+dist:]
    return newstring

def highlight(string,section,color):
    color_num=colordict[color]
    replacement=f"\x1b[{color_num};1;m"+section+f"\x1b[0;1;m"
    return replace(string,section, replacement)

def accentuate(string):
    accentors=[n for n in findall("'",string)]
    accented=highlight(string,string[(accentors[0]+1):accentors[1]],'R')
    return accented

def print_accent(string):
    print(accentuate(string))
    
def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)
        
def color_cap(color_letter, string):
    return C(color_letter)+string+C('N')
    
        
def edit_check():
    """
    Checks to see if pending edits remain. Returns whether or not to end the program.
    """
    if n_edits>0:
        print("You still have pending edits. Do you want to save them?")
        choice=input("")
        if choice in confirmdict:
             if UI.confirm():
                 return True
             else:
                 return False
        else:
            print("Choices not confirmed. Do you still want to proceed?")
            choice2=input("")
            if not choice2 in confirmdict:
                return False
        return True
    else:
        return True
    
    
C=color #Aliasing to make life easier
CC=color_cap
P=plural
HL=highlight
PA=print_accent

################################################
    
""" SONG UI """

UI=Records()
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
            
#Level freeze
#    elif statement in {'freeze','stop','pause'}:
#        if secondline == '':
#            print("Which song do you want to toggle freeze on?")
#            new_statement=UI.interpret(secondline)
#        if new_statement == None:
#            pass
#        else:
#            UI.freeze_level(secondline)
#            print("Added to the edit list.")
        
##Add UI.freeze_level
##Add song.toggle_freeze
            
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
        
    #Changes: could make it so you can say "remove song" in one line!
