#!/usr/bin/python

import os 
import re
import sys 


# functions
def isStlFile(file):
    if file[-4:] != ".stl":
        return False
    return True

def parseSTL(fileString, word1, word2):
    indexStart = re.search(word1, fileString).end() # get index where file starts with word1
    indexEnd = re.search(word2, fileString).start() - 1 # get index where file ends with word2
    numbers = fileString[indexStart : indexEnd].replace("\n", "").split() # the numbers in between facet normal and outer loop which are the normal numbers
    return numbers
    
def stlToString(file):
    input = ""
    for line in file.readlines():
        input += line
    return input
    
def stlToCSV(file):
    # Step 1 make new file which will be output
    outputName = file.name.replace(".stl", ".csv")
    output = open(outputName, "w")
    
    # Step 2 write to that file (header)
    output.write("Normal n1, Normal n2, Normal n3, Vertex1 x, Vertex1 y, Vertex1 z, Vertex2 x, Vertex2 y, Vertex2 z, Vertex3 x, Vertex3 y, Vertex3 z\n")
    
    fileString = stlToString(file) # file in string format
    
    # Step 3 check how many traingles there are and print results to ouputs
    inputs = re.findall("facet normal.*?endfacet", fileString, re.DOTALL)


    for text in inputs:
        normalNumbers = parseSTL(text, "facet normal", "outer loop")
        vertexNumbers = parseSTL(text, "outer loop", "endloop")
        
        for number in normalNumbers:
            output.write("{},".format(number))
        
        for number in vertexNumbers:
            if number != "vertex":
                output.write("{},".format(number))
        
        output.write("\n")
    
    return


     
# Get the input file
try: 
    file = open(sys.argv[1])
    #If not stl file then retrun error
    if isStlFile(file.name): 
        stlToCSV(file)
except FileNotFoundError:
    print("Error: File does not exist")

