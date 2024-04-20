import os
import json
import openai
from openai import OpenAI

def load_all_prompts(directory_path, amount):
    cnt = 0
    file_names = []
    all_prompts = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".cnf.txt"):
            full_path = os.path.join(directory_path, filename)
            with open(full_path, 'r', encoding='utf-8') as file:
                prompt = file.read()
                file_names.append(filename)
                all_prompts.append(prompt)
                cnt += 1
                if cnt >= amount:
                    break

    return file_names, all_prompts


if __name__ == "__main__":
    # Retrieve the API key from the environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Set the test prompt
    model = "gpt-4"
    #model = "gpt-3.5-turbo"
    prompt_path = './SATLIB/uf20-91/'
    type_name = 'prompts/single'
    amount_test = 20
    filenames, prompts = load_all_prompts(prompt_path + type_name + '/', amount_test)

    idx = 0
    for prompt in prompts:
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
        filename = prompt_path + model + "/full/" + filenames[idx][:-len(".cnf.txt")] + ".json"
        filename2 = prompt_path + model + "/msg/" + filenames[idx]

        # Write the complex dictionary to a JSON file
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

        with open(filename2, "w") as text_file:
            text_file.write(plain_message)

        print(f"Entire response saved to {filename}")
        idx += 1