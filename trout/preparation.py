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

# 画像内で指定色が使われている座標を取得する
# Get the coordinates where the specified color is used
def color_coords(b, g, r):
    # 使用する色のRGB値を定義する
    # Define the RGB values of the colors to be used
    color = np.array([b,g,r])
    
    # 画像中の指定色ピクセルの座標を取得する
    # Obtains the coordinates of a specified color pixel in an image
    pixels = np.where(np.all(img == color, axis=-1))
    
    # 指定色ピクセルの座標を配列に挿入する
    # Insert the coordinates of the specified color pixel into the array
    color_coords = []
    for x, y in zip(pixels[1], pixels[0]):
        coord = (x, y)
        color_coords.append(coord)
        
    return color_coords

# 指定の直線に対して、指定の座標から直角になるように線を引く
# Draw a line at a right angle from the specified coordinates to the specified line
def right_angle_line(line_coords, point_coords,b,g,r):
    x1, y1 = line_coords[0]
    x2, y2 = line_coords[1]

    angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
    orthogonal_angle = angle - 90

    x = point_coords[0][0] - int(1000 * math.cos(math.radians(orthogonal_angle)))
    y = point_coords[0][1] - int(1000 * math.sin(math.radians(orthogonal_angle)))
    endpoint = (x, y)
    cv2.line(img, point_coords[0], endpoint, (r, g, b), 1)
    
# 画像を読み込む
# Load image
img = cv2.imread('figure/preparation_before.tif')
if img is None:
    print("File could not be loaded")

# 指定色が使われている座標の始点と終点を求める
# Find the start and end points of the coordinates where the specified color is used
green_coords = filter_coords(color_coords(0,255,0))
blue_coords = filter_coords(color_coords(255,0,0))

# 指定の直線を体長(横)，指定の座標を背びれの先端とし，関数right_angle_lineを呼びだす
# Call the function right_angle_line with the specified line as the body length (width) and the specified coordinates as the tip of the dorsal fin
right_angle_line(blue_coords,green_coords,0,255,0)
        
# 画像を表示する
# Show Image
cv2.imshow('image', img)

# 画像を保存する
# Save Image
cv2.imwrite('figure/preparation_after.tif', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
