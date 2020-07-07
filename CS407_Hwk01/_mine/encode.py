# So, yeah, I snagged your code and tried to reverse-engineer it... (:
#     plus googled & looked at a few other examples in Java & Python...
#  	 yours seemed the most straight-forward though...
#           (some seemed kinda weird in some ways)
#     and have been working on learning python w/online tutorials  too.
#______________________________________________________________________

def encode(input_string):
    #return input_string
    # so this goes up here?? -- only for early testing...
    # end program is only supposed to return the original string
    # if it can't be shortened... 
    #
    # so, what... it does this, unless conditions below are met?
    # ... played around with it -- NO.  (:
    #
    # when testing in console, with this left in here like this,
    # i was *only* getting the original input_string back,
    # regardless of input... 
    #
    # which yeah, is what i thought it would do and makes sense...
    #__________________________________________________________________

    # set our various variable...
    encoded_string = ""     # variable to hold encoded string
                                # initialize to empty string
    #
    current_character = None    # variable to hold current character
                                    # we're examining/comparing
                    # in python, 'None' == 'null'... initialize to null
    #
    current_count = 0   # accumulator variable to count characters
    #__________________________________________________________________

    for c in input_string:
    # so this syntax threw me for a loop momentarily... (:
    # looked up for-loops in python @W3Schools -- think i get it now...
    #   we're using 'c' to look at each character 
    #   in the passed-in 'input_string'
    #
        if c == current_character:  # but current_character is null??
            current_count +=1

        else:
            if current_character:
                encoded_string += current_character + str(current_count)
                # add the current_character to encoded_string,
                # along with the current_count (cast to str), which
                # increments when it finds repeating characters

            current_character = c   # reset current_character to
                                    # whatever 'c' is currently at...

            current_count = 1   # resets current_count to 1,
                            # increments w/repeating characters found
    #__________________________________________________________________

    if current_character:
        encoded_string += current_character + str(current_count)
    return encoded_string

    #if input_string.len < encoded_string.len:
    #return input_string
    # when testing that to console, i get:
    #'TabError: inconsistent use of tabs and spaces in indentation'
    #
    # some versions i perused had like:
    # "if input_string.len <=3: return input_string"
    # (and had this line up-top after def encode() line)
    # b/c they figured 3 was the tipping point... 
    #   but i say they're not quite right... 
    #
    # b/c if input_string is "abc", then yeah, 
    # making it "a1b1c1" would be longer... 
    # if input_string is "abb", then still, "a1b2" is longer.
    # BUT, if input_string is "aaa", then "a3" would be shorter!
    # 
    # so i like using if-statement to see which is longer... 
    #   that seems to make more sense/be more correct... 
    #
    # now if I could only get it to work... (:
    # 
    # should the if-statement re: length,
    #   be an if-else-statement up before 'return encoded_string'?
    #   with 'return encoded_string' being the else, of course?
    # 
    # i promise i will come back to this and figure it out... 
    # i just ran into so many other difficulties & challenges
    # that i ran out of time and still have other work to get done (:
    #
    # right now i just don't want to screw existing stuff up
    # and have no more time... (:


#______________________________________________________________________
# added this part because i like to see stuff printed to console
# to prove to me it's doing what it's supposed to be doing... (: 

def main():
    print(encode("a"))
    print(encode("abc"))
    print(encode("aaabbbccc"))
    print(encode("aaabbbaaa"))
    print(encode("aaabbbaaacccaaa"))
    # some versions added up all the 'a's, for instance
    # so, for example, this would've been a6b3... 
    #
    # which is a neat trick... but doesn't seem right -- 
    # doesn't or shouldn't order matter???
    print(encode("aaabccccc"))
    print(encode("aaabbbbbbccccccccc"))
    print(encode("aaabbbbbbcccccccccdddddddddddd"))
    print(encode("possum"))
    
if __name__ == "__main__":
	main()

