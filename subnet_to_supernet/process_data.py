import re
import ipaddress
import sys
import argparse

def process_input_ouput(input_file,output_file):
    output_data=[]
    with open(input_file) as input_data:
        print(input_data)
        for each_line in input_data:
            # print(each_line.split(":")[1])
            if len(each_line.split(":")[1].split(","))>1:
                super_net,invalid_entries= data_filter(each_line.split(":")[1])
                if invalid_entries:
                    output_data.append(f"{each_line.split(':')[0]},{super_net};{invalid_entries}")
                else:
                    output_data.append(f"{each_line.split(':')[0]},{super_net}")
            else:
                output_data.append(f"{each_line.split(':')[0]},{each_line.split(':')[1]}")
        with open(output_file,"w") as file:
            for each_entry in output_data:
                print(each_entry)
                file.write(each_entry)
        
        #     break
            # id=re.search(id_identify_regex,each_line).group()
            # print(id)

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
    for each_entry in id_entries_list:
        # print(each_entry)
        if any(re.match(pattern,each_entry) for pattern in valid_patterns):
        # if ipaddress.ip_address(each_entry):
            # print("valid")
            try:
                if re.match(valid_patterns[1],each_entry):
                    entries['valid_enteries'].append(ipaddress.IPv4Network(each_entry))
                else:
                    entries['valid_enteries'].append(each_entry)
            except ValueError:
                entries['invalid_entries'].append(each_entry)
        else:
            # print("invalid_entry")
            entries['invalid_entries'].append(each_entry)
    supernet=list(ipaddress.collapse_addresses(entries['valid_enteries']))
    for ip in supernet:
        print(ip)
        supernet_ip.append(str(ip))
    return ";".join(supernet_ip),";".join(entries['invalid_entries'])
    # except AttributeError:
    #     return entries['invalid_entries'].append(entries['valid_enteries'])

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process subnet data.')
    parser.add_argument('input_file',help='The input file containing subnet data')
    parser.add_argument('output_file',help='The output file to write the processed data')
    
    args=parser.parse_args()
    process_input_ouput(args.input_file,args.output_file)
    
