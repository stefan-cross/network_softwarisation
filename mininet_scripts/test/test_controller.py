#!/usr/bin/env python

"""
Test a controller in Mininet
"""

import unittest
import pexpect

class testControllers( unittest.TestCase ):
    
    commandline = 'mininet>'
    
    def connectivityTest( self, name, controllerMap ):

        # test switches associated to the controller from by controller map
        pexp = pexpect.spawn( 'python -m %s' % name )
        pexp.expect( self.commandline )

        # test all nodes are reachable
        pexp.sendline( 'pingall' )
        pexp.expect( '(\d+)%  dropped' )
        percent = int( pexp.match.group( 1 ) ) if pexp.match else -1
        self.assertEqual( percent, 0 )
        pexp.expect( self.commandline )

        # test each switch connectivity to controller
        for switch in controllerMap:
            pexp.sendline( 'sh ovs-vsctl get-controller %s' % switch )
            pexp.expect( 'tcp:([\d.:]+)')
            actual = pexp.match.group(1)
            expected = controllerMap[ switch ]
            self.assertEqual( actual, expected )

        pexp.expect( self.commandline )
        pexp.sendline( 'exit' )
        pexp.wait()

    def testController( self ):
        controller0 = '127.0.0.1:6633'
        controller1 = '127.0.0.1:6634'
        controllerMap = { 's1': controller0, 's2': controller1}
        self.connectivityTest( 'controllers', controllerMap )

if __name__ == '__main__':
    unittest.main()
