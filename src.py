import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class GraphColoring:
    def __init__(self):
        self.root= tk.Tk()

    def start(self):
        self.canvas1 = tk.Canvas(self.root, width = 400, height = 300)
        self.canvas1.pack()

        self.variables_label = tk.Label(self.root, text= "Variables : ")
        self.canvas1.create_window(80, 80, window=self.variables_label)
        self.variables_input = tk.Entry (self.root) 
        self.canvas1.create_window(200, 80, window=self.variables_input)

        self.domains_label = tk.Label(self.root, text= "Domains : ")
        self.canvas1.create_window(80, 110, window=self.domains_label)
        self.domains_input = tk.Entry (self.root) 
        self.canvas1.create_window(200, 110, window=self.domains_input)

        self.constraints_label = tk.Label(self.root, text= "Constraints : ")
        self.canvas1.create_window(80, 140, window=self.constraints_label)
        self.constraints_input = tk.Entry (self.root)
        self.canvas1.create_window(200, 140, window=self.constraints_input)

        self.submit_button = tk.Button(text='Submit', command=self.submit_data)
        self.canvas1.create_window(200, 180, window=self.submit_button)
        self.root.mainloop()

    def generate_literals(self):
        self.literals = {}
        count = 1
        for variable in self.arr_variables:
            for domain in self.arr_domains:
                self.literals[variable + "_" + domain] = str(count)
                count += 1

    def graph_coloring_to_cnf(self):
        self.cnf = ""
        for variable in self.arr_variables:
            for domain in self.arr_domains:
                self.cnf += self.literals[variable+"_"+domain] + " "
            self.cnf += "0\n"
            visited1 = []
            for domain1 in self.arr_domains:
                for domain2 in self.arr_domains:
                    if (domain2 in visited1):
                        continue
                    if (domain1 != domain2):
                        self.cnf += "-" + self.literals[variable + "_" + domain1] + " -" + self.literals[variable + "_" + domain2] + " 0\n"
                visited1.append(domain1)
        for domain in self.arr_domains:
            visited2 = []
            for variable1 in self.arr_variables:
                for variable2 in self.arr_variables:
                    is_constrained = False
                    for constraint in self.arr_constraints:
                        if (variable1 in constraint and variable2 in constraint):
                            is_constrained = True
                    if (is_constrained):
                        continue
                    elif (variable2 in visited2):
                        continue
                    if (variable1 != variable2):
                        self.cnf += "-" + self.literals[variable1 + "_" + domain] + " -" + self.literals[variable2 + "_" + domain] + " 0\n"
                visited2.append(variable1)
    
    def write_to_cnf_file(self):
        with open("sat.cnf", "w") as writer:
            writer.write(self.cnf)
            writer.close()
        if (os.name) == "nt":
            os.system('cmd /c minisat sat.cnf result.cnf')
        else:
            print("masuk")
            subprocess.run(["minisat", "sat.cnf", "result.cnf"])

    def submit_data(self):  
        self.arr_variables = self.variables_input.get().split(",")
        self.arr_domains = self.domains_input.get().split(",")
        self.arr_constraints = self.constraints_input.get().split(",")
        self.generate_literals()
        self.graph_coloring_to_cnf()
        self.write_to_cnf_file()
        if (self.read_result()):
            self.translate_literal()
            self.print_answer()
        else:
            self.print_wrong()

    def read_result(self):
        with open("result.cnf") as reader:
            if("UNSAT" in reader.readline()):
                print("UNSATISFIABLE")
                return False
            else:
                temp_model = reader.readline()[:-3]
                self.model = temp_model.split(" ")
                return True
                
    def translate_literal(self):
        self.answer = ""
        print(self.model)
        for literal in self.model:
            if("-" not in literal):
                self.answer += self.get_key_by_value(literal) + " "

    def print_answer(self):
        messagebox.showinfo(title="Model", message=self.answer)

    def get_key_by_value(self, value_to_find):
        print(value_to_find)
        for val in self.literals.items():
            print(val)
            if val[1] == value_to_find:
                return val[0]

graph = GraphColoring()
graph.start()

# Reference
# https://github.com/ahnjaekwan/Graph-coloring-problem-with-SAT-solver/blob/master/SAT_solver_spec.pdf