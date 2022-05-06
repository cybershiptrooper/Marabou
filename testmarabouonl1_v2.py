from fileinput import filename
from maraboupy import Marabou
from test_utils import *
from maraboupy import MarabouCore

def check(filename, num_imgs, delta=0.03, l1norm = 1):
    good = 0
    eqs = 0
    dns = 0
    for _ in range(num_imgs):

        #clear constrints 
        print("getting network..", )
        network = Marabou.read_onnx(filename)
        options = Marabou.createOptions(verbosity = 0)###is there a better way??

        # network.equList = network.equList[:-eqs]

        # print(network.inputVars[0][0].shape)
        inputVars = network.inputVars[0][0]
        outputVars = network.outputVars[0]
        print("got network!", )

        #read image
        print("adding infinity norms..", )
        img, lab = get_image()
        lab += 1 #add extra space for l1 norm

        #set linf norm
        for h in range(img.shape[1]):
            for w in range(img.shape[1]):
                network.setLowerBound(inputVars[28*h+w], img[h][w])
                network.setUpperBound(inputVars[28*h+w], img[h][w])
                network.setLowerBound(inputVars[28*28+28*h+w], img[h][w]-delta)
                network.setUpperBound(inputVars[28*28+28*h+w], img[h][w]+delta)
                eqs +=4
        print("added infinity norms!", )

        #set l1 norm using disjunction
        print("adding other bounds..", flush = True)
        network.addInequality([1], [outputVars[0]], l1norm)

        #bounds for label
        # labineq = []
        for i in range(1, 11):
            if(i==lab): continue
            # network.setLowerBound(outputVars[lab], outputVars[i]) #shouldn't this be the opposite??
            network.addInequality([outputVars[lab], outputVars[i]],[1, -1], 0)
        print("adding all bounds!", flush = True)
        #check sat
        print("checking sat..")
        vals = network.solve(options = options)
        if(vals[0]=="unsat"): good += 1
    print("verified correctly: {}/{}".format(good,num_imgs))

if __name__=="__main__":
    filename = "l1model_combined_v2.onnx"
    num_imgs = 1
    check(filename, num_imgs, delta = 0.1, l1norm=0.0)
