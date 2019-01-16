# Copyright (c) 2010 Advanced Micro Devices, Inc.
#               2016 Georgia Institute of Technology
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Brad Beckmann
#          Tushar Krishna

from m5.params import *
from m5.objects import *

from BaseTopology import SimpleTopology


class ESUMA(SimpleTopology):
    description='ESUMA'

    def __init__(self, controllers):
        self.nodes = controllers


    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        # link counter to set unique link ids
	link_count = 0
	cache_nodes = []
	dir_nodes = []
	dma_nodes = []
		
	for node in self.nodes:
            if node.type == 'L1Cache_Controller':
                cache_nodes.append(node)
	    elif node.type == 'Directory_Controller' or \
		node.type == 'L2Cache_Controller':
		dir_nodes.append(node)
	    elif node.type == 'DMA_Controller':
		dma_nodes.append(node)
            elif node.type == 'L0Cache_Controller':
                pass
	    else:
		raise Exception("Bad node!")
		
	num_routers = 16
		
	routers = [Router(router_id=i, latency = 1) \
                    for i in range(num_routers)]
	network.routers = routers
		
		
	for (i, cntrl_node) in enumerate(cache_nodes):
	    link = ExtLink(link_id=link_count, ext_node=cntrl_node,
			    int_node=routers[i/8], latency = 1)
	    print "Connecting node %s to router %d" % (cntrl_node, routers[i/8].router_id)
	    link_count += 1
	    network.ext_links.append(link)
		
	for (i, cntrl_node) in enumerate(dir_nodes):
	    link = ExtLink(link_id=link_count, ext_node=cntrl_node,
			    int_node=routers[8+i%8], latency = 1)
	    print "Connecting node %s to router %d" % (cntrl_node, routers[8+i%8].router_id)
	    link_count += 1
	    network.ext_links.append(link)
		
	for (i, cntrl_node) in enumerate(dma_nodes):
	    link = ExtLink(link_id=link_count, ext_node=cntrl_node,
			    int_node=routers[0], latency = 1)
	    print "Connecting node %s to router %d" % (cntrl_node, routers[0].router_id)
	    link_count += 1
	    network.ext_links.append(link)
	
	# Now creating the desired topology (here is all to all) on top of clusters
	for i in range(len(routers)):
	    for j in range(i+1,len(routers)):
		link_out = IntLink(link_id=link_count, src_node=routers[i],
				dst_node=routers[j])
		link_count += 1
		link_in = IntLink(link_id=link_count, src_node=routers[j],
			        dst_node=routers[i])
		link_count += 1
		print "Connecting router %d to router %d" % (routers[i].router_id, routers[j].router_id)
		link_out.latency = 10
		link_in.latency = 10
		network.int_links.append(link_out)
		network.int_links.append(link_in)		
