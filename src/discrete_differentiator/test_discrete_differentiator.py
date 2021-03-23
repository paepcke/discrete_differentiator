'''
Created on Mar 23, 2021

@author: paepcke
'''
import os
import unittest

#from discrete_differentiator.discrete_differentiator import DiscreteDifferentiator
from discrete_differentiator.discrete_differentiator import DiscreteDifferentiator

class TestDiscreteDifferentiator(unittest.TestCase):


    def setUp(self):
        curr_dir = os.path.dirname(__file__)
        self.single_col_tst = os.path.join(curr_dir, 'TestData/singleCol.csv')
        self.two_col_tst    = os.path.join(curr_dir, 'TestData/twoCol.csv')
        self.single_col_with_header = os.path.join(curr_dir, 
                                                   'TestData/singleColWithHeader.csv'
                                                   )

    def tearDown(self):
        pass

# -------------- Tests --------------

    def testLinearFunc(self):
        # f(x) = 2x+3
        # df/dx = 2
        testSeq = []
        for x in range(20):
            testSeq.append(2*x+3)
        with open(os.devnull, 'w') as fd:
            res = DiscreteDifferentiator.differentiate(testSeq, 1, outFileFd=fd)
            expected = [2 for i in range(20)] #@UnusedVariable
            self.assertEqual(expected, res, 'Linear func failed')
        
    def testLinearFuncWithUptickAtStart(self):
        # f(x) = 2x+3
        # df/dx = 2
        testSeq = []
        for x in range(1,20):
            testSeq.append(2*x+3)
        testSeq[0] = 0
        with open(os.devnull, 'w') as fd:
            res = DiscreteDifferentiator.differentiate(testSeq, 1, outFileFd=fd)
            expected = [2 for i in range(1,20)] #@UnusedVariable
            expected[0] = 9.5
            expected[1] = 4.5
            self.assertEqual(expected, res, 'Linear func with uptick failed')
        
    def testSingleColFile(self):
        with open(os.devnull, 'w') as fd:
            res = DiscreteDifferentiator.differentiate(self.single_col_tst, 1, outFileFd=fd)
            expected = [2 for i in range(20)] #@UnusedVariable
            self.assertEqual(expected, res, 'Linear func from single column file failed')
        
    def testTwoColFile(self):
        with open(os.devnull, 'w') as fd:
            res = DiscreteDifferentiator.differentiate(self.two_col_tst, 1, outFileFd=fd, colIndex=1)
            expected = [2 for i in range(20)] #@UnusedVariable
            self.assertEqual(expected, res, 'Linear func from two column file failed')
        
    def testSingleColFileWithColHeader(self):
        with open(os.devnull, 'w') as fd:
            res = DiscreteDifferentiator.differentiate(self.single_col_with_header, 1, outFileFd=fd, skipLines=1)
            expected = [2 for i in range(20)] #@UnusedVariable
            self.assertEqual(expected, res, 'Linear func from single column file with column header failed')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()