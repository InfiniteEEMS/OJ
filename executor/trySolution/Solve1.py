import operator
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class WrongAnswerError(Exception):    
    pass


class Solver1:

    caseCount = 4
    testCases = [
        [2,7,11,15],
        [1,3],
        [1,5],
        [1,7]
    ]
    targets = [
        9,
        4,
        6,
        8
    ]
    expectedOutputs = [
        [0,1],
        [0,1],
        [0,1],
        [1,5]
    ]


    def run_tests(self, SolutionClass):

      solver = SolutionClass();
        
      with open("%s/%s" % (CURRENT_DIR, "log.txt" ), 'a') as source_file:
 

        for i in range(0,self.caseCount):
            res = solver.twoSum(self.testCases[i], self.targets[i])
            res.sort()
            self.expectedOutputs[i].sort()
            
            if operator.eq( set(res) , set(self.expectedOutputs[i]) ) is True:
                continue
            else:
                source_file.write("LastInput:" + str(self.testCases[i]) + "    "+ str(self.targets[i]) + "\n")
                source_file.write("ExpectedOutput:" + str(self.expectedOutputs[i])+"\n")
                source_file.write("YourOutput:" + str(res))

                raise WrongAnswerError


