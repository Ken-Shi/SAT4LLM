import os
import json
import openai
from openai import OpenAI

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        return False
    return True

def load_all_prompts(directory_path, amount):
    cnt = 0
    file_names = []
    all_prompts = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            full_path = os.path.join(directory_path, filename)
            with open(full_path, 'r', encoding='utf-8') as file:
                prompt = file.read()
                new_filename = filename[:-len(".txt")]
                file_names.append(filename)
                all_prompts.append(prompt)
                cnt += 1
                if cnt >= amount:
                    break

    return file_names, all_prompts

def file_exists(filepath):
    # Check if the filepath exists and is a file
    return os.path.exists(filepath) and os.path.isfile(filepath)

if __name__ == "__main__":
    # Retrieve the API key from the environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Set the test prompt
    models = ["gpt-3.5-turbo", "gpt-4"]
    cnf_path = './Generated3SAT/'
    #type_name = 'prompts/single-2'
    type_cat = 'complex'
    type_name = 'prompts/' + type_cat
    amount_test = 20

    for model in models:
        for entry in os.listdir(cnf_path):
            full_path = os.path.join(cnf_path, entry)
            if os.path.isdir(full_path):
                problem_set_path = entry + '/' #'uf3-2/'
                prompt_path = cnf_path + problem_set_path
                #prompt_path = full_path + '/'
                filenames, prompts = load_all_prompts(prompt_path + type_name + '/', amount_test)
                ensure_directory_exists(prompt_path + model)
                ensure_directory_exists(prompt_path + model + '/' + type_cat)
                ensure_directory_exists(prompt_path + model + '/' + type_cat + "/full/")
                ensure_directory_exists(prompt_path + model + '/' + type_cat + "/msg/")

                idx = 0
                for prompt in prompts:
                    generated = file_exists(prompt_path + model + '/' + type_cat + "/msg/" + filenames[idx])
                    if generated:
                        idx += 1
                        continue
                    else:
                        # Use the API for a request
                        client = OpenAI()
                        response = client.chat.completions.create(
                            model=model,
                            messages=[{"role": "user", "content": prompt}],
                        )

                        plain_message = response.choices[0].message.content

                        # Serialize the response to JSON
                        data = {
                            "id": response.id,
                            "object": response.object,
                            "created": response.created,
                            "model": response.model,
                            "system_fingerprint": response.system_fingerprint,
                            "choices": [{

                              }],
                            "usage": {
                                "prompt_tokens": response.usage.prompt_tokens,
                                "completion_tokens": response.usage.completion_tokens,
                                "total_tokens": response.usage.total_tokens
                            }
                        }
                        for choice in response.choices:
                            a_choice = {
                                "index": choice.index,
                                "message": {
                                    "role": choice.message.role,
                                    "content": choice.message.content,
                                },
                                "logprobs": choice.logprobs,
                                "finish_reason": choice.finish_reason
                            }
                            data["choices"].append(a_choice)

                        # Specify filename
                        filename = prompt_path + model + '/' + type_cat + "/full/" + filenames[idx] + ".json"
                        filename2 = prompt_path + model + '/' + type_cat + "/msg/" + filenames[idx]

                        # Write the complex dictionary to a JSON file
                        with open(filename, 'w') as file:
                            json.dump(data, file, indent=4)

                        with open(filename2, "w", encoding='ascii', errors='replace') as text_file:
                            text_file.write(plain_message)

                        print(f"Entire response saved to {filename}")
                        idx += 1