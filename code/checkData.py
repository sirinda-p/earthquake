

## To do
## 1. Get data per location
## 2. Check frequency of earthquake in each location 

def main():
	fname = "earthquake_wells_data.csv"
	path = "/home/ubuntu/Desktop/earthquake/data/"
	
	f_r = open(path+fname, "r")
	att_name_arr = f_r.readline().split(",")
	
	location_data_arr_hash = dict()
	## read each line in the file
	line = f_r.readline()
	while line:
		att_value_arr = line.strip().split(",")
		location = att_value_arr[4]+","+att_value_arr[5]
		if location not in location_data_arr_hash:
			location_data_arr_hash[location] = att_value_arr
		else:
			location_data_arr_hash[location].append(att_value_arr)
		line = f_r.readline()
	
	print len(location_data_arr_hash.keys())
	#for location, data_arr in location_data_arr_hash.items():
		#print location
		
		
main()
