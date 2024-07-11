import re
import ipaddress
import argparse
from netaddr import *
from pprint import pprint

def process_input_ouput(input_file,output_file):
    output_data=[]
    print(f"Reading the input file: {input_file}")
    with open(input_file) as input_data:
        for each_line in input_data:
            id,id_entry=each_line.split(":")
            if len(id_entry.split(","))>1:
                super_net,invalid_entries= data_filter(id_entry)
                if invalid_entries:
                    output_data.append(f"{id},{super_net};{invalid_entries}")
                else:
                    output_data.append(f"{id},{super_net}")
            else:
                output_data.append(f"{id},{id_entry}")
    sorted_output= sorted(output_data, key=lambda x:x[0])
    with open(output_file,"w") as csvfile:
        for each_line in sorted_output:
            if each_line:
                csvfile.write(f"{each_line}\n")
    pprint(output_data)
    print(f"Output file created successfully: {output_file}")

def data_filter(id_entries):
    supernet_ip=[]
    entries={
        "valid_enteries" : [],
        "invalid_entries" :[]
    }
    id_entries_list=id_entries.strip().split(",")
    valid_patterns= [
        r"^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$",
        r"^(\d{1,3}\.){3}\d{1,3}/(\d{1,3}\.){3}\d{1,3}",
    ]
    # print(id_entries_list)
    for each_entry in id_entries_list:
        each_entry=each_entry.strip()
        if any(re.match(pattern,each_entry) for pattern in valid_patterns):
            try:
                if re.match(valid_patterns[1],each_entry):
                    ip,subnet=each_entry.split('/')
                    cidr=IPAddress(subnet).netmask_bits()
                    entries['valid_enteries'].append(f"{ip}/{cidr}")
                else:
                    entries['valid_enteries'].append(each_entry)
            except ValueError:
                entries['invalid_entries'].append(each_entry)
        else:
            entries['invalid_entries'].append(each_entry)
    supernet= cidr_merge(entries['valid_enteries'])
    for ip in supernet:
        supernet_ip.append(str(ip))
    return ";".join(supernet_ip),";".join(entries['invalid_entries'])

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process subnet data.')
    parser.add_argument('input_file',help='The input file containing subnet data')
    parser.add_argument('output_file',help='The output file to write the processed data')
    
    args=parser.parse_args()
    process_input_ouput(args.input_file,args.output_file)
