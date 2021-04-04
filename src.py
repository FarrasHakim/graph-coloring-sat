import tkinter as tk
import subprocess

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

def graph_coloring_to_cnf(variables, domains, constraints):
    pass

def node_to_var(node_index, color_index, max_color_index):
    # PARAM:
    # node_index (n)
    # color_index (c)
    # max_color_index (k)
    # TODO:
    # return index of propositional variable 
    # that represents the constraint.
    # "node n receives color c"
    # use conversion convention
    # variable index = (n-1)*k + c
    pass

def at_least_one_color(node_index, color_index, max_color_index):
    pass

def at_most_one_color(node_index, color_index, max_color_index):
    pass

def generate_node_clauses(node_index, max_color_index):
    pass

def generate_edge_clauses(edge, max_color_index):
    pass

def submit_data():  
    temp_variables = variables_input.get().split(",")
    temp_domains = domains_input.get().split(",")
    temp_constraints = constraints_input.get().split(",")
    
    graph_coloring_to_cnf(temp_variables, temp_domains, temp_constraints)
    
    # with open("graph.in", "w") as writer:
        # writer.write(temp_variables + "\n")
        # writer.write(temp_domains + "\n")
        # writer.write(temp_constraints)
    # subprocess.run(["minisat", "graph.in graph.out"])
    
submit_button = tk.Button(text='Submit', command=submitData)
canvas1.create_window(200, 180, window=submit_button)

root.mainloop()