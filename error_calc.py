"""
Calculates error for circular & gaussian distributions. Command line interface.
"""
import sys

def error_from_68p(argv):
    for arg in argv[1:]:
        value = float(arg)
        err95 = 1.62 
        errCEP = 0.78
        err95_result = err95 * value
        errCEP_result = errCEP * value
        print "68% precision is {0}".format(value)
        print "95% precision is {0}".format(err95_result)
        print "CEP is {0}".format(errCEP_result)
        print "=========="

if __name__ == '__main__':
    error_from_68p(sys.argv)