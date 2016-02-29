from datetime import datetime
from sklearn.neural_network import MLPClassifier

def pilotNN():
	given_county = "ALFALFA"
	days_ahead = 1
	threshold = 2.5
	path = "/home/ubuntu/Desktop/earthquake/data/"
	f_w = open(path+ "earthquake_wells_data.csv" ,"r")	 
	
	#Date, Id, Magnitude, Depth, Latitude, None, location
	mag_days_hash = dict()
	occur_days_hash = dict()
	well_days_hash = dict()
	no_e = 0
	date_format = "%m/%d/%Y"
	Xtrain=[]
	Ytrain=[]
	Xtest = []
	Ytest = []
	d0 = datetime.strptime('12/31/2013', date_format)
	tt = 0
	for line in f_w.readlines()[1::]:
		val_arr = line.strip().split(",")
		well_data = val_arr[7::]
 		mag = val_arr[2]
 		d1 = datetime.strptime(val_arr[0], date_format)
 		days = (d1 - d0).days
 		well_days_hash[days] = well_data
 		
		if len(mag)>0 and val_arr[6] == given_county:
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
		tt += 1
		if tt<200:
			Ytrain.append(occur)
			Xtrain.append(well_data)
		else:
			Ytest.append(occur)
			Xtest.append(well_data)
			
	clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, random_state=1)
	print "build a model"
	clf.fit(Xtrain, Ytrain)
	print "test a model"
	acc = clf.score(Xtest, Ytest)
	print acc
	## TO DO: get a new version of scikit
pilotNN()
