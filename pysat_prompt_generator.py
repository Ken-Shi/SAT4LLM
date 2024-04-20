import os

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

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

def process_directory(directory_path, type_name="plain"):
    for filename in os.listdir(directory_path):
        combined_result = ""
        if filename.endswith(".cnf"):
            new_filename = filename[:-len(".cnf")]
            full_path = os.path.join(directory_path, filename)
            file_result = parse_cnf_to_string(full_path)
            # Single-2:
            #combined_result = "Please solve the following SAT Problem encoded in DIMACS format, only return a single solution assignment without explanations, if there is any: \n" + file_result + "\n"
            # Complex:
            combined_result = "Please solve the following SAT Problem encoded in DIMACS format, provide line of thoughts, write your final answer as a single solution at the end of response with header 'answer: ' : \n" + file_result + "\n"
            ensure_directory_exists(directory_path + "/prompts/")
            ensure_directory_exists(directory_path + "/prompts/" + type_name + "/")
            with open(directory_path + "/prompts/" + type_name + "/" + new_filename + ".txt", "w") as text_file:
                text_file.write(combined_result)

    return True

if __name__ == "__main__":
    directory_path = './Generated3SAT/'
    type_name = "complex"
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        if os.path.isdir(full_path):
            #print(full_path)
            result_string = process_directory(full_path, type_name)
            print("Prompt Generation Completed for " + entry)
    #print(result_string)