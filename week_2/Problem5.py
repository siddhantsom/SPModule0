#Sentiment analysis using openai api

import openai
import os
import argparse
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

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
    parser.add_argument("--text", type = str, help="Text to be analysed")
    args = parser.parse_args()
    with open(args.text, "r") as file:
        text = file.read().strip()
    
    prompt = f"""
    What is the sentiment of the following text, 
    which is delimited with triple backticks?

    Text: '''{text}'''
    """
    response = get_completion(prompt)
    print(response) 

if __name__ == "__main__":
    main()
