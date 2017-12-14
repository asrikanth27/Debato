import csv

'''inList = open('replace_list.csv', 'r').readlines()
for item in inList:
    kv = item.split(",")
    rList.append([kv[0],kv[1]])
    rList.append([kv[1],kv[0]])'''

rList = []    
input = '1'
while(input=='1'):
    k = raw_input("k: ")
    v = raw_input("v: ")
    rList.append([k,v])
    rList.append([v,k])
    input = raw_input("inp: ")


with open('replace_list.csv', 'wb') as f:
    wtr = csv.writer(f, delimiter=',')
    wtr.writerows(rList)