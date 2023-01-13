from genericpath import isfile
import os
import shutil
import cv2
import numpy as np
import random


class MangeImage:
    def __init__(self, data_path, save_path):
        self.data_path = data_path
        self.save_path = save_path

        if self.data_path:
            self.img_list = self.get_img_list()
            self.txt_list = self.get_txt_list()

        if not os.path.exists(save_path):
            os.makedirs(save_path)

    def get_img_list(self):
        file_list = [os.path.join(self.data_path, file) for file in os.listdir(self.data_path) if file.endswith(FORMAT_IMG)]
        return file_list

    def get_txt_list(self):
        file_list = [os.path.join(self.data_path, file) for file in os.listdir(self.data_path) if file.endswith(FORMAT_META)]
        return file_list

    # 특정 개수만큼 랜덤 인덱스 리스트 반환
    def get_sample(self, p: float) -> list:
        img_cnt = len(self.img_list)
        sample_cnt = int(img_cnt * p)
        sample_num = sorted(random.sample(range(img_cnt), sample_cnt))
        print(sample_num)
        return sample_num

    # 특정 레이블 번호 변경
    def change_label_num(self, from_num: int, to_num: int):        
        for file in self.txt_list:
            print(file)
            with open(file, 'r') as f:
                lines = f.readlines()

            with open(file, 'w') as f:
                for line in lines:    
                    line = line.split()
                    if line[0]==str(from_num):
                        line[0]=str(to_num)

                    new_line = ' '.join(line)
                    f.write(new_line+'\n')
    
    # 특정 레이블 번호 정보 삭제
    def remove_label(self, num: int):
        for file in self.txt_list:
            print(file)
            with open(file, 'r') as f:
                lines = f.readlines()

            with open(file, 'w') as f:
                for line in lines:          
                    if line[0]==str(num):
                        continue
                    f.write(line)


    def get_random_x_y(self, width, height):
        while True:
            x1 = random.randint(0, width)
            x2 = random.randint(0, width)
            xmin = min(x1, x2)
            xmax = max(x1, x2)
            if xmax-xmin > 20:
                break
        while True:
            y1 = random.randint(0, height)
            y2 = random.randint(0, height)
            ymin = min(y1, y2)
            ymax = max(y1, y2)
            if ymax-ymin > 20:
                break
        return xmin, xmax, ymin, ymax

    # 이미지 당 sample 개수만큼 랜덤 크기로 크롭
    def random_crop_image(self, sample=1):
        count_per_img = sample//len(self.img_list) 
        if count_per_img==0:
            count_per_img = 1       
        print(count_per_img)

        for file in self.img_list:
            print(file)
            filename = os.path.splitext(os.path.basename(file))
            img = cv2.imread(file)
            h, w, _ = img.shape
            
            for i in range(count_per_img):    
                xmin, xmax, ymin, ymax = self.get_random_x_y(w, h)
                cropped_image = img[ymin:ymax, xmin:xmax]

                save_filename = f'{filename[0]}_{i}{filename[1]}'
                print(save_filename)
                try:
                    cv2.imwrite(os.path.join(self.save_path, save_filename), cropped_image)
                except:
                    pass


    # roi 이미지 크롭하여 레이블 번호 별로 저장
    def save_roi_image(self, keyword='img', margin=0):
        class_roi_cnt = {}  # 레이블 별 roi 이미지 개수
        for file in self.img_list:
            txt_file = os.path.splitext(file)
            txt_file = txt_file[0] + FORMAT_META
            print(txt_file)
            img = cv2.imread(file)
            height, width, _ = img.shape

            if os.path.isfile(txt_file):
                with open(txt_file, 'r') as f:
                    for i, line in enumerate(f):
                        box = line.strip().split()
                        idx = box[0]
                        box = list(map(float, box[1:]))
                        # print(box)
                        
                        xmin = int((box[0] - box[2]/2)*width) - margin
                        ymin = int((box[1] - box[3]/2)*height) - margin
                        xmax = int((box[0] + box[2]/2)*width) + margin
                        ymax = int((box[1] + box[3]/2)*height) + margin
                        box = (xmin, ymin, xmax, ymax)

                        xmin, ymin, xmax, ymax = check_roi(width, height, box)
                        cropped_image = img[ymin:ymax, xmin:xmax]
                        
                        save_path = os.path.join(self.save_path, idx)
                        if not os.path.exists(save_path):
                            os.makedirs(save_path)
                            class_roi_cnt[idx] = 0

                        save_filename = f'{keyword}_{idx}_{class_roi_cnt[idx]}.jpg'
                        
                        try:
                            cv2.imwrite(os.path.join(save_path, save_filename), cropped_image)
                            class_roi_cnt[idx] += 1
                        except:
                            pass
                        

def check_roi(img_w, img_h, box):
    xmin, ymin, xmax, ymax = box
    xmin = xmin if (xmin >= 0) else 0
    ymin = ymin if (ymin >= 0) else 0
    xmax = xmax if (xmax <= img_w) else img_w
    ymax = ymax if (ymax <= img_h) else img_h
    box = (xmin, ymin, xmax, ymax)
    return box
    

if __name__ == '__main__':
    in_path = '/home/user/바탕화면/Dataset/4'
    out_path = '/home/user/dataset'

    FORMAT_IMG = ('.jpg', '.jpeg', '.png', '.bmp')
    FORMAT_VIDEO = ('.mp4', '.avi', '.mkv')
    FORMAT_META = '.txt'

    tool = MangeImage(in_path, out_path)
    # tool.change_label_num(2, 1)
    # tool.remove_label(5)
    keyword = os.path.basename(out_path)
    # tool.save_roi_image(keyword=keyword, margin=0)
    tool.random_crop_image(sample=10000)