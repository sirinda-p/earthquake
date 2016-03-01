from datetime import datetime
#from sklearn.neural_network import MLPClassifier
from sklearn import svm
import numpy as np

def pilotNN():
 	days_ahead = 7 ## this number is also a number of days of well data prior prediction
	threshold = 2.5
	ptrain = 0.7 ## percentage of training data
	path = "/home/ubuntu/Desktop/earthquake/data/"
	f_w = open(path+ "earthquake_wells_data.csv" ,"r")	 
	
	#Date, Id, Magnitude, Depth, Latitude, None, location
	mag_days_hash = dict()
	occur_days_hash = dict()
	well_days_hash = dict()
	no_e = 0
	date_format = "%m/%d/%Y"
	X=[]
	Y=[]
	Xtrain=[]
	Ytrain=[]
	Xtest = []
	Ytest = []
	d0 = datetime.strptime('1/1/2014', date_format)
	tt = 0
	i=0
	for line in f_w.readlines()[1::]:
		val_arr = line.strip().split(",")
		well_data = []
		j=6
		for v in val_arr[7::]:
			j+=1
			try:
				well_data.append(float(v))
			except:
				continue
				#print str(i)+","+str(j)+":"+v
		i+=1		
		#well_data = [ float(v)  for v in val_arr[7::]]
 		mag = val_arr[2]
 		print len(well_data)
 		d1 = datetime.strptime(val_arr[0], date_format)
 		days = (d1 - d0).days
 		well_days_hash[days] = well_data
 		
		if len(mag)>0 :
			mag = float(mag)
			if mag>threshold:
				occur = 1
			else:
				occur = 0
  		else:
			mag = 0
			occur = 0
		
		mag_days_hash[days] = mag 
		occur_days_hash[days] = occur
		
	#print mag_days_hash.keys()	
	for nday in range(7, days, 7):
 		Y.append(occur_days_hash[nday])
		X.append(well_days_hash[nday-days_ahead])
		
		
	data_size = len(Y)	
	  
	Ytrain= np.array(Y[0:int(ptrain*data_size)])
	Xtrain = np.array(X[0:int(ptrain*data_size)])
	
	#print Xtrain
	Ytest = np.array(Y[int(ptrain*data_size)::])
	Xtest = np.array(X[int(ptrain*data_size)::])
 	print Xtrain.shape
	print Ytrain.shape
	## use a simple model: svm 
	clf = svm.SVC()
	print "build a model"
	clf.fit(Ytrain, Ytrain)
	
	print clf.score(Xtest, Ytest)
	
	'''
	clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, random_state=1)
	print "build a model"
	clf.fit(Xtrain, Ytrain)
	print "test a model"
	acc = clf.score(Xtest, Ytest)
	print acc
	## TO DO: get a new version of scikit
	'''
	
pilotNN()
