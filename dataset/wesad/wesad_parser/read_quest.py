import pickle
import numpy as np;
import csv;
from datetime import datetime,timedelta;


def to_time(value):
    if value.find('.') == -1:
        minutes = int(value)
        seconds = 0
    else:
        minutes, seconds = [int(i) for i in value.split('.')]

    # if minutes is greater than 59 pass it to hour
    hour = 0
    if minutes > 59:
        hour = minutes//60
        minutes = minutes%60

    return timedelta(hours=hour,minutes=minutes,seconds=seconds)

#with open(""WESAD/S3/S3_respiban.txt","rb") as f:
#    data = pickle.load(f,encoding='latin1')
#    print (data)
quest_files_list = [
        "WESAD/S3/S3_quest.csv",
        "WESAD/S4/S4_quest.csv",
        "WESAD/S17/S17_quest.csv",
        "WESAD/S5/S5_quest.csv",
        "WESAD/S14/S14_quest.csv",
        "WESAD/S16/S16_quest.csv",
        "WESAD/S10/S10_quest.csv",
        "WESAD/S9/S9_quest.csv",
        "WESAD/S11/S11_quest.csv",
        "WESAD/S15/S15_quest.csv",
        "WESAD/S6/S6_quest.csv",
        "WESAD/S2/S2_quest.csv",
        "WESAD/S7/S7_quest.csv",
        "WESAD/S8/S8_quest.csv",
        "WESAD/S13/S13_quest.csv"
        ]

filterrow = ['# Subj','# ORDER','# START','# END','# DIM','# DIM','# DIM','# DIM','# DIM']
subjectdb={}
class questfileparser:
    def __init__(self):
        self.readfiles()

    def read_quest_file(self,filename):
        global filterrow;
        global subjectdb;
        filterindex=0;
        #print(filename)
        with open(filename,"r") as f:
            data = csv.reader(f,delimiter=';')
            i=0
            subjectdb_i = {}
            subjectdb_i['valence'] = {}
            subjectdb_i['arousal'] = {}
            for row in data:
                if filterrow[filterindex] in row[0] and filterindex == 0:
                    subjectdb_i['sub_id'] = row[1]
                    filterindex +=1
                elif row[0] == filterrow[filterindex] and filterindex == 1:
                    orderid = []
                    for j in range(1,5+1):
                        orderid.append(row[j])
                    subjectdb_i['order'] = orderid
                    filterindex +=1
                elif row[0] == filterrow[filterindex] and filterindex == 2:
                    starttime = {}
                    for j in range(1,5+1):
                        time = to_time(row[j])
                        starttime[subjectdb_i['order'][j-1]] = [time,0]
                    subjectdb_i['time'] = starttime
                    filterindex +=1
                elif row[0] == filterrow[filterindex] and filterindex == 3:
                    for j in range(1,5+1):
                        time = to_time(row[j])
                        subjectdb_i['time'][subjectdb_i['order'][j-1]][1] = time
                    filterindex +=1
                elif row[0] == filterrow[filterindex] and filterindex >= 4 and filterindex <= 8:
                    subjectdb_i['valence'][subjectdb_i['order'][filterindex-4]] = row[1]
                    subjectdb_i['arousal'][subjectdb_i['order'][filterindex-4]] = row[2]
                    filterindex +=1
                if filterindex > 8 :
                    break;
            subjectdb[subjectdb_i['sub_id']] = subjectdb_i
    
    def readfiles(self):
        for file in quest_files_list:
            self.read_quest_file(file)
        #print(subjectdb)

    def get_subject_details(self):
        return subjectdb
                    
'''
#3 index is data
with open("WESAD/S3/S3_respiban.txt","r") as f:
    data = csv.reader(f,delimiter='\t')
    i=0
    for row in data:
        if i==0 or i==2:
            pass
        elif i==1 :
            initialpos = row[0].find('"time":')
            initialpos = initialpos+8
            endpos = row[0].find('"',initialpos+1)
            time = row[0][initialpos+1:endpos]

            print(time)
            basetime = datetime.strptime(time,"%H:%M:%S.%f")
            break;
        else:
            pass

        i=i+1
'''

#if __name__ == "__main__":
#    main()
