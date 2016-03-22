import csv


class entry:

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)


data = []

with open('Salaries - Salaries.csv', 'r') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader:

        data.append(entry(row))


print [str(x) for x in data]
