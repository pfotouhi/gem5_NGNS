#!/usr/bin/env python
import sys 
import os
import string


# This file extracts stats while jumping over the first set of sets (in many workloads that is the app setup phase we're not interested in) 
# IMPORTANT: You have to pass the *absolute* path of the stats.txt file to this script, e.g. /home/pfotouhi/LBL/is_A-Garnet-Base/stats.tx)  
# as well as the absolute path to the output file, i.e. 
# ./lbl_bottleneck_parser.py /home/swerner/LBL/is_A-Base/stats.txt /home/swerner/gem5_NGNS/result_scripts/lbl_results.txt 

# IMPORTANT for stats, set me correctly
num_memory_controllers = 4 
num_routers = 4
ticks_to_cycles = 1000  # that'd be for 1GHz, i.e. 1000 ticks per cycle 

# General stats
sim_seconds = 0
sim_ticks = 0
sim_freq = 0
# NoC stats 
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
# DRAM / Memory controller stats
total_ticks_spent_queueing_mc = 0 # queueling delay indicating of BW and latency
total_time_on_data_bus = 0  # indication of impact on higher mc-to-dram BW 
total_bytes_read_mc = 0  # bytes read from dram 
total_bytes_written_mc = 0 # bytes written from dram
avg_memory_access_latency = 0 # total ticks spent from burst creation until serviced by the DRAM, avg. memory access latency per DRAM burst
data_bus_util_perc = 0 # Data bus utilization in percentage
avgQLat = 0

counter_begin = 0 # needed to skip the first set of stats, which is the warm-up phase

with open(sys.argv[1],'r') as search: 
	for line in search: 
		if "Begin" in line: 
			counter_begin = counter_begin + 1

		if counter_begin == 2: 
			if "sim_seconds" in line: 
				temp_list = line.split()
			        sim_seconds = float(temp_list[1])
                        if "sim_ticks" in line: 
                                temp_list = line.split()
                                sim_ticks = float(temp_list[1])
                        if "sim_freq" in line: 
                                temp_list = line.split()
                                sim_freq = float(temp_list[1])
                        if "final_tick" in line:
                                temp_list = line.split()
                                final_tick = float(temp_list[1])
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
                        if "avgMemAccLat" in line: 
                                temp_list = line.split()
                                avg_memory_access_latency = avg_memory_access_latency + float(temp_list[1])
                        if "busUtil " in line: 
                                temp_list = line.split()
                                data_bus_util_perc = data_bus_util_perc + float(temp_list[1])
                        if "avgQLat" in line: 
                                temp_list = line.split()
                                avgQLat = avgQLat + float(temp_list[1])

with open(sys.argv[2], "a") as results:
    results.write("=========================================================================== \n")
    results.write("Simulation Stats:" + str(sys.argv[1]) + "\n")
    results.write("=========================================================================== \n")
    results.write("Seconds simulated: " + str(sim_seconds) + "\n")
    results.write("Ticks simulated: " + str(sim_ticks) + "\n")
    results.write("Cycles simulated: " + str(sim_ticks / ticks_to_cycles) + "\n")
    results.write("System frequency (GHz): " + str(sim_freq / 1000000000000) + "\n")
    results.write("================================================================= \n")
    results.write("==== NoC stats ==== \n")    
    results.write("External Link traversals: " + str(external_link_traversals) + "\n")
    results.write("Internal Link traversals: " + str(internal_link_traversals) + "\n")
    results.write("Average hops: " + str(avgr_hops) + "\n")
    results.write("Average packet latency: " + str(average_packet_latency) + "\n")
    results.write("Router buffer reads (per router): " + str(buffer_reads / num_routers) + "\n")
    results.write("Router buffer reads (total): " + str(buffer_reads) + "\n")
    results.write("Router buffer writes (per router): " + str(buffer_writes / num_routers) + "\n")
    results.write("Router buffer writes (total): " + str(buffer_writes) + "\n")
    results.write("Router crossbar traversals (per router): " + str(crossbar_activity / num_routers) + "\n")
    results.write("Router crossbar traversals (total): " + str(crossbar_activity) + "\n")
    results.write("================================================================= \n")
    results.write("==== Memory Controller / DRAM stats ==== \n")
    results.write("Percentage data bus utilization (avg per controller): " + str((data_bus_util_perc / num_memory_controllers) / 100) + "\n")
    results.write("Total bytes read from DRAM: " + str(total_bytes_read_mc) + "B, " + str(total_bytes_read_mc/(1024*2014)) + "MB" + "\n") 
    results.write("Total bytes written to DRAM: " + str(total_bytes_written_mc) + "B, " + str(total_bytes_written_mc/(1024*2014)) + "MB" + "\n")
    results.write("Average memory access latency per DRAM burst (cycles): " + str(avg_memory_access_latency / num_memory_controllers / ticks_to_cycles) + "\n")
    results.write("Average memory queueing delay per DRAM burst (cycles): " + str(avgQLat / num_memory_controllers / ticks_to_cycles) + "\n")
    results.write("================================================================= \n")
    results.write("\n \n")

# remove comment if you want it printed out on screen 
'''
print "========= Simulation Stats =========="
print " "
print "Seconds simulated: ", sim_seconds 
print "Ticks simulated: ", sim_ticks
print "Cycles simulated: ", sim_ticks / ticks_to_cycles
sim_freq_GHz = sim_freq / 1000000000000 # one tick is one 1ps, so x 10^-12
print "System frequency (GHz): ", sim_freq_GHz
print " " 
print "===== NoC stats ====="
print "External Link traversals: ", external_link_traversals
print "Internal Link traversals: ", internal_link_traversals
print "Average hops: ", avgr_hops
print "Average packet latency: ", average_packet_latency
print "Router buffer reads "
print "     Total: ", buffer_reads
print "     Per Router: ", buffer_reads / num_routers
print "Router buffer writes "
print "     Total: ", buffer_writes 
print "     Per Router: ", buffer_writes / num_routers
print "Router crossbar traversals" 
print "     Total: ", crossbar_activity 
print "     Per Router: ", crossbar_activity / num_routers
print " "
print "===== Memory Controller / DRAM stats ======"
print "Total number of cycles spent queueing "
print "     Total: ", total_ticks_spent_queueing_mc / ticks_to_cycles 
print "     Per controller: ", (total_ticks_spent_queueing_mc / ticks_to_cycles) / num_memory_controllers 
print "Percentage cycles spent queueing (per controller): ", (total_ticks_spent_queueing_mc / num_memory_controllers) / sim_ticks
print "Total cycles on data bus "
print "     Total: ",  total_time_on_data_bus / ticks_to_cycles
print "     Per controller: ", (total_time_on_data_bus / ticks_to_cycles) / num_memory_controllers 
print "Percentage cycles spent on data bus vs. total executed cycles (avg per controller): ", (total_time_on_data_bus / num_memory_controllers) / sim_ticks / ticks_to_cycles
print "Percentage data bus utilization (avg per controller): ", (data_bus_util_perc / num_memory_controllers) / 100
print "Total bytes read from DRAM: ", total_bytes_read_mc,"B ,", total_bytes_read_mc/(1024*2014),"MB"
print "Total bytes written to DRAM: ", total_bytes_written_mc,"B ,", total_bytes_written_mc/(1024*2014),"MB"
print "Average memory access latency per DRAM burst (cycles): ", avg_memory_access_latency / num_memory_controllers / ticks_to_cycles
print "Average memory queueing delay per DRAM burst (cycles): ", avgQLat / num_memory_controllers / ticks_to_cycles
'''
