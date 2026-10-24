#!/bin/bash
#$ -N nn_experiment
#$ -cwd
#$ -q MANSCI,COB
#$ -pe smp 40
#$ -l h_rt=168:00:00
#$ -j y
#$ -o nn_experiment.log

set -euo pipefail

# Submit with qsub from the repository directory.
cd "${SGE_O_WORKDIR:-$(pwd)}"

module purge
module load stack/2022.2
module load gurobi/9.5.2_gcc-9.5.0
source .venv/bin/activate

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
# Use CPU training.
export CUDA_VISIBLE_DEVICES=""

date
hostname
python --version

python -u pipeline.py \
    --n_baseline_workers 20 \
    --n_ft_workers 20 \
    --n_opt_workers 10 \
    --gurobi_threads 1

date
