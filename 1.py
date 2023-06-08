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
    
# 緑，青のRGB値を定義する
# Define RGB values for green and blue
green = np.array([0, 255, 0])
blue = np.array([255, 0, 0])


# 画像中の指定色ピクセルの座標を取得する
# Obtains the coordinates of a specified color pixel in an image
green_pixels = np.where(np.all(img == green, axis=-1))
blue_pixels = np.where(np.all(img == blue, axis=-1))


# 指定色ピクセルの座標を配列に挿入する
# Insert the coordinates of the specified color pixel into the array
green_coords = []
blue_coords = []
for x, y in zip(green_pixels[1], green_pixels[0]):
    coord = (x, y)
    green_coords.append(coord)
for x, y in zip(blue_pixels[1], blue_pixels[0]):
    coord = (x, y)
    blue_coords.append(coord)

green_coords = filter_coords(green_coords
blue_coords = filter_coords(blue_coords)


# 上あごと尾びれを結んだ直線に対して、背びれの先端からの直線の角度が直角になるように線を引く
# Draw a line so that the angle of the line from the tip of the dorsal fin is perpendicular to the straight line connecting the upper jaw and the tail fin
x1, y1 = blue_coords[0]
x2, y2 = blue_coords[1]

angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
orthogonal_angle = angle - 90
x = green_coords[0][0] - int(1000 * math.cos(math.radians(orthogonal_angle)))
y = green_coords[0][1] - int(1000 * math.sin(math.radians(orthogonal_angle)))
endpoint = (x, y)
cv2.line(img, green_coords[0], endpoint, (0, 255, 0), 1)
        
# 画像を表示する
# Show Image
cv2.imshow('image', img)

# 画像を保存する
# Save Image
cv2.imwrite('output.tif', img)

cv2.waitKey(0)
cv2.destroyAllWindows()