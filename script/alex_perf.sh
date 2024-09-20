#!/bin/bash

OUTPUT_PATH="../output/alex_all_perf_.csv"
DATASETS="osm"
#DATASETS="fb"
SEARCHS="exponential mb_bbin ex_mb_bbin mb_slin ex_mb_slin"
#SEARCHS="ex_mb_bbin"
OP_NUM=100000
TABLE_SIZE=200000000
PERFS="2 3"
DELTAS="0.2 0.3 0.4 0.5 0.6 0.7"

for DATASET in $DATASETS; do
	for SEARCH in $SEARCHS; do
		for DELTA in $DELTAS; do
			for PERF in $PERFS; do
				# gdb --args \
				../build/microbench \
					--keys_file=../datasets/$DATASET \
					--keys_file_type=binary \
					--read=1 \
					--operations_num=$OP_NUM \
					--table_size=$TABLE_SIZE \
					--init_table_ratio=0.5 \
					--thread_num=1 \
					--index=alex \
					--memory \
					--search_type=$SEARCH \
					--output_path=$OUTPUT_PATH \
					--perf_no=$PERF \
					--delta=$DELTA 
				done
			done
		done
	done
