All the files in this folder need to be inside Marabou's root directory to work. Instructions for building marabou are given [here](/readmemarabou.md). Each of the experiments in the report is described below:

1. Testing robustness on regions using explicit constraints:

        python testmarabouwithl1constraints.py

    To test it with your own defined regions, you can edit the main method, or import it and call `check(<path to your image>, <delta>, <l1norm>, <region>)`. Note that going above 3x4 pixel regions might give memory issues.

2. Testing robustness on regions using auxilliary networks:

        python testmarabouregions_v2.py

    Or import the file and call `check(<path to your image>, <delta>, <l1norm>, <region>)`

3. Robustness on entire image ($L_1$/clipped norms):

        python testmarabouonl1_v2.py --delta <delta> --l1norm <l1norm>

4. Vanilla $L_\infty$ robustness:

        python testmarabou.py --delta <delta>

The image recored on SAT is stored in [Marabou/recovery/](/recovery/) do NOT delete the folder. The program only takes onnx networks as inputs. We have provided two example networks with our code. For generating new networks, please execute [l1net_generator.ipynb](/l1net_generator.ipynb). We also provide an [inference tester](/onnx_tester.py) for onnx networks. 

Note: we provide example images, but you will have to edit [test_utils.py](/test_utils.py) for new images. 