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

	
def replaceZeroRate():	 
	path = "/home/ubuntu/Desktop/earthquake/data/"
	f_r = open(path+ "earthquake_wells_data.csv" ,"r")	 

	## get values of each well
	## remove wells with no data for all year
	## add zero to days with no water flow
	lines = f_r.readlines() 
	name_arr = lines[0].strip().split(",")
	size = len(name_arr)
 	well_hash = dict()
 	basic_data_hash = dict()
 	day = 1
	for line in lines[1::]:
		val_arr = line.strip().split(",")
		#Date, Id, Magnitude, Depth, Latitude, None, location, wellID, ...
		basic_data_hash[day] = val_arr[0:7]
		day += 1
		for i in range(7,size):
			well_id = name_arr[i]
			well_data = val_arr[i]
			if len(well_data)>0:
				new_well_data = float(well_data)
			else:
				new_well_data = 0
				
			if well_id not in well_hash:
				well_hash[well_id] = [new_well_data]
			else:
				well_hash[well_id].append(new_well_data)
	
	removed_well = set() 
	well_tokeep = []
	for well_id, well_arr in well_hash.items():
		sum_data = sum(well_arr)
		if sum_data==0:
			removed_well.add(well_id)	
		else:
			well_tokeep.append(well_id)	
	f_w = open(path+ "earthquake_wells_processed_data.csv" ,"w")	 
	to_w = "Date, Id, Magnitude, Depth, Latitude, None, location,"+str(well_tokeep).replace("'","").replace("[","").replace("]","")+"\n"
	f_w.write(to_w)
	
	for j in range(1, 365):
		to_w = str(basic_data_hash[j]).replace("[","").replace("]","")
		for well_id in well_tokeep:
			to_w += ","+str(well_hash[well_id][j])
		to_w += "\n" 
		f_w.write(to_w)
		
	f_w.close()
	
replaceZeroRate()
