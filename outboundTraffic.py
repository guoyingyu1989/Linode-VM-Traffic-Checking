import subprocess
import csv
import re

# Define your variables
authorization = "Bearer <YOUR ACCESS TOKEN>" # put your access token behind the "Bearer ", I 
year = "2023" # change the date
month = "07" # change the month 

# Read the instance IDs from a text file, each line contains only one VM instance ID
with open('instance_ids.txt', 'r') as file:
    instance_ids = file.read().splitlines()

# Prepare a list to hold the output
output_list = []

# Loop through the instance IDs and execute the command for each one
for i, instance_id in enumerate(instance_ids, start=1):
    print(f"Processing instance {i} of {len(instance_ids)}: {instance_id}")
    command = f'curl -H "Authorization: {authorization}" https://api.linode.com/v4/linode/instances/{instance_id}/transfer/{year}/{month}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error:
        output_list.append([instance_id, "Error", error.decode('utf-8')])
    else:
        # Split the output into fields using both ',' and ':'
        fields = re.split(',|:', output.decode('utf-8'))
        
        # Select the fields you want to include in the CSV output
        selected_fields = [fields[i] for i in [2, 3]]   # Modify this line to select your fields
        
        output_list.append([instance_id] + selected_fields)

# Write the output list to a CSV file
with open('output.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Instance ID", "Traffic Type", "Bytes"])  # Modify this line to match your fields
    writer.writerows(output_list)
