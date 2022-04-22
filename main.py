# Python Version 3.8.12 (Anaconda Version 4.11.0)

import re                    # Python built-in
import math                  # Python built-in
import h5py                  # v3.2.1 or later
import numpy as np           # v1.20.3 or later
from PIL import Image        # v8.4.0 or later

from importlib_metadata import version # Only for version check
print("> Current Library Version Information")
print("   h5py          {}".format(str(version('h5py'))))
print("   numpy         {}".format(str(version('numpy'))))
print("   natsort       {}".format(str(version('natsort'))))
print("   PIL (Pillow)  {}".format(str(version('Pillow'))))
print("   tqdm          {}".format(str(version('h5py'))))


# 0. 기본 함수
def String_Splite_Into_List(target, Splitter):
    """
    긴 문자열을 입력된 문자를 기준으로 나누어 list 형태로 retrun
    :param target: 입력 문자열
    :param Splitter: 무엇으로 나눌것인가? (ex. '\s' - 공백, '\s|\t' - 공백 또는 탭으로 나누어라)
    :return:
    """
    StringArray = []
    StringArray = re.split(Splitter, target)
    StringArray = [item for item in StringArray if item]

    return StringArray



# 1. HDF 파일 생성
fileLocation = "D:\\11-CONFERENCE_AND_JOURNAL\\W2022-CONF-KSAS1-HDF\\2_HDF_Python_AeroCFD_DB\\sample.hdf5"
f = h5py.File(fileLocation, 'w')


# 2. 데이터 그룹 생성 (like 폴더)
g1 = f.create_group("1_DOE")
g11 = g1.create_group("1.1_Full_Factorial")
g12 = g1.create_group("1.2_LHS")
g2 = f.create_group("2_Geometry")
g3 = f.create_group("3_CFD")
g4 = f.create_group("4_Surrogate_Model")
g5 = f.create_group("5_Sensitivity_Analysis")
g6 = f.create_group("6_Optimization")


# 3. 데이터셋 생성 (like 파일)

## 3.1. 문자열 데이터셋 생성
string = f.create_dataset('CASE', data="A001_B2_C1")

## 3.2. 어레이 데이터셋 생성
chartData = [ [1, 1.0],
              [2, 0.5],
              [3, 0.2],
              [4, 0.1] ]
list2D_tuple = [tuple(x) for x in chartData]
dtype = np.dtype({'names':['iter','residual'], 'formats':['i4','f8']})
arr = np.array(list2D_tuple, dtype=dtype)

g3.create_dataset('array_sample', data=arr)


## 3.3.1. 레지듀얼 데이터 읽기
residualPath = 'D:\\11-CONFERENCE_AND_JOURNAL\\W2022-CONF-KSAS1-HDF\\2_HDF_Python_AeroCFD_DB\\RESOURCE\\Residual_Sample.DAT'
residualData = []
with open(residualPath, 'r') as loadfile:
    for iterm, line in enumerate(loadfile.readlines()[1::]):
        temp_1d = []
        Residual_list = String_Splite_Into_List(line, '\s|\n')
        Residual_Order = str(math.log10(float(Residual_list[1])))
        temp_1d.append(iterm + 1)
        temp_1d.append(Residual_list[1])
        temp_1d.append(Residual_Order)
        residualData.append(temp_1d)

## 3.3.2. 레지듀얼 데이터셋 생성
list2D_tuple = [tuple(x) for x in residualData]
dtype = np.dtype({'names':['iter','residual','residual_order'], 'formats':['i4','f8','f8']})
arr = np.array(list2D_tuple, dtype=dtype)
# Residual = g3.create_dataset('Residual_History', data=arr)
Residual = g3.create_dataset('Residual_History', data=arr, compression='gzip', compression_opts=9)


## 3.4. 이미지 데이터셋 생성
imagePath = 'D:\\11-CONFERENCE_AND_JOURNAL\\W2022-CONF-KSAS1-HDF\\2_HDF_Python_AeroCFD_DB\\RESOURCE\\Image_Sample.png'
img = Image.open(imagePath)
img = img.convert("RGB") # 색상이 있는 RGB로 변환
data = np.asarray((img), dtype="uint8")
# g3.create_dataset('Image_Sample', data=data, dtype='uint8')
g3.create_dataset('Image_Sample', data=data, dtype='uint8', compression='gzip', compression_opts=9)
dset = g3.get('Image_Sample')
dset.attrs['CLASS'] = np.string_('IMAGE')
dset.attrs['IMAGE_VERSION'] = np.string_('1.2')
arr = np.asarray([0, 255], dtype=np.uint8)
dset.attrs['IMAGE_MINMAXRANGE'] = list(arr)
dset.attrs['IMAGE_SUBCLASS'] = np.string_('IMAGE_TRUECOLOR')
dset.attrs['INTERLACE_MODE'] = np.string_('INTERLACE_PIXEL')


## 3.5.1. ONERA M6 Wing 해석 결과 이미지 가져오기
imageFolder = 'D:\\11-CONFERENCE_AND_JOURNAL\\W2022-CONF-KSAS1-HDF\\2_HDF_Python_AeroCFD_DB\\RESOURCE\\IMAGE\\'
imageName   = ['cp_distribution.png',
               'cp_distribution_y020.png', 'cp_distribution_y044.png', 'cp_distribution_y065.png',
               'cp_distribution_y090.png', 'cp_distribution_y095.png', 'cp_distribution_y099.png']

## 3.5.2. ONERA M6 Wing 해석 결과 이미지 쓰기
g31 = g3.create_group('ONERA_M6_Wing')

for i, Name in enumerate(imageName):
    imagePath = imageFolder + imageName[i]

    img = Image.open(imagePath)
    img = img.convert("RGB")  # 색상이 있는 RGB로 변환
    data = np.asarray((img), dtype="uint8")
    # g31.create_dataset(Name, data=data, dtype='uint8')
    g31.create_dataset(Name, data=data, dtype='uint8', compression='gzip', compression_opts=9)
    dset = g31.get(Name)
    dset.attrs['CLASS'] = np.string_('IMAGE')
    dset.attrs['IMAGE_VERSION'] = np.string_('1.2')
    arr = np.asarray([0, 255], dtype=np.uint8)
    dset.attrs['IMAGE_MINMAXRANGE'] = list(arr)
    dset.attrs['IMAGE_SUBCLASS'] = np.string_('IMAGE_TRUECOLOR')
    dset.attrs['INTERLACE_MODE'] = np.string_('INTERLACE_PIXEL')


## 데이터 링크
g3 = f.create_group("3_CFD")

g4['4.1_CFD_DATA'] = g3 # g3 데이터셋 오브젝트를 공유


## 메타 데이터 / 자기 기술적 속성
Residual.attrs['Owner']     = "Daesan Choi"
Residual.attrs['Homepage']  = "http://nextfoam.co.kr"
Residual.attrs['Time']      = "Steady"
Residual.attrs['CFL']       = "3.0"
Residual.attrs['Version']   = "1.39"
Residual.attrs['Project']   = "HDF_Sample"
Residual.attrs['Location']  = "D:\\11-CONFERENCE_AND_JOURNAL\\W2022-CONF-KSAS1-HDF\\2_HDF_Python_AeroCFD_DB\\RESOURCE\\"


## 파일 압축
## 3.3.2. 레지듀얼 데이터셋 생성
list2D_tuple = [tuple(x) for x in residualData]
dtype = np.dtype({'names':['iter','residual','residual_order'], 'formats':['i4','f8','f8']})
arr = np.array(list2D_tuple, dtype=dtype)
# Residual = g3.create_dataset('Residual_History_noCompression', data=arr)
Residual = g3.create_dataset('Residual_History_9Compression', data=arr, compression='gzip', compression_opts=9)


# 데이터셋 가져오기
loadedData = f.get('3_CFD/array_sample')[()]
print(loadedData)

# HDF 파일 닫기
f.close()







