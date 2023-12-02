import pickle
import numpy as np;
import pandas as pd;
import csv;
from datetime import datetime,timedelta;
from read_quest import questfileparser;


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

respiban_files_list = [
        "WESAD/S3/S3_respiban.txt",
        "WESAD/S4/S4_respiban.txt",
        "WESAD/S17/S17_respiban.txt",
        "WESAD/S5/S5_respiban.txt",
        "WESAD/S14/S14_respiban.txt",
        "WESAD/S16/S16_respiban.txt",
        "WESAD/S10/S10_respiban.txt",
        "WESAD/S9/S9_respiban.txt",
        "WESAD/S11/S11_respiban.txt",
        "WESAD/S15/S15_respiban.txt",
        "WESAD/S6/S6_respiban.txt",
        "WESAD/S2/S2_respiban.txt",
        "WESAD/S7/S7_respiban.txt",
        "WESAD/S8/S8_respiban.txt",
        "WESAD/S13/S13_respiban.txt"
        ]
db = {}
db_ordered = {}
class respibanfileparser:
    def __init__(self):
        self.qfp = None
        self.timeincrnum = 500 #Data sampled at 700Hz and filtered for every 1000 samples
        self.timeincrden = 700.00 #Data sampled at 700Hz and filtered for every 1000 samples

    def read_respiban_file(self,file):
        colnames = ['ignore',"ECG", "EDA", "EMG", "TEMP", "XYZ1", "XYZ2", "XYZ3", "RESPIRATION"]
        df = pd.read_csv(file,delim_whitespace=True,header=None,names=colnames,converters={"EDA":lambda x: (((int(x)/65536)*3)/0.12)},skiprows=lambda x:(x<3) or ((x-3)%500))
        df['EDA']
        return df['EDA'].to_numpy()
    
    def get_class_from_va_data(self,valence,arousal):
        if (valence>=5 and arousal >= 5):
            return 1;
        elif (valence <5 and arousal >= 5):
            return 2;
        elif (valence <5 and arousal < 5):
            return 3;
        elif (valence >=5 and arousal <5):
            return 4;

    def sync_data_with_valence_arousal(self,data_db,data_db_ord):
        if(self.qfp == None):
            self.qfp = questfileparser()
            self.qfp.readfiles()

        subjectinfodb = self.qfp.get_subject_details()
        curriterseconds = 0
        for key,value in data_db.items():
            subinfo = subjectinfodb[key]
            length = value.size
            index = 0
            edavalues = np.zeros(length)
            edavaluesclass = np.zeros(length)
            edaindex = 0
            orderid = 0
            orderidlength = len(subinfo['order'])

            while(orderid < orderidlength):
                timeval = subinfo['time'][subinfo['order'][orderid]]
                curriterseconds = index * self.timeincrnum / self.timeincrden
                curritertime = timedelta(seconds=int(curriterseconds))
                #print(curritertime)
                #print(timeval[0])
                while(curritertime < timeval[0] and index < length):
                    index += 1
                    curriterseconds = index * self.timeincrnum / self.timeincrden
                    curritertime = timedelta(seconds=int(curriterseconds))


                if (index >= length):
                    break;

                currclass = self.get_class_from_va_data(int(subinfo['valence'][subinfo['order'][orderid]]),
                                                        int(subinfo['arousal'][subinfo['order'][orderid]]))
                #print(currclass)
                #print(subinfo['order'][orderid])
                while(curritertime < timeval[1] and index < length):
                    edavalues[edaindex] = value[index]
                    edavaluesclass[edaindex] = currclass
                    index +=1
                    edaindex +=1
                    curriterseconds = index * self.timeincrnum / self.timeincrden
                    curritertime = timedelta(seconds=int(curriterseconds))
                
                if (index >= length):
                    break;
                orderid += 1

            #print(orderid)
            #print(index)
            edavalues = edavalues[edavalues != 0]
            edavaluesclass = edavaluesclass[edavaluesclass !=0]
            data_db_ord[key] = [edavalues,edavaluesclass]
            #print(edavalues)
            #print(edavaluesclass)




    def readfiles(self):
        global db
        global db_ordered
        for file in respiban_files_list:
            #print(file)
            modulename = file[6:9]
            split_name_index = modulename.find('/')
            if split_name_index != -1:
                modulename = modulename[:-1]
            edadata = self.read_respiban_file(file)
            db[modulename] = edadata
            self.sync_data_with_valence_arousal(db,db_ordered)
            #break;
        #print(db_ordered)

    def get_ordered_data(self):
        global db_ordered;
        return db_ordered

#def main():
#    rfp = respibanfileparser()
#    rfp.readfiles()

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
