from html_telegraph_poster import upload_image
import os

list_dir = os.listdir('D:/projects/online-shop/img/')

def upload_image_to_telegraph(img):
    res = upload_image(img)

    return res

for i in list_dir:
    up = upload_image_to_telegraph('D:/projects/online-shop/img/'+ i)
    print(up)
