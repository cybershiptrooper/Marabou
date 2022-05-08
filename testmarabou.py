from fileinput import filename
from maraboupy import Marabou
from test_utils import *
from maraboupy import MarabouCore
import argparse 

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
        #set norm
        for h in range(inputVars.shape[1]):
            for w in range(inputVars.shape[1]):
                network.setLowerBound(inputVars[h][w], img[h][w]-delta)
                network.setUpperBound(inputVars[h][w], img[h][w]+delta)

        #check sat
        disjuncts = []
        for i in range(10):
            if(i==lab): continue
            # network.setLowerBound(outputVars[lab], outputVars[i]) #shouldn't this be the opposite??  
            ineq = MarabouCore.Equation(MarabouCore.Equation.LE);
            ineq.addAddend(1, outputVars[lab])
            ineq.addAddend(-1, outputVars[i])
            ineq.setScalar(0)
            disjuncts.append([ineq])
            # network.addInequality([outputVars[lab], outputVars[i]],[1, -1], 0)
        network.addDisjunctionConstraint(disjuncts)
        vals = network.solve(options = options)
        # if(vals[0]=="sat"): bul=False
        if(vals[0]=="unsat"): good += 1
        else: recover_image(vals)
    print("verified correctly: {}/{}".format(good,num_imgs))

if __name__=="__main__":
    filename = "model_sigm_v2.onnx"
    num_imgs = 1
    parser = argparse.ArgumentParser()
    parser.add_argument("--delta", type = float, default= 0.1)
    args = parser.parse_args()
    print("delta:", args.delta)
    check(filename, num_imgs, delta = args.delta)
