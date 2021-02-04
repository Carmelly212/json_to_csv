import json
import time
import ast
from tkinter import *
from tkinter import ttk
from tkinter import filedialog



interface = Tk()
TodaysDate = time.strftime("%d-%b-%R")
interface.geometry("480x400+200+200")
interface.title("Json to CSV converter")
mylabel = Label(interface, text="CONVERT AND REFORMAT JSON TO CSV", font = "verdana 15 bold",padx=8, pady=5,justify="center")
mylabel2 = Label(interface, text="please select file to a convert", font = "verdana 12 ",wraplength=300, justify="center")
mylabel3 = Label(interface, text="",fg = "red",font = "verdana 14 bold",wraplength=300, justify="center")



mylabel.grid(row=6, column=1)
mylabel2.grid(row=10, column=1)

box = []
def openfile():
    tf = filedialog.askopenfile()
    box.append(tf.name)
    mylabel4 = Label(interface, text=str(box[0]), font="verdana 9 bold",wraplength=400, justify="center")
    mylabel4.grid(row=12, column=1)
    mylabel3.grid(row=13, column=1)
    button2 = ttk.Button(interface, text="RUN CONVERTER", command=quit)
    button2.grid(column=1, row=15, columnspan=2, padx=1, pady=1)

def quit():
    interface.destroy()



button = ttk.Button(interface, text="Click here to select file", command=openfile) # <------
button.grid(column=1, row=11, columnspan=2,padx=10, pady=50)


interface.mainloop()

# This script converts and reformat special JSON file to csv
nice = (str(box[0]))
# The name of the input file
in_file = nice
new_list = ""


# This function reads the input Json and returns a string
def read_data_file():
    text = ""
    try:
        f = open(in_file)
        text = f.read()
        f.close()
    except IOError as e:
        print("Could not find input file:", in_file)
        print(e)
        exit(1)

    return text


# Get the data from the file
string = read_data_file()

# The following code fixes the input format
w1 = '"day"'
w2 = "]"
results = []
event_list = []
postfixes = string.split(w1)
for postfix in postfixes[1:]:
    results=('{' + w1+postfix.split(w2)[0]+']}').replace("\n","").replace("\t","").replace("}]}}]}","}]}")
    event_list.append(results)


# Change the data to CSV format
def chng_data_format_csv(event):
    master = ""
    # Comma Separated Values
    # date, hour, user
    new_cvs = ""
    first_flag = True
    for entry in event['hourly_scores']:
        for hour, user in entry.items():
            user = (float(user) * 100)
            if first_flag:
                new_csv = f"{event['day']}, {hour}, {user}%\n"
                first_flag = False
            else:
                new_csv = f", {hour}, {user}%\n"

        master += new_csv

    # print("master =", master)
    return master

global globalBox
globalBox = []

# This function gets the json data and
# saves it to output file (updated_XXXX.csv)
def save_to_file(data):
    out_file = in_file.replace('.json', '_'+'UPDATED.csv')
    globalBox.append(str(out_file))

    try:
        fo = open(out_file, "w+")
        # WRITE A HEADER
        fo.write("Date, Hour, User Satisfaction, Event\n\n")
        data = str(data).replace("'", '"')
        fo.write(data)
        fo.close()
    except IOError as e:
        print("Could not save updated file:", out_file)
        print(e)
        exit(1)

    print(f"\nJSON SUCCESSFULLY CONVERTED TO CSV \n+++++++++++++++++++++++++++++++++++++++\nFlie is located at the same folder as the source\n+++++++++++++++++++++++++++++++++++++++\n({out_file})")


# Iterate over all the events and format data
for day in event_list:
    temp = chng_data_format_csv(ast.literal_eval(day))
    new_list += temp

# Save the data to CSV file
save_to_file(new_list)

new_file_name = str(globalBox[0])
sliced_name = new_file_name.split("/")


