from fileinput import filename
from maraboupy import Marabou
from test_utils import *
from maraboupy import MarabouCore

def check(filename, num_imgs, delta=0.03, b = 1):
    
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
        
        l1eq = MarabouCore.Equation(MarabouCore.Equation.GE);
        l1eq.addAddend(1, outputVars[0])
        l1eq.setScalar(b) #l1 norm > b condition

        #bounds for label
        # labineq = []
        for i in range(1, 10):
            if(i==lab+1): continue
            ineq = MarabouCore.Equation(MarabouCore.Equation.LE);
            ineq.addAddend(1, outputVars[lab+1])
            ineq.addAddend(-1, outputVars[lab+1])
            ineq.setScalar(0)
            # labineq.append(ineq)
            network.addDisjunctionConstraint([[l1eq] , [ineq] ])
        print("adding all bounds!", flush = True)
        #check sat
        print("checking sat..")
        vals = network.solve(options = options)
        # print(vals)
        if(vals[0]=="unsat"): good += 1
    print("verified correctly: {}/{}".format(good,num_imgs))

if __name__=="__main__":
    filename = "l1model_combined_v2.onnx"
    num_imgs = 1
    check(filename, num_imgs, delta = 0.0, b=0.0)
