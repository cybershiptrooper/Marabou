from fileinput import filename
from maraboupy import Marabou
from test_utils import *
from maraboupy import MarabouCore

def check(filename, num_imgs, delta=0.03, l1norm = 1, region = [[15, 17],[24, 27]]):
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
        #add label bounds
        for i in range(10):
            if(i==lab): continue
            # network.setLowerBound(outputVars[lab], outputVars[i]) #shouldn't this be the opposite??
            network.addInequality([outputVars[lab], outputVars[i]],[1, -1], 0)
        #check sat
        vals = network.solve(options = options)
        # print(vals)
        if(vals[0]=="unsat"): good += 1
    print("verified correctly: {}/{}".format(good,num_imgs))

if __name__=="__main__":
    filename = "model_sigm.onnx"
    num_imgs = 1
    
    for i in range(1, 24):
        for j in range(1, 24):
            print("i: ",i,"/",24,"j: ", j,"/",24)
            region=[[i, i+2],[j, j+3]]
            check(filename, num_imgs, delta = 1, l1norm=12.0, region = region)
