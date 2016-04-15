#Author :Zhu Zichen
#Date : 2016/3/23
#mode 1 : file 
#mode 2: directory 
import os, sys

def getData(input_filename):
	if os.path.exists(input_filename) :
		inputFile = open(input_filename, "r")
		origin_data = inputFile.readlines() 
		length = len(origin_data)
		result = list()
		i = 1
		for line in origin_data:
			percent = "%.2f" % ( (i*1.0/length)*100 )
			result.append(line.strip() + " " + str(percent))
			i += 1
		inputFile.close()
	else:
		print "Invalid File name."
		sys.exit()
	return '\n'.join(result)

def fileSupplement(input_filename, output_filename):
	data = getData(input_filename)
	outputFile = open((output_filename), "w")
	outputFile.write(data)
	outputFile.close()

def DirectorySupplement(input_directory, output_directory):
	try:
		os.makedirs(output_directory)
	except Exception as e:
		print e
		sys.exit()

	if os.path.exists(input_directory) :
		for parent, dirnames, filenames in os.walk(input_directory) : 
			print parent
			for filename in filenames :
				print filename
				output_filename = filename[:-4] + " OUT.txt"
				print output_filename
				data = getData(os.path.join(parent,filename))
				output_filepath = os.path.join(output_directory,output_filename)
				outputFile = open(output_filepath, "w")
				outputFile.write(data)
				outputFile.close()

	else:
		print "Invalid File name."

def main(mode, input_name, output_name):
	if mode == "1" :
		if input_name == output_name:
			output_name = input_name[:-4] + " OUT.txt"
		fileSupplement(input_name, output_name)
	elif mode == "2" :
		if input_name == output_name:
			output_name = input_name + " OUT"
		DirectorySupplement(input_name, output_name)
	else :
		print "Invalid mode."




if __name__ == '__main__':
 	length = len(sys.argv)
	if length <= 2:
		print "Invalid parameters."
		sys.exit()
	elif length == 3:
		input_name = sys.argv[2]
		output_name = input_name
	elif length == 4:
		print sys.argv[1]
		input_name = sys.argv[2]
		output_name = sys.argv[3]
	main(sys.argv[1], input_name, output_name)
	
