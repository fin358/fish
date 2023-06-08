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
img = cv2.imread('input.tif')
if img is None:
    print("ファイルが読み込めませんでした")

# 赤、黄、青、紫のRGB値を定義する
# Define RGB values for red, yellow, blue, and purple
red = np.array([0,0, 255])
yellow = np.array([0, 255, 255])
blue = np.array([255, 0, 0])
purple = np.array([255, 0, 255])

# 画像中の指定色ピクセルの座標を取得する
# Obtains the coordinates of a specified color pixel in an image
red_pixels = np.where(np.all(img == red, axis=-1))
yellow_pixels = np.where(np.all(img == yellow, axis=-1))
blue_pixels = np.where(np.all(img == blue, axis=-1))
purple_pixels = np.where(np.all(img == purple, axis=-1))

# 指定色ピクセルの座標を配列に挿入する
# Insert the coordinates of the specified color pixel into the array
red_coords = []
yellow_coords = []
blue_coords = []
purple_coords = []
for x, y in zip(red_pixels[1], red_pixels[0]):
    coord = (x, y)
    red_coords.append(coord)
for x, y in zip(yellow_pixels[1], yellow_pixels[0]):
    coord = (x, y)
    yellow_coords.append(coord)
for x, y in zip(blue_pixels[1], blue_pixels[0]):
    coord = (x, y)
    blue_coords.append(coord)
for x, y in zip(purple_pixels[1], purple_pixels[0]):
    coord = (x, y)
    purple_coords.append(coord)

red_coords = filter_coords(red_coords)
yellow_coords = filter_coords(yellow_coords)
blue_coords = filter_coords(blue_coords)
purple_coords = filter_coords(purple_coords)

# 赤、黄、青、それぞれ2つの座標の距離を求める
# Find the distance between two coordinates, red, yellow, and blue, respectively
red_dist = np.linalg.norm(np.array(red_coords[0])-np.array(red_coords[1]))
yellow_dist = np.linalg.norm(np.array(yellow_coords[0])-np.array(yellow_coords[1]))
blue_dist = np.linalg.norm(np.array(blue_coords[0])-np.array(blue_coords[1]))

# 正中線から腹の距離を求める
# Find the distance of the belly from the midline
lower_dist = np.linalg.norm(np.array(purple_coords[0])-np.array(yellow_coords[1]))

# 体長(height、length)、体長(縦)に対する正中線から腹までの割合(l_h / h）を求める
# Find body length (height, length) and the ratio of midline to belly (l_h / h) to body length (length)
height = (yellow_dist*10)/red_dist
length = (blue_dist*10)/red_dist
rat = ((lower_dist*10)/red_dist) / ((yellow_dist*10)/red_dist)

# 結果を表示する
# Show results
print("体長(height):", round(height,1),"cm")
print("体長(length):", round(length,1),"cm")
print("体長(縦)に対する中心線から腹までの割合(l_h / h)：",round(rat*100,1),"%")#lower_height/height

# 画像を表示する
# Show Image
cv2.imshow('image', img)

cv2.waitKey(0)
cv2.destroyAllWindows()