import os

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
            full_path = os.path.join(directory_path, filename)
            file_result = parse_cnf_to_string(full_path)
            combined_result = "Please solve the following SAT Problem encoded in DIMACS format, only return a single solution without explanations, if there is any: \n" + file_result + "\n"
            with open(directory_path + "/prompts/" + type_name + "/" + filename + ".txt", "w") as text_file:
                text_file.write(combined_result)

    return True

if __name__ == "__main__":
    directory_path = './SATLIB/uf20-91'
    type_name = "single"
    result_string = process_directory(directory_path, type_name)
    print("Prompt Generation Completed!")
    #print(result_string)