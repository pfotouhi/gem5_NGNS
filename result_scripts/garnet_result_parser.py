#!/usr/bin/env python

# This file extracts stats while jumping over the first set of sets

sim_seconds = 0
external_link_traversals = 0
internal_link_traversals = 0
average_packet_latency = 0
packets_received = 0
avgr_hops = 0 
packet_queuing_latency = 0
buffer_reads = 0
buffer_writes = 0
sw_input_arbiter_activity = 0
sw_output_arbiter_activity = 0
crossbar_activity = 0

counter_begin = 0 # you need to jump the first set of stats, which is the warm-up phase 

with open("blackscholes_medium.rcS/Mesh_XY") as search: 
	for line in search: 
		if "Begin" in line: 
			counter_begin = counter_begin + 1

		if counter_begin == 2: 
			if "sim_seconds" in line: 
				temp_list = line.split()
				print "sim_seconds: ", temp_list[1]
			if "system.ruby.network.ext_in_link_utilization" in line: 
				temp_list = line.split()
				external_link_traversals = external_link_traversals + float(temp_list[1]) 
			if "system.ruby.network.ext_out_link_utilization" in line: 
				temp_list = line.split()
                        	external_link_traversals = external_link_traversals + float(temp_list[1])
			if "system.ruby.network.int_link_utilization" in line:
                        	temp_list = line.split()
                        	internal_link_traversals = internal_link_traversals + float(temp_list[1])
			if "system.ruby.network.average_packet_latency" in line:
                        	temp_list = line.split()
                        	average_packet_latency = average_packet_latency + float(temp_list[1])
			if "system.ruby.network.packets_received::total" in line:
                        	temp_list = line.split()
                        	packets_received = packets_received + float(temp_list[1])
			if "system.ruby.network.average_hops" in line:
                        	temp_list = line.split()
                        	avgr_hops = avgr_hops + float(temp_list[1])
			if "buffer_reads" in line: 
				temp_list = line.split()
				buffer_reads = buffer_reads + float(temp_list[1])
			if "buffer_writes" in line: 
                        	temp_list = line.split()
				buffer_writes = buffer_writes + float(temp_list[1])	
			if "sw_input_arbiter_activity" in line: 
				temp_list = line.split()
				sw_input_arbiter_activity = sw_input_arbiter_activity + float(temp_list[1])
			if "sw_output_arbiter_activity" in line: 
				temp_list = line.split()
				sw_output_arbiter_activity = sw_output_arbiter_activity + float(temp_list[1])
			if "crossbar_activity" in line: 
				temp_list = line.split()
				crossbar_activity = crossbar_activity + float(temp_list[1])


print "External Link traversals: ", external_link_traversals
print "Internal Link traversals: ", internal_link_traversals
print "Average hops: ", avgr_hops
print "Average packet latency: ", average_packet_latency
print "Number of packets received: ", packets_received
print "Router buffer reads: ", buffer_reads
print "Router buffer writes: ", buffer_writes
print "Router sw input arbiter: ', sw_input_arbiter_activity
print "Router sw output arbiter: ", sw_output_arbiter_activity
print "Router crossbar traversals: ", crossbar_activity





