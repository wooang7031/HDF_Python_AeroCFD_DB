import os                    # Python built-in
import time                  # Python built-in
import math                  # Python built-in
import h5py                  # v3.2.1 or later
import numpy as np           # v1.20.3 or later
import natsort               # v7.1.1 or later
from PIL import Image        # v8.4.0 or later
from tqdm import tqdm        # v4.62.3 or later

from importlib_metadata import version # Only for version check
print("> Current Library Version Information")
print("   h5py          {}".format(str(version('h5py'))))
print("   numpy         {}".format(str(version('numpy'))))
print("   natsort       {}".format(str(version('natsort'))))
print("   PIL (Pillow)  {}".format(str(version('Pillow'))))
print("   tqdm          {}".format(str(version('h5py'))))


# HDF 파일 생성
fileLocation = "C:\\Users\\PC\\Desktop\\PycharmProject\\HDF_Python_AeroCFD_DB\\sample.hdf5"
hdf_file = h5py.File(fileLocation, 'w')


# 데이터 그룹 생성 (like 폴더)
g1 = hdf_file.create_group("1_DOE")
g11 = g1.create_group("1.1_Factorial")
g12 = g1.create_group("1.2_LHS")

g2 = hdf_file.create_group("2_Geometry")
g3 = hdf_file.create_group("3_CFD")
g4 = hdf_file.create_group("4_Surrogate_Model")
g5 = hdf_file.create_group("5_Sensitivity_Analysis")
g6 = hdf_file.create_group("6_Optimization")


# 데이터셋 생성 (like 파일)

## 문자열 데이터셋 생성
overview = hdf_file.create_dataset('dataset1', data="overview")

## 어레이 데이터셋 생성
list2D = [[1,2],[11,12],[21,22],[31,32]]
list2D_tuple = [tuple(x) for x in list2D]
dtype = np.dtype({'names':['iter','residual'], 'formats':['i4','f8']})
arr = np.array(list2D_tuple, dtype=dtype)
print(arr)
g3.create_dataset('Residual_History', data=arr)

## 이미지 데이터셋 생성
imagePate = 'C:\\Users\\PC\\Desktop\\PycharmProject\\HDF_Python_AeroCFD_DB\\RESOURCE\\Image.png'
img = Image.open(imagePate)
img = img.convert("RGB") # 색상이 있는 RGB로 변환
data = np.asarray((img), dtype="uint8")
g3.create_dataset('Contour', data=data, dtype='uint8')
dset = g3.get('Contour')
dset.attrs['CLASS'] = np.string_('IMAGE')
dset.attrs['IMAGE_VERSION'] = np.string_('1.2')
arr = np.asarray([0, 255], dtype=np.uint8)
dset.attrs['IMAGE_MINMAXRANGE'] = list(arr)
dset.attrs['IMAGE_SUBCLASS'] = np.string_('IMAGE_TRUECOLOR')
dset.attrs['INTERLACE_MODE'] = np.string_('INTERLACE_PIXEL')

## 데이터 링크


## 속성


## 메타 데이터



## 파일 압축



# HDF 파일 닫기
hdf_file.close()


