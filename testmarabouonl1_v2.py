from fileinput import filename
from maraboupy import Marabou
from test_utils import *
from maraboupy import MarabouCore
import argparse

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

        # print(network.outputVars.shape)
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
        # network.addInequality([1], [outputVars[0]], l1norm)
        network.setUpperBound(outputVars[0], l1norm)

        #bounds for label
        # labineq = []
        disjuncts = []
        for i in range(1, 11):
            if(i==lab): continue
            # network.setLowerBound(outputVars[lab], outputVars[i]) #shouldn't this be the opposite??  
            ineq = MarabouCore.Equation(MarabouCore.Equation.LE);
            ineq.addAddend(1, outputVars[lab])
            ineq.addAddend(-1, outputVars[i])
            ineq.setScalar(0)
            disjuncts.append([ineq])
            # network.addInequality([outputVars[lab], outputVars[i]],[1, -1], 0)
        network.addDisjunctionConstraint(disjuncts)
        print("added all bounds!", flush = True)
        #check sat
        print("checking sat..")
        # query = network.getMarabouQuery()
        # file = open("query.log", "w")
        # (query.printAllBounds())
        # file.close()
        vals = network.solve(options = options)
        if(vals[0]=="unsat"): good += 1
        else: recover_image(vals, f"l1_on_entire_image_label_{lab}", later=True)
    print("verified correctly: {}/{}".format(good,num_imgs))

if __name__=="__main__":
    filename = "l1model_combined_v2.onnx"
    num_imgs = 1
    parser = argparse.ArgumentParser()
    parser.add_argument("--delta", type = float, default= 1)
    parser.add_argument("--l1norm", type=float, default = 1)
    args = parser.parse_args()
    print("delta", args.delta,"l1norm", args.l1norm)
    check(filename, num_imgs, delta = args.delta, l1norm=args.l1norm)
