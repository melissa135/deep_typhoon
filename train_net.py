from define_net import Net
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.init as init
import torch.optim as optim
import torch
import torchvision
import os
from my_transform import transform
from my_image_folder import ImageFolder

def testset_loss(dataset,network):

    loader = torch.utils.data.DataLoader(dataset,batch_size=1,num_workers=2)

    all_loss = 0.0
    for i,data in enumerate(loader,0):

        inputs,labels = data
        inputs = Variable(inputs)

        outputs = network(inputs)   
        all_loss = all_loss + abs(labels[0]-outputs.data[0][0])

    return all_loss/i

if __name__ == '__main__':
	
    path_ = os.path.abspath('.')

    trainset = ImageFolder(path_+'/train_set/',transform)
    trainloader = torch.utils.data.DataLoader(trainset,batch_size=8,
                                              shuffle=True,num_workers=2)
    testset = ImageFolder(path_+'/test_set/',transform)

    net = Net()
    init.xavier_uniform(net.conv1.weight.data,gain=1)
    init.constant(net.conv1.bias.data,0.1)
    init.xavier_uniform(net.conv2.weight.data,gain=1)
    init.constant(net.conv2.bias.data,0.1)
    #net.load_state_dict(torch.load(path_+'net_relu.pth')) 
    print net

    criterion = nn.L1Loss()

    optimizer = optim.Adam(net.parameters(),lr=0.001)

    for epoch in range(10): #

        running_loss = 0.0
        for i,data in enumerate(trainloader,0):

            inputs,labels = data
            inputs,labels = Variable(inputs),Variable(labels)

            optimizer.zero_grad()

            outputs = net(inputs)   
            loss = criterion(outputs,labels.float())
            loss.backward()
            optimizer.step()

            running_loss += loss.data[0]
            if i%200 == 199:
                print('[%d, %5d] loss: %.3f' % (epoch+1,i+1,running_loss/200))
                running_loss = 0.0

	test_loss = testset_loss(testset,net)
	print('[%d ] test loss: %.3f' % (epoch+1,test_loss))

    print('Finished Training')
    torch.save(net.state_dict(),path_+'/net_relu.pth')
