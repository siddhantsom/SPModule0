import requests
import json
import os
import argparse

def response_from_url(url):
    """Gets data from given url.

    Parameters
    ----------
    url : link

    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        image = data.get('image')
        attributes = data.get('attributes')
    else:
        image = None
        attributes = None
        print('Oops')
    return image, attributes

def find_squirrels(max_squirrels, keyword, filename):
    """Adds data from required squirrels to a text file.

    Parameters
    ----------
    n : int
    keyword : str
    filename : str
    """
    if max_squirrels>14000:
        max_squirrels = 14000
    if os.path.exists(filename):
        os.remove(filename)
    count = 0
    for i in range(max_squirrels):
        url = f"https://scrappyart.s3.ap-south-1.amazonaws.com/json/{i+1}"
        image, attributes = response_from_url(url)

        for attribute in attributes:
            if keyword in attribute.get('value').lower():
                count+=1
                with open(filename, 'a') as file:
                    file.write(image+'\n')
                    file.write(str(attributes)+'\n'+'\n')
                break
    print(f'You found {count} squirrels!')
                

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_squirrels", type = int)
    parser.add_argument("--keyword", type = str)
    parser.add_argument("--filename", type = str)

    args = parser.parse_args()
    find_squirrels(args.max_squirrels, args.keyword, args.filename)

if __name__ == "__main__":
    main()


                












