import pandas as pd
import psycopg2 as pg
import re
import cv2
import numpy as np

pairs = pd.read_csv('ItemPairs_train.csv')

connection = pg.connect(database='avito', user='u1234x1234', host='localhost', password='avitoa')
cur = connection.cursor()

def read_images(image_list):
    size = 100
    root = '/mnt/data/u1234x1234/Images_'
    image_pan = np.zeros((size, size * len(image_list), 3), dtype=np.uint8)
    for i, x in enumerate(image_list):
        last2 = str(x)[-2:]
        arch = last2[0]
        folder = str(int(last2))
        filepath = root + arch + '/' + folder + '/' + str(x) + '.jpg'
        image = cv2.imread(filepath)
        image = cv2.resize(image, (size, size))
        image_pan[: size, i * size : (i + 1) * size] = image
        
    return image_pan
                
for index, row in pairs.iterrows():
    
    cur.execute('select * from iteminfo_train where itemid in(' + str(row[0]) + ',' + str(row[1]) + ')')
    res = cur.fetchall()

    if res[0][4] is not None:
        l1 = [int(x) for x in re.split(',', res[0][4])]
    if res[1][4] is not None:
        l2 = [int(x) for x in re.split(',', res[1][4])]
    
    print(res[0], '\n')
    print(res[1])
    print('is Duplicate: ', row[2])
    print('Generation method: ', row[3])
    print('------------------------------------------------------------------')
    cv2.imshow('im1', read_images(l1))
    cv2.imshow('im2', read_images(l2))
    cv2.waitKey()    
    
#    qwe