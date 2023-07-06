import cv2
import numpy as np

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

# 画像を読み込む
# Load image
img = cv2.imread('input.tif')
if img is None:
    print("ファイルが読み込めませんでした")

# 指定色が使われている座標の始点と終点を求める
# Find the start and end points of the coordinates where the specified color is used
yellow_coords = filter_coords(color_coords(0,255,255))
cyan_coords = filter_coords(color_coords(255,255,0))
blue_coords = filter_coords(color_coords(255,0,0))

# 同じ色の2つの座標の距離を求める
# Find the distance between two coordinates of the same color
yellow_dist = np.linalg.norm(np.array(yellow_coords[0])-np.array(yellow_coords[1]))
cyan_dist = np.linalg.norm(np.array(cyan_coords[0])-np.array(cyan_coords[1]))
blue_dist = np.linalg.norm(np.array(blue_coords[0])-np.array(blue_coords[1]))

# 胸鰭から背びれの距離を求める
# Find the distance from the pectoral fin to the dorsal fin
upper_dist = np.linalg.norm(np.array(yellow_coords[0])-np.array(cyan_coords[0]))
lower_dist = np.linalg.norm(np.array(yellow_coords[0])-np.array(cyan_coords[1]))

# 体長(length)を1としたときの体長(height)の比率を求める
# Find the ratio of body length (height) to body length (length) as 1
raito1 = yellow_dist / blue_dist

# 体長(height)を1としたときの胸鰭の幅の比率を求める
# Find the ratio of the width of the pectoral fins when the body length (height) is 1
raito2 = cyan_dist / yellow_dist

# 体長(height)を1としたときの胸鰭(上)の幅の比率を求める
# Find the ratio of the width of the pectoral fin (upper) to the body length (height) as 1
raito3 = upper_dist / yellow_dist

# 体長(height)を1としたときの胸鰭(下)の幅の比率を求める
# Find the ratio of the width of the pectoral fin (lower) to the body length (height) as 1
raito4 = lower_dist / yellow_dist

# 結果を表示する
# Show results
print("体長(length)を1としたときの体長(height)の比率:", round(raito1,))
print("体長(height)を1としたときの胸鰭の幅の比率:", round(raito2,3))
print("体長(height)を1としたときの胸鰭(上)の幅の比率:", round(raito3,3))
print("体長(height)を1としたときの胸鰭(下)の幅の比率:", round(raito4,3))

# 画像を表示する
# Show Image
cv2.imshow('image', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
