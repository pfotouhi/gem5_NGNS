from m5.params import *
from m5.objects import *

from BaseTopology import SimpleTopology

# This topology works only for 64 nodes
# It is the AWGR topology in which 8 nodes are clustered at one router, and you have a global bi-directional crossbar

class AWGR_64_8C_all_to_all(SimpleTopology):
    description='AWGR_64_8C_all_to_all'

    def __init__(self, controllers):
        self.nodes = controllers

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        nodes = self.nodes

        num_routers = 8

        #link_latency = options.link_latency # used by simple and garnet
        link_latency = 1
        router_latency = options.router_latency # only used by garnet

	cntrls_per_router, remainder = divmod(len(nodes), num_routers)
	

        routers = [Router(router_id=i, latency = router_latency) \
            for i in range(num_routers)]
        network.routers = routers

        # link counter to set unique link ids
        link_count = 0

        # Add all but the remainder nodes to the list of nodes to be uniformly
        # distributed across the network.
        network_nodes = []
        remainder_nodes = []
        for node_index in xrange(len(nodes)):
            if node_index < (len(nodes) - remainder):
                network_nodes.append(nodes[node_index])
            else:
                remainder_nodes.append(nodes[node_index])

        # Connect each node to the appropriate router
        ext_links = []
        for (i, n) in enumerate(network_nodes):
            cluster_id, in_cluster_id = divmod(i, 8) # since we have clusters of 8
            cntrl_level, router_id = divmod(cluster_id, num_routers)
            assert((cntrl_level*8 + in_cluster_id) < cntrls_per_router)
            ext_links.append(ExtLink(link_id=link_count, ext_node=n,
                                    int_node=routers[router_id],
                                    latency = link_latency,weight=1))
            link_count += 1
	
	# Connect the remainding nodes to router 0.  These should only be
        # DMA nodes.
        for (i, node) in enumerate(remainder_nodes):
            assert(node.type == 'DMA_Controller')
            assert(i < remainder)
            ext_links.append(ExtLink(link_id=link_count, ext_node=node,
                                    int_node=routers[0],
                                    latency = link_latency)) 
            link_count += 1

        network.ext_links = ext_links

	# ------- This is where the topology starts -------

        # Create links.
        int_links = []
	
	for x in xrange(num_routers):
	    for i in xrange(num_routers):
		if i != x: 
			int_links.append(IntLink(link_id=link_count,
                                         src_node=routers[x],
                                         dst_node=routers[i],
                                         src_outport=str(i),
                                         dst_inport=str(x),
                                         latency = link_latency+1, #+1 models the 64b/cyc BW (needs 1 cyc more than 128b/cyc of external links) 
                                         weight=1))
                	link_count += 1

	network.int_links = int_links	







