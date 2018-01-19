import time
from tkinter import *
import serial
from datetime import datetime
import numpy
import csv

#define the arduino serial address
ser1 = serial.Serial('COM3', 115200, timeout=None)


def onclick():
   pass


name_file = 1
counter = 0

#saving some values before stored in csv file
container1= numpy.zeros((50, 64)) 
time_now1 = ["" for x in range(50)]

#define the windows 
root = Tk()
text = Text(root)
text.pack()
text.config(height=60,width=180)

#clear the buffer
ser1.reset_input_buffer();


def monitor(a):
	text.delete(1.0,END)
	
	#read serial data
	data1 = a.strip()
	numbers1 = data1.split('a')

	#throwing exception
	if len(numbers1) == 60:
			numbers1.extend([0,0,0,0])
	if len(numbers1) == 61:
			numbers1.extend([0,0,0])
	if len(numbers1) == 62:
			numbers1.extend([0,0])
	if len(numbers1) == 63:
			numbers1.extend([0])

	
	#write on the window
	text.insert(INSERT,"\n")
	for x in range (8):
		text.insert(INSERT,numbers1[x])
		text.insert(INSERT," "*2)
	text.insert(INSERT,"\n")
	
	for x in range (8,16):
		text.insert(INSERT,numbers1[x])
		text.insert(INSERT," "*2)
	text.insert(INSERT,"\n")
	
	for x in range (16,24):
		text.insert(INSERT,numbers1[x])
		text.insert(INSERT," "*2)
	text.insert(INSERT,"\n")
	
	for x in range (24,32):
		text.insert(INSERT,numbers1[x])
		text.insert(INSERT," "*2)
	text.insert(INSERT,"\n")
	
	for x in range (32,40):
		text.insert(INSERT,numbers1[x])
		text.insert(INSERT," "*2)
	text.insert(INSERT,"\n")
	
	for x in range (40,48):
		text.insert(INSERT,numbers1[x])
		text.insert(INSERT," "*2)
	text.insert(INSERT,"\n")
	
	for x in range (48,56):
		text.insert(INSERT,numbers1[x])
		text.insert(INSERT," "*2)
	text.insert(INSERT,"\n")
	
	for x in range (56,64):
		text.insert(INSERT,numbers1[x])
		text.insert(INSERT," "*2)
	

	text.tag_add("one", "1.0", "10.50")

	text.tag_config("one", foreground="black",font=("Courier", 44),background="white")
	

def save(a):
	global container1
	global counter
	global name_file
	
	#read serial data
	data1 = a.strip()
	numbers1 = data1.split('a')
	
	#throwing exception
	if len(numbers1) == 60:
			numbers1.extend([0,0,0,0])
	if len(numbers1) == 61:
			numbers1.extend([0,0,0])
	if len(numbers1) == 62:
			numbers1.extend([0,0])
	if len(numbers1) == 63:
			numbers1.extend([0])
		
	time_now1[counter]=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	for x in range(64):
		container1[counter][x] = numbers1[x]


	
	if counter == 49:
		# ser1.reset_input_buffer();
		cob = str(name_file)+".csv"
		name_file = name_file+1
		#file = open(cob,"w")
		file = csv.writer(open(cob, "w",newline=''))
		x = 0
		while x <= counter:
			file.writerow([time_now1[x],container1[x][0],container1[x][1],container1[x][2],container1[x][3],container1[x][4],container1[x][5],container1[x][6],container1[x][7]])
			file.writerow([" ",container1[x][8],container1[x][9],container1[x][10],container1[x][11],container1[x][12],container1[x][13],container1[x][14],container1[x][15]])
			file.writerow([" ",container1[x][16],container1[x][17],container1[x][18],container1[x][19],container1[x][20],container1[x][21],container1[x][22],container1[x][23]])
			file.writerow([" ",container1[x][24],container1[x][25],container1[x][26],container1[x][27],container1[x][28],container1[x][29],container1[x][30],container1[x][31]])
			file.writerow([" ",container1[x][32],container1[x][33],container1[x][34],container1[x][35],container1[x][36],container1[x][37],container1[x][38],container1[x][39]])
			file.writerow([" ",container1[x][40],container1[x][41],container1[x][42],container1[x][43],container1[x][44],container1[x][45],container1[x][46],container1[x][47]])
			file.writerow([" ",container1[x][48],container1[x][49],container1[x][50],container1[x][51],container1[x][52],container1[x][53],container1[x][54],container1[x][55]])
			file.writerow([" ",container1[x][56],container1[x][57],container1[x][58],container1[x][59],container1[x][60],container1[x][61],container1[x][62],container1[x][63]])
			file.writerow([" "," "," "," "," "," "," "," "," "])
			x = x +1
		counter = 0
		
	else:
		counter = counter +1

	
def update_label():
	a = ser1.readline()[:-2] # attempt to read a character from Serial
	a = a.decode('utf-8')
	monitor(a)
	save(a)
	
	#calls update_label function again after 1 millisecond. (1000 milliseconds.)
	root.after(1, update_label)
    

root.after(1, update_label)
root.mainloop()
