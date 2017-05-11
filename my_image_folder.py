import torch.utils.data as data

from PIL import Image
import os
import os.path

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
]


def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


def make_dataset(dirt):
    images = []
    if not os.path.isdir(dirt):
        return None
    for root, _, fnames in sorted(os.walk(dirt)):
        for fname in fnames:
            if is_image_file(fname):
                path = os.path.join(root, fname)
                item = (path, fname)
                images.append(item)

    return images


def default_loader(path):
    return Image.open(path).convert('RGB')


def default_transform(target):
    wind = target.split('_')[2]
    return float(wind)

class ImageFolder(data.Dataset):

    def __init__(self, root, transform=None, target_transform=default_transform,
                 loader=default_loader):

        imgs = make_dataset(root)
        if len(imgs) == 0:
            raise(RuntimeError("Found 0 images in subfolders of: " + root + "\n"
                               "Supported image extensions are: " + ",".join(IMG_EXTENSIONS)))

        self.root = root
        self.imgs = imgs
        self.transform = transform
        self.target_transform = target_transform
        self.loader = loader

    def __getitem__(self, index):
        path, target = self.imgs[index]
        img = self.loader(path)
        if self.transform is not None:
            img = self.transform(img)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target
    
    def __getitemName__(self, index):
	_, fname = self.imgs[index]
	return fname.split('.')[0]

    def __len__(self):
        return len(self.imgs)
