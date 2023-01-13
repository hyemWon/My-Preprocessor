import os
import cv2
import numpy as np
import random
import tempfile
import shutil


FORMAT = ('.jpg', '.jpeg', '.png', '.bmp',
        '.mp4', '.avi', '.mkv')


def get_file_list(path):
    file_list = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(FORMAT)]
    file_list.sort()
    return file_list


def save_file_list(path):
    pass


def change_file_extension(path, from_ext_list=[], to_ext='.jpg'):
    file_list = get_file_list(path)

    for file in file_list:
        if not os.path.isdir(file):
            name, ext = os.path.splitext(file)

            if ext in from_ext_list:
                os.rename(file, name+to_ext)


def rename_file_list(path, keyword='temp'):
    file_list = get_file_list(path)

    with tempfile.TemporaryDirectory() as temp_dir:
        for idx, file in enumerate(file_list):
            shutil.move(file, os.path.join(temp_dir, os.path.basename(file)))
        temp_files = get_file_list(temp_dir)

        for idx, file in enumerate(temp_files):
            ext = os.path.splitext(file)[-1]
            new_filename = os.path.join(path, f'{keyword}_{idx}{ext}')
            new_filename = os.path.join(path, f'{idx}{ext}')
            print(file, ' ---->>> ', new_filename)
            shutil.move(file, new_filename)


def move_file_list(from_path, to_path, keyword='img', sample_cnt=None):
    _ = create_directory(out_path)
    rename_file_list(to_path, keyword=keyword)

    from_file_list = get_file_list(from_path)
    to_file_list = get_file_list(to_path)

    if sample_cnt is not None:
        from_file_list = random.sample(from_file_list, k=sample_cnt)

    cnt = len(to_file_list)

    for file in from_file_list:
        new_filename = os.path.join(to_path, f'{keyword}_{cnt}{ext}')
        print(file, ' ---->>> ', new_filename)
        shutil.copy(file, new_filename)
        cnt += 1


def create_directory(path):
    result = False
    if os.path.exists(path):
        result = True
    else:
        os.makedirs(path)
    return result


def split_directory(in_path, out_path, folder_cnt=2):
    for i in range(1, folder_cnt+1):
        _ = create_directory(os.path.join(out_path, str(i)))

    file_list = get_file_list(in_path)
    count_per_folder = int((len(file_list)+1) / folder_cnt + 0.5)
    print(count_per_folder)

    folder_seq = 1
    for i, file in enumerate(file_list):
        if i == (count_per_folder * folder_seq):
            folder_seq += 1

        new_path = os.path.join(out_path, str(folder_seq))
        shutil.copy(file, new_path)


def integrate_directory(in_path, out_path, keyword):   
    walk_list = []
    for (path, dir, files) in os.walk(in_path):
        if os.path.basename(path) == keyword:
            walk_list.append(path)

    print(walk_list)
    _ = create_directory(out_path)

    idx = 0
    for walk in walk_list:
        file_list = get_file_list(walk)

        for file in file_list:
            filename = f'{keyword}_{idx}.jpg'
            shutil.copy(file, os.path.join(out_path, filename))
            idx += 1
    

def save_video_frame(video_path, out_path): 
    _ = create_directory(out_path)
    video_list = get_file_list(video_path)
    print(video_list)
    for video in video_list:
        if video.endswith(FORMAT):
            name = os.path.splitext(os.path.basename(video))
            save_dir = os.path.join(out_path, name[0])
            _ = create_directory(save_dir)

            cap = cv2.VideoCapture(video)
            cnt = 0
            while True:
                ret, img = cap.read()

                if not ret:
                    print('video error')
                    break
                if (int(cap.get(1)) % 10 == 0):
                    print('Saved frame number : ' + str(int(cap.get(1))))
                    cv2.imwrite(('{0}/{1}_{2}.jpg').format(save_dir ,name[0], cnt), img)
                    cnt += 1

if __name__ == '__main__':
    in_path = '/home/user/바탕화면/Dataset/HELMET/dataset/TRAIN/train3/normal_unknown'
    out_path = '/home/user/바탕화면/Dataset/HELMET/dataset/TRAIN/train3/train/normal_unknown'


    ext = '.jpg'
    keyword = os.path.basename(in_path)
    print(keyword)


    # integrate_directory(in_path, out_path, keyword=keyword)
    # split_directory(in_path, out_path, 5)
    # change_file_extension(in_path, ['.jpg', '.bmp'], '.png')
    # move_file_list(in_path, out_path, keyword=keyword)
    move_file_list(in_path, out_path, keyword=keyword, sample_cnt=5000)
    # rename_file_list(in_path, keyword='helmet')
    # save_video_frame(in_path, out_path)

