from datetime import datetime, timedelta

#Local imports
import dictionaries as D
import date_compute as Date

from markup import CC, exact_length, remove_chars

#Common objects
def_song_dict = D.default_song_dict #Dictionary for song data.

class Editable():
    """An abstract object that allows you to give it any initial attributes using dictionaries."""

    def __init__(self, default_dict, real_dict):
        """
        default_dict: dictionary, giving the default values for each variable.
        real_dict: dictionary, giving the real values for each variable, if it differs from the default_dict values.
        
        Creates an instance with the attributes listed by default_dict. Values are given by real_dict unless they don't exist
        in real_dict, in which case they come from default_dict.
        """
        
        for attribute in default_dict: #Get all desired attributes
            
            if attribute in real_dict: #If attribute has a unique value
                value = real_dict[attribute] #Get value
            
            else: #If attribute has a generic value given by default_dict
                
                value = default_dict[attribute] #Get value

            self.__dict__ [attribute] = value #Set attribute value
            
    def get_attrs(self):
        """
        Returns: a dictionary containing the default attributes of the object as keys and the current values as values.
            {"attribute": value}
        """
        
        return self.__dict__


class Song(Editable):
    """A class that stores data and methods for one song."""

#Basic functionality
    def __init__(self, real_dict):
        super().__init__(def_song_dict, real_dict) #Use Editable's useful properties
        
    def __str__(self):
        """When a string is requested, the song name will be displayed."""
        name = self.song_name
        artist = self.artist
        return name + ' by ' + artist
    
    def __repr__(self):
        """When the song needs to be represented, the song name with be displayed."""
        return self.__str__()
        
    def disp(self):
        """
        Allows for a simple way to display all song information.
        
        Returns: String containing line breaks between each pair of keys and values in a user-friendly form.
        """
        output = '' #Text to be printed
        
        for attribute in def_song_dict: #Print every attribute
            
            value = self.__dict__[attribute]  #Get value
            
            new_text = str(attribute) + ': ' + str(value) + '\n' #Convert to full string (with line break '\n')
            output+=new_text #Add it to what you display
            
        return output
    
#Update
    def sang_today(self):
        """
        Indicate that you sang a song today.
        
        Edited Attributes: self.last_sung, self.dates_sung, self.how_many_times, self.xp.
        
        Calls Class Functions: self.check_streak, self.check_level
        """
        today = Date.get_today() #Get the date as string
        
        if today!=self.last_sung: #If it's a new date from last sung, then add it to the data.
            self.dates_sung=[today]+self.dates_sung
            self.last_sung=today
            
        self.how_many_times+=1 #Increase times sung
        self.xp+=1 #Increase xp
        
        #Check streaks and level after this event
        self.check_streak()
        self.check_level()
        
#Check data
    def check_level(self):
        """
        Check to see if the level needs to be updated, either by demotion or promotion.
        
        Calls Class Functions: self.check_demotion, self.check_promotion
        """ 
        current_level=self.current_level
        
        if current_level==20 or self.levelfreeze: #If you're level 20, or level is frozen, then make no edits
            return None
        
        #Check whether to demote or promote
        self.check_demotion()
        self.check_promotion()
        
    def check_demotion(self):
        """
        Check whether to demote this song based on days since last sung.
        
        Calls Class Functions: self.demote, self.get_days_since_last
        """
        
        days_since=self.get_days_since_last() #Get days since last sung
        days_past_deadline = days_since - D.leveldict[self.current_level]["days_to_lose"] #Get days to start losing xp
        
        #Conditions
        song_past_deadline = days_past_deadline>0
        song_above_level_zero = self.current_level>0
        
        if song_past_deadline and song_above_level_zero: #If too long, demote 
            self.demote()
            
    
    def check_promotion(self):
        """
        Check whether to promote this song to next level based on your current level and xp. 
        
        Edited Attributes: self.xp, self.current_level
        """
        
        new_level=self.current_level+1 #Get new level
        xp_to_next_level = D.leveldict[ new_level ]["req_xp"] #Get xp to reach next level
            
        #Conditions
        streak_is_long_enough = self.longest_streak>=D.leveldict[new_level]["req_streak"]
        xp_is_high_enough = self.xp>=xp_to_next_level
    
        if streak_is_long_enough and xp_is_high_enough:
            #If longest streak is sufficiently long, and xp is high enough, upgrade
            
            song = self.song_name
            level = CC('R',str(new_level))
                
            print(CC('G','Level up!'),\
                  song, 'is now level', level+'.')
            
            #Change values
            self.current_level=new_level
            self.xp=0
            
            
    def check_streak(self):
        """
        Check to see if the current streak needs to be updated. 
        Will also update highest streak.
        Streak is broken if it has been more than one day since you've sung.
        
        Edited Attributes: self.current_streak, self.longest_streak
        """
        
        if self.last_sung == None: #If never sung
            self.current_streak = 0
        
        yesterday = Date.n_days_ago(1) 
        last_sung = Date.string_to_date(self.last_sung) #Last time song was sung
        
        streak_broken = ( yesterday > last_sung) #Yesterday is more recent than last sung, too long
        
        if streak_broken:
            self.current_streak = 0 #If the streak is broken, reset
            return None
        
        last_date = Date.n_days_ago(0)#Start from today
        streak_length = 0 #Start fresh
        
        for day in self.dates_sung:
            date = Date.string_to_day(day)
            
            desired_dates = {last_date, last_date - timedelta(days = 1) } #The expected or the day before are both acceptable
            
            if date in desired_dates: #Streak is unbroken
                streak_length += 1
                last_date = date - timedelta(days = 1)#Go back in time
                
            else: #Streak ends
                break
            
        self.current_streak = streak_length #Set streak
        
        if self.current_streak > self.longest_streak: #Update longest streak if necessary
            self.longest_streak=self.current_streak
            
            
#Apply changes with no user input
    def demote(self):
        """
        Demoting this song to remove either XP or levels. Only removes levels if XP has reached below zero.
        Previously penalized days will not be penalized repeatedly with XP losses.
        Level will not drop below zero or half of the maximum level achieved.
        
        Edited Attributes: self.xp, self.current_level, self.last_demoted
        """
        level = self.current_level
        days_allowed = D.leveldict[level]["days_to_lose"] #Days you can skip with no penalty
        
        days_past_deadline = self.get_days_since_last() - days_allowed #Total days
        
        
        def get_penalty_days():
            """Get how many days you should penalize the late player for."""
        
            if self.last_demoted != None: #If it has been demoted previously, check how recently
                today = Date.get_today()
                last_demotion = Date.string_to_date(self.last_demoted)
                
                days_since_demotion = (today - last_demotion).days #Compare today to last demotion
                
                if days_since_demotion<days_past_deadline: #If it's been demoted recently, don't penalize days already demoted
                    how_many_days_late = days_since_demotion
                else: #Otherwise, it's an old demotion, and just use how late you are
                    how_many_days_late = days_past_deadline
                    
            else: #If never demoted, then you don't need to worry about previous demotion days
                how_many_days_late = days_past_deadline
                
            return how_many_days_late #Number of days to penalize for being late
            
        def apply_penalty():
            """Apply penalty days to remove xp."""
            for penalty_day in range(get_penalty_days()): #Iterate over penalty days
                
                if self.current_level <= self.max_level//2: #If your level is low, stop penalizing
                    return None
                
                xp_to_next_level = D.leveldict[self.current_level+1]["req_xp"] #XP to level up
                
                xp_loss = xp_to_next_level//4 #Get xp loss
                xp_loss = xp_loss if xp_loss>=1 else 1 #Make sure xp_loss is at least 1
                self.xp -= xp_loss#Remove a quarter of this level's xp
                
                song = CC('R',self.song_name)
                print(song, 'has lost xp.')
                
                self.last_demoted = Date.get_today() #Set last demotion
                
                if self.xp < 0: #Remove a level
                    self.current_level-=1
                    next_level = self.current_level + 1
                    
                    print(song, 'has lost a level.')
                    
                    xp_to_next_level = D.leveldict[next_level]["req_xp"] #XP to reach old level
                    self.xp= round( xp_to_next_level*(3/4) ) #Set xp to 3/4 of what it takes to reach next level
                
        apply_penalty()
        
#Display data
        
        def list_item(self,xp_show=False):
            """
            Compactly print this song's most important parameters.
            
            xp_show: If xp_show is set to False, then the total number of times this song has been played will be displayed.
                     If xp_show is set to True, then the "current_xp/xp_to_next_level" will be displayed.
                     
            Calls Class Functions: self.get_days_since_last
            """
            days_since_last_sung = self.get_days_since_last()
            
            #Convert all strings to the correct length
            song      = exact_length( self.song_name,          15 )
            level     = exact_length( str(self.current_level),  2 )
            artist    = exact_length( self.artist,             15 )
            streak    = exact_length( str(self.current_streak), 2 )
            last_sung = exact_length( self.last_sung,          10 )
            
            
            #Check whether to display xp or 
            
            if xp_show: #Display XP
                xp = str(self.xp) #Get xp
                xp_to_next = D.leveldict[ self.current_level + 1] ["req_xp"] #Get xp goal
                
                xp_ratio = xp + '/' + xp_to_next #Combine as xp/goal
                xp_or_total = exact_length( xp_ratio, 5) #Correct length
            
            else: #Display total
                total =  'x' + str( self.how_many_times ) #Get total times sung
                xp_or_total = exact_length( total, 3 )
                
            #Final display
            
            V = CC('R', ' | ') #Draw red vertical bar
            
            print( song +              ": L." + level +       ( V ) + artist + ( V )+ \
              
                   "S:"+streak +        ( V )  + xp_or_total + ( V ) + \
              
                   'Last: '+last_sung+  ( V )  + 'Days:', days_since_last_sung)
        
#View data
        
        def get_days_since_last(self):
            
            if self.last_sung == None: #If never sung
                return 'N/A'
            
            #Get dates to compare
            today = Date.string_to_date(      Date.get_today()  ) 
            last_sung = Date.string_to_date(  self.last_sung  )
            
            if today == last_sung: #Zero days since sung
                return 0
            
            time_difference = today - last_sung #Get the timedelta if not same delta
            
            return time_difference.days #Get *days*
                        
                    
            #####################
                    
            
                    
                    
                    
                    
                
