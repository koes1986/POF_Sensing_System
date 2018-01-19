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

#set array to save pressure value and measurement time
container1= numpy.zeros((50, 3))
container2= numpy.zeros((50, 3))
time_now1 = ["" for x in range(50)]
time_now2 = ["" for x in range(50)]

#read initiate matrix
init= numpy.genfromtxt('init.csv',delimiter=',',dtype=str)
xxx = [int(s) for ss in init for s in ss]
init=numpy.add(xxx,0)
init.resize(2,3)

#read normalize matrix
norm= numpy.genfromtxt('norm.csv',delimiter=',',dtype=str)
yyy = [int(s) for ss in norm for s in ss]
norm=numpy.add(yyy,0)
norm.resize(2,3)

diff_norm= numpy.subtract (norm,init)

root = Tk()
text = Text(root)
text.pack()
text.config(height=60,width=120)

#clear the buffer
ser1.reset_input_buffer();
ser2.reset_input_buffer();

#to showing in real time
def monitor(a,b):
	text.delete(1.0,END)
	
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
	text.insert(INSERT,abs(round((int(numbers1[0])-init[0][0])/diff_norm[0][0],2)))
	text.insert(INSERT," "*2)
	text.insert(INSERT,abs(round((int(numbers1[1])-init[0][1])/diff_norm[0][1],2)))
	text.insert(INSERT," "*2)
	text.insert(INSERT,abs(round((int(numbers1[2])-init[0][2])/diff_norm[0][2],2)))
	text.tag_add("one", "2.0", "3.200")
	
	text.insert(INSERT,"\n")

	text.insert(INSERT,abs(round((int(numbers2[0])-init[1][0])/diff_norm[1][0],2)))
	text.insert(INSERT," "*2)
	text.insert(INSERT,abs(round((int(numbers2[1])-init[1][1])/diff_norm[1][1],2)))
	text.insert(INSERT," "*2)
	text.insert(INSERT,abs((round((int(numbers2[2])-init[1][2])/diff_norm[1][2],2))))
	
	text.tag_config("one", foreground="black",font=("Courier", 30),background="white")
	
#save into file
def save(a,b):
	global container1
	global container2
	global counter
	global name_file
	
	#read the serial data
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
	
	#saving the data
	time_now1[counter]=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	container1[counter][0] = round((int(numbers1[0])-init[0][0])/diff_norm[0][0],3)
	container1[counter][1] = round((int(numbers1[1])-init[0][1])/diff_norm[0][1],3)
	container1[counter][2] = round((int(numbers1[2])-init[0][2])/diff_norm[0][2],3)
	
	container2[counter][0] = round((int(numbers2[0])-init[1][0])/diff_norm[1][0],3)
	container2[counter][1] = round((int(numbers2[1])-init[1][1])/diff_norm[1][1],3)
	container2[counter][2] = round((int(numbers2[2])-init[1][2])/diff_norm[1][2],3)
	
	#save when 50 measurements are collected
	if counter == 49:
		ser1.reset_input_buffer();
		ser2.reset_input_buffer();
		cob = str(name_file)+".csv"
		name_file = name_file+1
		#file = open(cob,"w")
		file = csv.writer(open(cob, "w",newline=''))
		x = 0
		while x <= counter:
			file.writerow([time_now1[x],container1[x][0],container1[x][1],container1[x][2]])
			file.writerow([" ",container2[x][0],container2[x][1],container2[x][2]])
			#file.writerow([" ",)
			file.writerow([" "," "," "," "])
			x = x +1
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
