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
total_ticks_spent_queueing_mc = 0 # queueling delay indicating of BW and latency
total_time_on_data_bus = 0  # indication of impact on higher mc-to-dram BW 
total_bytes_read_mc = 0  # bytes read from dram 
total_bytes_written_mc = 0 # bytes written from dram 

sim_ticks = 0


counter_begin = 0 # you need to jump the first set of stats, which is the warm-up phase 

with open("/home/pfotouhi/LBL/is_A-Garnet-Base/stats.txt") as search: 
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
                        if "totQLat" in line:
                                temp_list = line.split()
                                total_ticks_spent_queueing_mc = total_ticks_spent_queueing_mc + float(temp_list[1])
                        if "totBusLat" in line: 
                                temp_list = line.split()
                                total_time_on_data_bus = total_time_on_data_bus + float(temp_list[1])      
                        if "bytesReadDRAM" in line: 
                                temp_list = line.split()
                                total_bytes_read_mc = total_bytes_read_mc + float(temp_list[1])
                        if "bytesWritten" in line:
                                temp_list = line.split()
                                total_bytes_written_mc = total_bytes_written_mc + float(temp_list[1])
                        if "final_tick" in line: 
                                temp_list = line.split()
                                final_tick = float(temp_list[1])

print "==== NoC stats ===="
print "External Link traversals: ", external_link_traversals
print "Internal Link traversals: ", internal_link_traversals
print "Average hops: ", avgr_hops
print "Average packet latency: ", average_packet_latency
print "Router buffer reads: ", buffer_reads
print "Router buffer writes: ", buffer_writes
print "Router sw input arbiter: ", sw_input_arbiter_activity
print "Router sw output arbiter: ", sw_output_arbiter_activity
print "Router crossbar traversals: ", crossbar_activity
print "==== Memory Controller / DRAM stats"
print "Total number of ticks spent queueing: ", total_ticks_spent_queueing_mc
print "Total number of cycles spent queueing: ", total_ticks_spent_queueing_mc / 1000
print "Total number of cycles simulated ", final_tick / 1000
print "Percentage cycles spent queueing: ", total_ticks_spent_queueing_mc / final_tick
print "Total time on data bus: ", total_time_on_data_bus
print "Total bytes read from DRAM: ", total_bytes_read_mc
print "Total bytes written to DRAM: ", total_bytes_written_mc




