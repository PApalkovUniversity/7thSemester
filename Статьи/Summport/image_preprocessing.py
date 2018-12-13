import numpy as np
import os
import cv2

"""
внешние функции

get_preprocessing_areas(file_path,  simple_div=False, del_original=False, rescaling=True)
возвращает ndarray, хранящий все вырезанные области фото

save_preprocessing_areas(file_path, dir_to_save=None, simple_div=False, del_original=True)
сохраняет все вырезанные области фото в папке dir_to_save

simple_div: if true -> simple_divide else -> full_preprocessing
del_original: удалить оригинальное фоно или нет
при save_preprocessing_areas

"""



#===============NEW SCRAP FILTER============================

def find_bad_areas(edges_map):

    max_el = edges_map.max()
    min_value = max_el * 0.15

    for i in range(0, edges_map.shape[0]):
        for j in range(0, edges_map.shape[1]):
            if (edges_map[i, j] < min_value):
                edges_map[i , j] = 0

    return edges_map


def new_scrap_filter(file_path):
    gray = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(gray, 50, 400, apertureSize=3)
    N = 50

    edges_map = []

    for i in range(0, edges.shape[0] - N, N):
        line = []
        for j in range(0, edges.shape[1] - N, N):
            line.append(edges[i:i+N, j:j+N].sum())
        edges_map.append(line)

    edges_map = np.array(edges_map)
    edges_map = find_bad_areas(edges_map)

    i_img = 0
    for i in range(0, edges_map.shape[0]):
        j_img = 0
        for j in range(0, edges_map.shape[1]):
            if (edges_map[i, j] == 0):
                gray[i_img : i_img + N, j_img : j_img + N] = 0
            j_img += N
        i_img += N


    return gray


def divide(img, small_pic_size, file_path, percent_to_save):

    original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    all_areas = []

    step = int(small_pic_size / 2)

    for i in range(0, img.shape[0], step):
        for j in range(0, img.shape[1], step):
            filtered_area = img[i:i+small_pic_size, j:j+small_pic_size]
            original_area = original_image[i:i+small_pic_size, j:j+small_pic_size]

            #если пустая область
            if filtered_area.shape[0] < small_pic_size or filtered_area.shape[1] < small_pic_size:
                break


            if (filtered_area.sum() / original_area.sum() > percent_to_save):
                all_areas.append(original_area)

    return all_areas


def simple_divide(file_path, small_pic_size):
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    all_areas = []
    step = int(small_pic_size / 2)

    for i in range(0, img.shape[0], step):
        for j in range(0, img.shape[1], step):
            area = img[i:i+small_pic_size, j:j+small_pic_size]

            if not((area.shape[0] < small_pic_size) or (area.shape[1] < small_pic_size)):
                all_areas.append(area)

    return all_areas


def get_preprocessing_areas(file_path,  simple_div=False, del_original=False, rescaling=True):

    if simple_div is True:
        areas = simple_divide(file_path, 300)
    else:
        believe_coeff = 0.6 #Коэффициент доверия))
        #areas = divide(old_scrap_filter(file_path), 300, file_path, believe_coeff)
        areas = divide(new_scrap_filter(file_path), 300, file_path, believe_coeff)


    three_channel_areas = []
    if rescaling is True:
        for area in areas:
            three_channel_areas.append(cv2.cvtColor(area, cv2.COLOR_GRAY2RGB) / 255.)
    else:
        for area in areas:
            three_channel_areas.append(cv2.cvtColor(area, cv2.COLOR_GRAY2RGB))


    if del_original:
        os.remove(file_path)

    result_areas = np.array(three_channel_areas)


    return result_areas


def save_preprocessing_areas(file_path, dir_to_save=None, simple_div=False, del_original=True):
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)[:-4]

    if simple_div is True:
        areas = simple_divide(file_path, 300)
    else:
        believe_coeff = 0.9 #Коэффициент доверия))
        #areas = divide(old_scrap_filter(file_path), 300, file_path, believe_coeff)
        areas = divide(new_scrap_filter(file_path), 300, file_path, believe_coeff)

    if dir_to_save is None:
        dir_to_save = file_dir

    for i, area in enumerate(areas):
        small_file_name = os.path.join(dir_to_save, str(i) + "_" + file_name + ".jpg")
        cv2.imwrite(small_file_name, area)

    if del_original:
        os.remove(file_path)


def run_findimg_bad_areas():
    main_folder = "Original"
    folders = os.listdir(path=main_folder)

    if ".DS_Store" in folders:
        folders.remove(".DS_Store")

    for folder in folders:
        folder_path = os.path.join(main_folder, folder)
        pics = os.listdir(folder_path)

        if ".DS_Store" in pics:
            pics.remove(".DS_Store")

        for pic in pics:
            pic_path = os.path.join(folder_path, pic)
            save_preprocessing_areas(pic_path)
            print(get_preprocessing_areas(pic_path))
            #new_scrap_filter(pic_path)


if __name__=="__main__":
    # run_findimg_bad_areas()
    file = "1.jpg"
    # to = "3_1.jpg"
    # gray = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    # edges = cv2.Canny(gray, 50, 400, apertureSize=3)
    # cv2.imwrite(file, gray)
    save_preprocessing_areas(file)
