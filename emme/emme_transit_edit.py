import re

search_transit_line = '94XO'
search_stop_init = '80402'
search_stop_end = '80359'
insert_string = 'dwt=*.01  ttf=11'

always_print = False # Initial flag state
with open('d221.2015_RTP18_pm2', 'r') as src:
    with open('test_out', 'w') as dest:
        for line in src:
            # Search and retain ttf, dwt values in memory
            current_ttf = re.search('ttf=\S*', line)
            current_dwt = re.search('dwt=\S*', line)
            if current_ttf:
                ttf = current_ttf.group()
            if current_dwt:
                dwt = current_dwt.group()

            if always_print or "a'{0}".format(search_transit_line) in line: 
                # Match initial transit stop location of speed change.
                # Write new dwt, ttf values.
                if search_stop_init in line:
                    dest.write(line.replace(search_stop_init, search_stop_init + '\n   ' + insert_string + '\n '))

                # Revert to previous dwt, ttf after desired stop.
                elif always_print and search_stop_end in line:
                    if ttf and dwt:
                        revert_string = dwt + '  ' + ttf
                        dest.write(line.replace(search_stop_end, search_stop_end + '\n   ' + revert_string))
                
                # End of transit line condition, terminate write to file.
                elif "lay=0" in line:
                    dest.write(line)
                    always_print=False

                # Standard Write line condition.
                else: 
                    dest.write(line)
                    always_print=True

src.close()
dest.close()