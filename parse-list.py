import csv

# Read the CSV file and store data as a list of dictionaries
projects = []

with open('list.csv', 'r', newline='') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        projects.append(row)

print(f"Loaded {len(projects)} projects from the CSV file.")

# You can now access the data like this:
for project in projects:
    print(f"District: {project['District']}")
    print(f"Project Title: {project['Project Title']}")
    print(f"Project Description: {project['Project Description (Brief)']}")
    print(f"Project Location: {project['Project Location']}")
    print(f"Status: {project['Status ']}")
    print(f"POC: {project['Project point-of-contact']}")
    print(f"Project Category: {project['Project Category']}")
    print("---")

# The 'projects' list now contains all the data from the CSV file
# Each item in the list is a dictionary representing one row from the CSV