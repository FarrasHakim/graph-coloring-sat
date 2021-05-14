import subprocess
import os
import eel
import platform
import sys

if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
    pass
else:
    subprocess.run(["sudo", "apt", "install", "-y", "minisat"])


eel.init("web")

class GraphColoring:
    def __init__(self, variables, domains, constraints):
        self.literals = {}
        self.cnf = ""
        self.model_str = ""
        self.model_arr = []
        self.arr_variables = variables
        self.arr_domains = domains
        self.arr_constraints = constraints
        self.generate_literals()

    def generate_literals(self):
        count = 1
        for variable in self.arr_variables:
            for domain in self.arr_domains:
                self.literals[variable + "_" + domain] = str(count)
                count += 1

    def graph_coloring_to_cnf(self):
        if (len(self.arr_variables) == 0 or len(self.arr_domains) == 0):
            return False

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
    
    def runMinisat(self):
        if (os.name) == "nt":
            os.system('cmd /c minisat sat.cnf result.cnf')
        else:
            subprocess.run(["minisat", "sat.cnf", "result.cnf"])

    def parse_model(self):
        with open("result.cnf") as reader:
            if("UNSAT" not in reader.readline()):
                temp_model = reader.readline()[:-3]
                self.model_arr = temp_model.split(" ")

    def parse_new_model(self):
        result = ""
        for literal in self.model_arr:
            if ("-" in literal):
                temp = literal.replace("-", "")
                result += temp + " 0\n"
            else:
                result += "-" + literal + " 0\n"
        self.model_str = result

    def add_result_as_new_constraint(self):
        self.parse_new_model()
        with open("sat.cnf", "a") as writer:
            writer.write(self.model_str)
            writer.close()

    def is_satisfiable(self):
        if (len(self.model_arr) > 0):
            return True
        return False

    def submit_data(self):
        is_cnf_generated = self.graph_coloring_to_cnf()
        if (is_cnf_generated):
            self.write_to_cnf_file()
            return self.find_solution()
        return ""

    def find_solution(self):
        self.runMinisat()
        self.parse_model()
        self.add_result_as_new_constraint()
        if (self.is_satisfiable()):
            return self.translate_literal()
        return ""

    def translate_literal(self):
        result = ""
        for literal in self.model_arr:
            if("-" not in literal):
                result += self.get_key_by_value(literal) + " "
        return result

    def get_key_by_value(self, value_to_find):
        print(self.literals)
        key_list = list(self.literals.keys())
        val_list = list(self.literals.values())
        print(val_list)
        print(value_to_find)
        pos = val_list.index(value_to_find)
        return key_list[pos]

@eel.expose
def color_the_graph(variables, domains, constraints):
    print("color")
    graph = GraphColoring(variables, domains, constraints)
    data = graph.submit_data()
    return data

@eel.expose
def recolor_the_graph(variables, domains, constraints):
    print("recolor")
    graph = GraphColoring(variables, domains, constraints)
    data = graph.find_solution()
    return data

eel.start("index.html", mode="default")
