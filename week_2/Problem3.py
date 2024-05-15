#Using openai API to create the 20Q game

import openai 
import os 
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.1):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

def collect_messages(prompt, context):
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context)
    print(response)
    context.append({'role':'assistant', 'content':f"{response}"})

def twentyQ(context):
    game = True
    initial_prompt = "I want to play the 20Q game!"
    collect_messages(initial_prompt, context)
    print(context[-1]['content'])
    while game:
        prompt = input()
        collect_messages(prompt, context)
        print(context[-1]['content'])
        if context[-1]['content'] == "Congratulations, you win!" or context[-1]['content'] == "Better luck next time!":
            print(context)
            game = False

def main():
    context = [{'role':'system', 'content':"""
    You are 20Qbot, a bot which replicates the famous 20Q game. \
    You ask the user to think of an entity and then you try to guess \
    what the user is thinking using 20 yes-or-no questions. The entity \
    can be anything such as a movie, book, fictional character and so on. \
    You get 20 questions to try and guess what the user is thinking of. \
    If you fail to guess in 20 questions, you get an additional 5 questions. \
    Thus, you get a maximum of 25 questions. \
    Display the question number of each question and make sure \
    you keep a track of how many questions you have asked. \
    If you fail to guess in 25 questions, the user is the winner and you write \
    "Congratulations, you win!". If you guess the entity correctly, \
    write "Better luck next time!". \
    Make sure your questions are fun and engaging. Do not resort to wild guessing \
    Before asking a question, pay attention to each of the user's \
    answers to all of your previous questions. \
    The user begins by saying that he wants to play the 20Q game. \
    You then greet the user and ask the category of the entity. \
    Once the user mentions the category, you begin with your first question. \
    """}]
    
    twentyQ(context)

if __name__ == "__main__":
    main()


#This game has a few small issues. The model dosen't keep track of everything if asked in the past
#It also loses track of the number of questions it has asked, occasioanlly. 