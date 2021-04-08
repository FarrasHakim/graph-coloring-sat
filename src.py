from tkinter import *
from tkinter import messagebox
import subprocess
import os

class GraphColoring:
    def __init__(self):
        self.root= Tk()
        self.literals = {}
        self.cnf = ""
        self.answer = "Hasil: \n"
        self.model = []

    def start(self):
        self.variables_label_frame = Frame()
        self.variables_label_frame.grid(row=0, column=0)
        self.variables_label = Label(self.variables_label_frame, text= "Variables : ")
        self.variables_label.pack()
        self.variables_input_frame = Frame()
        self.variables_input_frame.grid(row=0, column=1)
        self.variables_input = Entry (self.variables_input_frame)
        self.variables_input.pack()

        self.domains_label_frame = Frame()
        self.domains_label_frame.grid(row=1, column=0)
        self.domains_label = Label(self.domains_label_frame, text= "Domains : ")
        self.domains_label.pack()
        self.domains_input_frame = Frame()
        self.domains_input_frame.grid(row=1, column=1)
        self.domains_input = Entry(self.domains_input_frame)
        self.domains_input.pack()

        self.constraints_label_frame = Frame()
        self.constraints_label_frame.grid(row=2, column=0)
        self.constraints_label = Label(self.constraints_label_frame, text= "Constraints : ")
        self.constraints_label.pack()
        self.constraints_input_frame = Frame()
        self.constraints_input_frame.grid(row=2, column=1)
        self.constraints_input = Entry(self.constraints_input_frame)
        self.constraints_input.pack()

        self.submit_button = Button(text='Submit', command=self.submit_data)
        self.submit_button.grid(row=3, column=0, columnspan=2)
        self.root.mainloop()

    def generate_literals(self):
        count = 1
        for variable in self.arr_variables:
            for domain in self.arr_domains:
                self.literals[variable + "_" + domain] = str(count)
                count += 1

    def graph_coloring_to_cnf(self):
        print(self.literals)
        for variable in self.arr_variables:
            for domain in self.arr_domains:
                self.cnf += self.literals[variable+"_"+domain] + " "
            self.cnf += "0\n"
            visited1 = []
            for domain1 in self.arr_domains:
                for domain2 in self.arr_domains:
                    if (domain2 in visited1):
                        continue
                    elif (domain1 != domain2):
                        self.cnf += "-" + self.literals[variable + "_" + domain1] + " -" + self.literals[variable + "_" + domain2] + " 0\n"
                visited1.append(domain1)
        try:
            for constraint in self.arr_constraints:
                const_variable1 = constraint.split("!=")[0]
                const_variable2 = constraint.split("!=")[1]
                for domain in self.arr_domains:
                    self.cnf += "-" + self.literals[const_variable1 + "_" + domain] + " -" + self.literals[const_variable2 + "_" + domain] + " 0\n"
            return True
        except:
            return False

    def write_to_cnf_file(self):
        with open("sat.cnf", "w") as writer:
            writer.write(self.cnf)
            writer.close()
        if (os.name) == "nt":
            os.system('cmd /c minisat sat.cnf result.cnf')
        else:
            subprocess.run(["minisat", "sat.cnf", "result.cnf"])

    def parse_input_data(self):
        self.arr_variables = self.variables_input.get().split(",")
        self.arr_domains = self.domains_input.get().split(",")
        self.arr_constraints = self.constraints_input.get().split(",")

    def submit_data(self):
        self.parse_input_data()
        self.generate_literals()
        is_cnf_generated = self.graph_coloring_to_cnf()
        if (is_cnf_generated):
            self.write_to_cnf_file()
            self.parse_model()
            if (self.is_satisfiable()):
                self.translate_literal()
                self.print_answer()
            else:
                self.print_wrong()
        else:
            messagebox.showinfo(title="Wrong Input", message="Please check your input! it's may be wrong :)")

    def parse_model(self):
        with open("result.cnf") as reader:
            if("UNSAT" not in reader.readline()):
                temp_model = reader.readline()[:-3]
                self.model = temp_model.split(" ")

    def is_satisfiable(self):
        if (len(self.model) > 0):
            return True
        return False

    def translate_literal(self):
        for literal in self.model:
            if("-" not in literal):
                self.answer += self.get_key_by_value(literal) + "\n"

    def print_answer(self):
        messagebox.showinfo(title="Model", message=self.answer)

    def print_wrong(self):
        messagebox.showinfo(title="No Model", message="Not Satisfiable")

    def get_key_by_value(self, value_to_find):
        key_list = list(self.literals.keys())
        val_list = list(self.literals.values())
        pos = val_list.index(value_to_find)
        return key_list[pos]

graph = GraphColoring()
graph.start()

# Reference
# https://github.com/ahnjaekwan/Graph-coloring-problem-with-SAT-solver/blob/master/SAT_solver_spec.pdf