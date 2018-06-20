##############################################################
## 
## Get all auto volumes from a peak spread bank
## It could have the option to gather other link attributes by creating a dic
## This script uses the Emmy_functions methods and Emmys class method to fetch scenarios and links
## Daniel Jimenez, Metro, Jan 19, 2016 
## Updated by Kevin Saavedra, Metro, Jun 2018
##############################################################

from emmy_24 import Emmys
from Emmy_Functions import Emmy_Functions
from collections import defaultdict
import csv

#Function that creates the time header
def times():
    times = []
    for i in range(24):
        times.append("AutoVol {}:00 - {}:00".format(i, i+1))
    return times    

#Function that get the values from each link id by the hour using the range loop.
#It returns a list with all the values by hour that gets added to the writting function
#This will guarntee that the values order will start at 00 and end at 23    
def volumes(values):
    volumes_values = []
    for i in range(0,24):
        volumes_values.append(int(round(values[i])))
    return volumes_values   
    

def pick_attribute():
    print "Select integer of the desired attribuite to generate:"
    print "1 - volume (volau)"
    print "2 - vehicle volumes (@vehvol)"
    try:
        return int(raw_input().strip())
    except ValueError:
        print "Please enter the integer of the desired attribute to generate "
        return int(raw_input().strip())        
                        
def link_attribute(link, att):
    if att == 1: return link.auto_volume
    else: return link["@vehvol"]

def main():
    attribute = pick_attribute()
    bank = Emmy_Functions()
    links,capacity = get_data(bank,attribute)
    write_file(links,capacity, attribute)

def get_data(bank, attribute = 1):
    auto_links = defaultdict(dict)
    capacity = {}
    for s in Emmys.fetch_scenario(bank.bank):
        for link in Emmys.fetch_links(bank.bank, s):
            #Remove centroids
#            if not any([link.i_node.is_centroid,link.j_node.is_centroid]):
                # auto_links key is [linkid][hour] = link value depending on field
                auto_links[link.id][int(s.id[2:])] = link_attribute(link, attribute)
                #Dict that holds capacity for each link
                if not capacity.has_key(link.id):
                    capacity[link.id] = link.data3
    return auto_links,capacity 

def write_file(links,capacity, attribute):                     
    att_name = {1:"volumes.csv", 2:"vehicle_volumes.csv"}                
    with open(att_name[attribute], "wb") as f:
        header = ["OBJECTID", "UNIQUEID","From","To","Capacity"] + times()
        csv_writer = csv.writer(f)
        csv_writer.writerow(header) 
        for k,v in links.iteritems():
            unique = k
            fr, to = k.split("-")
            #Check volumes commments for clarification
            csv_writer.writerow([unique,fr,to,capacity[k]] + volumes(v))

if __name__ == "__main__":
    main()          
        
        


