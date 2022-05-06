import numpy as np
import matplotlib.pyplot as plt

def get_image(idx=1):
    return (plt.imread("mnist/img_2.jpg")/255.0-0.1307)/0.3081, 9

    # return (plt.imread("../1.png")/255.0-0.1307)/0.3081, 5

    ## img3 - 9
    ## mnist/img_2.jpg - 0

def recover_image(image):
    #obtain image from vars (in case of SAT) and convert to viewable array
    pass