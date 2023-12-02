from read_respiban import respibanfileparser
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
import numpy as np;


class trainsvmclassifier():
    def __init__(self):
        self.respban = respibanfileparser()
        self.model = None

    def get_training_data(self):
        self.respban.readfiles()
        data = self.respban.get_ordered_data()
        X = None
        y= None
        X_arr = []
        Y_arr = []
        for k,v in data.items():
            X_arr.append(v[0])
            Y_arr.append(v[1])
        X = np.concatenate(X_arr)
        y = np.concatenate(Y_arr)
        data1 = [X,y]

        #print(data1)
        return data1
    
    def getclasslabelfromvalue(self,value):
      if value == 1:
        return 'HAHV'
      elif value == 2:
        return 'HALV'
      elif value == 3:
        return 'LALV'
      elif value == 4:
        return 'LAHV'
  
    def print_data_file(self):
      self.respban.readfiles()
      data = self.respban.get_ordered_data()
      for k,v in data.items():
        filename = "data_" + k + ".csv"
        with open(filename,"w") as f:
            for vi in range(len(v[0])):
                lab = self.getclasslabelfromvalue(v[1][vi])
                f.write(f"{v[0][vi]},{lab}\n")


    def train_model_multiclass(self):
        data = self.get_training_data()
        print(len(data[0]))
        with open("test.csv","w") as f:
            for i in range(len(data[0])):
                f.write(f"{data[0][i]},{data[1][i]}\n")
        X = data[0].reshape(-1,1)
        y = data[1].reshape(-1,1)
        

        X_train,X_test = np.split(X,2)
        y_train,y_test = np.split(y,2)

        self.model = OneVsRestClassifier(SVC()).fit(X_train, y_train)
        y_predict = self.model.predict(X_test)

        print(confusion_matrix(y_test,y_predict))
        print("\n")
        print(classification_report(y_test,y_predict))
        print("Training set score for SVM: %f" % self.model.score(X_train , y_train))
        print("Testing  set score for SVM: %f" % self.model.score(X_test  , y_test ))
            
def main():
    tsc = trainsvmclassifier()
    #tsc.train_model_multiclass()
    tsc.print_data_file()
if __name__ == '__main__':
    main()

