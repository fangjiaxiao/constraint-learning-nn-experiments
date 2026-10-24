# Neural Network Training, Pruning, and Optimization Pipeline

This repository provides the computational pipeline accompanying *Constraint Learning by Optimizing over Trained Neural Networks: A Pragmatic Tutorial*.

A configurable pipeline for training and pruning ReLU neural networks and embedding them into mixed-integer linear optimization models.

The workflow includes training, pruning and fine-tuning, efficient-frontier selection, optimization, and result analysis. An example dataset, `complex_data.csv`, is included.

## Setup

Use Python 3.10 and install the dependencies:

```bash
pip install -r requirements.txt
```

A valid Gurobi license is required for optimization.

## Usage

1. Edit `CONFIG` at the beginning of `pipeline.py` to specify your dataset, features, network and training settings, and optimization constraints. Replace the example-specific settings with those for your problem.
2. For cluster execution, edit `run_experiment.sh` to configure your environment, resources, and parallel workers.
3. Run from the repository directory:

```bash
python pipeline.py
```

Or submit the provided Grid Engine script:

```bash
qsub run_experiment.sh
```

Results are saved under the configured output directory and experiment name.

## Notes

- The current pipeline targets Linux and single-output regression with ReLU networks. Frontier analysis expects two hidden layers of equal width.
- Ground-truth evaluation is optional. Disable it for a new dataset unless you provide a matching evaluation function.
