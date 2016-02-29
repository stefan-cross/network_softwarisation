#!/usr/bin/python

"""
Create a network where different switches are connected to
different controllers, by creating a custom Switch() subclass.
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.topolib import TreeTopo
from mininet.cli import CLI

# Set up two local controllers
controller0 = Controller( 'controller0', port=6633 )
controller1 = Controller( 'controller1', port=6634 )
controllerMap = { 's1': controller0, 's2': controller1 }

class MultipleSwitch( OVSSwitch ):
    def start( self, controllers ):
        return OVSSwitch.start( self, [ controllerMap[ self.name ] ] )

topo = TreeTopo( depth=2, fanout=2 )
net = Mininet( topo=topo, switch=MultiSwitch, build=False )
for c in [ controller0, controller1 ]:
    net.addController(c)
net.build()
net.start()
CLI( net )
net.stop()
