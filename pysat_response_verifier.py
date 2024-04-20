import os

from pysat.solvers import Solver
from pysat.formula import CNF

def check_cnf_satisfaction(cnf_file, assignment_str):
    # Load the CNF file
    if assignment_str == "SATISFIABLE" or assignment_str == "UNSATISFIABLE":
        return False
    assignment = parse_assignment(assignment_str)
    cnf = parse_cnf_from_string(parse_cnf_to_string(cnf_file))
    # Create a SAT solver instance
    with Solver(name='cadical153', bootstrap_with=cnf.clauses) as solver:
        # Add the assignment as unit clauses to constrain the solver
        for variable, value in assignment.items():
            solver.add_clause([variable if value else -variable])

        # Check for satisfiability
        is_satisfiable = solver.solve()

    return is_satisfiable

def parse_assignment(assignment_str):
    assignment = {}
    items = assignment_str.split()
    for item in items:
        var = abs(int(item))
        if var == 0:
            continue
        value = int(item) > 0
        assignment[var] = value
    return assignment

def parse_cnf_to_string(filename):
    header = ""
    clause_lines = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('c'):
                continue
            if line.startswith('p'):
                header = line  # captures the "p cnf x y" line
            else:
                # Convert clause line to space-separated values, excluding the trailing 0
                parts = line.split()
                if len(parts) == 0 or parts[-1] == '%':
                    continue
                if len(parts) == 1 and parts[-1] == '0':
                    continue
                clause_lines.append(" ".join(parts))
    clauses_str = "\n".join(clause_lines)
    return f"{header}\n{clauses_str}\n"

def parse_cnf_from_string(cnf_string):
    lines = cnf_string.splitlines()
    clauses = []
    for line in lines:
        line = line.strip()
        if line.startswith('c') or line.startswith('p'):
            continue  # skip comments and the problem line
        # process clause lines
        parts = line.split()
        if parts and parts[-1] == '0':
            clause = [int(literal) for literal in parts[:-1]]
            clauses.append(clause)

    cnf = CNF()
    cnf.extend(clauses)
    return cnf

if __name__ == "__main__":

    #model = "gpt-3.5-turbo"
    model = "gpt-4"
    sat_path = './Generated3SAT/'
    problem_set_path = 'uf3-2/'
    prompt_path = sat_path + problem_set_path
    #type_name = '/msg-single-uf20-20/'
    type_name = '/msg/'

    solution_results = []
    correct_count = 0

    for filename in os.listdir(prompt_path + model + type_name):
        if filename.endswith(".txt"):
            cnf_name = filename[:-len(".txt")]
            full_path = os.path.join(prompt_path + model + type_name, filename)
            with open(full_path, 'r') as file:
                solution = file.readline().strip()
            #print(solution)
            cnf_path = prompt_path + cnf_name + ".cnf"
            satisfied = check_cnf_satisfaction(cnf_path, solution)
            solution_results.append(satisfied)
            if satisfied:
                correct_count += 1

    accuracy = correct_count / len(solution_results)
    print(f"The Accuracy of model {model} is {accuracy} ({correct_count} / {len(solution_results)})")
