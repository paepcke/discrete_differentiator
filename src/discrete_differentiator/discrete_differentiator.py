#!/usr/bin/env python
'''
Created on Jan 27, 2015

@author: paepcke

Takes a sequence of numbers, and returns a sequence of numbers 
that are the derivative of the given sample. Takes the sequence
either as a Python array, or in a CSV file. Differentiation is
done as follows:

	For first data point uses:        f'(x) =(-f(x+2h) + 4*f(x+h) - 3*f(x))/(2h)
	For internal data points uses:    f'(x) =(f(x+h) - f(x-h))/(2h)
	For last data point uses:         f'(x) =(f(x-2h)  - 4*f(x-h) + 3*f(x))/(2h)

Accommodates CSV files with multiple columns, of which one is
contains the sequence to differentiate. Accommodates CSV files
with or without column header.

To run unit tests, uncomment the unittest main at the bottom.
'''

import argparse
import csv
import os
import sys
import unittest


class DiscreteDifferentiator(object):
    
    # ------------------------------  Public --------------------------------

    @classmethod
    def differentiate(theClass, seqOrFileName, xDelta=1, outFileFd=sys.stdout, colIndex=0, csvDelimiter=',', csvQuotechar='"', skipLines=0):
        '''
        Main and only (class) method. So, call with DiscreteDifferentiator.differentiate(...)
        The sequence is assumed to be the Y-values of a function over an
        even-spaced series of x values. Like this:
                 x   y
                 -----
                 0  10
                 1  20
                 2  14
                  ...
        But only the Y values are supplied. 
        
        In spite of the many parameters, simple cases are simple. Examples:
        
            o differentiate([2,4,6,7])
            o Given a csv file foo.csv with a single column of numbers:
               differentiate('foo.txt')
            o A csv file like this:
                 "trash column", 10
                 "more trash", 20
               differentiate('foo.txt', colIndex=1)
        
        :param seqOrFileName: Either the number array, or a file name 
        :type seqOrFileName: {[{float | int}] | string}
        :param xDelta: the number of integers between two X-axis ticks.
            Assumed to be 1, but can be any positive int. Assumes
            that first number in given sequence is f(0)
        :type xDelta: int
        :param outFileFd: file object of the file to which result sequence
            is written. Default is sys.stdout 
        :type outFileFd: FILE
        :param colIndex: if sequence is given in a CSV file, this parameter is the 
            CSV zero-origin column index. Default is 0 
        :type colIndex: int
        :param csvDelimiter: delimiter used in CSV file. Default is comma
        :type csvDelimiter: str
        :param csvQuotechar: char used to quote column fields that contain the delimiter.
            Default is '"'
        :type csvQuotechar: str
        :param skipLines: number of lines in CSV file to skip before number sequence starts.
            Default is 0
        :type skipLines: int 
        '''
        try:
            seq = theClass.importSequence(seqOrFileName, colIndex=colIndex, csvDelimiter=csvDelimiter, csvQuotechar=csvQuotechar, skipLines=skipLines)
        except ValueError as e:
            outFileFd.write('Error during file import: ' + `e`)
        res = []
        res.append((-(seq[0+2*xDelta]) + 4*seq[0+xDelta] - 3*seq[0])/float(2*xDelta))
        for indx in range(1,len(seq)-1):
            res.append((seq[indx+xDelta] - seq[indx-xDelta]) / float(2*xDelta))
        res.append((seq[-1-2*xDelta] - 4*seq[-1-xDelta] + 3*seq[-1])/float(2*xDelta))
        # Print to stdout, one value at a time:
        for resNum in res:
            outFileFd.write(str(resNum) + '\n')
        return res
                    
    # ------------------------------  Private --------------------------------
    
    @classmethod
    def importSequence(theClass, seqOrFileName, colIndex=0, csvDelimiter=',', csvQuotechar='"', skipLines=0):
        '''
        Import the sequence of numbers, either given a sequence
        as an array, or a file name.
        
        :param seqOrFileName: Either the number array, or a file name 
        :type seqOrFileName: {[{float | int}] | string}
        :param colIndex: if sequence is given in a CSV file, this parameter is the 
            CSV zero-origin column index. Default is 0 
        :type colIndex: int
        :param csvDelimiter: delimiter used in CSV file. Default is comma
        :type csvDelimiter: str
        :param csvQuotechar: char used to quote column fields that contain the delimiter.
            Default is '"'
        :type csvQuotechar: str
        :param skipLines: number of lines in CSV file to skip before number sequence starts.
            Default is 0
        :type skipLines: int 
        '''
        
        if type(seqOrFileName) == list:
            seq = seqOrFileName
        else:
            seq = []
            with open(seqOrFileName, 'r') as fd:
                csvReader = csv.reader(fd, delimiter=csvDelimiter, quotechar=csvQuotechar)
                for i in range(skipLines): #@UnusedVariable
                    csvReader.next()
                for rowArr in csvReader:
                    try:
                        num = float(rowArr[colIndex])
                    except ValueError:
                        raise ValueError("All rows in the data file ('%s') must be numbers in column %s; found: %s" % (seqOrFileName, str(colIndex), str(rowArr)))
                    except IndexError:
                        # If empty line, just skip it:
                        if len(rowArr) == 0:
                            continue
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
        
    def testSingleColFile(self):
        res = DiscreteDifferentiator.differentiate('TestData/singleCol.csv', 1, outFileFd=open(os.devnull,'w'))
        expected = [2 for i in range(20)] #@UnusedVariable
        self.assertEqual(expected, res, 'Linear func from single column file failed')
        
    def testTwoColFile(self):
        res = DiscreteDifferentiator.differentiate('TestData/twoCol.csv', 1, outFileFd=open(os.devnull,'w'), colIndex=1)
        expected = [2 for i in range(20)] #@UnusedVariable
        self.assertEqual(expected, res, 'Linear func from two column file failed')
        
    def testSingleColFileWithColHeader(self):
        res = DiscreteDifferentiator.differentiate('TestData/singleColWithHeader.csv', 1, outFileFd=open(os.devnull,'w'), skipLines=1)
        expected = [2 for i in range(20)] #@UnusedVariable
        self.assertEqual(expected, res, 'Linear func from single column file with column header failed')

if __name__ == '__main__':
    #unittest.main()
    #sys.exit()
    
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--colIndex', 
                        help='index of column in CSV file that contains the number sequence to differentiate \n' +\
                             'Default: 0.',
                        dest='colIndex',
                        default=0);
    parser.add_argument('-d', '--delimiter', 
                        help='CSV field delimiter. Default: comma.', 
                        dest='csvDelimiter',
                        default=',');
    parser.add_argument('-q', '--csvQuotechar', 
                        help='CSV delimiter escape quote char. Default: double-quote.', 
                        dest='csvQuotechar',
                        default='"');
    parser.add_argument('-s', '--skipLines', 
                        help='number of lines to skip in file to avoid column headers, etc. Default: 0', 
                        dest='skipLines',
                        default=0);
    parser.add_argument('fileName',
                        help='The CSV file path.'
                        ) 
    
    args = parser.parse_args();

    DiscreteDifferentiator.differentiate(args.fileName, 
                                         colIndex=int(args.colIndex),
                                         csvDelimiter=args.csvDelimiter,
                                         csvQuotechar=args.csvQuotechar,
                                         skipLines=int(args.skipLines)
                                         )
    
        
    