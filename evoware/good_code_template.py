#! /usr/bin/env python

"""Short one-line description of this module"""

import sys ## keep import statements at the top of the module


class ExampleException( Exception ):
    pass


class ExampleClass( object ):
    """
    Detailed description of this class.

    The first letter of a class is Uppercase. All classes should be
    derived from object to allow the use of properties in Python 2.

    Coding rules:

      * Indentation -- 4 spaces; no Tab characters. Adapt your editor!

      * Reporting -- don't use print statements anywhere within library classes.

      * Width -- please try to keep your code within the classic 80 char. limit.
    """

    def __init__(self, name, parent=None, verbose=0 ):
        """
        Describe all arguments of the method so that they can be parsed by
        epydoc.
        
        @param name:   str; name of this object
        @param parent: ExampleClass; parent object [None]
        @param verbose: int; verbosity level from 0 (default) to 3
        """
        ## try declaring all fields 
        self.name = name
        self._parent = parent
        self.verbose = verbose


    def reportSomething( self ):
        """
        Create a simple report.
        @return: str; Fake report
        """
        return "%s: Hello World!" % self.name

    ## Use properties!
    def setParent( self, o ):
        self._parent = str(o)

    def getParent( self ):
        return self._parent

    parent = property( getParent, setParent )

    ## Override Python special methods!
    def __str__( self ):
        """String representation of this object"""
        if not self.parent:
            return self.name

        return str( self.parent ) + ' > ' + self.name

######################
### Module testing ###
import test

class Test(test.AutoTest):
    """Test GoodCodeTemplate"""

    TAGS = [ test.LONG ]

    def prepare( self ):
        self.e1 = ExampleClass( 'example1' )

    def test_exampleReport( self ):
        """ExampleClass.report test"""
        self.result = self.e1.reportSomething()

        if self.local:   ## only if the module is executed directly
            print
            print self.result 

        self.assertEqual( self.result, 'example1: Hello World!',
                          'unexpected result' )

    def test_exampleParent( self ):
        """ExampleClass.parent test"""
        self.e2 = ExampleClass( 'example2' )
        self.e2.parent = self.e1
        
        if self.local:
            print
            print self.e2

        self.assertEqual( str(self.e2), 'example1 > example2' )

if __name__ == '__main__':

    test.localTest()
