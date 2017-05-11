import torch
import torchvision.transforms as transforms

class demension_reduce(object):
    def __call__(self,tensor):
        return tensor[0:2] # only need Red and Green channel

transform = transforms.Compose([transforms.ToTensor(),
                                demension_reduce(),
                                transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))])
