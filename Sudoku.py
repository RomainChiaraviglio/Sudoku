from tkinter import *
import tkinter.font as font
import tkinter as tk
import random
from timeit import default_timer
from tkinter import messagebox

root = Tk() #First thing to do
root.title("Sudoku")

myFont = font.Font(family='Calibri', size=21)
myFont2 = font.Font(family='Calibri bold', size=12)

class ent(tk.Entry): #class to create the entries
    def __init__(self, master=None, max_len=1): #
        self.var = tk.StringVar() #on implémente une variable string que l'on pourra surveiller dans chaque entry
        self.max_len = max_len
        tk.Entry.__init__(self, master, textvariable=self.var, width=3, justify='center')
        self.old_value = '' #on défini notre variable de blocage en cas de remplissage non autorisé, initiée nulle car notre cellule est vide
        self.var.trace('w', self.check) #trace(mode, callback) MODE is one of "r", "w", "u" for read, write, undefine. CALLBACK must be a function which is called when the variable is read, written or undefined.

    def check(self, *args):
        if len(self.get()) <= self.max_len and (self.get().isnumeric() or self.get()==""): #si le remplissage est sup à 2 et est numéric ou null
            self.old_value = self.get() # alors on accepte le changement
        else:
            self.var.set(self.old_value) # sinon on oblige la cellule à rester égale à la valeur précédente

        #vérification que le chiffre entré correspond à la solution
        if self.get()==str(soluce[self.grid_info()['column']+9*self.grid_info()['row']]):
        	self.configure(fg='green')
        elif self.get()!="":
        	self.configure(fg='red')
        	global error
        	error.set(int(error.get())+1)

        if soluce.count('')==0:
        	if verification():
         		message()


r=0 #row counter
c=0 #column counter
count=0
entries = [] #list of entries

for i in range(1,82):
	i=ent(root, max_len=1)
	if count%9 ==0: #reseting the column on reaching the 9th position
		c=0
	i.grid(row=r, column=c)
	count+=1
	c+=1
	r=int(count/9) #incrementing a new row on reaching the 9th position
	i['font'] = myFont
	entries.append(i)


def trouvevide(li):
	i = 1
	for l in li:
		if l =="":
			return (int(i/9.1),(i-9*int(i/9.1)-1))
		i+=1
	return None

#list with each entry position in each square
carré=[[0,1,2,9,10,11,18,19,20],[3,4,5,12,13,14,21,22,23],[6,7,8,15,16,17,24,25,26],[27,28,29,36,37,38,45,46,47],[30,31,32,39,40,41,48,49,50],[33,34,35,42,43,44,51,52,53],[54,55,56,63,64,65,72,73,74],[57,58,59,66,67,68,75,76,77],[60,61,62,69,70,71,78,79,80]]

def carre(pos): #function to find in wich square with the given position
	for c in carré:
		if (pos[1]+9*pos[0]) in c:
			return c

def validation(lis,num,pos):
	#verification ligne
	for r in range(9):
		if lis[r+9*pos[0]]==(num):
			return False

	#verification colonne
	for r in range(9):
		if lis[pos[1]+9*r]==(num):
			return False

	#verification carré
	car = carre(pos)
	for c in car:
		if lis[c]==(num):
			return False
	return True

def resolve(lis):
	if not trouvevide(lis):
		return True
	else: 
		row,col = trouvevide(lis)
	for n in range(1,10):
		if validation(lis,n,(row,col)):
			lis[col+9*row]=n
			if resolve(lis):
				return True
			lis[col+9*row]=""
	return False


def creation():
	global start
	start = default_timer()

	x = difficulty.get()
	crea=[1,2,3,4,5,6,7,8,9]
	random.shuffle(crea)
	for i in range(72):
		crea.append("")
	resolve(crea)

	if x == "Facile":
		while crea.count('')<40:
			crea[random.randint(0,80)]=""
		return crea
	elif x == "Intermédiaire":
		while crea.count('')<50:
			crea[random.randint(0,80)]=""
		return crea
	elif x == "Difficile":
		while crea.count('')<55:
			crea[random.randint(0,80)]=""
		return crea

def generation():
	global error
	error.set(0)
	c = 0 
	global soluce
	soluce=creation()
	for e in entries:
		e.configure(state='normal')
		e.delete(0)
		e.insert(0,soluce[c])
		c+=1
		if e.get()!="":
			e.configure(state='disabled')
	resolve(soluce)
	chrono()

def verification():
	for e in entries:
		if e.get()=="" or e.get()!=str(soluce[e.grid_info()['column']+9*e.grid_info()['row']]):
			return False
	return True


def resolving():
	c = 0
	for e in entries:
		e.delete(0)
		e.insert(0,soluce[c])
		c+=1


def chrono():
	now = default_timer() - start
	minutes, seconds = divmod(now,60)
	str_time = "%02d:%02d"%(minutes,seconds)
	mylabtime.configure(text=str_time)
	root.after(1000,chrono)

start = default_timer()

def message():
	msg =Tk()
	msg.eval('tk::PlaceWindow %s center' % msg.winfo_toplevel())
	msg.withdraw()
	messagebox.showinfo('Victory !',"Partie terminée en "+ mylabtime["text"] + " et " + error.get() + " erreurs")
	msg.deiconify()
	msg.destroy()

mybuttonresou = Button(root, text="Résoudre", command=resolving, padx=10)
mybuttonresou.grid(row = 9, column =7, columnspan=2)

difficulty = tk.StringVar()
difficulty.set("Facile") # default value
diff=OptionMenu(root, difficulty, "Facile", "Intermédiaire", "Difficile")
diff.grid(row = 9, column =2, columnspan=3, sticky="W")

mybuttongene = Button(root, text="Lancer", command=generation,padx=20) 
mybuttongene.grid(row = 9, column =5, columnspan=2)

mylabdiff=Label(root, text="Difficulté :")
mylabdiff.grid(row = 9, column =0, columnspan=2)

mylabtimer=Label(root, text="Timer :")
mylabtimer.grid(row = 10, column =0, columnspan=2)

mylabtime=Label(root, text="00:00")
mylabtime.grid(row = 10, column =2, columnspan=2, sticky="W")

mylaberror=Label(root, text="nb erreurs :")
mylaberror.grid(row = 10, column =5, columnspan=2)

error = tk.StringVar()
error.set(0)
mylaberr=Label(root, textvariable=error)
mylaberr.grid(row = 10, column =7)


mybuttonresou['font'] = myFont2
mybuttongene['font'] = myFont2
mylabdiff['font'] = myFont2
diff['font'] = myFont2
mylabtimer['font'] = myFont2
mylabtime['font'] = myFont2
mylaberror['font'] = myFont2
mylaberr['font'] = myFont2

# Création des bordures
mylbalx1=Label(root, bg="black", padx=0.4, pady=11)
mylbalx2=Label(root, bg="black", padx=0.4, pady=11)
mylbalx3=Label(root, bg="black", padx=0.4, pady=11)
mylbalx4=Label(root, bg="black", padx=0.4, pady=11)
mylbalx5=Label(root, bg="black", padx=0.4, pady=11)
mylbalx6=Label(root, bg="black", padx=0.4, pady=11)
mylbalx7=Label(root, bg="black", padx=0.4, pady=11)
mylbalx8=Label(root, bg="black", padx=0.4, pady=11)
mylbalx9=Label(root, bg="black", padx=0.4, pady=11)
mylbalx10=Label(root, bg="black", padx=0.4, pady=11)
mylbalx11=Label(root, bg="black", padx=0.4, pady=11)
mylbalx12=Label(root, bg="black", padx=0.4, pady=11)
mylbalx13=Label(root, bg="black", padx=0.4, pady=11)
mylbalx14=Label(root, bg="black", padx=0.4, pady=11)
mylbalx15=Label(root, bg="black", padx=0.4, pady=11)
mylbalx16=Label(root, bg="black", padx=0.4, pady=11)
mylbalx17=Label(root, bg="black", padx=0.4, pady=11)
mylbalx18=Label(root, bg="black", padx=0.4, pady=11)
mylbalx19=Label(root, bg="black", padx=0.4, pady=11)
mylbalx20=Label(root, bg="black", padx=0.4, pady=11)
mylbalx21=Label(root, bg="black", padx=0.4, pady=11)
mylbalx22=Label(root, bg="black", padx=0.4, pady=11)
mylbalx23=Label(root, bg="black", padx=0.4, pady=11)
mylbalx24=Label(root, bg="black", padx=0.4, pady=11)
mylbalx25=Label(root, bg="black", padx=0.4, pady=11)
mylbalx26=Label(root, bg="black", padx=0.4, pady=11)
mylbalx27=Label(root, bg="black", padx=0.4, pady=11)
mylbalx28=Label(root, bg="black", padx=0.4, pady=11)
mylbalx29=Label(root, bg="black", padx=0.4, pady=11)
mylbalx30=Label(root, bg="black", padx=0.4, pady=11)
mylbalx31=Label(root, bg="black", padx=0.4, pady=11)
mylbalx32=Label(root, bg="black", padx=0.4, pady=11)
mylbalx33=Label(root, bg="black", padx=0.4, pady=11)
mylbalx34=Label(root, bg="black", padx=0.4, pady=11)
mylbalx35=Label(root, bg="black", padx=0.4, pady=11)
mylbalx36=Label(root, bg="black", padx=0.4, pady=11)

mylbalx1.grid(row=0,column=0,sticky="W")
mylbalx2.grid(row=1,column=0,sticky="W")
mylbalx3.grid(row=2,column=0,sticky="W")
mylbalx4.grid(row=3,column=0,sticky="W")
mylbalx5.grid(row=4,column=0,sticky="W")
mylbalx6.grid(row=5,column=0,sticky="W")
mylbalx7.grid(row=6,column=0,sticky="W")
mylbalx8.grid(row=7,column=0,sticky="W")
mylbalx9.grid(row=8,column=0,sticky="W")
mylbalx10.grid(row=0,column=3,sticky="W")
mylbalx11.grid(row=1,column=3,sticky="W")
mylbalx12.grid(row=2,column=3,sticky="W")
mylbalx13.grid(row=3,column=3,sticky="W")
mylbalx14.grid(row=4,column=3,sticky="W")
mylbalx15.grid(row=5,column=3,sticky="W")
mylbalx16.grid(row=6,column=3,sticky="W")
mylbalx17.grid(row=7,column=3,sticky="W")
mylbalx18.grid(row=8,column=3,sticky="W")
mylbalx19.grid(row=0,column=6,sticky="W")
mylbalx20.grid(row=1,column=6,sticky="W")
mylbalx21.grid(row=2,column=6,sticky="W")
mylbalx22.grid(row=3,column=6,sticky="W")
mylbalx23.grid(row=4,column=6,sticky="W")
mylbalx24.grid(row=5,column=6,sticky="W")
mylbalx25.grid(row=6,column=6,sticky="W")
mylbalx26.grid(row=7,column=6,sticky="W")
mylbalx27.grid(row=8,column=6,sticky="W")
mylbalx28.grid(row=0,column=8,sticky="E")
mylbalx29.grid(row=1,column=8,sticky="E")
mylbalx30.grid(row=2,column=8,sticky="E")
mylbalx31.grid(row=3,column=8,sticky="E")
mylbalx32.grid(row=4,column=8,sticky="E")
mylbalx33.grid(row=5,column=8,sticky="E")
mylbalx34.grid(row=6,column=8,sticky="E")
mylbalx35.grid(row=7,column=8,sticky="E")
mylbalx36.grid(row=8,column=8,sticky="E")

mylbaly1=Label(root, bg="black", padx=210, pady=0, font = "Verdana 1")
mylbaly2=Label(root, bg="black", padx=210, pady=0, font = "Verdana 1")
mylbaly3=Label(root, bg="black", padx=210, pady=0, font = "Verdana 1")
mylbaly4=Label(root, bg="black", padx=210, pady=0, font = "Verdana 1")
mylbaly1.grid(row=0,column=0,sticky="N", columnspan=9)
mylbaly2.grid(row=3,column=0,sticky="N", columnspan=9)
mylbaly3.grid(row=6,column=0,sticky="N", columnspan=9)
mylbaly4.grid(row=8,column=0,sticky="S", columnspan=9)

root.mainloop()