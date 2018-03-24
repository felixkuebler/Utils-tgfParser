import numpy as np
import sys




if len(sys.argv) == 2 or len(sys.argv) == 3:

	if sys.argv[1].split(".")[1] != "tgf":

		print "error: wrong file format. tgf-format required"

	else:

		output_path = sys.argv[1].split(".")[0]
		if len(sys.argv) == 3:
			output_path = sys.argv[2].split(".")[0]

		matrix = np.empty((1,1),dtype=object)
		list = []
		line_count = 0
		read_edges = False

		with open(sys.argv[1], "r") as file:

			for line in file:

				line = line.replace("\n", "")

				if (read_edges == False) and (line == "#"):

					matrix = np.empty((line_count+1, line_count+1), dtype=str)

					for i in range(1, line_count+1):
						matrix[i,0] = list[i-1]
						matrix[0,i] = list[i-1]

					read_edges = True


				elif read_edges == True:

					edge_params = line.split(' ')

					if (len(edge_params) > 2) and edge_params[2]:
						matrix[edge_params[1],edge_params[0]] = edge_params[2]
						matrix[edge_params[0],edge_params[1]] = edge_params[2]

					else:
						print edge_params[0]
	
				if read_edges == False:
					line_count += 1
					list.append(line.split(" ",1)[1])

			if read_edges == False:
				print "error parsing tgf due to #-divider"



			else:

				with open(output_path + ".csv", 'w') as file:

					for i in range(0, matrix.shape[0]-1):
						for j in range(0, matrix.shape[0]-2):

							file.write(str(matrix[i, j]) + ";")

						file.write(str(matrix[i, matrix.shape[0]-1]) + "\n")

else:

	print ""
	print ""
	print "Manual"
	print ""
	print "argument1: input file path (tgf-format)"
	print "argument2: output file path (csv-format)"
	print ""
	print "python " + sys.argv[0] + ".py argument1"
	print "python " + sys.argv[0] + ".py argument1 argument2"
	print ""
	print ""


