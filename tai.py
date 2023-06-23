import cv2
import numpy as np
import math

# 座標が格納されている配列から始点と終点を取り出す
# Retrieve the starting and ending points from the array where the coordinates are stored
def filter_coords(coords):
    start_coords = coords[0]
    end_coords = coords[-1]
    if len(coords) > 2:
        for i in range(1,len(coords)):
            if start_coords[0] > coords[i][0]:
                start_coords = coords[i]
            if end_coords[0] < coords[i][1]:
                end_coords = coords[i]
        return [start_coords, (end_coords)]
    else:
        return coords
    
# 画像を読み込む
# Load image
img = cv2.imread('output.tif')
if img is None:
    print("ファイルが読み込めませんでした")

# 赤、黄、青、紫のRGB値を定義する
# Define RGB values for red, yellow, blue, and purple
yellow = np.array([0, 255, 255])
blue = np.array([255, 0, 0])

# 画像中の指定色ピクセルの座標を取得する
# Obtains the coordinates of a specified color pixel in an image
yellow_pixels = np.where(np.all(img == yellow, axis=-1))
blue_pixels = np.where(np.all(img == blue, axis=-1))

# 指定色ピクセルの座標を配列に挿入する
# Insert the coordinates of the specified color pixel into the array
yellow_coords = []
blue_coords = []
for x, y in zip(yellow_pixels[1], yellow_pixels[0]):
    coord = (x, y)
    yellow_coords.append(coord)
for x, y in zip(blue_pixels[1], blue_pixels[0]):
    coord = (x, y)
    blue_coords.append(coord)

yellow_coords = filter_coords(yellow_coords)
blue_coords = filter_coords(blue_coords)

# 赤、黄、青、それぞれ2つの座標の距離を求める
# Find the distance between two coordinates, red, yellow, and blue, respectively
yellow_dist = np.linalg.norm(np.array(yellow_coords[0])-np.array(yellow_coords[1]))
blue_dist = np.linalg.norm(np.array(blue_coords[0])-np.array(blue_coords[1]))

# 体長(height、length)、体長(縦)に対する正中線から腹までの割合(l_h / h）を求める
# Find body length (height, length) and the ratio of midline to belly (l_h / h) to body length (length)
height = yellow_dist
length = blue_dist

raito = height / length
# 結果を表示する
# Show results
print("体長(length)を1としたときの体長(height)の比率:", round(raito,3))

# 画像を表示する
# Show Image
cv2.imshow('image', img)

cv2.waitKey(0)
cv2.destroyAllWindows()