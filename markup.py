

"""
This file contains methods for marking up text to make it more appealing with different colors and other modifications.

"""


#Gives the numbers associated with different colors.
colordict={'S':30, 'R':31,'G':32,'Y':33, 'B':34,'P':35,'C':36,'W':37,'N':0}
           #Silver, Red,   Green, Yellow, Blue,  Pink,  Cyan,  White, No Color

def color(letter):
    """Change the color of the successive string when printed."""
    color_num=colordict[letter]
    return f"\x1b[{color_num};1;m"

def color_cap(color_letter, string):
    """Change the color of this string, but cap it so that added characters will not be colored."""
    return C(color_letter)+string+C('N')

C = color
CC = color_cap



"""Ensure that a string reaches a desired length."""
fill_empty_space = lambda string, desired_length: string + ' ' * (desired_length - len(string) )

def limit_length(string, desired_length):
    """Ensure that a string is no longer than a desired length."""
    if desired_length < 2:
        raise ValueError( "You cannot limit a string to such a short length!")
    
    if len(string)<=desired_length: #If not too long, you're done
        return string
    
    starter = string[ : desired_length - 2] #Remove ellipse
    
    return starter + '..' #Add an ellipsis at the end
        

def exact_length(string, desired_length):
    """Ensure that a string is exactly the desired length."""
    shortened = limit_length(string, desired_length) #Remove any extra characters
    lengthened = fill_empty_space(shortened, desired_length) #Fill in any missing characters
    
    return lengthened #String is cut to the correct length

def remove_chars(string, removers):
    """
    Takes a string and removes all of the characters in removers.
    
    string: string we would like to make edits to.
    removers: iterable containing characters, to be removed from string.
    """
    
    new_string = string #String to edit
    
    for char in removers: #Iterate through characters
        
        new_string = string.replace( char, '' ) #Remove chars one by one

    return new_string        
        




####################################################################################
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