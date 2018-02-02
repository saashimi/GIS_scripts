import re

search_transit_line = '12TPa'
search_stop_init = '57739'
search_stop_end = '80359'
insert_string = 'dwt=*.01  ttf=11'


def line_as_list(line_in):  
    return filter(None, line_in.rstrip().split(' '))

def line_to_list_generator(list_in):
    # generates sublists of len 7
    for i in xrange(0, len(list_in), 7):
        yield list_in[i:i + 7]    

def sublist_writer(list_in):
    #TODO: WATCH FOR EDGE CASES > 9 CHAR in length
    str = ''
    for item in list_in:
        column = '{:>9} '.format(item)
        str = str + column
    str = str + '\n'
    dest.write(str)


# Initial flag states
parse_following_lines=False
always_write=False 
inside_stop=False
temp_list = []
with open('d221.2015_RTP18_pm2', 'r') as src:
    with open('2test_out', 'w') as dest:
        for line in src:
            # Write header row and break loop if transit line of interest
            if "a'{0}".format(search_transit_line) in line: 
                dest.write(line)
                parse_following_lines=True
                continue

            if parse_following_lines:
                line_list = line_as_list(line)
                for item in line_list:
                    temp_list.append(item)
           
            if parse_following_lines and 'lay=0' in line:            
                parse_following_lines=False
                generated = line_to_list_generator(temp_list)
                for sublist in generated:
                    sublist_writer(sublist)
                temp_list = []



                #for subitem in item:
                #    dest.write(subitem + ' ')     
            
            """
            if search_stop_end in line:
                line_list = line_as_list(line)
                parse_following_lines=False
            

            """
            
            """
            else:
                dest.write(line)
            """

            """
            # In final stage, we need to write all lines.
            else:
                dest.write(line)
                always_print=True
            """

            """
            else: 
                if inside_stop:
                    parsed_line = dwt_ttf_search_and_replace(ttf, dwt, line)
                    dest.write(parsed_line)
                    always_print=True

                else:
                    dest.write(line)
                    always_print=True 
            """

src.close()
dest.close()
