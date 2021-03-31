import tkinter as tk

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 400, height = 300)
canvas1.pack()

variables_label = tk.Label(root, text= "Variables : ")
canvas1.create_window(80, 80, window=variables_label)
variables_input = tk.Entry (root) 
canvas1.create_window(200, 80, window=variables_input)

domains_label = tk.Label(root, text= "Domains : ")
canvas1.create_window(80, 110, window=domains_label)
domains_input = tk.Entry (root) 
canvas1.create_window(200, 110, window=domains_input)

constraints_label = tk.Label(root, text= "Constraints : ")
canvas1.create_window(80, 140, window=constraints_label)
constraints_input = tk.Entry (root) 
canvas1.create_window(200, 140, window=constraints_input)

def submitData ():  
    x1 = variables_input.get()  
    x2 = domains_input.get()  
    x3 = constraints_input.get()
    
    label1 = tk.Label(root, text= str(x1) + "," + str(x2) + "," + str(x3))
    canvas1.create_window(200, 230, window=label1)
    
submit_button = tk.Button(text='Submit', command=submitData)
canvas1.create_window(200, 180, window=submit_button)

root.mainloop()