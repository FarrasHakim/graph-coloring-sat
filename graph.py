import subprocess
import os
import eel

eel.init("web")

class GraphColoring:
    def __init__(self, variables, domains, constraints):
        self.literals = {}
        self.cnf = ""
        self.model = []
        self.arr_variables = variables
        self.arr_domains = domains
        self.arr_constraints = constraints

    def generate_literals(self):
        count = 1
        for variable in self.arr_variables:
            for domain in self.arr_domains:
                self.literals[variable + "_" + domain] = str(count)
                count += 1

    def graph_coloring_to_cnf(self):
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

    def submit_data(self):
        self.generate_literals()
        is_cnf_generated = self.graph_coloring_to_cnf()
        result = ""
        if (is_cnf_generated):
            self.write_to_cnf_file()
            self.parse_model()
            if (self.is_satisfiable()):
                result = self.translate_literal()
                
        return result

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
        result = ""
        for literal in self.model:
            if("-" not in literal):
                result += self.get_key_by_value(literal) + " "
        return result

    def get_key_by_value(self, value_to_find):
        key_list = list(self.literals.keys())
        val_list = list(self.literals.values())
        pos = val_list.index(value_to_find)
        return key_list[pos]

@eel.expose
def color_the_graph(variables, domains, constraints):
    graph = GraphColoring(variables, domains, constraints)
    return graph.submit_data()

eel.start("index.html", size=(1000, 600))