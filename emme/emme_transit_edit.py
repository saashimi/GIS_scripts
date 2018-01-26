search_transit_line = '12TPa'
search_stop_init = '57739'
insert_string = 'dwt=*.01  ttf=11'

always_print = False # Initial flag state
with open('d221.2015_RTP18_pm2', 'r') as src:
    with open('test_out', 'w') as dest:
        for line in src:
            if always_print or "a'{0}".format(search_transit_line) in line: 
                if search_stop_init in line:
                    dest.write(line.replace(search_stop_init, search_stop_init + '\n   ' + insert_string + '\n '))
                else: 
                    dest.write(line)
                always_print=True

                if "lay=0" in line:
                    always_print=False
src.close()
dest.close()