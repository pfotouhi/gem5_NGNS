import math
from m5.params import *
from m5.objects import *

from BaseTopology import SimpleTopology

class Mesh_XY_Test_MemNet_Chain(SimpleTopology):
    description='Mesh_XY_Test_MemNet_Chain'

    def __init__(self, controllers):
        self.nodes = controllers

    # Makes a generic mesh with memory pins on the side edges of the chip (e.g. makes 16 pins on a 8x8 mesh)
    # HMCs, modelled as Dirs, are chained on each memory pin 

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        nodes = self.nodes
	
	# it looks like len(nodes) is num_cpus + num_dirs
	concentration_factor = options.concentration
	num_of_cpus 	     = options.num_cpus
	num_of_dirs 	     = options.num_dirs
	num_rows 	     = int(math.sqrt(num_of_cpus))
	num_columns 	     = num_rows # Assume a square mesh
	num_routers 	     = int(options.num_cpus / concentration_factor + num_of_dirs) 	
	num_on_chip_routers  = int(options.num_cpus / concentration_factor)

        link_latency   = options.link_latency   # used by simple and garnet
        router_latency = options.router_latency # only used by garnet

        # There must be an evenly divisible number of cntrls to routers
        # Also, obviously the number or rows must be <= the number of routers
        cntrls_per_router, remainder = divmod(len(nodes), num_routers)
        assert(num_rows > 0 and num_rows <= num_routers)

        # Create the routers in the mesh
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
        # for(i,n): i is iterator, n the actual payload in network_nodes
	# nodes: first all l1_cntrls (e.g. 0..15) then all dir_cntrl (e.g. 0..15)
	# In Mesh_XY, num_cpu = num_routers. I.e. L1cntrl and Dir1ctrnl are at same router
	
	ext_links = []
        # Connect CPUs to routers 
	for (i, n) in enumerate(network_nodes):
	    if(i < num_of_cpus):
            	print "EXTERNAL LINKS ", i,n 
	    	cntrl_level, router_id = divmod(i, num_on_chip_routers)
            	assert(cntrl_level < cntrls_per_router)
            	ext_links.append(ExtLink(link_id=link_count, ext_node=n,
                                    int_node=routers[router_id],
                                    latency = link_latency, weight=1))
            	link_count += 1
	# Connect Dirs to routers (modelling an HMC)
	# Example topology here: Chain HMCs at each pin, assume one pin per row on each side of chip
	num_of_pins = num_rows
	num_of_dirs_per_pin = num_of_dirs / (num_rows*2)
	for (i, n) in enumerate(network_nodes):
	    if(i >= num_of_cpus):
	    	pin_id = (i-num_of_cpus) / num_of_dirs_per_pin
 	    	router_id = num_of_cpus + pin_id*num_of_dirs_per_pin + i%num_of_dirs_per_pin
	    	current_node_id = i
  	    	ext_links.append(ExtLink(link_id=link_count, ext_node=n, 
					int_node=routers[router_id],
					latency = link_latency, weight=1))
		link_count+=1	    
	
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

        # Create the mesh links.
        int_links = []
	
	# FIRST: Create router links on-chip:
        # East output to West input links (weight = 1)
        for row in xrange(num_rows):
            for col in xrange(num_columns):
                if (col + 1 < num_columns):
                    east_out = col + (row * num_columns)
                    west_in = (col + 1) + (row * num_columns)
                    int_links.append(IntLink(link_id=link_count,
                                             src_node=routers[east_out],
                                             dst_node=routers[west_in],
                                             src_outport="East",
                                             dst_inport="West",
                                             latency = link_latency,
                                             weight=1))
                    link_count += 1

	# West output to East input links (weight = 1)
        for row in xrange(num_rows):
            for col in xrange(num_columns):
                if (col + 1 < num_columns):
                    east_in = col + (row * num_columns)
                    west_out = (col + 1) + (row * num_columns)
                    int_links.append(IntLink(link_id=link_count,
                                             src_node=routers[west_out],
                                             dst_node=routers[east_in],
                                             src_outport="West",
                                             dst_inport="East",
                                             latency = link_latency,
                                             weight=1))
                    link_count += 1

        # North output to South input links (weight = 2)
        for col in xrange(num_columns):
            for row in xrange(num_rows):
                if (row + 1 < num_rows):
                    north_out = col + (row * num_columns)
                    south_in = col + ((row + 1) * num_columns)
                    int_links.append(IntLink(link_id=link_count,
                                             src_node=routers[north_out],
                                             dst_node=routers[south_in],
                                             src_outport="North",
                                             dst_inport="South",
                                             latency = link_latency,
                                             weight=2))
                    link_count += 1

        # South output to North input links (weight = 2)
        for col in xrange(num_columns):
            for row in xrange(num_rows):
                if (row + 1 < num_rows):
                    north_in = col + (row * num_columns)
                    south_out = col + ((row + 1) * num_columns)
                    int_links.append(IntLink(link_id=link_count,
                                             src_node=routers[south_out],
                                             dst_node=routers[north_in],
                                             src_outport="South",
                                             dst_inport="North",
                                             latency = link_latency,
                                             weight=2))
                    link_count += 1


	# SECOND: Connect routers with directories 	
	for row in xrange(num_rows):
		rid_left_edge 		= row*num_columns
		rid_right_edge	        = row*num_columns + num_columns-1
		rid_first_dir_left_edge   = num_of_cpus + row*num_of_dirs_per_pin
		rid_first_dir_right_edge   = num_of_cpus + row*num_of_dirs_per_pin + (num_rows*num_of_dirs_per_pin)
		
		print " row: ", row
		print " rid_left_edge: ", rid_left_edge
		print " rid_right_edge ", rid_right_edge
		print " rid_first_dir_left_edge: ", rid_first_dir_left_edge
		print " rid_first_dir_right_edge: ", rid_first_dir_right_edge 

		# Left edge of chip	
		# Edge router to first dir left 
		int_links.append(IntLink(link_id=link_count,src_node=routers[rid_left_edge],dst_node=routers[rid_first_dir_left_edge],
                                         src_outport="West",dst_inport="East",latency = link_latency,weight=1))
                link_count += 1
		print "IntLink: Router ", rid_left_edge , " West to East " , rid_first_dir_left_edge  
		int_links.append(IntLink(link_id=link_count,src_node=routers[rid_first_dir_left_edge],dst_node=routers[rid_left_edge],
                                         src_outport="East",dst_inport="West",latency = link_latency,weight=1))
                link_count += 1
		print "IntLink: Router ", rid_first_dir_left_edge , " East to West " , rid_left_edge    
					
		# Edge router to first dir right 
		int_links.append(IntLink(link_id=link_count,src_node=routers[rid_right_edge],dst_node=routers[rid_first_dir_right_edge],
                                         src_outport="East",dst_inport="West",latency = link_latency,weight=1))
                link_count += 1
                print "IntLink: Router ", rid_right_edge , " West to East " , rid_first_dir_right_edge
                int_links.append(IntLink(link_id=link_count,src_node=routers[rid_first_dir_right_edge],dst_node=routers[rid_right_edge],
                                         src_outport="West",dst_inport="East",latency = link_latency,weight=1))
                link_count += 1
                print "IntLink: Router ", rid_first_dir_right_edge , " West to East " , rid_right_edge

	
		for i in range(1, num_of_dirs_per_pin):
			int_links.append(IntLink(link_id=link_count,src_node=routers[rid_first_dir_left_edge + (i-1)],dst_node=routers[rid_first_dir_left_edge + i],
                                         src_outport="West",dst_inport="East",latency = link_latency,weight=1))
	                link_count += 1
        	        print "IntLink: Router ", rid_first_dir_left_edge + (i-1) , " West to East " , rid_first_dir_left_edge + i
			int_links.append(IntLink(link_id=link_count,src_node=routers[rid_first_dir_left_edge + i],dst_node=routers[rid_first_dir_left_edge + (i-1)],
                                         src_outport="East",dst_inport="West",latency = link_latency,weight=1))
                	link_count += 1
			print "IntLink: Router ", rid_first_dir_left_edge + i , " East to West " , rid_first_dir_left_edge + (i-1)
			int_links.append(IntLink(link_id=link_count,src_node=routers[rid_first_dir_right_edge + (i-1)],dst_node=routers[rid_first_dir_right_edge + i],
                                         src_outport="East",dst_inport="West",latency = link_latency,weight=1))
                        link_count += 1
			print "IntLink: Router ", rid_first_dir_right_edge + (i-1) , " East to West " , rid_first_dir_right_edge + i
                        int_links.append(IntLink(link_id=link_count,src_node=routers[rid_first_dir_right_edge + i],dst_node=routers[rid_first_dir_right_edge + (i-1)],
                                         src_outport="West",dst_inport="East",latency = link_latency,weight=1))
                        link_count += 1
	       	        print "IntLink: Router ", rid_first_dir_right_edge + i , " West to East " , rid_first_dir_right_edge + (i-1)
	network.int_links = int_links
