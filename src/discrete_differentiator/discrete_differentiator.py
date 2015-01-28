'''
Created on Jan 27, 2015

@author: paepcke
'''

import os
import sys
import unittest


class DiscreteDifferentiator(object):
    

#     @classmethod
#     def differentiate(theClass, seqOrFileName, xDelta):
#         seq = theClass.importSequence(seqOrFileName)
#         res = []
#         res.append(4*(seq[1]-seq[0])/xDelta)
#         for indx in range(1,len(seq)-1):
#             res.append(2*(seq[indx]-seq[indx-1])/xDelta)
#         res.append(4*(seq[-1]-seq[-2])/xDelta)
#         # Print to stdout, one value at a time:
#         for resNum in res:
#             print(resNum)
                    
    @classmethod
    def differentiate(theClass, seqOrFileName, xDelta, colNum=0, outFileFd=sys.stdout):
        seq = theClass.importSequence(seqOrFileName)
        res = []
        res.append((-(seq[0+2*xDelta]) + 4*seq[0+xDelta] - 3*seq[0])/float(2*xDelta))
        for indx in range(1,len(seq)-1):
            res.append((seq[indx+xDelta]-seq[indx-xDelta])/float(2*xDelta))
        res.append((seq[-1-2*xDelta]- 4*seq[-1-xDelta] + 3*seq[-1])/float(2*xDelta))
        # Print to stdout, one value at a time:
        for resNum in res:
            outFileFd.write(str(resNum) + '\n')
        return res
                    
    
    @classmethod
    def importSequence(theClass, seqOrFileName):
        if type(seqOrFileName) == list:
            seq = seqOrFileName
        else:
            seq = []
            with open(seqOrFileName, 'r') as fd:
                for numStr in fd:
                    try:
                        num = float(numStr)
                    except ValueError:
                        raise ValueError("All lines in the data file ('%s') must be numbers; found: %s" % (seqOrFileName, numStr))
                    seq.append(num)
        return seq
                    
class TestDifferentiator(unittest.TestCase):

    def testLinearFunc(self):
        # f(x) = 2x+3
        # df/dx = 2
        testSeq = []
        for x in range(20):
            testSeq.append(2*x+3)
        res = DiscreteDifferentiator.differentiate(testSeq, 1, outFileFd=open(os.devnull,'w'))
        expected = [2 for i in range(20)] #@UnusedVariable
        self.assertEqual(expected, res, 'Linear func failed')
        
    def testLinearFuncWithUptickAtStart(self):
        # f(x) = 2x+3
        # df/dx = 2
        testSeq = []
        for x in range(1,20):
            testSeq.append(2*x+3)
        testSeq[0] = 0
        res = DiscreteDifferentiator.differentiate(testSeq, 1, outFileFd=open(os.devnull,'w'))
        expected = [2 for i in range(1,20)] #@UnusedVariable
        expected[0] = 9.5
        expected[1] = 4.5
        self.assertEqual(expected, res, 'Linear func with uptick failed')
        
        

if __name__ == '__main__':
    #unittest.main()
    if len(sys.argv) != 1:
        print('Usage: discrete_differentiator <fileNameWithSingleColNumSeq>')
        
    