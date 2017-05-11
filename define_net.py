from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.conv1 = nn.Conv2d(2,8,11)
        self.pool1 = nn.MaxPool2d(6,6)
        self.conv2 = nn.Conv2d(8,20,12)
	self.pool2 = nn.MaxPool2d(5,5)
        self.fc1 = nn.Linear(20*6*6,80)
        self.fc2 = nn.Linear(80,16)
        self.fc3 = nn.Linear(16,1)

    def forward(self,x):
        x = self.pool1(F.relu(self.conv1(x))) # better than sigmoid/tanh
        x = self.pool2(F.relu(self.conv2(x))) # better than sigmoid/tanh
        x = x.view(-1,self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features
