import os

from pysat.solvers import Solver
from pysat.formula import CNF
import matplotlib.pyplot as plt
import numpy as np


def plot_bar_chart_with_line_and_annotations(L, L2, K, xlabels):
    # Number of bars for each group
    n = len(L)
    index = np.arange(n)  # Array of indices

    # Width of a bar
    bar_width = 0.35

    # Create a figure and a set of subplots.
    fig, ax = plt.subplots()

    # Create bar charts for L and L2
    bars1 = ax.bar(index - bar_width / 2, L, bar_width, color='blue', label='gpt-3.5-turbo')
    bars2 = ax.bar(index + bar_width / 2, L2, bar_width, color='green', label='gpt-4')

    # Draw a red dotted horizontal line at the height of K
    ax.axhline(y=K, color='red', linestyle='dotted', label=f'Amount of Problems')

    # Annotate each bar with Lx / K for L and L2
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ratio = height / K
            ax.annotate(f'{ratio:.2f}',  # Formatting the ratio to 2 decimal places
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # Offset text by 3 points vertically
                        textcoords="offset points",
                        ha='center', va='bottom')

    # Adding labels and title
    ax.set_xlabel('3-SAT Problem')
    ax.set_ylabel('Number of Problems Solved')
    ax.set_title('GPT Model Performance in solving SAT problems with standard prompts')
    ax.set_xticks(index)
    ax.set_xticklabels(xlabels)  # Optional: set custom x-tick labels
    ax.legend(loc='upper right')
    #ax.legend(loc='lower right')

    # Show the plot
    plt.show()

def check_cnf_satisfaction(cnf_file, assignment_str):
    # Load the CNF file
    if assignment_str == "SATISFIABLE" or assignment_str == "UNSATISFIABLE":
        return False
    assignment = parse_assignment(assignment_str)
    if len(assignment) == 0:
        return False
    cnf = parse_cnf_from_string(parse_cnf_to_string(cnf_file))
    # Create a SAT solver instance
    with Solver(name='cadical153', bootstrap_with=cnf.clauses) as solver:
        #print(solver.solve())
        # Add the assignment as unit clauses to constrain the solver
        for variable, value in assignment.items():
            solver.add_clause([variable if value else -variable])

        # Check for satisfiability
        is_satisfiable = solver.solve()

    return is_satisfiable

def parse_assignment(assignment_str):
    assignment = {}
    items = assignment_str.split()
    #print(items[0:3])
    new_items = []
    for item in items:
        if item.isnumeric():
            new_items.append(item)
        elif len(item) > 1 and item[0] == "-" and item[1:].isnumeric():
            new_items.append(item)
    for item in new_items:
        var = abs(int(item))
        if var == 0:
            continue
        value = int(item) > 0
        assignment[var] = value
    #if assignment_str == "1 -1 2 1 3 1 4 1 5 1":
    #    print(assignment)
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

def parse_weight(s):
    """Extract x and y from the string formatted as 'uf-{x}-{y}' and calculate their weight."""
    parts = s.split('-')
    x = int(parts[0][2:])
    y = int(parts[1])
    return x * 100 + y

def sort_strings(strings):
    """Sort the list of strings based on the weight calculated from each string."""
    return sorted(strings, key=parse_weight)

if __name__ == "__main__":

    models = ["gpt-3.5-turbo", "gpt-4"]
    sat_path = './Generated3SAT/'
    #problem_set_path = 'uf3-2/'
    #prompt_path = sat_path + problem_set_path
    #type_name = '/msg-single-uf20-20/'
    prompt_type = 'single-2'
    type_name = '/' + prompt_type + '/msg/'
    keywords = [
        #"uf3",
        #"uf5",
        "uf10",
    ]

    gpt3_result = []
    gpt4_result = []
    problems_included = []
    amount_problems = 5

    for entry in os.listdir(sat_path):
        full_sat_path = os.path.join(sat_path, entry)
        if os.path.isdir(full_sat_path):
            problems_included.append(entry)

    problems_included = sort_strings(problems_included)
    labels_to_include = []

    for entry in problems_included:
        for keyword in keywords:
            if keyword in entry:
                labels_to_include.append(entry)
                break

    for entry in labels_to_include:
        problem_set_path = entry + '/' #'uf3-2/'
        prompt_path = sat_path + problem_set_path
        print("Dealing with " + entry)
        for model in models:
            solution_results = []
            correct_count = 0
            problem_count = 0
            for filename in os.listdir(prompt_path + model + type_name):
                if filename.endswith(".txt"):
                    cnf_name = filename[:-len(".txt")]
                    full_path = os.path.join(prompt_path + model + type_name, filename)
                    with open(full_path, 'r') as file:
                        #solution = file.readline().strip()
                        solution = file.read().strip()
                    #print(solution)
                    cnf_path = prompt_path + cnf_name + ".cnf"
                    satisfied = check_cnf_satisfaction(cnf_path, solution)
                    #if not satisfied:
                    #    print(solution)
                    solution_results.append(satisfied)
                    problem_count += 1
                    if satisfied:
                        correct_count += 1
                    if problem_count >= amount_problems:
                        break
            if model == "gpt-3.5-turbo":
                gpt3_result.append(correct_count)
            elif model == "gpt-4":
                gpt4_result.append(correct_count)
            accuracy = correct_count / len(solution_results)
            #print(f"The Accuracy of model {model} is {accuracy} ({correct_count} / {len(solution_results)})")
    plot_bar_chart_with_line_and_annotations(gpt3_result, gpt4_result, amount_problems, labels_to_include)



