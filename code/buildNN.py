from datetime import datetime
import skflow
from sklearn import svm, metrics
import sklearn.feature_selection as fsel
import numpy as np
from operator import itemgetter
 
def pilotNN():
 	days_ahead = 14 ## this number is also a number of days of well data prior prediction
 	ttf = 201 ## total number of original features
 	threshold = 2.5
 	ptrain = 0.6 ## percentage of training data
	path = "/home/ubuntu/Desktop/earthquake/data/"
	f_w = open(path+ "earthquake_wells_processed_data.csv" ,"r")	 
	
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
 				print "ERROR"+str(i)+","+str(j)+":"+v
		i+=1		
		#well_data = [ float(v)  for v in val_arr[7::]]
 		mag = val_arr[2]
  		d1 = datetime.strptime(val_arr[0], date_format)
 		days = (d1 - d0).days
 		well_days_hash[days] = well_data
 		
		if len(mag)>0 :
			try:
				mag = float(mag)
			except:
				mag = 0
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
	for nday in range(days_ahead, days, days_ahead):
 		Y.append(occur_days_hash[nday])
		X.append(well_days_hash[nday-days_ahead])
	
	for k in range(50,100,10): 
		print "Percent of selected features = "+str(k)
		
		selector = fsel.SelectPercentile(score_func=fsel.chi2, percentile=k)
		X_new = selector.fit_transform(X, Y)
 		 
		data_size = len(Y)	
		
		Ytrain= np.array(Y[0:int(ptrain*data_size)])
		Xtrain = np.array(X_new[0:int(ptrain*data_size)])
		
		#print Xtrain
		Ytest = np.array(Y[int(ptrain*data_size)::])
		Xtest = np.array(X_new[int(ptrain*data_size)::] )
		
		kernel_svm = svm.SVC(gamma=.2)
		linear_svm = svm.LinearSVC()

		print "linear SVM"
		linear_svm.fit(Xtrain, Ytrain)
		YPredicted = linear_svm.predict(Xtrain)
		print "#1sin training set = "+str(sum(Ytrain))+", #1sin test set = "+str(sum(YPredicted))
		YPredicted2 = linear_svm.predict(Xtest)
		print "#1sin training set = "+str(sum(Ytest))+", #1sin test set = "+str(sum(YPredicted2))

		print linear_svm.score(Xtest, Ytest) 
		
		print "rbf SVM"
		kernel_svm.fit(Xtrain, Ytrain)
		YPredicted = kernel_svm.predict(Xtrain)
		print "#1s in training set = "+str(sum(Ytrain))+", #1sin test set = "+str(sum(YPredicted))
		YPredicted2 = kernel_svm.predict(Xtest)
		print "#1s in training set = "+str(sum(Ytest))+", #1sin test set = "+str(sum(YPredicted2))
		print kernel_svm.score(Xtest, Ytest)  
		myrange = range(900, 1000,100)
		for x,y,z in zip( myrange,myrange,myrange):
			print "DNN"
			print (x,y,z)
			classifier2 = skflow.TensorFlowDNNClassifier(hidden_units=[x,y,z], steps=1000, n_classes=2)
			classifier2.fit(Xtrain, Ytrain)
			YPredicted1 = classifier2.predict(Xtrain)
			score1 = metrics.accuracy_score(Ytrain,  classifier2.predict(Xtrain))
			#print("Accuracy train : %f" % score1)
			YPredicted3 = classifier2.predict(Xtest)
			score2 = metrics.accuracy_score(Ytest, YPredicted3)
			
			print("Accuracy test : %f" % score2)
			
			print Ytrain
			print YPredicted1
			print Ytest
			print YPredicted3
			''' 
			n = 0
			input_warr = classifier2.weights_[0]
			print input_warr
			 
			indices, L_sorted = zip(*sorted(enumerate(input_warr), key=itemgetter(1)))
			print list(sorted_features)
			print ""
			print  list(indices)
		'''
pilotNN()


'''
## use a simple model: svm 
	 
	clf = svm.SVC()
 	clf.fit(Xtrain, Ytrain)
	YPredicted = clf.predict(Xtrain)
	print Ytrain
	print YPredicted
	print clf.score(Xtrain, Ytrain)
	YPredicted2 = clf.predict(Xtest)
	print Ytest
	print YPredicted2
	print clf.score(Xtest, Ytest)
	
	classifier = skflow.TensorFlowLinearClassifier(n_classes=2, batch_size=128, steps=500, learning_rate=0.05)
	classifier.fit(Xtrain, Ytrain)
	print classifier.score(Xtest, Ytest)
	
	print Ytrain
	'''
