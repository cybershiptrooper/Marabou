from fileinput import filename
from maraboupy import Marabou
from test_utils import *
from maraboupy import MarabouCore

def check(filename, delta=0.03, l1norm = 1, region = [[15, 17],[24, 27]]):
    good = 0
    eqs = 0
    dns = 0

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
    for h in range(region[0][0], region[0][1]+1):
        for w in range(region[1][0], region[1][1]+1):
            network.setLowerBound(inputVars[28*28+28*h+w], img[h][w]-delta)
            network.setUpperBound(inputVars[28*28+28*h+w], img[h][w]+delta)

    for h in range(img.shape[1]):
        for w in range(img.shape[1]):
            network.setLowerBound(inputVars[28*h+w], img[h][w])
            network.setUpperBound(inputVars[28*h+w], img[h][w])
            if(h in range(region[0][0], region[0][1]+1)):
                if(w in range(region[1][0], region[1][1]+1)):
                    continue
            network.setLowerBound(inputVars[28*28+28*h+w], img[h][w])
            network.setUpperBound(inputVars[28*28+28*h+w], img[h][w])
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
    vals = network.solve(options = options)
    if(vals[0]=="unsat"): return 1
    else: recover_image(vals, f"l1_on_regionv2_image_label{lab}", later=True)
    # print("verified correctly: {}/{}".format(good,num_imgs))
    return 0

if __name__=="__main__":
    filename = "l1model_combined_v2.onnx"
    good = 0
    li = 12
    hi = 23
    lj = 7
    hj = 23
    for i in range(li, hi):
        for j in range(lj, hj):
            print("i: ",i,"/",hi,"j: ", j,"/",hj)
            region=[[i, i+3],[j, j+3]]
            good += check(filename, delta = 1, l1norm=1, region = region)
    print("verified correctly: {}/{}".format(good, (hj-lj)*(hi-li)))

