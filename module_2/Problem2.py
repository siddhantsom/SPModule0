#Implementing a basic QnA bot

import os
import openai
import argparse
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')
print(openai.api_key)

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output 
    )
    return response.choices[0].message["content"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type = str)
    args = parser.parse_args()
    response = get_completion(args.prompt)
    print(response)
if __name__ == "__main__":
    main()