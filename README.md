# deep_typhoon
Analysis satellite images of typhoons by deep-learning (CNN), based on PyTorch.  

This CNN learns the relationships between the max wind speed of typhoons and their satellite images from the labeled train set (obtained from agora/JMA), then it can estimate the wind of typhoons by the no-label images.

## Requirements
* BeautifulSoup  
* PIL  
* Pytorch  

## Usage
1. Run `download_agora.py` to download the satellite images of typhoons as the raw data, save them in folder `tys_raw`.  
2. Run `create_samples.py` to convert raw data into the legal samples for our CNN, create two new forlder `train_set` and `test_set`.  
3. Run `train_net.py` to train CNN with the train set, the trained CNN will be saved as a disk file `net_relu.pth`.  
4. Run `test_net.py`, analysis the test set with the CNN saved in previous step.  

After 10 epoches training we can get a CNN regressor which mean loss in train set is about 8 (knots) and in test set is about 10 (knots).  
![](https://raw.githubusercontent.com/melissa135/deep_typhoon/master/loss_sequence.png)  

Here is what this CNN thinks of the top 20 typhoons in max wind.

Downloading images and training CNN may take a long time. Here I offerd a trained CNN named `net_relu.pth`, so that you can directly use it in step 4 and skip step 1-3. But you need to prepare your test set by running `create_samples.py` with some necessary modified.  

## Tips
* Memory should be at least 1.5G .  
* This project is written without `cuda()`, while you can use `cuda()` to transfer the CNN onto GPU and speedup the training.  
* The images and labels are crawled from agora.ax.nii.ac.jp/digital-typhoon , and the labels are refered to JMA(Japan Meteorological agency).  

## More Information
See ...
