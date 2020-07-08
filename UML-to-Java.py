"""
We use the csv module to easily parse CSV file to our 2D array
We operate on the array that has the fields:
class_name	|	 data_members	|	 functions




row -> classname
	-> data_members -> data_member1
					-> data_member2
					-> data_member3
					-> data_member4
	-> functions	-> function1
					-> function2
					-> function3
					-> function4
					-> function5
"""

"""
input fortmat:

<< exception >>
<< interface >>
{abstract}

donot set = defaultValue

<< constructor >>

varname : datatype
"""



#####################################################################################
############################	INITIAL STUFF 	#####################################
#####################################################################################



# importing csv module
import csv 

# csv file name
filename = "./input.csv"   # file to read from
outputFile = open("./output.java", "a") # file to write to



list_lines = []

# reading csv file
with open(filename, 'r') as csvfile:
	# creating a csv reader object
	data = csv.reader(csvfile)
	# extracting each data row one by one
	# each row in data is a list - properly seperated by commas by default
	for row in data:
		# appending only rows which are about classes
		if(row[1] == "Class"):
			list_lines.append(row)
			# print(row)


for i in range(len(list_lines)):
	new_row = []
	# adjust accordingly if you didn't use LucidChart
	new_row.append(list_lines[i][10]) # 0th position
	new_row.append(list_lines[i][11]) # 1st position
	new_row.append(list_lines[i][12]) # 2nd position
	list_lines[i] = list(new_row)

# now list_lines is a 2D matrix with	i 	rows and 	3 	columns


# remove spaces at start, end -> string_1.strip()
# remove a substring from string -> str_1 = str_1.replace(substr, "")



#####################################################################################
############################	MINOR FUNCTION 		#################################
#####################################################################################


def A_colon_B_to_B_A(string):
	"""
	Example:
		progressPercentage : Double
		becomes
		Double progressPercentage

	find last ':'
	A : B
	just make this as B A
	"""
	pos1 = string.rfind(":")
	if(pos1!=-1):
		string = string[pos1+1:] + string[:pos1]


	start_bracket = string.find("(")
	end_bracket = string.find(")")
	if(start_bracket > -1 and end_bracket > -1):
		corrected_within_brackets = A_colon_B_to_B_A(string[start_bracket+1:end_bracket].strip())
		# string is currently like : 		datatype funcname( <erroneous> )
		string = string[:start_bracket] + "( " + corrected_within_brackets.strip() + " )"

	return string


#####################################################################################
####################		PROCESS_FIELD_X FUNCTIONS 		#########################
#####################################################################################



def processFieldZero(field0_classname):
	"""
	Field 0 : class name
	"""
	field0_classname = ''.join(letter for letter in field0_classname)

	outputFile.write("\n\n")

	if("{abstract}" in field0_classname):
		field0_classname = field0_classname.replace("{abstract}", "")
		field0_classname = field0_classname.strip()
		outputFile.write("abstract class " + field0_classname + "\n")
		outputFile.write("{\n")
	elif("<< interface >>" in field0_classname):
		field0_classname = field0_classname.replace("<< interface >>", "")
		field0_classname = field0_classname.strip()
		outputFile.write("interface " + field0_classname + "\n")
		outputFile.write("{\n")
	elif("<< exception >>" in field0_classname):
		field0_classname = field0_classname.replace("<< exception >>", "")
		field0_classname = field0_classname.strip()
		outputFile.write("class " + field0_classname + " extends Exception\n")
		outputFile.write("{\n")
	else:
		field0_classname = field0_classname.strip()
		outputFile.write("class " + field0_classname + "\n")
		outputFile.write("{\n")



def processFieldOne(field1_datamembers):
	"""
	Field 1 : data members

	field1_datamembers is a string right now
	"""
	field1_datamembers = field1_datamembers.replace("-", "\n-")
	field1_datamembers = field1_datamembers.replace("+", "\n+")
	field1_datamembers = field1_datamembers.replace("#", "\n#")
	field1_datamembers = field1_datamembers.replace("\n", "\u2808")
	field1_datamembers = field1_datamembers.split("\u2808")


	for i in field1_datamembers:
		one_line = str(i)
		# one_line is always a str

		access_modifier = ""

		if(len(one_line)<2):
			continue

		if one_line.find("-"):
			access_modifier = "private"
		elif one_line.find("+"):
			access_modifier = "public"
		elif one_line.find("#"):
			access_modifier = "protected"

		one_line = one_line.replace("-", "")
		one_line = one_line.replace("+", "")
		one_line = one_line.replace("#", "")


		one_line = A_colon_B_to_B_A(one_line)
		one_line = one_line.strip()

		outputFile.write("\t" + access_modifier + " " + one_line + ";\n")



def processFieldTwo(field2_functions):
	""""
	Field 2 : functions

	field2_functions is a string right now
	"""
	field2_functions = field2_functions.replace("+", "\n+")
	field2_functions = field2_functions.replace("-", "\n-")
	field2_functions = field2_functions.replace("#", "\n#")

	field2_functions = field2_functions.replace("\n", "\u2808")
	field2_functions = field2_functions.split("\u2808")

	for i in field2_functions:
		one_line = str(i)
		# one_line is always a str

		if one_line.split() == "<< constructor >>":
			continue

		if(len(one_line)<2):
			continue

		# default is nothing - for constructors!
		access_modifier = ""

		# assigning access modifiers
		if(one_line.find("-")!=-1):
			access_modifier = "private"
		elif(one_line.find("+")!=-1):
			access_modifier = "public"
		elif(one_line.find("#")!=-1):
			access_modifier = "protected"

		# removing access modifier characters
		one_line = one_line.replace("-", "")
		one_line = one_line.replace("+", "")
		one_line = one_line.replace("#", "")

		# handling if it is abstract
		is_abstract = False
		if(one_line.find("{abstract}")!=-1):
			is_abstract = True
			one_line = one_line.replace("{abstract}", "")


		one_line = A_colon_B_to_B_A(one_line)
		one_line = one_line.strip()

		outputFile.write("\n")
		if(is_abstract == False):
			outputFile.write("\t" + access_modifier + " " + one_line + "\n")
		elif(is_abstract == True):
			outputFile.write("\t" + access_modifier + " abstract " + one_line + "\n")

		outputFile.write("\t{\n")
		outputFile.write("\t}\n")
	
	# endmost one
	outputFile.write("}\n")




#####################################################################################
############################		MAIN BELOW		#################################
#####################################################################################



for i in range(len(list_lines)):
	processFieldZero(list_lines[i][0])
	processFieldOne(list_lines[i][1])
	processFieldTwo(list_lines[i][2])


