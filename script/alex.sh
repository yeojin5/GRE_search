#!/bin/bash

OUTPUT_PATH="../output/alex_breakdown_ex.csv"
DATASETS="books covid fb genome libio osm planet stack wise"
OP_NUM=200000000
TABLE_SIZE=200000000

for DATASET in $DATASETS; do
    ../build/microbench \
        --keys_file=../datasets/$DATASET \
        --keys_file_type=binary \
        --read=0.5 --insert=0.5 \
        --operations_num=$OP_NUM \
        --table_size=$TABLE_SIZE \
        --init_table_ratio=0.5 \
        --thread_num=1 \
        --index=alex \
        --memory \
        --output_path=$OUTPUT_PATH
done
