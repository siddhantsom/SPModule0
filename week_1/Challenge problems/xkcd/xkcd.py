#This script compiles xkcd comics into a single pdf.

import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
import argparse


def get_image_from_url(url, folder):
    response = requests.get(url)
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        comic_div = soup.find('div', id='comic')
        img_src = 'https:'+str(comic_div.find('img').get('src'))
        img_name = img_src.split('/')[-1]
        img_path = os.path.join(folder, img_name)
        if os.path.exists(img_path):
            os.remove(img_path)
        img = requests.get(img_src)
        return img, img_path
    except:
        return None, None

    

def save_images(n, folder):
    """
    Downloads all images and saves them in folder. Returns paths to all images.

    Parameters
    ----------
    n : number of images to be downloaded (int)
    folder: name of folder where images are saved (str)

    Returns
    -------
    image_paths : paths to all images (list)
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    image_paths = []
    for i in range(1, n+1):
        url = f"https://xkcd.com/{i}/"
        if i%20 == 0:
            print(f"Downloading image {i}")
        img, img_path = get_image_from_url(url, folder)
        if img and img_path:
            with open(img_path, 'wb') as file:
                file.write(img.content)
            image_paths.append(img_path)
        else:
            continue
    return image_paths 

def create_pdf(image_paths, pdf_name):
    """
    Compiles all images into a pdf.

    Parameters
    ----------
    image_paths : paths to all images to be compiled (list)
    pdf_name: name of pdf (str)

    Returns
    -------
    None
    """
    images = [Image.open(img_file).convert("RGB") for img_file in image_paths]
    if not pdf_name.endswith('.pdf'):
        pdf_name = pdf_name + '.pdf'
    pdf_path = os.path.join(pdf_name)
    images[0].save(pdf_path, save_all=True, append_images=images[1:])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_comics", type = int)
    parser.add_argument("--images_folder", type = str)
    parser.add_argument("--pdf_name", type = str)

    args = parser.parse_args()
    image_paths = save_images(args.n_comics, args.images_folder)
    create_pdf(image_paths, args.pdf_name)

if __name__ == "__main__":
    main()
  
#Example usage - python xkcd.py --n_comics 2919 --images_folder xkcd_images --pdf_name xkcd_compiled