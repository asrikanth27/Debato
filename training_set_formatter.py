import csv

f = open('sentiment_training.txt')
list_lines = f.readlines()
f.close()

training_list = []
for line in list_lines:
    s = line.split("\t")
    s[1] = s[1][:-1]
    s[0],s[1] = s[1],s[0]
    if s[1]=='1':
        s[1] = 'pos'
    elif s[1]=='0':
        s[1] = 'neg'
    training_list.append(s)

with open('sentiment_training_formatted.csv', 'wb') as f:
    wtr = csv.writer(f, delimiter=',')
    wtr.writerows(training_list)

