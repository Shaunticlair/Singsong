from datetime import datetime, timedelta

def date_to_string(date):
    """
    Convert datetime object to string.
    
    date: datetime object.
    Returns: string of the form month/day/year
    """
    month, day, year = str(date.month), str(date.day), str(date.year) #Convert to string
    return month + '/' + day + '/' + year #Combine


def string_to_date(string):
    """
    Convert string to datettime object.
    
    string: string of the form month/day/year
    returns: datetime object.
    """
    for char in ' {}[]': #Clean out any extra characters
        string=string.replace(char,'')
        
    try: 
        (M,D,Y)=string.split('/') #Split along / dividers
        gettime=datetime(year=int(Y),month=int(M),day=int(D)) #Convert to datetime 
        return gettime 
    
    except: #If something went wrong, you input a bad data format.
        return None
    
def get_today():
    """
    Get the string associated with today.
    
    returns: string of the form month/day/year
    """
    today = datetime.today().date() #Get in datetime form
    return date_to_string(today) #Convert to string
    
def n_days_ago(n):
    """
    Get the date associated with n days ago.
    
    returns: datetime object from n days before today.
    """
    today = datetime.today().date()
    return today - timedelta(days=n)
    
    
    
    
    
    
#############################################
        
    
def parse_dates_sung(string):
    """
    Convert list/set of dates into list of date strings.
    """
    for char in ' {}[]':
        string=string.replace(char,'')
    string_list=string.split(',')
    return string_list


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
