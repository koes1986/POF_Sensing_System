import time
from tkinter import *
import serial
from datetime import datetime
import numpy
import csv
#arduino = serial.Serial('COM3', 115200, timeout=.05)
ser1 = serial.Serial('COM3', 115200, timeout=None)
ser2 = serial.Serial('COM6', 115200, timeout=None)


def onclick():
   pass


name_file = 1
counter = 0

container1= numpy.zeros((200, 3))
container2= numpy.zeros((200, 3))


root = Tk()
text = Text(root)
text.pack()
text.config(height=60,width=120)


def monitor(a,b):
	text.delete(1.0,END)
	global counter
	#read serial data
	data1 = a.strip()
	numbers1 = data1.split('a')
	data2 = b.strip()
	numbers2 = data2.split('a')

	#throwing exception
	if len(numbers1) == 1:
			numbers1.extend([0,0])
	if len(numbers2) == 1:
			numbers2.extend([0,0])
	if len(numbers1) == 2:
			numbers1.extend([0])
	if len(numbers2) == 2:
			numbers2.extend([0])
	if numbers1[0]=='' :
		numbers1[0] = 0
	if numbers1[1]== '':
		numbers1[1] = 0
	if numbers1[2]== '' :
		numbers1[2] = 0
	if numbers2[0]== '' :
		numbers2[0] = 0
	if numbers2[1]== '' :
		numbers2[1] = 0
	if numbers2[2]=='' :
		numbers2[2] = 0
	
	#write on the window
	text.insert(INSERT,"\n")
	text.insert(INSERT,numbers1[0])
	text.insert(INSERT," "*2)
	text.insert(INSERT,numbers1[1])
	text.insert(INSERT," "*2)
	text.insert(INSERT,numbers1[2])
	text.tag_add("one", "2.0", "3.20")
	
	text.insert(INSERT,"\n")
	text.insert(INSERT,numbers2[0])
	text.insert(INSERT," "*2)
	text.insert(INSERT,numbers2[1])
	text.insert(INSERT," "*2)
	text.insert(INSERT,numbers2[2])
	
	text.insert(INSERT,"\n")
	text.insert(INSERT,"Counter :")
	text.insert(INSERT,counter)
	
	text.tag_config("one", foreground="black",font=("Courier", 44),background="white")
	

def save(a,b):
	global container1
	global container2
	global counter
	global name_file
	
	#read serial data
	data1 = a.strip()
	numbers1 = data1.split('a')
	data2 = b.strip()
	numbers2 = data2.split('a')
	
	#throwing exception
	if len(numbers1) == 1:
			numbers1.extend([0,0])
	if len(numbers2) == 1:
			numbers2.extend([0,0])
	if len(numbers1) == 2:
			numbers1.extend([0])
	if len(numbers2) == 2:
			numbers2.extend([0])
	if numbers1[0]=='' :
		numbers1[0] = 0
	if numbers1[1]== '':
		numbers1[1] = 0
	if numbers1[2]== '' :
		numbers1[2] = 0
	if numbers2[0]== '' :
		numbers2[0] = 0
	if numbers2[1]== '' :
		numbers2[1] = 0
	if numbers2[2]=='' :
		numbers2[2] = 0
		
	container1[counter][0] = numbers1[0]
	container1[counter][1] = numbers1[1]
	container1[counter][2] = numbers1[2]
	
	container2[counter][0] = numbers2[0]
	container2[counter][1] = numbers2[1]
	container2[counter][2] = numbers2[2]
	
	if counter == 199:
		average1 = numpy.sum(container1 , axis=0)/200
		average2 = numpy.sum(container2 , axis=0)/200
		cob = "init.csv"
		file = csv.writer(open(cob, "w",newline=''))
		#file.writerow([container1[1][0], container1[1][1], container1[1][2]])
		file.writerow([int(average1[0]), int(average1[1]), int(average1[2])])
		file.writerow([int(average2[0]), int(average2[1]), int(average2[2])])
		counter = 0
		
	else:
		counter = counter +1

	
def update_label():
	a = ser1.readline()[:-2] # attempt to read a character from Serial
	b = ser2.readline()[:-2] # attempt to read a character from Serial
	a = a.decode('utf-8')
	b = b.decode('utf-8')
	monitor(a,b)
	save(a,b)
	
	#calls update_label function again after 1 millisecond. (1000 milliseconds.)
	root.after(1, update_label)
    

root.after(1, update_label)
root.mainloop()
