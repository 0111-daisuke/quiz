#OpenCVのインポート
import cv2

#画像読み込み関数
img=cv2.imread("stock/tatutori.png")

#画像表示関数
cv2.imshow("stock",img)
cv2.waitKey(0)

