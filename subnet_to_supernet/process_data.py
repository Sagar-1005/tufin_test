'''re module is for regex.
argparse for taking command line arguments.
netaddr to validate ip.'''
import re
import argparse
from netaddr import cidr_merge,IPAddress

def process_input_ouput(input_file,output_file):
    """
    Reads input file and write to output data

    Args:
        input_file(str): The path to the input file containing subnet data.
        output_file(str): The path to the output file where the processed data will be written,
    """
    output_data=[]
    print(f"Reading the input file: {input_file}")
    with open(input_file,encoding='utf-8') as input_data:
        for each_line in input_data:
            id_num,id_entry=each_line.strip().split(":") # Splitting to identify the id_num and id_entry
            if len(id_entry.split(","))>1: #Ignoring supernet if id is having single entry
                super_net_details,invalid_entries= data_filter_create_supernet(id_entry)
                if invalid_entries:#wring to output only if invalid entries.
                    output_data.append(f"{id_num},{super_net_details};{invalid_entries}")
                else:
                    output_data.append(f"{id_num},{super_net_details}")
            else:
                output_data.append(f"{id_num},{id_entry}")
    sorted_output= sorted(output_data, key=lambda x:x.split(",")[0]) # Sorting the final output
    with open(output_file,"w",encoding='utf-8') as csvfile:
        for each_line in sorted_output:
            if each_line:
                csvfile.write(f"{each_line}\n")
    print(f"Output file created successfully: {output_file}")

def data_filter_create_supernet(id_entries):
    """
    Filters and merges into supernet for entries from a list of entries. 

    Args:
        id_entries(str): A comma separated string of subnet entries.
    
    Returns:
        tupple: A tupple containing a string of merged subnets and string of invalid entries.

    """
    supernet_ip=[]
    entries={
        "valid_enteries" : [],
        "invalid_entries" :[]
    }
    id_entries_list=id_entries.strip().split(",")
    valid_patterns= [
        r"^(\d{1,3}\.){3}\d{1,3}/([0-9]|[12][0-9]|[3][0-2])$",
        r"^(\d{1,3}\.){3}\d{1,3}/(\d{1,3}\.){3}\d{1,3}",
    ]
    for each_entry in id_entries_list:
        each_entry=each_entry.strip()
        if any(re.match(pattern,each_entry) for pattern in valid_patterns): #Checking whether input is  valid.
            try:
                if re.match(valid_patterns[1],each_entry): # This condition will match entries which has subnetmask.
                    ip,subnet=each_entry.split('/')
                    cidr=IPAddress(subnet).netmask_bits() # Converting subnet mask to CIDR becuse netaddr will only take CIDR as input
                    entries['valid_enteries'].append(f"{ip}/{cidr}")
                else:
                    entries['valid_enteries'].append(each_entry)
            except:
                entries['invalid_entries'].append(each_entry)
        else:
            entries['invalid_entries'].append(each_entry)
    supernet= cidr_merge(entries['valid_enteries']) # Merging subnet to supernet
    for ip in supernet:
        supernet_ip.append(str(ip))
    return ";".join(supernet_ip),";".join(entries['invalid_entries']) # Converted list to string.

if __name__=="__main__":
    # Process the arguments entered via CLI.
    parser = argparse.ArgumentParser(description='Process subnet data.')
    parser.add_argument('input_file',help='The input file containing subnet data')
    parser.add_argument('output_file',help='The output file to write the processed data')
    args=parser.parse_args()
    process_input_ouput(args.input_file,args.output_file)
