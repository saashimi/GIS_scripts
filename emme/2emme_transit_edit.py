##################################
# TODO: Develop payload system to systematize bulk changes
search_transit_line = '12TPa'
search_stop_init = '57738' # ttf, dwt defined BEFORE this stop
search_stop_end = '80359'  # previous ttf, dwt defined AFTER this stop
new_dwt = 'dwt=*.01' 
new_ttf = 'ttf=11'
##################################

def line_as_list(line_in):  
    return filter(None, line_in.rstrip().split(' '))

def line_to_list_generator(list_in):
    # Breaks list of network stops into sublists of len 7 for easy writefile
    # formatting.  
    for i in xrange(0, len(list_in), 7):
        yield list_in[i:i + 7]    

def sublist_writer(list_in):
    str = ''
    last_line=False
    for item in list_in:
        if item.startswith(('dwt', 'ttf')):
            column = ' {:^9}'.format(item) # note leading space
        else:
            if item == 'lay=0':
                last_line=True
            column = '{:>9} '.format(item) # note trailing space
        str = str + column
    if not last_line:
        # newlines for every line except last one
        str = str + '\n' 
    return str

def network_parser(list_in):
    # main dwt, ttf parser
    # make list edits by slicing into the main network stop list.
    # TODO: check edge case if multiple instances of init and end stops
    current_dwt = ''
    current_ttf = ''
    edit_network = []
    init_index = list_in.index(search_stop_init)
    end_index = list_in.index(search_stop_end) + 1
    for item in list_in:
        if 'dwt' in item:
            current_dwt = item
        if 'ttf' in item:
            current_ttf = item
        if search_stop_init == item:
            edit_network = list_in[init_index:end_index]
    return edit_network, current_dwt, current_ttf, init_index, end_index

def network_editor(orig_network, network_slice, dwt_in, ttf_in, index_start, index_end):
    # create the edited network as a separate list
    new_network = []
    new_network.extend((new_dwt, new_ttf))
    for item in network_slice:
        if not item.startswith(('dwt', 'ttf')):
            new_network.append(item)
    new_network.extend((dwt_in, ttf_in))

    # splice the edited network into the original_network 
    del orig_network[index_start:index_end]
    counter = 0
    for item in new_network:
        orig_network.insert(index_start + counter, item)
        counter += 1
    
    # delete existing dwt, ttf right before edited stop
    if orig_network[index_start - 2].startswith(('dwt','ttf')):
        del orig_network[index_start - 2]

    return orig_network

def main():
    # Initial flag and list states
    parse_following_lines=False
    temp_list = []
    with open('d221.2015_RTP18_pm2', 'r') as src:
        with open('2test_out', 'w') as dest:
            for line in src:
                # Writes header row and breaks loop if transit line of interest
                if "a'{0}".format(search_transit_line) in line: 
                    dest.write(line)
                    parse_following_lines=True
                    continue

                if parse_following_lines:
                    # Converts raw text lines into list items
                    line_list = line_as_list(line)
                    for item in line_list:
                        temp_list.append(item)
               
                if parse_following_lines and 'lay=0' in line:            
                    # Begin parsing accumulated list items
                    parsed_network, dwt, ttf, index_i, index_e = network_parser(temp_list)
                    edited_network = network_editor(temp_list, parsed_network, dwt, ttf, index_i, index_e)
                    parse_following_lines=False
                    generated = line_to_list_generator(edited_network)
                    for sublist in generated:
                        write_str = sublist_writer(sublist)
                        dest.write(write_str)

                    temp_list = []

    src.close()
    dest.close()

if __name__ == '__main__':
    main()