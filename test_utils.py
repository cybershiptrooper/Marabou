import numpy as np
import matplotlib.pyplot as plt
# from PIL import Image
import matplotlib
import imageio

def get_image(idx=1):
    return (plt.imread("mnist/img_2.jpg")/255.0-0.1307)/0.3081, 0
    image = plt.imread("mnist/img_49.jpg")
    image = image/float(image.max())
    if(len(image.shape) > 2):
        image = (image[:,:,0] + image[:,:,1] + image[:,:,2])/3
    return (image-0.1307)/0.3081, 6

def recover_image(vals, name= "", later=False):
    #obtain image from vars (in case of SAT) and convert to viewable array
    image = np.zeros([28, 28])
    d = vals[1]
    add = 0
    if(later): add = 28*28
    for x in range(28):
        for y in range(28):
            k = add+28*x+y
            image[x][y] = d[k]
    image*0.3081 + 0.1307
    # print(image.min())
    # np.clip(image, 0, 1.0)
    image -= image.min()
    image /= image.max()

    a = np.random.randint(1000000)
    # print(image)
    # im = Image.fromarray(image)
    # im.save("recovery/{}.png".format(a))
    matplotlib.image.imsave(f'recovery/{a}_'+name+'.png', image, cmap = "gray")
    # imageio.imwrite('recovery/{}.png'.format(a), image)
    