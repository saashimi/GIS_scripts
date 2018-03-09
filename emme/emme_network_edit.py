"""
Allows batch changes of ttf, dwt values between two transit network stops
to emme d221 files.

Usage:
>>> python emme_network_edit.py <d221 file to edit> <network edit file>

Requires a network edit file in csv format with the following headers:
edit_transit_network, init_stop_ID, end_stop_ID, new_dwt, new_ttf

#NOTE: Does not currently support instances of two stop IDs occuring within
same network.
"""
__author__ = 'Kevin Saavedra'

import sys
import csv


def line_as_list(line_in, line_number):
    # Converts raw text lines to cleaned lists.
    return filter(None, line_in.rstrip().split(' '))


def line_to_list_generator(list_in):
    # Breaks list of network stops into sublists of len 7 for easy writefile
    # formatting.
    for i in xrange(0, len(list_in), 7):
        yield list_in[i:i + 7]


def sublist_writer(list_in):
    # Formats input list items into Emme-compatible text strings.
    str = ''
    for item in list_in:
        if item.startswith(('dwt', 'ttf')):
            column = ' {:^8}'.format(item)  # Note leading space
        else:
            column = '{:>8} '.format(item)  # Note trailing space
        str = str + column
    return str + '\n'


def network_parser(list_in, init_stop_in, end_stop_in):
    # Parses ingested network file for location of init/end stops to edit.
    # TODO: check edge case if multiple instances of init and end stops.
    current_dwt = ''
    current_ttf = ''
    edit_network = []
    init_index = list_in.index(init_stop_in)
    end_index = list_in.index(end_stop_in) + 1
    for item in list_in:
        # Main dwt, ttf parser. Keeps current dwt, ttf values in memory for
        # reinsertion after edited stops.
        if 'dwt' in item:
            current_dwt = item
        if 'ttf' in item:
            current_ttf = item
        if init_stop_in == item:
            edit_network = list_in[init_index:end_index]
    return edit_network, current_dwt, current_ttf, init_index, end_index


def network_editor(orig_network, network_slice, dwt_in, ttf_in, index_start,
                   index_end, edit_dwt_in, edit_ttf_in):
    # Creates a separate list for network edits and inserts new dwt, ttf values
    # from the network edit payload file.
    new_network = []
    new_network.extend((edit_dwt_in, edit_ttf_in))
    for item in network_slice:
        if not item.startswith(('dwt', 'ttf')):
            # removes existing dwt, ttf values if located between edited stops.
            new_network.append(item)
    new_network.extend((dwt_in, ttf_in))

    # splice the edited network into the original_network
    del orig_network[index_start:index_end]
    counter = 0
    for item in new_network:
        orig_network.insert(index_start + counter, item)
        counter += 1

    # delete existing dwt, ttf right before edited stop
    if orig_network[index_start - 2].startswith(('dwt', 'ttf')):
        del orig_network[index_start - 2]
    return orig_network


def main(network_file, edit_payload):
    # Initial flag and list states
    edited_file = network_file + '_edit'
    parse_following_lines = False
    temp_list = []

    with open(network_file, 'r') as src:
        # Allow for looping through orig. network file
        lines = src.read().splitlines(True)
        line_number = 0

        with open(edit_payload, 'rb') as edits:
            with open(edited_file, 'w') as dest:
                reader = csv.reader(edits)
                next(reader)  # Skip the header row
                for row in reader:
                    edit_transit_network = row[0]
                    init_stop_ID = row[1]  # new ttf, dwt inserted BEFORE this
                    end_stop_ID = row[2]   # prev. ttf, dwt inserted AFTER stop
                    new_dwt = row[3]
                    new_ttf = row[4]
                    indexed_lines = lines[line_number:]

                    for line in indexed_lines:
                        line_number += 1
                        # Writes header row and breaks loop if desired network.
                        if "a'{0}".format(edit_transit_network) in line:
                            dest.write(line)
                            parse_following_lines = True
                            continue

                        if parse_following_lines:
                            # Converts raw text lines into list items
                            line_list = line_as_list(line, line_number)
                            for item in line_list:
                                temp_list.append(item)

                        if parse_following_lines and 'lay=0' in line:
                            # Begin parsing accumulated list items
                            parsed_netwk, dwt, ttf, idx_i, idx_e = \
                                network_parser(temp_list, init_stop_ID,
                                               end_stop_ID)

                            edited_network = network_editor(
                                temp_list, parsed_netwk, dwt, ttf,
                                idx_i, idx_e, new_ttf, new_dwt)

                            generated = line_to_list_generator(edited_network)
                            for sublist in generated:
                                dest.write(sublist_writer(sublist))
                            temp_list = []
                            parse_following_lines = False
                            break

                        if not parse_following_lines:
                            # Writes all unedited transit network lines.
                            dest.write(line)

                # Write all remaining lines after network edits complete
                indexed_lines = lines[line_number:]
                for line in indexed_lines:
                    dest.write(line)

    edits.close()
    src.close()
    dest.close()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
