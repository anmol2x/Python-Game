import tkinter
import random
import sqlite3
from tkinter import messagebox

global score
global timeleft
global user


def create_table():
    con = sqlite3.connect("winners.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS winners(user TEXT,score TEXT)")
    return [con, cur]   # return the created connection


def data_entry(user_nickname, user_score, con, cur):
    cur.execute("INSERT INTO winners values('"+str(user_nickname)+"','"+str(user_score)+"')") # save the user and score
    # in database.
    con.commit()
    cur.close()
    con.close()


def start_game(event):
    if timeleft == 30:
        countdown()
    next_colour()


def next_colour():
    global score
    global timeleft
    if timeleft > 0:
        e.focus_set()
        if e.get().lower() == colours[1].lower():
            score += 1
        e.delete(0, tkinter.END)
        random.shuffle(colours)
        label.config(fg=str(colours[1]), text=str(colours[0]))
        scoreLabel.config(text="Score: " + str(score))
    else:    # if the timeleft is equal to zero, it means that the game is over and we need to save the record in db.
        global user
        messagebox.showinfo("Time Up!", "Your score is : "+str(score))  # message box to show the score.
        con, cur = create_table()   # first of all, call the 'create_table' function. This function will create database
        # connection and execute the query to to create table 'winnings'. After which this function will return the
        # db connection and cursor.

        data_entry(user, score, con, cur) # Once, the table is created, the user and score will be entered in the db.
        root.destroy() # After which the game window will be destroyed.


def countdown():
    global timeleft
    if timeleft > 0:
        timeleft -= 1
        timeLabel.config(text="Time left: "+ str(timeleft))
        timeLabel.after(1000, countdown)


def close_this_window(nickname, window):
    global user
    user = nickname   # save the nickname into global variable 'user'
    # if user field is empty it means that user hasn't entered the nickname. In this case user will be prompted to
    # enter his nickname on message box.
    if user != "":     # if user is empty
        window.destroy()    # quit this window, so that we can move to game window.
    else:
        messagebox.showinfo("Color Game", "Please enter your nickname!")


def ask_user_for_nickname():
    root1 = tkinter.Tk()     # first window
    root1.title("Colour Game")
    root1.geometry("370x190")         # window size
    root1.configure(background="#3b3b3b")
    instructions1 = tkinter.Label(root1, bg='#3b3b3b', text="Type in your nickname and click on Start Game", fg="white", font=12)
    instructions1.pack()
    instructions1.place(x=20, y=20)    # x and y position of 'instuctions1' label on gui.

    entry1 = tkinter.Entry(root1)          # text field for user to enter his/her nickname
    entry1.pack()
    entry1.place(x=115, y=50)    # x and y position of 'entry1' text field on gui.

    # start game button
    button = tkinter.Button(root1, text="Start Game", command=lambda: close_this_window(entry1.get(), root1))
    # on this button click this windowi will be closed, for this purpose, this button is bound with 'close_this_window'
    # function. Whenever this button will be clicked, the 'close_this_window' button will be called.
    # Moreover, 'close_this_window' function will save the nickname (from text field) in the global variable 'user'

    button.pack()
    button.place(x=140, y=80)  # x and y position of button on gui.
    root1.mainloop()


colours = ['Red', 'Blue', 'Green', 'Pink', 'Black', 'Yellow', 'Orange', 'White', 'Purple', 'Brown']
score = 0
timeleft = 30


# Code execution will start from here
ask_user_for_nickname()  # Firstly, this function will ask user to enter nickname which will be saved in 'user'


# At this point, the nickname window will be closed. Now the game should start.
root = tkinter.Tk()   # game window
root.title("Colour Game")
root.geometry("370x190")
root.configure(background="#3b3b3b")


instructions = tkinter.Label(root, bg='#3b3b3b', text="Type in the colour of the words", fg="white", font=12)
instructions.pack()
scoreLabel = tkinter.Label(root, bg='#3b3b3b', text="Score: 0", fg="white", font=('Helvetica', 12))
scoreLabel.pack()
timeLabel = tkinter.Label(root, bg='#3b3b3b', fg="white", text="Time left: " + str(timeleft), font=('Helvetica', 12))
timeLabel.pack()
label = tkinter.Label(root, bg='#3b3b3b', font=('Helvetica', 60))
label.config(fg=str(colours[1]), text=str(colours[0]))
label.pack()
e = tkinter.Entry(root)   # text field to enter the color
root.bind('<Return>', start_game)
e.pack()
root.mainloop()