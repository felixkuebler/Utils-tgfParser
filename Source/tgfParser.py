#!/usr/bin/python

import numpy as np
import sys

from Tkinter import Tk, Label, Button
from tkFileDialog import *



class GUI:

    input_file = ""
    output_file = ""

    def __init__(self, master):

        self.master = master
        master.title("tgf to csv Parser")

        self.fileInputButton = Button(master, text="Input File...", command=self.selectFileInput)
        self.fileInputButton.pack(pady=(15,0))

        self.fileInputLabel = Label(master, text="path/to/inputfile.tgf")
        self.fileInputLabel.pack(pady=(0,15))

        self.fileOutputButton = Button(master, text="Output File...", command=self.selectFileOutput)
        self.fileOutputButton.pack()

        self.fileOutputLabel = Label(master, text="path/to/outputfile.csv (optional)")
        self.fileOutputLabel.pack(pady=(0,15))

        self.compileButton = Button(master, text="Parse", command=self.triggerCompilation)
        self.compileButton.pack()

        self.compileLabel = Label(master, text="")
        self.compileLabel.pack()



    def selectFileInput(self):

        self.input_file = askopenfilename(initialdir="~/", filetypes =(("trivial graph format", "*.tgf"),("All Files","*.tgf")), title = "Choose a tgf-file.")
        if len(self.input_file) > 0:
            self.fileInputLabel["text"] = self.input_file


    def selectFileOutput(self):

        self.output_file = asksaveasfilename(initialdir="~/", filetypes =(("character separated values", "*.csv"),("All Files","*.csv")), title = "Choose a tgf-file.", defaultextension = ".csv")
        if len(self.output_file) > 0:
            self.fileOutputLabel["text"] = self.output_file


    def triggerCompilation(self):

        if len(self.input_file) <= 0:
            self.compileLabel["text"] = "No input file selected.\nPlease use the file-chooser\nto pick a tgf-file."

        elif len(self.output_file) <= 0:
                self.output_file =  self.input_file.split(".")[0] + ".csv"
                self.compileFiles()

        else:
            self.compileFiles()


    def compileFiles(self):
		self.compileLabel["text"] = "Compiling..."

		matrix = np.empty((1,1),dtype=object)
		list = []

		with open(sys.argv[1], "r") as file:

			line_count = 0
			read_edges = False
			for line in file:

				line = line.replace("\n", "")

				if (read_edges == False) and (line == "#"):

					matrix = np.empty((line_count+1, line_count+1), dtype=object)

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
				self.compileLabel["text"] = "Error: Parsing tgf file failed due to #-divider"



			else:

				with open(self.output_file + ".csv", 'w') as file:

					for i in range(0, matrix.shape[0]-1):
						for j in range(0, matrix.shape[0]-2):

							file.write(str(matrix[i, j]) + ";")

						file.write(str(matrix[i, matrix.shape[0]-1]) + "\n")

				self.compileLabel["text"] = "Done!"


             




root = Tk()
root.geometry("250x250") 
root.resizable(width=False, height=False)

my_gui = GUI(root)

root.mainloop()