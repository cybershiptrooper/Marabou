from fileinput import filename
from maraboupy import Marabou
from test_utils import *

def check(filename, num_imgs, delta=0.03, l1norm = 1):
    network = Marabou.read_onnx(filename)
    # networkori = Marabou.read_onnx(filename)
    options = Marabou.createOptions(verbosity = 0)
    
    inputVars = network.inputVars[0][0]
    outputVars = network.outputVars[0]
    good = 0
    for _ in range(num_imgs):
        #clear constrints
        
        #read image
        img, lab = get_image()
        print(outputVars[lab],outputVars[0])
        #set norm
        for h in range(inputVars.shape[1]):
            for w in range(inputVars.shape[1]):
                network.setLowerBound(inputVars[h][w], img[h][w]-delta)
                network.setUpperBound(inputVars[h][w], img[h][w]+delta)

        #check sat
        for i in range(10):
            if(i==lab): continue
            # network.setLowerBound(outputVars[lab], outputVars[i]) #shouldn't this be the opposite??
            network.addInequality([outputVars[lab], outputVars[i]],[1, -1], 0)
        
        vals = network.solve(options = options)
        # print(vals)
        if(vals[0]=="unsat"): good += 1
    print("verified correctly: {}/{}".format(good,num_imgs))

if __name__=="__main__":
    filename = "model_sigm_v2.onnx"
    num_imgs = 1
    check(filename, num_imgs, delta = 0.0)
