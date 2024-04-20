import os
import random
from pysat.formula import CNF

def ensure_directory_exists(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        # Create the directory
        os.makedirs(directory_path)
        print(f"Directory created: {directory_path}")
        return True
    else:
        print(f"Directory already exists: {directory_path}")
        return False

def generate_satisfiable_3sat(n, k):
    # Randomly decide the true/false assignment for each variable
    truth_assignment = {i: random.choice([True, False]) for i in range(1, n + 1)}

    cnf = CNF()

    # Generate k clauses, each with exactly 3 distinct variables
    for _ in range(k):
        clause = []
        variables = random.sample(range(1, n + 1), 3)  # Pick 3 unique variables
        for var in variables:
            if random.random() < 0.5:
                # Flip the literal to ensure the clause is satisfiable
                clause.append(var if truth_assignment[var] else -var)
            else:
                # Normal random assignment, might not align with the truth assignment
                clause.append(var if random.choice([True, False]) else -var)

        # Ensure at least one literal aligns with the truth assignment
        # Randomly choose one of the three literals to align for sure
        idx = random.randint(0, 2)
        var = abs(clause[idx])
        clause[idx] = var if truth_assignment[var] else -var

        cnf.append(clause)

    return cnf

if __name__ == "__main__":
    # Example usage
    generate_path = './Generated3SAT/'
    sample_amount = 20
    # Number of variables
    N_low = 10
    N_high = 10
    N_increment = 1
    # Number of clauses
    K_low = 40
    K_high = 100
    K_increment = 5
    for n in range(N_low, N_high + 1, N_increment):
        for k in range(K_low, K_high + 1, K_increment):
            folder_name = 'uf' + str(n) + '-' + str(k)
            missing = ensure_directory_exists(generate_path + folder_name + '/')
            if missing:
                for i in range(0, sample_amount, 1):
                    filename = generate_path + folder_name + '/uf' + str(n) + '-' + str(i + 1) + '.cnf'
                    entire_string = 'p cnf ' + str(n) + ' ' + str(k) + '\n'
                    satisfiable_cnf = generate_satisfiable_3sat(n, k)
                    for clause in satisfiable_cnf.clauses:
                        line = ''
                        for l in clause:
                            line = line + str(l) + ' '
                        line = line + '0\n'
                        entire_string = entire_string + line
                        #print(clause)
                    entire_string = entire_string + '%\n0'
                    with open(filename, "w") as text_file:
                        text_file.write(entire_string)
                print("Generated 3-SAT problems " + folder_name)