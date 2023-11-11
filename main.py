import os
import cv2
import numpy as np
# import openslide
from RIFT import RIFT
from rotated_source_calculate import rotated_source_calculate

# # 遍历文件夹进行配准
# HE_images_directory = r'D:\datasets\HE'
# IHC_images_directory = r'D:\datasets\IHC'
#
# HE_svs_files = [f for f in os.listdir(HE_images_directory) if f.endswith('.svs')]
# IHC_svs_files = [f for f in os.listdir(IHC_images_directory) if f.endswith('.svs')]
#
# for i in range(0, len(HE_svs_files)):
#     image1_path = os.path.join(HE_images_directory, HE_svs_files[i])
#     image2_path = os.path.join(IHC_images_directory, IHC_svs_files[i])
#
#     slide1 = openslide.OpenSlide(image1_path)
#     slide2 = openslide.OpenSlide(image2_path)
#
#     level = 2
#     img_array = np.array(slide1.read_region((0, 0), level, slide1.level_dimensions[level]))
#     img_array2 = np.array(slide2.read_region((0, 0), level, slide2.level_dimensions[level]))
#
#     # Convert the ARGB image to BGR   BGR为opencv中要求的图片格式
#     bgr_image1 = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
#     bgr_image2 = cv2.cvtColor(img_array2, cv2.COLOR_RGBA2BGR)
#     target_width = 1000
#     target_height = 1000
#     img1 = cv2.resize(bgr_image1, (target_width, target_height))
#     img2 = cv2.resize(bgr_image2, (target_width, target_height))


# # 单独两张图片测试
s_img1 = cv2.imread(r"D:\samples\HE.png")
s_img2 = cv2.imread(r"D:\samples\IHC_CD4.png")
target_width = 1000
target_height = 1000
img1 = cv2.resize(s_img1, (target_width, target_height))
img2 = cv2.resize(s_img2, (target_width, target_height))

# RIFT首次配准，得到初始值作为best，再进行优化
costs, inliersIndex, match_point1, match_point2 = RIFT(img1, img2)

# 旋转优化
inliersIndex, match_point1, match_point2, rotated_img2 = rotated_source_calculate(img1, img2, costs,
                                                                     inliersIndex,match_point1, match_point2)

# 选出误差足够小的点对
clean_point1 = match_point1[inliersIndex]
clean_point2 = match_point2[inliersIndex]

kp1 = [cv2.KeyPoint(float(clean_point1[i][0]), float(clean_point1[i][1]), 1) for i in range(len(clean_point1))]
kp2 = [cv2.KeyPoint(float(clean_point2[i][0]), float(clean_point2[i][1]), 1) for i in range(len(clean_point2))]
matches = [cv2.DMatch(i, i, 1) for i in range(len(clean_point1))]

# 可视化
img3 = cv2.drawMatches(img1, kp1, rotated_img2, kp2, matches, None, flags=2)
cv2.imshow('img3', img3)
cv2.waitKey(0)
cv2.destroyAllWindows()

# # 可视化图像进行存储
# store_path = f"D:\\img{i}.jpg"
# cv2.imwrite(store_path, img3)
