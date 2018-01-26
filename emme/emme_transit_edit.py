search_transit_line = '12TPa'

always_print = False # Initial flag state
with open('d221.2015_RTP18_pm2', 'r') as src:
    with open('test_out', 'w') as dest:
        for line in src:
            if always_print or "a'{0}".format(search_transit_line) in line: 
                dest.write(line)
                always_print=True
                if "lay=0" in line:
                    always_print=False
src.close()
dest.close()