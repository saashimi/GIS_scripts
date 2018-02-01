import re

search_transit_line = '12TPa'
search_stop_init = '57739'
search_stop_end = '80359'
insert_string = 'dwt=*.01  ttf=11'

### Does not work if dwt, ttf info on same line as end station


def dwt_ttf_search_and_replace(ttf_in, dwt_in, line_in):
    return line_in

def line_as_list(line_in):  
    return filter(None, line_in.rstrip().split(' '))

def unpack_list(list_in):
    for item in list_in:
        dest.write(item)

always_write=False # Initial flag state
inside_stop=False
header=False
parse_following_lines=False
with open('d221.2015_RTP18_pm2', 'r') as src:
    with open('2test_out', 'w') as dest:
        for line in src:
            if "a'{0}".format(search_transit_line) in line: 
                dest.write(line)
                parse_following_lines=True
                continue
            
            if search_stop_end in line:
                line_list = line_as_list(line)
                parse_following_lines=False
            
            if parse_following_lines:
                line_list = line_as_list(line)
                unpack_list(line_list)


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