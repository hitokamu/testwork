from pprint import pprint

loglist = [['1/1', '晴れ'],
           ['1/2', '晴れ'],
           ['1/3', '曇り'],
           ['1/4', '雨'],
           ['1/5', '雨'],
           ['1/6', '曇り'],
           ['1/7', '晴れ']]


daylist=[]
wetherlist=[]
for i in range(0,7):
    daylist.append(loglist[i][0])
    wetherlist.append(loglist[i][1])

loglist2 =[daylist,wetherlist]

pprint(loglist2)

loglist2 = [[it[i] for it in loglist] for i in range(2)]
pprint(loglist2)

print('loglist3')
loglist3 = []
for i in range(2):
    sublist = []
    for it in loglist:
        sublist.append(it[i])
    loglist3.append(sublist)
pprint(loglist3)

oods = [ i for i in range(10) if i %2 == 1]
print(oods)