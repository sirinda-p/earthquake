from datetime import datetime

def matchID_earthquake():
	efile = "earthquake_2014.csv"
	e_w_file = "earthquake_wells_data.csv" 
	
	## get earthquake county from efile and put in e_w_file 
	path = "/home/ubuntu/Desktop/earthquake/data/"
	
	f_e = open(path+efile, "r")
	f_well = open(path+e_w_file, "r")
	
	f_e.readline() 
	
	## make a hash table of eq id and its county
	id_county_hash = dict()
	for line in f_e.readlines():
		val_arr = line.strip().split(",")
		id = val_arr[0]
		if id in id_county_hash:
			print "Error "+str(id)+" already in a hash table"
		else:
 			id_county_hash[id] = val_arr[9]
	
	## write a new file that contains the location (county) of an earthquake
	f_w = open(path+ "earthquakeWithLocation_wells_data.csv" ,"w")
	line = f_well.readline()
	att_arr = line.strip().split(",")
	larr = len(att_arr)
	new_arr_arr = [None] * larr
	new_arr_arr[0:6] = att_arr[0:5] 
	new_arr_arr[6] = "location"
	new_arr_arr[7::] = att_arr[6::] 
	f_w.write(str(new_arr_arr).replace("'","").strip("]").strip("[")+"\n")
	
	line = f_well.readline()
 	while line:
		val_arr = line.strip().split(",")
		id = val_arr[1] 
		if id in id_county_hash:
			county = id_county_hash[id]
		else:
			county = ""
		newval_arr = [None] * larr
		newval_arr[0:5] = val_arr[0:6] 
		newval_arr[6] = county
		newval_arr[7::] = val_arr[6::] 
		f_w.write(str(newval_arr).replace("'","").strip("]").strip("[")+"\n")	
		line = f_well.readline()
	
	f_w.close()
	f_well.close()
	f_e.close()
		 
def getFreq():
	path = "/home/ubuntu/Desktop/earthquake/data/"
	f_w = open(path+ "earthquake_wells_data.csv" ,"r")	 
	
	#Date, Id, Magnitude, Depth, Latitude, None, location
	county_mag = dict()
	no_e = 0
	date_format = "%m/%d/%Y"
	d0 = datetime.strptime('12/31/2013', date_format)
	for line in f_w.readlines()[1::]:
		val_arr = line.strip().split(",")
 		mag = val_arr[2]
 		d1 = datetime.strptime(val_arr[0], date_format)
 		days = (b - a).days
		if len(mag)>0:
			mag = float(mag)
			county = val_arr[6]
			if county in county_freq:
				county_mag[county].append(mag)
			else:
				county_mag[county] = [mag]
		else:
			no_e+=1
	tte = 0		
	for county, mag_arr in county_freq.items():
		print county+":"+str(len(mag_arr))
 		tte += len(mag_arr)
	print "No earthquake:"+str(no_e)

	
	 


checkTime()
