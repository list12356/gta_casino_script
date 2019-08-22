import os
import random
import torchvision.transforms as transforms
import cv2
import numpy as np

from torch.utils import data
from PIL import Image

class RandomCrop(object):
    def __init__(self):
        pass
    
    def __call__(self, img):
        h, w = img.size
        h = int(round(random.uniform(0.9, 1.0)*h))
        w = int(round(random.uniform(0.9, 1.0)*w))
        x1 = random.randint(0, img.size[1] - w)
        y1 = random.randint(0, img.size[0] - h)
        # img = img[y1 : y1 + h, x1 : x1 + w]
        img = img.crop((y1, x1, y1+h, x1+w))
        return img

class GTADataSet(data.Dataset):

    def __init__(self):
        self.images = []
        self.labels = []
        self.transforms = transforms.Compose([
            transforms.Grayscale(),
            RandomCrop(),
            transforms.Resize(size=(28, 14)),
            transforms.ToTensor()
        ])
        for i in range(10):
            tmp_img = []
            for filename in os.listdir('./img/train/{!s}'.format(i)):
                img = cv2.imread('./img/train/{!s}/{!s}'.format(i, filename))
                img = img[:, :, ::-1]  # BGR -> RGB
                img = Image.fromarray(img)
                tmp_img.append(img)
                if len(tmp_img) < 20:
                    tmp_img.extend(random.choices(tmp_img, k=20 - len(tmp_img)))

            self.images.extend(tmp_img)
            self.labels.extend([int(i) for _ in range(len(tmp_img))])

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        # load img and label
        img = self.images[index]
        label = self.labels[index]

        # apply data augmentation
        if self.transforms is not None:
            img  = self.transforms(img)
        return img, label

class GTATestDataSet(data.Dataset):

    def __init__(self):
        self.images = []
        self.labels = []
        self.transforms = transforms.Compose([
            transforms.Grayscale(),
            RandomCrop(),
            transforms.Resize(size=(28, 14)),
            transforms.ToTensor()
        ])
        for i in range(10):
            tmp_img = []
            for filename in os.listdir('./img/train/{!s}'.format(i)):
                img = cv2.imread('./img/train/{!s}/{!s}'.format(i, filename))
                img = img[:, :, ::-1]  # BGR -> RGB
                img = Image.fromarray(img)
                tmp_img.append(img)
                if len(tmp_img) < 20:
                    tmp_img.extend(random.choices(tmp_img, k=20 - len(tmp_img)))

            self.images.extend(tmp_img)
            self.labels.extend([int(i) for _ in range(len(tmp_img))])

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        # load img and label
        img = self.images[index]
        label = self.labels[index]

        # apply data augmentation
        if self.transforms is not None:
            img  = self.transforms(img)
        return img, label