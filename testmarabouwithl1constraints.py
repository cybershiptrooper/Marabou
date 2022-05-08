from fileinput import filename
from maraboupy import Marabou
from test_utils import *
from maraboupy import MarabouCore

def check(filename, delta=0.03, l1norm = 1, region = [[15, 17],[24, 27]]):
    network = Marabou.read_onnx(filename)
    # networkori = Marabou.read_onnx(filename)
    options = Marabou.createOptions(verbosity = 0)
    
    inputVars = network.inputVars[0][0]
    outputVars = network.outputVars[0]
    #clear constrints
    
    #read image
    img, lab = get_image()
    #set norm
    for h in range(region[0][0], region[0][1]+1):
        for w in range(region[1][0], region[1][1]+1):
            network.setLowerBound(inputVars[h][w], img[h][w]-delta)
            network.setUpperBound(inputVars[h][w], img[h][w]+delta)

    for h in range(inputVars.shape[1]):
        for w in range(inputVars.shape[1]):
            if(h in range(region[0][0], region[0][1]+1)):
                if(w in range(region[1][0], region[1][1]+1)):
                    continue
            network.setLowerBound(inputVars[h][w], img[h][w])
            network.setUpperBound(inputVars[h][w], img[h][w])
    #add l1 bounds
    rpixels = (region[0][1]-region[0][0]+1)*(region[1][1]-region[1][0]+1)
    xrange = region[0][1]-region[0][0]+1

    for i in range(2**(rpixels)):
        variables = []
        coeffs = []
        for h in range(region[0][0], region[0][1]+1):
            for w in range(region[1][0], region[1][1]+1):
                x = h-region[0][0]
                y = w-region[1][0]
                j = y*xrange + x
                a = 2*((i//(2**j))%2 - 0.5)
                variables.append(inputVars[h][w])
                coeffs.append(a)
        
        sc = np.array(coeffs)@np.ravel((img[region[0][0]:region[0][1]+1,region[1][0]:region[1][1]+1]))
        network.addInequality(variables, coeffs, sc+l1norm)
    # add label bounds
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
    #check sat
    vals = network.solve(options = options)
    # print(vals)
    if(vals[0]=="unsat"): return 1
    else: recover_image(vals, f"region_{delta}_{l1norm}")
    return 0

if __name__=="__main__":
    filename = "model_sigm_v2.onnx"
    good = 0
    li = 12
    hi = 23
    lj = 7
    hj = 23
    for i in range(li, hi):
        for j in range(lj, hj):
            print("i: ",i,"/",hi,"j: ", j,"/",hj)
            region=[[i, i+2],[j, j+3]]
            good += check(filename, delta = 1, l1norm=100, region = region)
    print("verified correctly: {}/{}".format(good, (hj-lj)*(hi-li)))
