import csv

with open('sp_500_stocks.csv') as file:
    reader = csv.reader(file)
    reader = list(reader)[1:]
    data = {rows[0]: 1 for rows in reader}
    data = tuple(data.keys())
