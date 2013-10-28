from Tkinter import *
import tkFileDialog
import sys
import os

'''
  will hopefully be a list making program
  should diplay checkboxes next to lines of text and allow them to be checked
'''	
	
def toggleCheck():
	for i in range(len(checkvariables)):
		if displayed[i] != checkvariables[i].get():
			if checkvariables[i].get() == 1:
				displayed[i] = 1
				english_list[i] = str(word_list[i].get(1.0, END))
				word_list[i].delete(1.0, END)
				word_list[i].insert(END, japanese_list[i])
			else:
				displayed[i] = 0
				japanese_list[i] = str(word_list[i].get(1.0, END))
				word_list[i].delete(1.0, END)
				word_list[i].insert(END, english_list[i])

# saves data in specific format, using given file path
def save(filename):
	global rownumber
	# make sure the word lists are up to date
	for i in range(len(checkvariables)):
		if displayed[i] == 0:
			english_list[i] = str(word_list[i].get(1.0, END))
		else:
			japanese_list[i] = str(word_list[i].get(1.0, END))
	# save the data into a file
	if filename != '':
		data = str(rownumber) + "\n"
		for i in range(len(checkvariables)):
			data += str(i) + ": "
			data += str(checkvariables[i].get()) + ", "
			data += english_list[i] + ", "
			data += japanese_list[i] + "\n"
		file = open(filename, 'w')
		file.write(data)
		file.close()

#will open a dialogue box asking the user where to save the file
#will then save it in a specific format it will decipher later
def saveAsText():
	#print "save"
	global currentsave
	filename = tkFileDialog.asksaveasfilename(defaultextension='.cjl', initialfile="vocab.cjl", title="Save")
	currentsave = filename
	save(filename)
	
def saveText(event=None):
	global currentsave
	if currentsave != None:
		save(currentsave)
	else:
		saveAsText()
	
# will open and parse a given file
def openFile(filename):
	global currentsave
	currentsave = filename
	file = open(filename)
	for line in file:
		if line.isspace():
			continue
		if line.find(':') == -1:
			continue
		part = line.partition(': ')
		part2 = part[2].partition(', ')
		part3 = part2[2].partition(', ')
		i = int(part[0])
		english_list[i] = part3[0]
		japanese_list[i] = part3[2]
		word_list[i].insert(END, english_list[i])
		if int(part2[0]) == 1:
			check_list[i].invoke()
	file.close()
	
# will open a dialogue box asking the user what file to open
# will check that the file is in the correct format
# will recreate the state of the widgets as the file dictates
def loadText():
	#print "load"
	filename = tkFileDialog.askopenfilename(defaultextension=".cjl", title="Open")
	openFile(filename)
	
def addLine(event=None):
	global rownumber, checkvariables, jap_list, eng_list
	x = IntVar()				# create a variable to contain the state of the corresponding
	checkvariables.append(x)	# ... checkbutton
	displayed.append(0)
	y = Checkbutton(screen, text = '', variable = checkvariables[rownumber], command = toggleCheck)
	check_list.append(y)
	b = Text(screen, height = 2, width = 30, wrap = WORD)		# add a textbox where the user can write their goal
	word_list.append(b)
	english_list.append("")
	japanese_list.append("")
	check_list[rownumber].grid(row=rownumber, column=0)
	word_list[rownumber].grid(row=rownumber, column=1, sticky=W+E+N+S, padx=2)
	screen.rowconfigure(rownumber, weight=1)
	rownumber += 1
	
def removeLine(event=None):
	global rownumber, checkvariables, check_list, word_list
	checkvariables.pop()
	check_list.pop().grid_forget()
	word_list.pop().grid_forget()
	rownumber -= 1

# gives the next widget focus - called when tab is pressed
def nextWidget(event):
	currentFocus = screen.focus_get()
	newFocus = currentFocus.tk_focusNext()
	newFocus.focus_set()
	
#sys.stdout = open(os.devnull, 'w')
screen = Tk()


# create a menu attached to the top of the window
top = screen.winfo_toplevel()
menuBar = Menu(top)
top["menu"] = menuBar

# create the drop down and add items to it
dropMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="File", menu=dropMenu)
dropMenu.add("command", label="save - Ctrl+s", command=saveText)
dropMenu.add("command", label="save as", command=saveAsText)
dropMenu.add("command", label="load", command=loadText)
dropMenu.add("command", label="add line - Ctrl+shift+n", command=addLine)
dropMenu.add("command", label="remove line - Ctrl+shift+d", command=removeLine)


# create a grid of checkboxes followed by text boxes
# when you select the checkbox it changes the formattting of the
#  text in the adjacent textbox
check_list = []
checkvariables = []
displayed = []
word_list = []
english_list = []
japanese_list = []
rownumber = 5
currentsave = None
# if opened from file determine number of rows
if len(sys.argv) > 1:
	file = sys.argv[1]
	openfile = open(file)
	string = openfile.readline()
	string.strip(' \n.')
	rownumber = int(string)
	#print repr(rownumber)
	openfile.close()
	

for i in range(rownumber):
	x = IntVar()				# create a variable to contain the state of the corresponding
	checkvariables.append(x)	# ... checkbutton
	displayed.append(0)
	y = Checkbutton(screen, text = '', variable = checkvariables[i], command = toggleCheck)
	check_list.append(y)
	b = Text(screen, height = 2, width = 30, wrap = WORD)		# add a textbox where the user can write the words
	word_list.append(b)
	english_list.append("")
	japanese_list.append("")
	check_list[i].grid(row=i, column=0)
	word_list[i].grid(row=i, column=1, sticky=W+E+N+S, padx=2, pady=1)
	screen.rowconfigure(i, weight=1)
screen.columnconfigure(1, weight=1)

	
# load in data from the file
if len(sys.argv) > 1:
	file = sys.argv[1]
	openFile(file)

# bind events to the application
screen.unbind_class('Text', '<Tab>')	#override standard tab effect
screen.bind_all('<Tab>', nextWidget)	# move to next widget when tab is pressed
screen.bind_all('<Control-KeyPress-s>', saveText)	# save when control s is pressed
screen.bind_all('<Control-KeyPress-N>', addLine)	# shortcut to add an extra line
screen.bind_all('<Control-KeyPress-D>', removeLine)	# shortcut to remove the last line

screen.mainloop()




