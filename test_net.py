import torch
import os
from my_transform import demension_reduce
from my_image_folder import ImageFolder
from torch.autograd import Variable
from my_transform import transform
from define_net import Net
from torch.autograd import Variable

if __name__ == '__main__':
        
    path_ = os.path.abspath('.')

    net = Net() 
    net.load_state_dict(torch.load(path_+'net_relu.pth')) # your net

    testset = ImageFolder(path_+'/test_set/',transform) # your test set

    f = open(path_+'/result_relu.txt','w') # where to write answer

    tys = {} # map typhoon to its max wind
    tys_time = {} # map typhoon-time to wind

    for i in range(0,testset.__len__()):
        
        image, actual = testset.__getitem__(i)
        image = image.expand(1,image.size(0),image.size(1),image.size(2))
        name = testset.__getitemName__(i)
        
        output = net(Variable(image))
        wind = output.data[0][0]

        name = name.split('_')
        
        tid = name[0]
        if tys.has_key(tid):
            if tys[tid] < wind:
                tys[tid] = wind
        else :
            tys[tid] = wind
            
        tid_time = name[0]+'_'+name[1]+'_'+name[2]+'_'+name[3]
        tys_time[tid_time] = wind

    tys = sorted(tys.iteritems(),key=lambda asd:asd[1],reverse=True)
    for ty in tys:
        print ty # show the sort of typhoons' wind

    tys_time = sorted(tys_time.iteritems(),key=lambda asd:asd[0],reverse=False)
    for ty in tys_time:
        f.write(str(ty)+'\n') # record all result by time
    f.close()
