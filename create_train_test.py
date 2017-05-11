import os
import os.path
import random
from PIL import Image
from my_image_folder import is_image_file

def oversample(wind): # return how many to oversample (according to wind level)
    if wind < 60:
        return 1
    if wind < 80:
        return 1 + random.randint(0,1)
    if wind < 100:
        return 1 + random.randint(0,2)
    return 1 + random.randint(0,10)

def create_file(f,fname,f_root,count): # oversample specific copies
    wind = int(fname.split('_')[2])
    cps = oversample(wind)
    count = count + cps
    for i in range(0,cps):
        temp = fname.split('.')
        temp[0] = temp[0]+'_'+str(i)
        new_fname = temp[0]+'.'+temp[1] # append a copy-number to filename
        f.save(f_root+new_fname)
    return count

def if_match(f1,f2): # match : f1 is 6-hour earlier than f2, and they are same ty
    tname1 = f1.split('_')
    tname2 = f2.split('_')
    if tname1[0]!=tname2[0]:
	return False
    date1 = tname1[1]
    date2 = tname2[1]
    h1 = date1[len(date1)-1]
    h2 = date2[len(date2)-1]
    if (h1=='0' and h2=='6')or(h1=='6' and h2=='2')or(h1=='2' and h2=='8')or(h1=='8' and h2=='0'):
	return True
    else :
	return False

def cut_pics(p): # only reserve central area
    box = (128,128,384,384)
    p = p.crop(box)
    return p

def merge_pics(p1,p2): # red-channel:6-hour earlier pic, green-channel:current pic
                       # blue-channel:useless/unmeaning
    p1 = p1.convert('RGB')
    p2 = p2.convert('RGB')
    r,_,_ = p1.split()
    _,g,b = p2.split()
    im = Image.merge('RGB',(r,g,b))
    return im


if __name__ == '__main__':
    
    path_ = os.path.abspath('.')
    raw_dir = path_ + '/tys_raw/'

    train_root = path_ + '/train_set/'
    if not os.path.exists(train_root):
	os.mkdir(train_root)
    test_root = path_ + '/test_set/'
    if not os.path.exists(test_root):
	os.mkdir(test_root)

    global count_train,count_test
    count_train,count_test = 0,0

    for root, _, fnames in sorted(os.walk(raw_dir)):

	fnames = sorted(fnames)
	boundary = int(len(fnames)*0.8) # 80% samples as train set and 20% samples as test set

	for i in range(1,len(fnames)):
	    if not is_image_file(fnames[i-1]) or not is_image_file(fnames[i]):
		continue
	    
	    img_1 = Image.open(os.path.join(root,fnames[i-1]))
	    img = Image.open(os.path.join(root,fnames[i]))
	    
	    if if_match(fnames[i-1],fnames[i]):
		img_1 = cut_pics(img_1)
		img = cut_pics(img)
		im = merge_pics(img_1,img)

		if i <= boundary :
                    count_train = create_file(im,fnames[i],train_root,count_train)
                else :
                    count_test = create_file(im,fnames[i],test_root,count_test)
                    
                if count_train > 30000 or count_test > 30000: # upper limit of files count in a dir
                    break
                
    print 'items in train set: ',count_train
    print 'items in test set: ',count_test
