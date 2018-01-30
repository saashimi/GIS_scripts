import re

search_transit_line = '94XO'
search_stop_init = '57738'
search_stop_end = '80359'
insert_string = 'dwt=*.01  ttf=11'

### Does not work if dwt, ttf info on same line as end station


def dwt_ttf_search_and_replace(ttf_in, dwt_in, line_in):
    search_ttf = re.search('ttf=\S*', line_in)
    search_dwt = re.search('ttf=\S*', line_in)
    print line_in
    if search_ttf:
        line_in = line_in.replace(search_ttf.group(), '')
    if search_dwt:
        line_in = line_in.replace(search_dwt.group(), '')
    return line_in


always_print=False # Initial flag state
inside_stop=False
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
                    inside_stop=True

                # Revert to previous dwt, ttf after desired stop.
                if always_print and search_stop_end in line:
                    if ttf and dwt:
                        revert_string = dwt + '  ' + ttf
                        dest.write(line.replace(search_stop_end, search_stop_end + '\n   ' + revert_string))
                        inside_stop=False

                # End of transit line condition, terminate write to file.
                elif "lay=0" in line:
                    dest.write(line)
                    always_print=False

                # Standard Write line condition.
                else: 
                    if inside_stop:
                        parsed_line = dwt_ttf_search_and_replace(ttf, dwt, line)
                        dest.write(parsed_line)
                        always_print=True

                    else:
                        dest.write(line)
                        always_print=True

src.close()
dest.close()