#Metaprogramming to download xkcd comics 

import openai 
import os 
import subprocess
import argparse
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output 
    )
    return response.choices[0].message["content"]


f1 = """
Write a function get_image_from_url which downloads an image \
from a given url. It should take in 2 arguments - url and folder. \
First use the requests library to get a response from the url. \
Then use BeautifulSoup's html parser to parse through the response's text. \
Now, in the html find a div with id = 'comic' and save it as comic_div. \
From the comic_div, find 'img', use the get method on this to get 'src' \ 
and save this as img_src. \
Cast img_src to a string and prepend the string \
'https:' to it and save the resultant \
string as img_src again. Split img_src on '/' and store the last element as img_name. \
Now create a variable img_path which uses the path.join method from \
the os module to create a path by joining the name of the folder passed \
in as argument and the img_name obtained in the previous step. \
Check if img_path already exists and if it does, remove it. \
Now, use the requests library again to get a response from img_src \
Save this response to a vairable named img. Finally, \
return both img and img_path. If there is an issue in getting a 
response from the initial url, return None and None instead of 
img and img_path. You may use a try and except to achieve this. 
"""

f2 = """
Write a function save_images downloads a number of images and \
saves them to a folder. It should take in 2 arguments - 'n', which is the \
number of images to be downloaded and 'folder', which is the destination \
of those images. \
First, check if the 'folder' exists and create it if it does not. \
Next, create an empty list named image_paths. \
Now start a for loop from 1 to n+1. In each iteration, save a variable \
url equal to f"https://xkcd.com/{i}/", where i is the iteration number. \
Pass in the url and folder arguments to the function get_image_from_url \
and save the returned values as img and img_path. The function \
get_image_from_url will be defined separately so there is no \
need to define it here. If both img and img_path have values other None \
open img_path as a file in mode 'wb' write the content of img \
to it. Then append img_path to image_paths. \
After all the iterations, return the list image_paths. 
"""

f3 = """
Write a function create_pdf which takes in 2 arguments - image_paths, \
which is a list of image files and pdf_name which is string. The objective \
of the function is to compile all image files into a pdf. If \
pdf_name does not end with '.pdf', append '.pdf' to it. Use the pdf_name and 
the os library to create a save path for the pdf and save it as pdf_path. \
Open each file in the list image_paths, convert them to RGB format \
and compile them into a pdf. Save the pdf with the name given \
by pdf_name to pdf_path. This function does not return anything. 
"""

f4 = """
Write a function named main which does not take in any arguments. \
First, create a parser using argparse. Make this parser take in 3 \
arguments - n_comics, images_folder and pdf_name. Then pass in the \
arguments n_comics and images_folder to the custom function save_images and \
save the output of this function as image_paths. Then pass in \
image_paths and the argument pdf name to the custom function create_pdf. \
he custom functions save_images and create_pdf are already defined separately, \
so do not include them here. This main function does not have a return value. 
"""

prompt = f"""
Your job is to write python code to download xkcd comic books based on the \
directions given below. Make sure you write clean and correct code, \
which runs without any error. You are supposed to write \
a total of 4 functions. Import the following packages at the top - \
requests, BeautifulSoup, os, Image, argparse and use them. Do not import any other packages
when writing the functions. Follow the directions given below for each function. \
Directions for function 1: {f1} \
Directions for function 2: {f2} \
Directions for function 3: {f3} \
Directions for function 4: {f4}
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metacode_file", type = str)
    args = parser.parse_args()
    response = get_completion(prompt)
    response = response.replace("`", "").replace("python", "", 1).strip()
    with open(f"{args.metacode_file}", "w") as file:
        file.write(response)
    subprocess.run(["python", f"{args.metacode_file}"])

if __name__ == "__main__":
    main()
    