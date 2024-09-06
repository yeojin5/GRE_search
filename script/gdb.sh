#!/bin/bash

OUTPUT_PATH="../output/gdb.csv"
DATASETS="books"
OP_NUM=20000000
TABLE_SIZE=20000000

for DATASET in $DATASETS; do
    gdb --args ../build/microbench \
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

