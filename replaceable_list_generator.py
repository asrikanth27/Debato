import csv

inList = open('antonym_list.txt', 'r').readlines()
f = open('replace_list2.csv', 'w')
kv = []
for item in inList:
    kv = item.split("\t")
    kv[2] = kv[2].split(",")
    for antonym in kv[2]:
        if not antonym==' ':
            f.write(' '+kv[0]+' ,'+' '+antonym.strip()+"  \n")
            f.write(' '+antonym.strip()+' ,'+' '+kv[0]+"  \n")
f.close()

'''rList = []    
input = '1'
while(input=='1'):
    k = raw_input("k: ")
    v = raw_input("v: ")
    rList.append([k,v])
    rList.append([v,k])
    input = raw_input("inp: ")


f = open('replace_list.csv', 'ws')
for item in rList:
    f.write(item[0]+" ,"+item[1]+" \n")'''