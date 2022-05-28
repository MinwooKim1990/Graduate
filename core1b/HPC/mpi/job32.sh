#!/bin/bash

mpiexec -n 32 ./main -N 1 -t BENCH
mpiexec -n 32 ./main -N 2 -t BENCH
mpiexec -n 32 ./main -N 4 -t BENCH
mpiexec -n 32 ./main -N 8 -t BENCH
mpiexec -n 32 ./main -N 16 -t BENCH
mpiexec -n 32 ./main -N 32 -t BENCH
mpiexec -n 32 ./main -N 64 -t BENCH
mpiexec -n 32 ./main -N 128 -t BENCH
mpiexec -n 32 ./main -N 256 -t BENCH
mpiexec -n 32 ./main -N 512 -t BENCH
mpiexec -n 32 ./main -N 1024 -t BENCH
mpiexec -n 32 ./main -N 2048 -t BENCH
mpiexec -n 32 ./main -N 4096 -t BENCH
mpiexec -n 32 ./main -N 8192 -t BENCH
mpiexec -n 32 ./main -N 16384 -t BENCH
mpiexec -n 32 ./main -N 32768 -t BENCH
mpiexec -n 32 ./main -N 65536 -t BENCH
mpiexec -n 32 ./main -N 131072 -t BENCH
mpiexec -n 32 ./main -N 262144 -t BENCH
mpiexec -n 32 ./main -N 524288 -t BENCH
mpiexec -n 32 ./main -N 1048576 -t BENCH
mpiexec -n 32 ./main -N 2097152 -t BENCH
mpiexec -n 32 ./main -N 4194304 -t BENCH
mpiexec -n 32 ./main -N 8388608 -t BENCH
mpiexec -n 32 ./main -N 16777216 -t BENCH
