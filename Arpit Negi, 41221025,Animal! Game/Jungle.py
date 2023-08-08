from tkinter import *
from PIL import Image, ImageTk
from random import randint
from functools import partial
import pygame
from tkinter import messagebox
count = 0
def window(menu):
    menu.destroy()
    root = Tk()

    root.geometry("1000x600")
    root.title("ANIMAL!")
    root.configure(background="#D96E36")
    pygame.mixer.init()
    pygame.mixer.music.load("GameOn.mp3")
    pygame.mixer.music.play(loops=0)
    
#Picture
    lion_img = ImageTk.PhotoImage(Image.open("Lion.png"))
    tiger_img = ImageTk.PhotoImage(Image.open("Tiger.png"))
    hyena_img = ImageTk.PhotoImage(Image.open("Hyena.png"))
    wolf_img = ImageTk.PhotoImage(Image.open("Wolf.png"))
    leopard_img = ImageTk.PhotoImage(Image.open("Leopard.png"))
    jaguar_img = ImageTk.PhotoImage(Image.open("Jaguar.png"))
    deer_img = ImageTk.PhotoImage(Image.open("Deer.png"))
    zebra_img = ImageTk.PhotoImage(Image.open("Zebra.png"))
    human_img = ImageTk.PhotoImage(Image.open("Human.png"))

#Insert images
    user_label = Label(root,image=lion_img,bg="#D96E36")
    computer_label = Label(root,image=tiger_img,bg="#D96E36")
    user_label.grid(row=1, column=0)
    computer_label.grid(row=1,column=8)

    user = Label(root,text="USER",font=50,bg="#D96E36",fg="white").grid(row=0,column=1)
    computer = Label(root,text="COMPUTER",font=50,bg="#D96E36",fg="white").grid(row=0,column=7)

    userScore = Label(root,text=0,font=100,bg="#D96E36",fg="white")
    computerScore = Label(root,text=0,font=100,bg="#D96E36",fg="white")
    userScore.grid(row=1,column=1)
    computerScore.grid(row=1,column=7)

    msg = Label(root,text="PLAY THE GAME!",font=500,bg="#D96E36",fg="white")
    msg.grid(row=6,column=4)

    choice = ["tiger","wolf","jaguar","unarmed_human1","zebra"]

    def updateMessage(x):
        msg['text'] = x

    def updateUser():
        score = int(userScore["text"])
        score +=1
        userScore["text"] = str(score)

    def updateComputer():
        score = int(computerScore["text"])
        score +=1
        computerScore["text"] = str(score)

    def checkWin(player,computer):
        if(player=="lion"):
            if(computer=="tiger"):
                updateMessage("Both animals survived the fight")
                lion.configure(state=DISABLED)
                choice.remove("tiger")
            else:
                updateMessage("Lion won!")
                updateUser()
                lion.configure(state=DISABLED)   
                choice.remove(computer)

        elif(player=="hyena"):
            if(computer=="tiger"):
                updateMessage("Hyena died!")
                updateComputer()
                hyena.configure(state=DISABLED)
                choice.remove(computer)
            elif(computer=="wolf"):
                updateMessage("Both animals survived the fight")
                hyena.configure(state=DISABLED)
                choice.remove(computer)
            else:
                updateMessage("Hyena won!")
                updateUser()
                hyena.configure(state=DISABLED)
                choice.remove(computer)

        elif(player=="leopard"):
            if(computer=="zebra" or computer=="unarmed_human1"):
                updateMessage("leopard won!")
                updateUser()
                leopard.configure(state=DISABLED)
                choice.remove(computer)
            elif(computer=="jaguar"):
                updateMessage("Both animals survived!")
                leopard.configure(state=DISABLED)
                choice.remove(computer)
            else:
                updateMessage("leopard died!")
                updateComputer()
                leopard.configure(state=DISABLED)
                leopard.configure(state=DISABLED)
                choice.remove(computer)
        elif(player=="unarmed_human"):
            if(computer=="unarmed_human  1"):
                updateMessage("Both animals survived the fight")
                unarmed_human.configure(state=DISABLED)
                choice.remove(computer)

            elif(computer=="zebra"):
                updateMessage("Human won!")
                updateUser()
                choice.remove(computer)
            else:
                updateMessage("Human died!")
                updateComputer()
                unarmed_human.configure(state=DISABLED)
        else:
            if(computer=="zebra"):
                updateMessage("Both animals create peace!")
            else:
                updateMessage("Deer died!")
                updateComputer()
                deer.configure(state=DISABLED)
        get_text(userScore,computerScore)
        

    def updatePicture(x):
    
    #for users
        if(x=="lion"):
            user_label.configure(image=lion_img)
        elif(x=="hyena"):
            user_label.configure(image=hyena_img)
        elif(x=="leopard"):
            user_label.configure(image=leopard_img)
        elif(x=="unarmed_human"):
         user_label.configure(image=human_img)
        elif(x=="deer"):
            user_label.configure(image=deer_img)

        # if(length!=0):
        #for computer
        length = len(choice)
        computerChoice = choice[randint(0,length-1)]
        # else:
        #     get_text(userScore,computerScore)

        if(computerChoice == "tiger"):
            computer_label.configure(image=tiger_img)
        elif(computerChoice == "wolf"):
            computer_label.configure(image=wolf_img)
        elif(computerChoice=="jaguar"):
            computer_label.configure(image=jaguar_img)
        elif(computerChoice=="unarmed_human1"):
            computer_label.configure(image=human_img)
        else:
            computer_label.configure(image=zebra_img)
        checkWin(x,computerChoice)
        
    #Empty labels to fill the gap   
    label1 = Label(root,text="",bg="#D96E36").grid(row=1,column=2)
    label2 = Label(root,text="",bg="#D96E36").grid(row=1,column=3)
    label3 = Label(root,text="",bg="#D96E36").grid(row=1,column=4)
    label4 = Label(root,text="",bg="#D96E36").grid(row=1,column=5)
    label5 = Label(root,text="",bg="#D96E36").grid(row=1,column=6)
#Buttons
    lion = Button(root,width=20,height=2,text="LION",bg="#DE8F3C",fg="white",command=lambda:updatePicture("lion"))
    lion.grid(row=2,column=0)
    tiger = Button(root,width=20,height=2,text="TIGER",bg="#F96815",state=DISABLED,fg="white",command=lambda:updatePicture("tiger"))
    tiger.grid(row=2,column=8)
    hyena = Button(root,width=20,height=2,text="HYENA",bg="#BFA27E",fg="white",command=lambda:updatePicture("hyena"),)
    hyena.grid(row=3,column=0)
    wolf = Button(root,width=20,height=2,text="WOLF",bg="#919494",state=DISABLED,fg="white",command=lambda:updatePicture("wolf"))
    wolf.grid(row=3,column=8)
    leopard = Button(root,width=20,height=2,text="LEOPARD",bg="#CF9800",fg="white",command=lambda:updatePicture("leopard"))
    leopard.grid(row=4,column=0)
    jaguar = Button(root,width=20,height=2,text="JAGUAR",bg="#FAC80F",state=DISABLED,fg="white",command=lambda:updatePicture("jaguar"))
    jaguar.grid(row=4,column=8)
    deer = Button(root,width=20,height=2,text="DEER",bg="#AE6134",fg="white",command=lambda:updatePicture("deer"))
    deer.grid(row=6,column=0)
    zebra = Button(root,width=20,height=2,text="ZEBRA",bg="#0F0F12",state=DISABLED,fg="white",command=lambda:updatePicture("zebra"))
    zebra.grid(row=6,column=8)
    unarmed_human = Button(root,width=20,height=2,text="UNARMED HUMAN1",bg="#8A3C01",fg="white",command=lambda:updatePicture("unarmed_human"))
    unarmed_human.grid(row=5,column=0)
    unarmed_human1 = Button(root,width=20,height=2,text="UNARMED HUMAN2",bg="#8A3C01",state=DISABLED,fg="white",command=lambda:updatePicture("unarmed_human1"))
    unarmed_human1.grid(row=5,column=8)
    def get_text(userScore,computerScore):
        global count
        count = count + 1
        if(count==5):
            if(int(userScore["text"]) > int(computerScore["text"])):
                box = messagebox.showinfo("Winner", "USER won the match")
                root.destroy()
            elif(int(userScore["text"]) < int(computerScore["text"])):
                box = messagebox.showinfo("Winner", "COMPUTER won the match")
                root.destroy()
            else:
                box = messagebox.showinfo("Draw","It's a tie!")
                root.destroy()

def play():
    menu = Tk()
    menu.geometry("600x450")

    menu.title("Welcome to the jungle!")
    img= PhotoImage(file='jungle.png', master= menu)
    img_label= Label(menu,image=img)
    img_label.place(x=0, y=0)
    game = partial(window,menu)
    pygame.mixer.init()
    pygame.mixer.music.load("Start.mp3")
    pygame.mixer.music.play(loops=0)

    head = Button(menu, text="---Welcome to the jungle---",
                  activeforeground='red',
                  activebackground="yellow", bg="red",
                  fg="yellow", width=100, font='summer', bd=5)
 
    B1 = Button(menu, text="Play the game!", command=game,
                activeforeground='red',
                activebackground="yellow", bg="red",
                fg="yellow", width=100, font='summer', bd=5)

    B2 = Button(menu, text="Exit", command=menu.quit, activeforeground='red',
                activebackground="yellow", bg="red", fg="yellow",
                width=100, font='summer', bd=5)
    head.pack(side='top')
    B1.pack(side='top')
    B2.pack(side='top')
    menu.mainloop()

if __name__ == '__main__':
    
    play()
    
#Empty Labels to create spaces
