import csv

with open(r"C:\Users\eguzman\Downloads\esclavos.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    print(f"INSERT INTO Persons VALUES('{row[0]}','{row[1]}','{row[2]}', {row[3]});")