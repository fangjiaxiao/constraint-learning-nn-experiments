# ----------Configuration Settings----------
# =========================
# CONFIG
# =========================

CONFIG = {
    "experiment_name": "example_experiment",

    "paths": {
        "csv_path": "./complex_data.csv",      # <-- change this
        "output_root": ".",
    },

    "run": {
        "prepare_data": True,
        "train_baseline": True,
        "prune_and_finetune": True,
        "combine_and_select_frontier": True,
        "export_artifacts": True,
        "run_optimization": True,            # requires gurobipy
    },

    "data": {
        "target_column": "total_sale",

        # Option A: explicitly provide final raw feature columns (recommended)
        "feature_columns": None,

        # Option B: let the notebook infer numeric features if feature_columns is None
        "numeric_feature_columns": None,
        "categorical_feature_columns": [],

        # Optional manual one-hot groups (use final feature names after encoding)
        "manual_one_hot_groups": [
            ["a0", "a1", "a2", "a3", "a4"]
        ],

        # Variables to hold fixed during optimization / inverse design
        "fixed_inputs": [
            "price",
            "last_month_sale",
            "biggest_competitor_spend",
        ],

        # If None, decision variables = all final feature columns except fixed_inputs
        "decision_variables": None,

        # How fixed values are chosen when exporting artifacts:
        # "mean", "median", "row", or "manual"
        "fixed_mode": "mean",
        "fixed_row_index": 0,
        "manual_fixed_values": {},

        "drop_id_like_columns": True,
        "id_like_patterns": ["unnamed", "id"],

        # Fractions of the full dataset
        "val_size": 0.2,
        "test_size": 0.0,
        "split_seed": 42,

        "standardize_features": True,
    },

    "model": {
        # Use either width_candidates + num_hidden_layers,
        # OR provide architecture_candidates explicitly.
        "num_hidden_layers": 2,
        "width_candidates": [ 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],   
        "architecture_candidates": None,   # example: [[64,64], [128,128], [256,128]]
        "activation": "relu",
        "output_dim": 1,
    },

    "train": {
        "seeds": list(range(10)),
        "batch_size": 64,
        "lr": 1e-3,
        "weight_decay": 1e-4,
        "optimizer": "adam",
        "epochs_first_round": 1000,
        "epochs_finetune": 200,
        "patience_first_round": 30,
        "patience_finetune": 20,
        "device": "auto",

        # Number of independent baseline-training jobs to run at once.
        # This can also be overridden from the command line with --n_baseline_workers.
        "parallel_workers": 10,
    },

    "prune": {
        "enabled": True,
        "method": "l1_unstructured",
        "rates": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
        "prune_output_layer": True,

        # Number of independent pruning + fine-tuning jobs to run at once.
        # This can also be overridden from the command line with --n_ft_workers.
        "parallel_workers": 10,
    },

    "frontier": {
        "selection_metric": "val_mse",
        "selection_mode": "min",       # for now this notebook expects min
        "complexity_metric": "effective_weight_size",
    },

    "optimization": {
        "enabled": True,
        "objective_sense": "maximize",   # "maximize" or "minimize"

        # Optional per-variable type overrides:
        # "binary", "integer", or "continuous"
        "variable_types": {},

        # Example budget / linear constraints on raw decision variables
        "budget_constraints": [
            {
                "name": "total_budget",
                "vars": [
                    "tv",
                    "radio",
                    "social_media_app",
                    "influencer_sponsorship",
                    "billboard",
                    "browser",
                    "email",
                    "event_sponsorship",
                ],
                "coeffs": [1, 1, 1, 1, 1, 1, 1, 1],
                "sense": "<=",
                "rhs": 500.0,
            }
        ],

        # Additional generic linear constraints
        "linear_constraints": [
            # Example:
            # {
            #   "name": "tv_ge_radio",
            #   "vars": ["tv", "radio"],
            #   "coeffs": [1, -1],
            #   "sense": ">=",
            #   "rhs": 0.0,
            # }
        ],

        "time_limit": 1000,
        "mip_gap": 0.01,
        "output_flag": 0,
        "threads": 1,
        "parallel_workers": 10,
    },

   

    "analysis": {
        "enabled": True,
        "allowed_statuses": ["OPTIMAL", "SUBOPTIMAL", "TIME_LIMIT"],
        "param_metric": "effective_weight_size",
        "runtime_metrics": ["wall_time_sec", "runtime_sec"],
        "value_plot_xscale": "log",     # linear or log
        "value_plot_yscale": "linear",

        "runtime_plot_xscale": "log",
        "runtime_plot_yscale": "log",

        "std_band_alpha": 0.15,
        "std_band_multiplier": 1.0,
        "save_png": True,
    },

    "ground_truth": {
        "enabled": True,
        "callable_name": "example_ground_truth",
        "round_output": False,

        # Optional ground-truth configuration for the included example dataset.
        "feature_map": {
            "tv": "tv",
            "radio": "radio",
            "social_media_app": "social_media_app",
            "influencer_sponsorship": "influencer_sponsorship",
            "billboard": "billboard",
            "browser": "browser",
            "email": "email",
            "event_sponsorship": "event_sponsorship",
            "price": "price",
            "last_month_sale": "last_month_sale",
            "biggest_competitor_spend": "biggest_competitor_spend",
        },

        "one_hot_cols": ["a0", "a1", "a2", "a3", "a4"],

        "coefficients": {
            "last_month_sale_weight": 0.2,
            "main_effect_weight": 0.8,
            "tv_log_coef": 100.0,
            "radio_log_coef": 50.0,
            "social_media_outer_coef": 100.0,
            "influencer_log_coef": 130.0,
            "billboard_log_coef": 30.0,
            "browser_log_coef": 60.0,
            "email_log_coef": 90.0,
            "event_log_coef": 20.0,
            "price_numerator": 10000.0,
            "competitor_penalty": 0.12,
        },

        # For each app dummy: log2(1 + max(0, a*x - b*x^2))
        "social_media_shapes": {
            "a0": {"linear": 6.66, "quadratic": 0.111},
            "a1": {"linear": 2.22, "quadratic": 0.012},
            "a2": {"linear": 1.33, "quadratic": 0.004},
            "a3": {"linear": 0.95, "quadratic": 0.002},
            "a4": {"linear": 0.66, "quadratic": 0.001},
        },
    },
}

print("Edit CONFIG first, then run this script from the command line.")

# -----------------End Configuration Settings, no need to modify below this line-----------------



# =========================
# Imports and global helpers
# =========================

import argparse
import copy
import json
import math
import os
import random
import time
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import numpy as np
import pandas as pd

import torch
import torch.nn as nn
import torch.nn.utils.prune as prune
from torch.utils.data import DataLoader, TensorDataset

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

warnings.filterwarnings("ignore")

try:
    from IPython.display import display
except ImportError:
    def display(x):
        if hasattr(x, "to_string"):
            try:
                print(x.to_string())
            except Exception:
                print(x)
        else:
            print(x)

def parse_cli_args():
    parser = argparse.ArgumentParser(
        description=(
            "Train models, run parallel pruning/fine-tuning, export artifacts, "
            "and optionally run parallel optimization."
        )
    )
    parser.add_argument(
        "--n_baseline_workers",
        type=int,
        default=None,
        help="Number of parallel worker processes for the baseline-training stage.",
    )
    parser.add_argument(
        "--n_ft_workers",
        type=int,
        default=None,
        help="Number of parallel worker processes for the pruning + fine-tuning stage.",
    )
    parser.add_argument(
        "--n_opt_workers",
        type=int,
        default=None,
        help="Number of parallel worker processes for the optimization stage.",
    )
    parser.add_argument(
        "--gurobi_threads",
        type=int,
        default=None,
        help="Number of Gurobi threads per optimization worker.",
    )
    return parser.parse_args()

CLI_ARGS = parse_cli_args()

def resolve_device(device_cfg: str):
    if device_cfg == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(device_cfg)

DEVICE = resolve_device(CONFIG["train"]["device"])
print("DEVICE =", DEVICE)

if CLI_ARGS.n_baseline_workers is not None:
    CONFIG["train"]["parallel_workers"] = int(CLI_ARGS.n_baseline_workers)
if CLI_ARGS.n_ft_workers is not None:
    CONFIG["prune"]["parallel_workers"] = int(CLI_ARGS.n_ft_workers)
if CLI_ARGS.gurobi_threads is not None:
    CONFIG["optimization"]["threads"] = int(CLI_ARGS.gurobi_threads)
if CLI_ARGS.n_opt_workers is not None:
    CONFIG["optimization"]["parallel_workers"] = int(CLI_ARGS.n_opt_workers)

print("Baseline parallel workers =", CONFIG["train"].get("parallel_workers", 1))
print("Fine-tuning parallel workers =", CONFIG["prune"].get("parallel_workers", 1))
print("Optimization parallel workers =", CONFIG["optimization"].get("parallel_workers", 1))
print("Gurobi threads per worker =", CONFIG["optimization"].get("threads", 1))

def runtime_now():
    """High-resolution wall-clock timer with CUDA synchronization when needed."""
    if DEVICE.type == "cuda":
        torch.cuda.synchronize()
    return time.perf_counter()

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
    return Path(path)

def make_output_dirs(config):
    root = ensure_dir(Path(config["paths"]["output_root"]) / config["experiment_name"])
    dirs = {
        "root": root,
        "baseline_ckpts": ensure_dir(root / "baseline_checkpoints"),
        "pruned_ckpts": ensure_dir(root / "pruned_checkpoints"),
        "artifacts": ensure_dir(root / "artifacts"),
        "tables": ensure_dir(root / "tables"),
        "optimization": ensure_dir(root / "optimization"),
    }
    return dirs

OUT_DIRS = make_output_dirs(CONFIG)

def arch_to_label(hidden_layers):
    return "x".join(str(int(h)) for h in hidden_layers)

def resolve_architectures(model_cfg):
    if model_cfg.get("architecture_candidates"):
        return [list(map(int, arch)) for arch in model_cfg["architecture_candidates"]]
    n_layers = int(model_cfg["num_hidden_layers"])
    widths = list(model_cfg["width_candidates"])
    return [[int(w)] * n_layers for w in widths]

ARCHITECTURES = resolve_architectures(CONFIG["model"])
print("Architectures to train:", ARCHITECTURES[:5], "..." if len(ARCHITECTURES) > 5 else "")

def get_linear_modules(model):
    return [m for m in model.modules() if isinstance(m, nn.Linear)]

def count_total_params_from_state_dict(state_dict):
    total = 0
    for tensor in state_dict.values():
        total += int(np.prod(tensor.shape))
    return total

def count_nonzero_params_from_state_dict(state_dict, tol=0.0):
    total = 0
    for tensor in state_dict.values():
        arr = tensor.detach().cpu().numpy()
        total += int(np.count_nonzero(np.abs(arr) > tol))
    return total

def deep_copy_state_dict(model):
    return {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}

def strip_pruning_inplace(model):
    for layer in get_linear_modules(model):
        if hasattr(layer, "weight_orig"):
            prune.remove(layer, "weight")
    return model

def dense_state_dict_from_model(model):
    model_copy = copy.deepcopy(model).cpu()
    strip_pruning_inplace(model_copy)
    return deep_copy_state_dict(model_copy)

def save_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    


# =========================
# Data preparation helpers
# =========================

def infer_numeric_features(df, target_col, categorical_cols, drop_id_like, id_like_patterns):
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    features = [c for c in num_cols if c != target_col]

    if drop_id_like:
        lowered_patterns = [p.lower() for p in id_like_patterns]
        features = [
            c for c in features
            if not any(p in c.lower() for p in lowered_patterns)
        ]

    # do not double count categoricals if user passed encoded versions differently
    features = [c for c in features if c not in categorical_cols]
    return features

def build_feature_frame(df, config):
    data_cfg = config["data"]
    target_col = data_cfg["target_column"]
    categorical_cols = list(data_cfg.get("categorical_feature_columns", []))

    if data_cfg.get("feature_columns") is not None:
        raw_feature_cols = list(data_cfg["feature_columns"])
    else:
        numeric_cols = data_cfg.get("numeric_feature_columns")
        if numeric_cols is None:
            numeric_cols = infer_numeric_features(
                df=df,
                target_col=target_col,
                categorical_cols=categorical_cols,
                drop_id_like=data_cfg.get("drop_id_like_columns", True),
                id_like_patterns=data_cfg.get("id_like_patterns", ["unnamed", "id"]),
            )
        raw_feature_cols = list(numeric_cols) + list(categorical_cols)

    missing = [c for c in [target_col] + raw_feature_cols if c not in df.columns]
    if missing:
        raise ValueError(f"These columns are missing from the dataset: {missing}")

    X_raw = df[raw_feature_cols].copy()
    auto_one_hot_groups = []

    if categorical_cols:
        X_encoded = pd.get_dummies(X_raw, columns=categorical_cols, drop_first=False, dtype=float)
        for cat in categorical_cols:
            prefix = f"{cat}_"
            group = [c for c in X_encoded.columns if c.startswith(prefix)]
            if len(group) >= 2:
                auto_one_hot_groups.append(group)
    else:
        X_encoded = X_raw.copy()

    # normalize bool -> int/float
    for c in X_encoded.columns:
        if pd.api.types.is_bool_dtype(X_encoded[c]):
            X_encoded[c] = X_encoded[c].astype(int)

    X_encoded = X_encoded.astype(float)

    manual_groups = []
    for group in data_cfg.get("manual_one_hot_groups", []):
        valid_group = [g for g in group if g in X_encoded.columns]
        if len(valid_group) >= 2:
            manual_groups.append(valid_group)

    # merge groups while preserving order and uniqueness
    merged_groups = []
    seen = set()
    for group in auto_one_hot_groups + manual_groups:
        key = tuple(group)
        if key not in seen:
            merged_groups.append(group)
            seen.add(key)

    return X_encoded, merged_groups, raw_feature_cols

def compute_feature_bounds(X_df, one_hot_groups):
    one_hot_set = set(sum(one_hot_groups, []))
    bounds = {}
    for c in X_df.columns:
        if c in one_hot_set:
            bounds[c] = {"low": 0.0, "high": 1.0}
        else:
            s = X_df[c].dropna()
            lo, hi = float(s.min()), float(s.max())
            if lo == hi:
                lo -= 1.0
                hi += 1.0
            bounds[c] = {"low": lo, "high": hi}
    return bounds

def make_splits(X_df, y, val_size, test_size, split_seed):
    if val_size <= 0:
        raise ValueError("val_size must be > 0 because early stopping uses a validation set.")
    if test_size < 0 or val_size < 0 or val_size + test_size >= 1:
        raise ValueError("Require val_size >= 0, test_size >= 0, and val_size + test_size < 1.")

    all_idx = np.arange(len(X_df))

    if test_size > 0:
        train_val_idx, test_idx = train_test_split(
            all_idx, test_size=test_size, random_state=split_seed, shuffle=True
        )
        relative_val_size = val_size / (1.0 - test_size)
    else:
        train_val_idx = all_idx
        test_idx = np.array([], dtype=int)
        relative_val_size = val_size

    train_idx, val_idx = train_test_split(
        train_val_idx, test_size=relative_val_size, random_state=split_seed, shuffle=True
    )

    return train_idx, val_idx, test_idx

def prepare_data_bundle(config):
    csv_path = config["paths"]["csv_path"]
    df = pd.read_csv(csv_path)

    target_col = config["data"]["target_column"]
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset.")

    y = df[target_col].astype(float).values
    X_df, one_hot_groups, raw_feature_cols = build_feature_frame(df, config)
    feature_names = X_df.columns.tolist()

    train_idx, val_idx, test_idx = make_splits(
        X_df=X_df,
        y=y,
        val_size=config["data"]["val_size"],
        test_size=config["data"]["test_size"],
        split_seed=config["data"]["split_seed"],
    )

    X_train_raw = X_df.iloc[train_idx].copy()
    X_val_raw = X_df.iloc[val_idx].copy()
    X_test_raw = X_df.iloc[test_idx].copy() if len(test_idx) > 0 else pd.DataFrame(columns=X_df.columns)

    y_train = y[train_idx]
    y_val = y[val_idx]
    y_test = y[test_idx] if len(test_idx) > 0 else np.array([])

    if config["data"]["standardize_features"]:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train_raw.values)
        X_val = scaler.transform(X_val_raw.values)
        X_test = scaler.transform(X_test_raw.values) if len(test_idx) > 0 else np.empty((0, X_df.shape[1]))
        means = scaler.mean_.astype(float)
        stds = scaler.scale_.astype(float)
    else:
        X_train = X_train_raw.values.astype(float)
        X_val = X_val_raw.values.astype(float)
        X_test = X_test_raw.values.astype(float) if len(test_idx) > 0 else np.empty((0, X_df.shape[1]))
        means = np.zeros(X_df.shape[1], dtype=float)
        stds = np.ones(X_df.shape[1], dtype=float)

    fixed_inputs = [c for c in config["data"].get("fixed_inputs", []) if c in feature_names]
    decision_variables = config["data"].get("decision_variables")
    if decision_variables is None:
        decision_variables = [c for c in feature_names if c not in fixed_inputs]
    else:
        decision_variables = [c for c in decision_variables if c in feature_names]

    bundle = {
        "df": df,
        "target_column": target_col,
        "X_df": X_df,
        "feature_names": feature_names,
        "raw_feature_columns": raw_feature_cols,
        "one_hot_groups": one_hot_groups,
        "bounds": compute_feature_bounds(X_df, one_hot_groups),
        "fixed_inputs": fixed_inputs,
        "decision_variables": decision_variables,
        "train_idx": train_idx,
        "val_idx": val_idx,
        "test_idx": test_idx,
        "X_train": X_train.astype(np.float32),
        "X_val": X_val.astype(np.float32),
        "X_test": X_test.astype(np.float32),
        "y_train": y_train.astype(np.float32),
        "y_val": y_val.astype(np.float32),
        "y_test": y_test.astype(np.float32),
        "scaler_means": means.tolist(),
        "scaler_stds": stds.tolist(),
    }
    return bundle




# =========================
# Model, training, pruning, and evaluation helpers
# =========================

class MLPRegressor(nn.Module):
    def __init__(self, in_dim, hidden_layers, out_dim=1, activation="relu"):
        super().__init__()
        if activation.lower() != "relu":
            raise ValueError("This v1 notebook currently supports ReLU hidden layers only.")

        layers = []
        prev = int(in_dim)
        for h in hidden_layers:
            layers.append(nn.Linear(prev, int(h)))
            layers.append(nn.ReLU())
            prev = int(h)
        layers.append(nn.Linear(prev, int(out_dim)))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)

def build_optimizer(model, train_cfg):
    opt_name = train_cfg.get("optimizer", "adam").lower()
    lr = float(train_cfg["lr"])
    wd = float(train_cfg["weight_decay"])

    if opt_name == "adam":
        return torch.optim.Adam(model.parameters(), lr=lr, weight_decay=wd)
    elif opt_name == "adamw":
        return torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)
    elif opt_name == "sgd":
        return torch.optim.SGD(model.parameters(), lr=lr, weight_decay=wd, momentum=0.9)
    else:
        raise ValueError(f"Unsupported optimizer: {opt_name}")

def make_dataloader(X, y, batch_size, seed):
    ds = TensorDataset(torch.from_numpy(X), torch.from_numpy(y).unsqueeze(1))
    g = torch.Generator()
    g.manual_seed(seed)
    return DataLoader(ds, batch_size=batch_size, shuffle=True, generator=g)

def predict_numpy(model, X_np, device):
    model.eval()
    with torch.no_grad():
        X_t = torch.from_numpy(X_np).to(device)
        preds = model(X_t).detach().cpu().numpy().reshape(-1)
    return preds

def regression_metrics(y_true, y_pred):
    out = {
        "mse": float(mean_squared_error(y_true, y_pred)),
        "mae": float(mean_absolute_error(y_true, y_pred)),
    }
    try:
        out["r2"] = float(r2_score(y_true, y_pred))
    except Exception:
        out["r2"] = np.nan
    return out

def evaluate_splits(model, bundle, device):
    metrics = {}

    pred_train = predict_numpy(model, bundle["X_train"], device)
    metrics["train"] = regression_metrics(bundle["y_train"], pred_train)

    pred_val = predict_numpy(model, bundle["X_val"], device)
    metrics["val"] = regression_metrics(bundle["y_val"], pred_val)

    if len(bundle["y_test"]) > 0:
        pred_test = predict_numpy(model, bundle["X_test"], device)
        metrics["test"] = regression_metrics(bundle["y_test"], pred_test)
    else:
        metrics["test"] = {"mse": np.nan, "mae": np.nan, "r2": np.nan}

    return metrics

def apply_unstructured_pruning(model, amount, prune_output_layer=True):
    linear_layers = get_linear_modules(model)
    if not prune_output_layer and len(linear_layers) >= 1:
        linear_layers = linear_layers[:-1]

    for layer in linear_layers:
        prune.l1_unstructured(layer, name="weight", amount=amount)

def fit_model(
    model,
    bundle,
    seed,
    epochs,
    patience,
    device,
    dense_save=False,
):
    model = model.to(device)
    optimizer = build_optimizer(model, CONFIG["train"])
    criterion = nn.MSELoss()
    train_loader = make_dataloader(
        bundle["X_train"],
        bundle["y_train"],
        batch_size=int(CONFIG["train"]["batch_size"]),
        seed=seed,
    )

    best_metric = float("inf")
    best_epoch = -1
    best_state = None
    best_metrics = None
    wait = 0
    history = []

    X_train_t = torch.from_numpy(bundle["X_train"]).to(device)
    y_train_t = torch.from_numpy(bundle["y_train"]).unsqueeze(1).to(device)

    for epoch in range(1, int(epochs) + 1):
        model.train()
        for xb, yb in train_loader:
            xb = xb.to(device)
            yb = yb.unsqueeze(1).to(device) if yb.ndim == 1 else yb.to(device)

            pred = model(xb)
            loss = criterion(pred, yb)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        metrics = evaluate_splits(model, bundle, device)
        val_mse = metrics["val"]["mse"]
        history.append({
            "epoch": epoch,
            "train_mse": metrics["train"]["mse"],
            "val_mse": metrics["val"]["mse"],
            "test_mse": metrics["test"]["mse"],
        })

        if val_mse < best_metric:
            best_metric = val_mse
            best_epoch = epoch
            best_state = dense_state_dict_from_model(model) if dense_save else deep_copy_state_dict(model)
            best_metrics = metrics
            wait = 0
        else:
            wait += 1
            if wait >= int(patience):
                break

    return {
        "best_epoch": best_epoch,
        "best_state": best_state,
        "best_metrics": best_metrics,
        "history": history,
    }

def summarize_run_row(
    seed,
    hidden_layers,
    prune_rate,
    best_epoch,
    best_metrics,
    checkpoint_path,
    state_dict,
    stage,
):
    arch_label = arch_to_label(hidden_layers)
    total_params = count_total_params_from_state_dict(state_dict)
    effsize = count_nonzero_params_from_state_dict(state_dict)

    row = {
        "stage": stage,
        "seed": int(seed),
        "arch_label": arch_label,
        "hidden_layers_json": json.dumps(list(map(int, hidden_layers))),
        "prune_rate": float(prune_rate),
        "best_epoch": int(best_epoch),
        "train_mse": best_metrics["train"]["mse"],
        "train_mae": best_metrics["train"]["mae"],
        "train_r2": best_metrics["train"]["r2"],
        "val_mse": best_metrics["val"]["mse"],
        "val_mae": best_metrics["val"]["mae"],
        "val_r2": best_metrics["val"]["r2"],
        "test_mse": best_metrics["test"]["mse"],
        "test_mae": best_metrics["test"]["mae"],
        "test_r2": best_metrics["test"]["r2"],
        "total_params": int(total_params),
        "effsize": int(effsize),
        "checkpoint_path": str(checkpoint_path),
    }
    return row

# =========================
# Run data preparation
# =========================

DATA_BUNDLE = prepare_data_bundle(CONFIG)

print("Target column:", DATA_BUNDLE["target_column"])
print("Number of final features:", len(DATA_BUNDLE["feature_names"]))
print("First few feature names:", DATA_BUNDLE["feature_names"][:10])
print("One-hot groups:", DATA_BUNDLE["one_hot_groups"])
print("Fixed inputs:", DATA_BUNDLE["fixed_inputs"])
print("Decision variables:", DATA_BUNDLE["decision_variables"][:10], "..." if len(DATA_BUNDLE["decision_variables"]) > 10 else "")
print("Train / Val / Test sizes:", len(DATA_BUNDLE["train_idx"]), len(DATA_BUNDLE["val_idx"]), len(DATA_BUNDLE["test_idx"]))

save_json(
    {
        "feature_names": DATA_BUNDLE["feature_names"],
        "target_column": DATA_BUNDLE["target_column"],
        "one_hot_groups": DATA_BUNDLE["one_hot_groups"],
        "fixed_inputs": DATA_BUNDLE["fixed_inputs"],
        "decision_variables": DATA_BUNDLE["decision_variables"],
        "bounds": DATA_BUNDLE["bounds"],
        "scaler_means": DATA_BUNDLE["scaler_means"],
        "scaler_stds": DATA_BUNDLE["scaler_stds"],
    },
    OUT_DIRS["tables"] / "data_bundle_summary.json",
)
print("Saved data summary to:", OUT_DIRS["tables"] / "data_bundle_summary.json")




# =========================
# Stage 1: parallel baseline training
# =========================

baseline_csv_path = OUT_DIRS["tables"] / "baseline_results.csv"
baseline_error_csv_path = OUT_DIRS["tables"] / "baseline_errors.csv"


def _configure_baseline_worker():
    """Keep every baseline worker to one CPU thread."""
    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass


def train_one_baseline_task(task):
    """
    Train one independent (seed, architecture) baseline model.

    Each worker saves a unique checkpoint. Only the parent process writes the
    shared baseline-results CSV.
    """
    _configure_baseline_worker()

    seed = int(task["seed"])
    hidden_layers = [int(x) for x in task["hidden_layers"]]
    arch_label = arch_to_label(hidden_layers)

    # Reset the RNG independently for every configuration.
    set_seed(seed)
    worker_device = DEVICE
    runtime_start = time.perf_counter()

    model = MLPRegressor(
        in_dim=len(DATA_BUNDLE["feature_names"]),
        hidden_layers=hidden_layers,
        out_dim=CONFIG["model"]["output_dim"],
        activation=CONFIG["model"]["activation"],
    )

    fit_out = fit_model(
        model=model,
        bundle=DATA_BUNDLE,
        seed=seed,
        epochs=CONFIG["train"]["epochs_first_round"],
        patience=CONFIG["train"]["patience_first_round"],
        device=worker_device,
        dense_save=True,
    )

    checkpoint_path = (
        OUT_DIRS["baseline_ckpts"]
        / f"best_model_seed{seed}_arch{arch_label}.pt"
    )
    torch.save(fit_out["best_state"], checkpoint_path)

    train_runtime_sec = float(time.perf_counter() - runtime_start)

    row = summarize_run_row(
        seed=seed,
        hidden_layers=hidden_layers,
        prune_rate=0.0,
        best_epoch=fit_out["best_epoch"],
        best_metrics=fit_out["best_metrics"],
        checkpoint_path=checkpoint_path,
        state_dict=fit_out["best_state"],
        stage="baseline",
    )
    row["runtime_sec"] = train_runtime_sec
    row["train_runtime_sec"] = train_runtime_sec
    row["prune_finetune_runtime_sec"] = 0.0
    row["finetune_runtime_sec"] = 0.0
    row["total_training_runtime_sec"] = train_runtime_sec
    return row


def _save_baseline_snapshot(rows, csv_path):
    """Atomically save all baseline tasks completed so far."""
    if not rows:
        return pd.DataFrame()

    snapshot = (
        pd.DataFrame(rows)
        .sort_values(["seed", "arch_label"])
        .reset_index(drop=True)
    )
    tmp_path = Path(str(csv_path) + ".tmp")
    snapshot.to_csv(tmp_path, index=False)
    os.replace(tmp_path, csv_path)
    return snapshot


if CONFIG["run"]["train_baseline"]:
    baseline_jobs = [
        {
            "seed": int(seed),
            "hidden_layers": list(map(int, hidden_layers)),
        }
        for seed in CONFIG["train"]["seeds"]
        for hidden_layers in ARCHITECTURES
    ]

    n_baseline_workers = max(
        1, int(CONFIG["train"].get("parallel_workers", 1))
    )
    max_workers = (
        min(n_baseline_workers, len(baseline_jobs))
        if baseline_jobs else 0
    )

    print("\n" + "=" * 90)
    print("Parallel baseline training")
    print("Number of baseline tasks:", len(baseline_jobs))
    print("Baseline workers:", max_workers)
    print("=" * 90)

    baseline_rows = []
    baseline_errors = []

    # Start a fresh summary for this run. A completed worker overwrites only its
    # own uniquely named checkpoint.
    if baseline_csv_path.exists():
        baseline_csv_path.unlink()
    if baseline_error_csv_path.exists():
        baseline_error_csv_path.unlink()

    if len(baseline_jobs) == 0:
        BASELINE_DF = pd.DataFrame()
        print("No baseline tasks were created.")
    elif max_workers == 1:
        for task in baseline_jobs:
            try:
                row = train_one_baseline_task(task)
                baseline_rows.append(row)
                BASELINE_DF = _save_baseline_snapshot(
                    baseline_rows, baseline_csv_path
                )
                print(
                    f"Finished baseline: seed={row['seed']} | "
                    f"arch={row['arch_label']} | "
                    f"best_epoch={row['best_epoch']} | "
                    f"val_mse={row['val_mse']:.6f} | "
                    f"runtime={row['train_runtime_sec']:.2f}s | "
                    f"completed={len(baseline_rows)}/{len(baseline_jobs)}"
                )
            except Exception as exc:
                error_row = dict(task)
                error_row["error"] = repr(exc)
                baseline_errors.append(error_row)
                print(
                    f"[ERROR] Baseline failed: seed={task['seed']} | "
                    f"hidden_layers={task['hidden_layers']} | {exc}"
                )
    else:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(train_one_baseline_task, task): task
                for task in baseline_jobs
            }

            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    row = future.result()
                    baseline_rows.append(row)
                    BASELINE_DF = _save_baseline_snapshot(
                        baseline_rows, baseline_csv_path
                    )
                    print(
                        f"Finished baseline: seed={row['seed']} | "
                        f"arch={row['arch_label']} | "
                        f"best_epoch={row['best_epoch']} | "
                        f"val_mse={row['val_mse']:.6f} | "
                        f"runtime={row['train_runtime_sec']:.2f}s | "
                        f"completed={len(baseline_rows)}/{len(baseline_jobs)}"
                    )
                except Exception as exc:
                    error_row = dict(task)
                    error_row["error"] = repr(exc)
                    baseline_errors.append(error_row)
                    print(
                        f"[ERROR] Baseline failed: seed={task['seed']} | "
                        f"hidden_layers={task['hidden_layers']} | {exc}"
                    )

    if baseline_rows:
        BASELINE_DF = _save_baseline_snapshot(
            baseline_rows, baseline_csv_path
        )
        print("Saved baseline results to:", baseline_csv_path)
    else:
        BASELINE_DF = pd.DataFrame()
        print("No baseline tasks completed successfully.")

    if baseline_errors:
        pd.DataFrame(baseline_errors).to_csv(
            baseline_error_csv_path, index=False
        )
        raise RuntimeError(
            f"{len(baseline_errors)} baseline task(s) failed. "
            f"Completed rows were preserved in {baseline_csv_path}; "
            f"error details were saved to {baseline_error_csv_path}."
        )
else:
    BASELINE_DF = pd.read_csv(baseline_csv_path)
    print("Loaded existing baseline results from:", baseline_csv_path)

display(BASELINE_DF.head())



# =========================
# Stage 2: parallel prune + fine-tune
# =========================

pruned_csv_path = OUT_DIRS["tables"] / "pruned_results.csv"
pruned_error_csv_path = OUT_DIRS["tables"] / "pruned_errors.csv"


def _configure_finetune_worker():
    """Keep every worker to one CPU thread so parallel jobs do not oversubscribe the node."""
    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        # PyTorch permits this setting only before inter-op work starts.
        pass


def prune_finetune_one_task(task):
    """
    Run one independent (seed, architecture, pruning-rate) fine-tuning task.

    Workers save unique checkpoint files, but they do not write shared CSV files.
    The parent process collects rows and writes the CSV safely.
    """
    _configure_finetune_worker()

    seed = int(task["seed"])
    arch_label = str(task["arch_label"])
    hidden_layers = [int(x) for x in task["hidden_layers"]]
    rate = float(task["rate"])
    base_ckpt = Path(task["base_ckpt"])
    baseline_train_runtime_sec = float(task["baseline_train_runtime_sec"])

    if not base_ckpt.exists():
        raise FileNotFoundError(f"Missing baseline checkpoint: {base_ckpt}")

    # Each task starts from a deterministic RNG state.
    set_seed(seed)

    # Argon pilot jobs are CPU jobs. If a CUDA device is explicitly requested,
    # this still follows the global DEVICE setting, but multiple GPU workers are
    # generally not recommended without assigning one GPU per process.
    worker_device = DEVICE
    runtime_start = time.perf_counter()

    base_state = torch.load(base_ckpt, map_location="cpu")

    model = MLPRegressor(
        in_dim=len(DATA_BUNDLE["feature_names"]),
        hidden_layers=hidden_layers,
        out_dim=CONFIG["model"]["output_dim"],
        activation=CONFIG["model"]["activation"],
    )
    model.load_state_dict(base_state)

    apply_unstructured_pruning(
        model,
        amount=rate,
        prune_output_layer=bool(CONFIG["prune"]["prune_output_layer"]),
    )

    fit_out = fit_model(
        model=model,
        bundle=DATA_BUNDLE,
        seed=seed,
        epochs=CONFIG["train"]["epochs_finetune"],
        patience=CONFIG["train"]["patience_finetune"],
        device=worker_device,
        dense_save=True,
    )

    checkpoint_path = (
        OUT_DIRS["pruned_ckpts"]
        / f"best_pruned_seed{seed}_arch{arch_label}_r{int(round(rate * 100))}.pt"
    )
    torch.save(fit_out["best_state"], checkpoint_path)

    prune_finetune_runtime_sec = float(time.perf_counter() - runtime_start)
    total_training_runtime_sec = (
        baseline_train_runtime_sec + prune_finetune_runtime_sec
    )

    row = summarize_run_row(
        seed=seed,
        hidden_layers=hidden_layers,
        prune_rate=rate,
        best_epoch=fit_out["best_epoch"],
        best_metrics=fit_out["best_metrics"],
        checkpoint_path=checkpoint_path,
        state_dict=fit_out["best_state"],
        stage="pruned",
    )
    row["runtime_sec"] = prune_finetune_runtime_sec
    row["train_runtime_sec"] = baseline_train_runtime_sec
    row["prune_finetune_runtime_sec"] = prune_finetune_runtime_sec
    row["finetune_runtime_sec"] = prune_finetune_runtime_sec
    row["total_training_runtime_sec"] = total_training_runtime_sec
    return row


def _save_pruned_snapshot(rows, csv_path):
    """
    Save completed fine-tuning rows after each finished task.

    Writing to a temporary file and replacing the target prevents a partially
    written CSV if the scheduler stops the job during a write.
    """
    if not rows:
        return pd.DataFrame()

    snapshot = (
        pd.DataFrame(rows)
        .sort_values(["seed", "arch_label", "prune_rate"])
        .reset_index(drop=True)
    )
    tmp_path = Path(str(csv_path) + ".tmp")
    snapshot.to_csv(tmp_path, index=False)
    os.replace(tmp_path, csv_path)
    return snapshot


if CONFIG["prune"]["enabled"] and CONFIG["run"]["prune_and_finetune"]:
    finetune_jobs = []

    for _, base_row in BASELINE_DF.iterrows():
        seed = int(base_row["seed"])
        arch_label = str(base_row["arch_label"])
        hidden_layers = json.loads(base_row["hidden_layers_json"])
        base_ckpt = Path(base_row["checkpoint_path"])
        baseline_train_runtime_sec = float(
            base_row.get("train_runtime_sec", base_row.get("runtime_sec", np.nan))
        )

        if not base_ckpt.exists():
            print(f"[WARN] Missing baseline checkpoint: {base_ckpt}")
            continue

        for rate in CONFIG["prune"]["rates"]:
            finetune_jobs.append(
                {
                    "seed": seed,
                    "arch_label": arch_label,
                    "hidden_layers": hidden_layers,
                    "base_ckpt": str(base_ckpt),
                    "baseline_train_runtime_sec": baseline_train_runtime_sec,
                    "rate": float(rate),
                }
            )

    n_ft_workers = max(1, int(CONFIG["prune"].get("parallel_workers", 1)))
    max_workers = min(n_ft_workers, len(finetune_jobs)) if finetune_jobs else 0

    print("\n" + "=" * 90)
    print("Parallel pruning + fine-tuning")
    print("Number of fine-tuning tasks:", len(finetune_jobs))
    print("Fine-tuning workers:", max_workers)
    print("=" * 90)

    pruned_rows = []
    pruned_errors = []

    # Start a fresh summary for this run. Unique checkpoint files will be overwritten
    # as their corresponding tasks finish.
    if pruned_csv_path.exists():
        pruned_csv_path.unlink()
    if pruned_error_csv_path.exists():
        pruned_error_csv_path.unlink()

    if len(finetune_jobs) == 0:
        PRUNED_DF = pd.DataFrame()
        print("No valid fine-tuning tasks were created.")
    elif max_workers == 1:
        for task in finetune_jobs:
            try:
                row = prune_finetune_one_task(task)
                pruned_rows.append(row)
                PRUNED_DF = _save_pruned_snapshot(pruned_rows, pruned_csv_path)
                print(
                    f"Finished fine-tuning: seed={row['seed']} | "
                    f"arch={row['arch_label']} | rate={row['prune_rate']:.2f} | "
                    f"best_epoch={row['best_epoch']} | "
                    f"val_mse={row['val_mse']:.6f} | "
                    f"runtime={row['prune_finetune_runtime_sec']:.2f}s | "
                    f"completed={len(pruned_rows)}/{len(finetune_jobs)}"
                )
            except Exception as exc:
                error_row = dict(task)
                error_row["error"] = repr(exc)
                pruned_errors.append(error_row)
                print(
                    f"[ERROR] Fine-tuning failed: seed={task['seed']} | "
                    f"arch={task['arch_label']} | rate={task['rate']:.2f} | {exc}"
                )
    else:
        # Argon runs Linux, so ProcessPoolExecutor uses independent worker processes.
        # The parent process remains the only process writing pruned_results.csv.
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(prune_finetune_one_task, task): task
                for task in finetune_jobs
            }

            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    row = future.result()
                    pruned_rows.append(row)
                    PRUNED_DF = _save_pruned_snapshot(pruned_rows, pruned_csv_path)
                    print(
                        f"Finished fine-tuning: seed={row['seed']} | "
                        f"arch={row['arch_label']} | rate={row['prune_rate']:.2f} | "
                        f"best_epoch={row['best_epoch']} | "
                        f"val_mse={row['val_mse']:.6f} | "
                        f"runtime={row['prune_finetune_runtime_sec']:.2f}s | "
                        f"completed={len(pruned_rows)}/{len(finetune_jobs)}"
                    )
                except Exception as exc:
                    error_row = dict(task)
                    error_row["error"] = repr(exc)
                    pruned_errors.append(error_row)
                    print(
                        f"[ERROR] Fine-tuning failed: seed={task['seed']} | "
                        f"arch={task['arch_label']} | rate={task['rate']:.2f} | {exc}"
                    )

    if pruned_rows:
        PRUNED_DF = _save_pruned_snapshot(pruned_rows, pruned_csv_path)
        print("Saved pruned results to:", pruned_csv_path)
    else:
        PRUNED_DF = pd.DataFrame()
        print("No fine-tuning tasks completed successfully.")

    if pruned_errors:
        pd.DataFrame(pruned_errors).to_csv(pruned_error_csv_path, index=False)
        raise RuntimeError(
            f"{len(pruned_errors)} fine-tuning task(s) failed. "
            f"Completed rows were preserved in {pruned_csv_path}; "
            f"error details were saved to {pruned_error_csv_path}."
        )
else:
    if pruned_csv_path.exists():
        PRUNED_DF = pd.read_csv(pruned_csv_path)
        print("Loaded existing pruned results from:", pruned_csv_path)
    else:
        PRUNED_DF = pd.DataFrame()
        print("No pruned results found; using empty DataFrame.")

display(PRUNED_DF.head())


# =========================
# Stage 3: combine + formula-based effective weight size frontier
# =========================

combined_csv_path = OUT_DIRS["tables"] / "combined_results.csv"
avg_csv_path = OUT_DIRS["tables"] / "combined_results_avg_over_seeds.csv"
median_csv_path = OUT_DIRS["tables"] / "combined_results_median_over_seeds.csv"
frontier_csv_path = OUT_DIRS["tables"] / "frontier_effective_weight_size.csv"

def extract_width(hidden_layers_json):
    hidden_layers = json.loads(hidden_layers_json)
    hidden_layers = [int(x) for x in hidden_layers]

    if len(hidden_layers) != 2:
        raise ValueError(f"Expected 2 hidden layers, got {hidden_layers}")
    if hidden_layers[0] != hidden_layers[1]:
        raise ValueError(f"Expected same width, got {hidden_layers}")

    return hidden_layers[0]

def attach_configuration_metrics(combined_df, input_size):
    """Add effective size and explicit training-runtime columns to every seed/configuration row."""
    df = combined_df.copy()

    def numeric_series(name):
        if name in df.columns:
            return pd.to_numeric(df[name], errors="coerce")
        return pd.Series(np.nan, index=df.index, dtype=float)

    df["runtime_sec"] = numeric_series("runtime_sec")
    baseline_mask = pd.to_numeric(df["prune_rate"], errors="coerce").fillna(0.0).eq(0.0)

    current_train = numeric_series("train_runtime_sec")
    baseline_own_runtime = current_train.where(current_train.notna(), df["runtime_sec"])
    baseline_lookup = (
        df.loc[baseline_mask, ["seed", "arch_label"]]
        .assign(_baseline_train_runtime=baseline_own_runtime.loc[baseline_mask].values)
        .drop_duplicates(["seed", "arch_label"])
    )
    df = df.merge(baseline_lookup, on=["seed", "arch_label"], how="left")

    existing_train = pd.to_numeric(df["train_runtime_sec"], errors="coerce") if "train_runtime_sec" in df else pd.Series(np.nan, index=df.index)
    df["train_runtime_sec"] = existing_train.where(existing_train.notna(), df["_baseline_train_runtime"])
    df.loc[baseline_mask.values, "train_runtime_sec"] = df.loc[baseline_mask.values, "train_runtime_sec"].fillna(
        df.loc[baseline_mask.values, "runtime_sec"]
    )

    if "prune_finetune_runtime_sec" in df.columns:
        existing_ft = pd.to_numeric(df["prune_finetune_runtime_sec"], errors="coerce")
    elif "finetune_runtime_sec" in df.columns:
        existing_ft = pd.to_numeric(df["finetune_runtime_sec"], errors="coerce")
    else:
        existing_ft = pd.Series(np.nan, index=df.index)

    df["prune_finetune_runtime_sec"] = existing_ft
    df.loc[baseline_mask.values, "prune_finetune_runtime_sec"] = 0.0
    nonbaseline = ~baseline_mask.values
    df.loc[nonbaseline, "prune_finetune_runtime_sec"] = df.loc[nonbaseline, "prune_finetune_runtime_sec"].fillna(
        df.loc[nonbaseline, "runtime_sec"]
    )
    df["finetune_runtime_sec"] = df["prune_finetune_runtime_sec"]
    df["total_training_runtime_sec"] = (
        df["train_runtime_sec"].fillna(0.0)
        + df["prune_finetune_runtime_sec"].fillna(0.0)
    )
    df = df.drop(columns=["_baseline_train_runtime"])

    df["size"] = df["hidden_layers_json"].apply(extract_width).astype(int)
    df["effective_weight_size"] = (
        (input_size * df["size"] + df["size"] * df["size"] + df["size"])
        * (1.0 - df["prune_rate"])
    )
    return df


def aggregate_over_seeds(combined_df):
    group_cols = ["arch_label", "hidden_layers_json", "prune_rate", "size"]

    summary_df = (
        combined_df
        .groupby(group_cols, as_index=False)
        .agg(
            n_seeds=("seed", "nunique"),
            train_mse=("train_mse", "mean"),
            train_mse_median=("train_mse", "median"),
            train_mae=("train_mae", "mean"),
            train_r2=("train_r2", "mean"),
            val_mse=("val_mse", "mean"),
            val_mse_median=("val_mse", "median"),
            val_mae=("val_mae", "mean"),
            val_r2=("val_r2", "mean"),
            test_mse=("test_mse", "mean"),
            test_mse_median=("test_mse", "median"),
            test_mae=("test_mae", "mean"),
            test_r2=("test_r2", "mean"),
            total_params=("total_params", "mean"),
            effective_weight_size=("effective_weight_size", "mean"),
            train_runtime_sec=("train_runtime_sec", "mean"),
            train_runtime_sec_median=("train_runtime_sec", "median"),
            prune_finetune_runtime_sec=("prune_finetune_runtime_sec", "mean"),
            prune_finetune_runtime_sec_median=("prune_finetune_runtime_sec", "median"),
            finetune_runtime_sec=("finetune_runtime_sec", "mean"),
            total_training_runtime_sec=("total_training_runtime_sec", "mean"),
            total_training_runtime_sec_median=("total_training_runtime_sec", "median"),
        )
        .sort_values(["val_mse"])
        .reset_index(drop=True)
    )
    # Frontier selection continues to use mean validation MSE.
    summary_df["mse"] = summary_df["val_mse"]
    return summary_df


def select_frontier(avg_df):
    df_sorted = avg_df.sort_values(by=["mse"]).reset_index(drop=True)
    remaining = df_sorted.copy()
    frontier_rows = []

    while not remaining.empty:
        best = remaining.iloc[0]
        frontier_rows.append(best)

        eff_star = float(best["effective_weight_size"])
        prune_star = float(best["prune_rate"])

        requirement = ~(
            (remaining["effective_weight_size"] > eff_star) |
            ((remaining["effective_weight_size"] == eff_star) &
             (remaining["prune_rate"] <= prune_star))
        )

        remaining = remaining[requirement].copy()
        remaining = remaining.sort_values(by=["mse"]).reset_index(drop=True)

    frontier_df = pd.DataFrame(frontier_rows).reset_index(drop=True)
    frontier_df["frontier_rank"] = np.arange(len(frontier_df))
    return frontier_df

if CONFIG["run"]["combine_and_select_frontier"]:
    frames = [BASELINE_DF]
    if len(PRUNED_DF) > 0:
        frames.append(PRUNED_DF)

    raw_combined_df = pd.concat(frames, ignore_index=True)
    input_size = len(DATA_BUNDLE["feature_names"])
    COMBINED_DF = attach_configuration_metrics(raw_combined_df, input_size)
    AVG_DF = aggregate_over_seeds(COMBINED_DF)
    FRONTIER_DF = select_frontier(AVG_DF)

    median_cols = [
        "arch_label", "hidden_layers_json", "prune_rate", "size", "n_seeds",
        "effective_weight_size", "train_mse_median", "val_mse_median", "test_mse_median",
        "train_runtime_sec_median", "prune_finetune_runtime_sec_median",
        "total_training_runtime_sec_median",
    ]
    MEDIAN_DF = AVG_DF[median_cols].copy()

    COMBINED_DF.to_csv(combined_csv_path, index=False)
    AVG_DF.to_csv(avg_csv_path, index=False)
    MEDIAN_DF.to_csv(median_csv_path, index=False)
    FRONTIER_DF.to_csv(frontier_csv_path, index=False)

    print("Saved combined per-seed results to:", combined_csv_path)
    print("Saved mean/median summary to:", avg_csv_path)
    print("Saved median summary to:", median_csv_path)
    print("Saved frontier to:", frontier_csv_path)
else:
    COMBINED_DF = pd.read_csv(combined_csv_path)
    AVG_DF = pd.read_csv(avg_csv_path)
    MEDIAN_DF = pd.read_csv(median_csv_path) if median_csv_path.exists() else pd.DataFrame()
    FRONTIER_DF = pd.read_csv(frontier_csv_path)

display(AVG_DF.head())
display(FRONTIER_DF)



# =========================
# Stage 4: export artifacts
# =========================

artifact_index_csv = OUT_DIRS["tables"] / "artifact_index.csv"

def build_fixed_values(data_bundle, config):
    fixed_mode = config["data"]["fixed_mode"]
    fixed_row_index = int(config["data"].get("fixed_row_index", 0))
    manual_fixed_values = dict(config["data"].get("manual_fixed_values", {}))

    X_df = data_bundle["X_df"]
    bounds = data_bundle["bounds"]

    fixed_values = {}
    for c in data_bundle["fixed_inputs"]:
        if c not in X_df.columns:
            continue

        if fixed_mode == "manual":
            if c not in manual_fixed_values:
                raise ValueError(f"fixed_mode='manual' but no value was provided for fixed input '{c}'.")
            val = float(manual_fixed_values[c])
        elif fixed_mode == "median":
            val = float(X_df[c].median())
        elif fixed_mode == "row":
            val = float(X_df.iloc[fixed_row_index][c])
        else:
            val = float(X_df[c].mean())

        val = max(bounds[c]["low"], min(bounds[c]["high"], val))
        fixed_values[c] = float(val)

    return fixed_values

def export_artifact(checkpoint_row, data_bundle, config, out_dir):
    checkpoint_path = Path(checkpoint_row["checkpoint_path"])
    if not checkpoint_path.exists():
        print(f"[SKIP] checkpoint not found: {checkpoint_path}")
        return None

    hidden_layers = json.loads(checkpoint_row["hidden_layers_json"])
    model = MLPRegressor(
        in_dim=len(data_bundle["feature_names"]),
        hidden_layers=hidden_layers,
        out_dim=config["model"]["output_dim"],
        activation=config["model"]["activation"],
    )
    state = torch.load(checkpoint_path, map_location="cpu")
    model.load_state_dict(state)
    model.eval()

    linear_layers = get_linear_modules(model)
    weights = [layer.weight.detach().cpu().numpy().tolist() for layer in linear_layers]
    biases = [layer.bias.detach().cpu().numpy().tolist() for layer in linear_layers]

    variable_types = dict(config["optimization"].get("variable_types", {}))
    for group in data_bundle["one_hot_groups"]:
        for v in group:
            variable_types[v] = "binary"

    fixed_values = build_fixed_values(data_bundle, config)
    seed = int(checkpoint_row["seed"])
    arch_label = str(checkpoint_row["arch_label"])
    prune_rate = float(checkpoint_row["prune_rate"])
    prune_pct = int(round(prune_rate * 100))
    frontier_rank_raw = checkpoint_row.get("frontier_rank", np.nan)
    is_frontier = bool(checkpoint_row.get("is_frontier", False)) or pd.notna(frontier_rank_raw)
    frontier_rank = int(frontier_rank_raw) if pd.notna(frontier_rank_raw) else None

    artifact = {
        "model_id": f"seed{seed}_arch{arch_label}_r{prune_pct}",
        "meta": {
            "seed": seed,
            "arch_label": arch_label,
            "hidden_layers": hidden_layers,
            "prune_rate": prune_rate,
            "effective_weight_size": float(checkpoint_row["effective_weight_size"]),
            "total_params": float(checkpoint_row.get("total_params", np.nan)),
            "is_frontier": is_frontier,
            "frontier_rank": frontier_rank,
            "stage": checkpoint_row["stage"],
            "target_column": data_bundle["target_column"],
            "train_runtime_sec": float(checkpoint_row.get("train_runtime_sec", np.nan)),
            "prune_finetune_runtime_sec": float(checkpoint_row.get("prune_finetune_runtime_sec", np.nan)),
            "total_training_runtime_sec": float(checkpoint_row.get("total_training_runtime_sec", np.nan)),
        },
        "arch": {
            "in_dim": len(data_bundle["feature_names"]),
            "hidden_layers": hidden_layers,
            "out_dim": int(config["model"]["output_dim"]),
            "activation": config["model"]["activation"],
        },
        "features": data_bundle["feature_names"],
        "target_column": data_bundle["target_column"],
        "decision_vars": data_bundle["decision_variables"],
        "fixed_inputs": data_bundle["fixed_inputs"],
        "fixed_values": fixed_values,
        "one_hot_groups": data_bundle["one_hot_groups"],
        "variable_types": variable_types,
        "bounds": data_bundle["bounds"],
        "scaler": {
            "means": data_bundle["scaler_means"],
            "stds": data_bundle["scaler_stds"],
        },
        "weights": weights,
        "biases": biases,
    }

    out_path = Path(out_dir) / f"nn_artifact_seed{seed}_arch{arch_label}_r{prune_pct}.json"
    save_json(artifact, out_path)

    return {
        "seed": seed,
        "arch_label": arch_label,
        "prune_rate": prune_rate,
        "effective_weight_size": float(checkpoint_row["effective_weight_size"]),
        "is_frontier": is_frontier,
        "frontier_rank": frontier_rank,
        "train_runtime_sec": float(checkpoint_row.get("train_runtime_sec", np.nan)),
        "prune_finetune_runtime_sec": float(checkpoint_row.get("prune_finetune_runtime_sec", np.nan)),
        "total_training_runtime_sec": float(checkpoint_row.get("total_training_runtime_sec", np.nan)),
        "artifact_path": str(out_path),
        "checkpoint_path": str(checkpoint_path),
    }


if CONFIG["run"]["export_artifacts"]:
    artifact_rows = []
    frontier_artifact_index_csv = OUT_DIRS["tables"] / "frontier_artifact_index.csv"

    frontier_keys = FRONTIER_DF[["arch_label", "prune_rate", "frontier_rank"]].drop_duplicates()
    all_ckpts = COMBINED_DF.merge(frontier_keys, on=["arch_label", "prune_rate"], how="left")
    all_ckpts["is_frontier"] = all_ckpts["frontier_rank"].notna()

    # Remove stale artifacts from earlier runs of the same experiment directory.
    for old_artifact in Path(OUT_DIRS["artifacts"]).glob("nn_artifact_*.json"):
        old_artifact.unlink()

    for _, ckpt_row in all_ckpts.iterrows():
        exported = export_artifact(
            checkpoint_row=ckpt_row,
            data_bundle=DATA_BUNDLE,
            config=CONFIG,
            out_dir=OUT_DIRS["artifacts"],
        )
        if exported is not None:
            artifact_rows.append(exported)

    ARTIFACT_INDEX_DF = pd.DataFrame(artifact_rows)
    if len(ARTIFACT_INDEX_DF) > 0:
        ARTIFACT_INDEX_DF = ARTIFACT_INDEX_DF.sort_values(["seed", "arch_label", "prune_rate"]).reset_index(drop=True)
    ARTIFACT_INDEX_DF.to_csv(artifact_index_csv, index=False)
    if "is_frontier" in ARTIFACT_INDEX_DF.columns:
        FRONTIER_ARTIFACT_INDEX_DF = ARTIFACT_INDEX_DF[ARTIFACT_INDEX_DF["is_frontier"].fillna(False)].copy()
    else:
        FRONTIER_ARTIFACT_INDEX_DF = pd.DataFrame(columns=ARTIFACT_INDEX_DF.columns)
    FRONTIER_ARTIFACT_INDEX_DF.to_csv(frontier_artifact_index_csv, index=False)
    print("Saved all-model artifact index to:", artifact_index_csv)
    print("Saved frontier-only artifact index to:", frontier_artifact_index_csv)
else:
    ARTIFACT_INDEX_DF = pd.read_csv(artifact_index_csv)
    print("Loaded existing artifact index from:", artifact_index_csv)

display(ARTIFACT_INDEX_DF.head())
print("Number of exported artifacts (all models):", len(ARTIFACT_INDEX_DF))
if "is_frontier" in ARTIFACT_INDEX_DF.columns:
    print("Number of frontier artifacts:", int(ARTIFACT_INDEX_DF["is_frontier"].fillna(False).sum()))



# =========================
# Stage 5: inverse optimization
# =========================

import time

try:
    import gurobipy as gp
    from gurobipy import GRB
    GUROBI_AVAILABLE = True
except Exception as e:
    GUROBI_AVAILABLE = False
    print("Gurobi is not available in this environment. Optimization stage will be skipped.")
    print("Import error:", e)

optimization_csv_path = OUT_DIRS["optimization"] / "batch_optimization_results.csv"

def linear_bounds(W, b, prev_L, prev_U):
    W = np.asarray(W, dtype=float)
    b = np.asarray(b, dtype=float)
    prev_L = np.asarray(prev_L, dtype=float)
    prev_U = np.asarray(prev_U, dtype=float)

    W_pos = np.maximum(W, 0.0)
    W_neg = np.minimum(W, 0.0)

    L = W_pos @ prev_L + W_neg @ prev_U + b
    U = W_pos @ prev_U + W_neg @ prev_L + b
    return L, U

def add_named_linear_constraint(model, x_raw, spec):
    vars_ = spec["vars"]
    coeffs = spec.get("coeffs", [1.0] * len(vars_))
    sense = spec["sense"]
    rhs = float(spec["rhs"])
    name = spec.get("name", "linear_constraint")

    expr = gp.quicksum(float(c) * x_raw[v] for c, v in zip(coeffs, vars_) if v in x_raw)

    if sense == "<=":
        model.addConstr(expr <= rhs, name=name)
    elif sense == ">=":
        model.addConstr(expr >= rhs, name=name)
    elif sense == "==":
        model.addConstr(expr == rhs, name=name)
    else:
        raise ValueError(f"Unsupported constraint sense: {sense}")

def solve_one_artifact(artifact_path, optimization_cfg):
    art = load_json(artifact_path)

    feat_names = art["features"]
    one_hot_groups = art.get("one_hot_groups", [])
    one_hot_vars = set(sum(one_hot_groups, []))
    variable_types = art.get("variable_types", {})
    fixed_inputs = set(art.get("fixed_inputs", []))
    fixed_values = art.get("fixed_values", {})
    bounds = art["bounds"]

    mu = np.array(art["scaler"]["means"], dtype=float)
    sd = np.array(art["scaler"]["stds"], dtype=float)

    weights = [np.array(W, dtype=float) for W in art["weights"]]
    biases = [np.array(b, dtype=float) for b in art["biases"]]

    if int(art["arch"]["out_dim"]) != 1:
        raise ValueError("This v1 optimization cell only supports single-output models.")

    model = gp.Model(f"opt_{art['model_id']}")
    model.Params.OutputFlag = int(optimization_cfg.get("output_flag", 0))
    model.Params.TimeLimit = float(optimization_cfg.get("time_limit", 1000))
    model.Params.MIPGap = float(optimization_cfg.get("mip_gap", 0.01))
    model.Params.Threads = int(optimization_cfg.get("threads", 1))

    # raw input vars
    x_raw = {}
    for name in feat_names:
        lo = float(bounds[name]["low"])
        hi = float(bounds[name]["high"])

        var_type = variable_types.get(name, "continuous").lower()
        if name in one_hot_vars or var_type == "binary":
            x_raw[name] = model.addVar(vtype=GRB.BINARY, name=f"x_{name}")
        elif var_type == "integer":
            x_raw[name] = model.addVar(vtype=GRB.INTEGER, lb=lo, ub=hi, name=f"x_{name}")
        else:
            x_raw[name] = model.addVar(lb=lo, ub=hi, name=f"x_{name}")

    # fixed inputs
    for name in fixed_inputs:
        if name in x_raw and name in fixed_values:
            model.addConstr(x_raw[name] == float(fixed_values[name]), name=f"fix_{name}")

    # one-hot constraints
    for group in one_hot_groups:
        valid = [g for g in group if g in x_raw]
        if len(valid) >= 2:
            model.addConstr(gp.quicksum(x_raw[g] for g in valid) == 1, name="onehot_" + "_".join(valid))

    # user constraints
    for spec in optimization_cfg.get("budget_constraints", []):
        add_named_linear_constraint(model, x_raw, spec)
    for spec in optimization_cfg.get("linear_constraints", []):
        add_named_linear_constraint(model, x_raw, spec)

    # standardization vars
    x_std = []
    input_L = []
    input_U = []
    for j, name in enumerate(feat_names):
        lo = float(bounds[name]["low"])
        hi = float(bounds[name]["high"])

        if abs(sd[j]) < 1e-12:
            zlo, zhi = 0.0, 0.0
            var = model.addVar(lb=0.0, ub=0.0, name=f"xstd_{name}")
            model.addConstr(var == 0.0, name=f"stdfix_{name}")
        else:
            zlo = (lo - mu[j]) / sd[j]
            zhi = (hi - mu[j]) / sd[j]
            lb = float(min(zlo, zhi))
            ub = float(max(zlo, zhi))
            var = model.addVar(lb=lb, ub=ub, name=f"xstd_{name}")
            model.addConstr(var * float(sd[j]) == x_raw[name] - float(mu[j]), name=f"std_{name}")
            zlo, zhi = lb, ub

        x_std.append(var)
        input_L.append(zlo)
        input_U.append(zhi)

    prev_vars = x_std
    prev_L = np.array(input_L, dtype=float)
    prev_U = np.array(input_U, dtype=float)
    relu_bin_count = 0

    for layer_idx, (W, b) in enumerate(zip(weights, biases)):
        zL, zU = linear_bounds(W, b, prev_L, prev_U)
        z_vars = []

        for i in range(W.shape[0]):
            z = model.addVar(lb=float(zL[i]), ub=float(zU[i]), name=f"z_{layer_idx}_{i}")
            expr = gp.quicksum(float(W[i, j]) * prev_vars[j] for j in range(W.shape[1])) + float(b[i])
            model.addConstr(z == expr, name=f"lin_{layer_idx}_{i}")
            z_vars.append(z)

        is_output_layer = (layer_idx == len(weights) - 1)

        if is_output_layer:
            prev_vars = z_vars
            prev_L = zL
            prev_U = zU
        else:
            a_vars = []
            aL = np.maximum(0.0, zL)
            aU = np.maximum(0.0, zU)

            for i, z in enumerate(z_vars):
                if zU[i] <= 0:
                    a = model.addVar(lb=0.0, ub=0.0, name=f"a_{layer_idx}_{i}")
                    model.addConstr(a == 0.0, name=f"relu_zero_{layer_idx}_{i}")
                elif zL[i] >= 0:
                    a = model.addVar(lb=float(zL[i]), ub=float(zU[i]), name=f"a_{layer_idx}_{i}")
                    model.addConstr(a == z, name=f"relu_linear_{layer_idx}_{i}")
                else:
                    a = model.addVar(lb=0.0, ub=float(max(0.0, zU[i])), name=f"a_{layer_idx}_{i}")
                    d = model.addVar(vtype=GRB.BINARY, name=f"d_{layer_idx}_{i}")
                    relu_bin_count += 1

                    model.addConstr(a >= z, name=f"relu1_{layer_idx}_{i}")
                    model.addConstr(a >= 0.0, name=f"relu2_{layer_idx}_{i}")
                    model.addConstr(a <= z - float(zL[i]) * (1 - d), name=f"relu3_{layer_idx}_{i}")
                    model.addConstr(a <= float(zU[i]) * d, name=f"relu4_{layer_idx}_{i}")

                a_vars.append(a)

            prev_vars = a_vars
            prev_L = aL
            prev_U = aU

    y_var = prev_vars[0]
    sense = optimization_cfg.get("objective_sense", "maximize").lower()
    if sense == "maximize":
        model.setObjective(y_var, GRB.MAXIMIZE)
    elif sense == "minimize":
        model.setObjective(y_var, GRB.MINIMIZE)
    else:
        raise ValueError(f"Unsupported objective_sense: {sense}")

    model.optimize()

    status_name = {
        GRB.OPTIMAL: "OPTIMAL",
        GRB.SUBOPTIMAL: "SUBOPTIMAL",
        GRB.TIME_LIMIT: "TIME_LIMIT",
        GRB.INFEASIBLE: "INFEASIBLE",
        GRB.INF_OR_UNBD: "INF_OR_UNBD",
        GRB.UNBOUNDED: "UNBOUNDED",
    }.get(model.Status, str(model.Status))

    has_solution = bool(model.SolCount > 0)
    timed_out = bool(model.Status == GRB.TIME_LIMIT)
    optimality_proven = bool(model.Status == GRB.OPTIMAL)

    if optimality_proven:
        solve_outcome = "OPTIMAL"
    elif timed_out and has_solution:
        solve_outcome = "TIME_LIMIT_WITH_SOLUTION"
    elif timed_out:
        solve_outcome = "TIME_LIMIT_NO_SOLUTION"
    elif has_solution:
        solve_outcome = "FEASIBLE_NOT_PROVEN"
    else:
        solve_outcome = status_name

    try:
        best_bound = float(model.ObjBound)
    except Exception:
        best_bound = np.nan
    try:
        achieved_mip_gap = float(model.MIPGap) if has_solution else np.nan
    except Exception:
        achieved_mip_gap = np.nan

    frontier_rank_raw = art["meta"].get("frontier_rank")
    result = {
        "artifact_path": str(artifact_path),
        "model_id": art["model_id"],
        "seed": art["meta"]["seed"],
        "arch_label": art["meta"]["arch_label"],
        "prune_rate": art["meta"]["prune_rate"],
        "status": status_name,
        "status_code": int(model.Status),
        "solve_outcome": solve_outcome,
        "solved": has_solution,
        "has_solution": has_solution,
        "timed_out": timed_out,
        "optimality_proven": optimality_proven,
        "solution_count": int(model.SolCount),
        "objective_value": float(model.ObjVal) if has_solution else np.nan,
        "best_bound": best_bound,
        "achieved_mip_gap": achieved_mip_gap,
        "runtime_sec": float(model.Runtime),
        "time_limit_sec": float(optimization_cfg.get("time_limit", 1000)),
        "node_count": float(model.NodeCount),
        "relu_binary_count": int(relu_bin_count),
        "effective_weight_size": art["meta"].get("effective_weight_size", np.nan),
        "total_params": art["meta"].get("total_params", np.nan),
        "is_frontier": bool(art["meta"].get("is_frontier", False)),
        "frontier_rank": np.nan if frontier_rank_raw is None else frontier_rank_raw,
        "train_runtime_sec": art["meta"].get("train_runtime_sec", np.nan),
        "prune_finetune_runtime_sec": art["meta"].get("prune_finetune_runtime_sec", np.nan),
        "total_training_runtime_sec": art["meta"].get("total_training_runtime_sec", np.nan),
    }

    if has_solution:
        solution = {name: float(var.X) for name, var in x_raw.items()}
        result["solution_json"] = json.dumps(solution)
    else:
        result["solution_json"] = json.dumps({})

    return result

def solve_one_artifact_safe(args):
    artifact_path, optimization_cfg = args
    p = Path(artifact_path)
    t0 = time.perf_counter()

    try:
        row = solve_one_artifact(p, optimization_cfg)
    except Exception as e:
        row = {
            "artifact_path": str(p),
            "model_id": p.stem,
            "seed": np.nan,
            "arch_label": None,
            "prune_rate": np.nan,
            "status": "ERROR",
            "status_code": np.nan,
            "solve_outcome": "ERROR",
            "solved": False,
            "has_solution": False,
            "timed_out": False,
            "optimality_proven": False,
            "solution_count": 0,
            "objective_value": np.nan,
            "best_bound": np.nan,
            "achieved_mip_gap": np.nan,
            "runtime_sec": np.nan,
            "time_limit_sec": float(optimization_cfg.get("time_limit", 1000)),
            "node_count": np.nan,
            "relu_binary_count": np.nan,
            "effective_weight_size": np.nan,
            "total_params": np.nan,
            "is_frontier": False,
            "frontier_rank": np.nan,
            "train_runtime_sec": np.nan,
            "prune_finetune_runtime_sec": np.nan,
            "total_training_runtime_sec": np.nan,
            "solution_json": json.dumps({}),
            "error": str(e),
        }
    row["wall_time_sec"] = float(time.perf_counter() - t0)
    return row


if CONFIG["run"]["run_optimization"]:
    if not GUROBI_AVAILABLE:
        print("Skipping optimization because gurobipy is unavailable in this environment.")
        OPT_RESULTS_DF = pd.DataFrame()
    else:
        artifact_paths = sorted(Path(OUT_DIRS["artifacts"]).glob("nn_artifact_*.json"))
        n_workers = max(1, int(CONFIG["optimization"].get("parallel_workers", 1)))

        print("Number of artifacts to optimize:", len(artifact_paths))
        print("Optimization workers:", n_workers)

        if len(artifact_paths) == 0:
            OPT_RESULTS_DF = pd.DataFrame()
            print("No artifacts found to optimize.")
        elif n_workers == 1:
            opt_rows = []
            for p in artifact_paths:
                print("Optimizing artifact:", p.name)
                row = solve_one_artifact_safe((str(p), CONFIG["optimization"]))
                opt_rows.append(row)
            OPT_RESULTS_DF = pd.DataFrame(opt_rows)
        else:
            opt_rows = []
            jobs = [(str(p), CONFIG["optimization"]) for p in artifact_paths]
            max_workers = min(n_workers, len(jobs))
            print("Launching parallel optimization with", max_workers, "workers...")

            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                future_to_job = {executor.submit(solve_one_artifact_safe, job): job[0] for job in jobs}
                for fut in as_completed(future_to_job):
                    row = fut.result()
                    print("Finished:", row.get("model_id"), "| outcome:", row.get("solve_outcome"))
                    opt_rows.append(row)
            OPT_RESULTS_DF = pd.DataFrame(opt_rows)

        if len(OPT_RESULTS_DF) > 0:
            OPT_RESULTS_DF = OPT_RESULTS_DF.sort_values(["seed", "arch_label", "prune_rate"], na_position="last").reset_index(drop=True)
        OPT_RESULTS_DF.to_csv(optimization_csv_path, index=False)
        print("Saved optimization results to:", optimization_csv_path)
else:
    if optimization_csv_path.exists():
        OPT_RESULTS_DF = pd.read_csv(optimization_csv_path)
        print("Loaded existing optimization results from:", optimization_csv_path)
    else:
        OPT_RESULTS_DF = pd.DataFrame()
        print("No optimization results file found.")

display(OPT_RESULTS_DF.head())


# Final output summary¶

print("Output root:", OUT_DIRS["root"])
print("Baseline results:", baseline_csv_path)
print("Pruned results:", pruned_csv_path)
print("Combined results:", combined_csv_path)
print("Averaged results:", avg_csv_path)
print("Median results:", median_csv_path)
print("Effsize frontier:", frontier_csv_path)
print("Artifact index:", artifact_index_csv)
print("Optimization results:", optimization_csv_path)


# =========================
# Stage 6 helpers: optional ground-truth evaluation
# =========================

def _safe_log2_spend(x):
    x = float(x)
    return math.log2(1.0 if x <= 0 else x)

def _positive_log2_quadratic(linear_coef, quadratic_coef, x):
    x = float(x)
    inner = max(0.0, float(linear_coef) * x - float(quadratic_coef) * (x ** 2))
    return math.log2(1.0 + inner)

def example_ground_truth(solution_dict, gt_cfg):
    feature_map = gt_cfg["feature_map"]
    coeffs = gt_cfg["coefficients"]
    shapes = gt_cfg["social_media_shapes"]
    one_hot_cols = list(gt_cfg["one_hot_cols"])

    def val(name, default=0.0):
        col = feature_map.get(name, name)
        return float(solution_dict.get(col, default))

    tv = val("tv")
    radio = val("radio")
    social_media_app = val("social_media_app")
    influencer_sponsorship = val("influencer_sponsorship")
    billboard = val("billboard")
    browser = val("browser")
    email = val("email")
    event_sponsorship = val("event_sponsorship")
    price = max(1e-12, val("price", 1.0))
    last_month_sale = val("last_month_sale")
    biggest_competitor_spend = val("biggest_competitor_spend")

    social_media_term = 0.0
    for col in one_hot_cols:
        gate = float(solution_dict.get(col, 0.0))
        if col not in shapes:
            continue
        s = shapes[col]
        social_media_term += gate * _positive_log2_quadratic(
            linear_coef=s["linear"],
            quadratic_coef=s["quadratic"],
            x=social_media_app,
        )

    deterministic = (
        coeffs["last_month_sale_weight"] * last_month_sale
        + coeffs["main_effect_weight"] * (
            coeffs["tv_log_coef"] * _safe_log2_spend(tv)
            + coeffs["radio_log_coef"] * _safe_log2_spend(radio)
            + coeffs["social_media_outer_coef"] * social_media_term
            + coeffs["influencer_log_coef"] * _safe_log2_spend(influencer_sponsorship)
            + coeffs["billboard_log_coef"] * _safe_log2_spend(billboard)
            + coeffs["browser_log_coef"] * _safe_log2_spend(browser)
            + coeffs["email_log_coef"] * _safe_log2_spend(email)
            + coeffs["event_log_coef"] * _safe_log2_spend(event_sponsorship)
            + coeffs["price_numerator"] / price
            - coeffs["competitor_penalty"] * biggest_competitor_spend
        )
    )

    if gt_cfg.get("round_output", False):
        deterministic = float(round(deterministic))

    return float(deterministic)



# =========================
# Stage 6: post-optimization analysis + plots
# Creates both frontier-only and all-model versions.
# =========================

import matplotlib.pyplot as plt

analysis_cfg = dict(CONFIG.get("analysis", {}))
gt_cfg = dict(CONFIG.get("ground_truth", {}))
analysis_csv_path = OUT_DIRS["optimization"] / "optimization_analysis_enriched_all_models.csv"
all_summary_csv_path = OUT_DIRS["optimization"] / "optimization_analysis_summary_all_models.csv"
frontier_summary_csv_path = OUT_DIRS["optimization"] / "optimization_analysis_summary_frontier.csv"
all_value_plot_path = OUT_DIRS["optimization"] / "optimization_value_vs_params_all_models.png"
all_runtime_plot_path = OUT_DIRS["optimization"] / "optimization_runtime_vs_params_all_models.png"
frontier_value_plot_path = OUT_DIRS["optimization"] / "optimization_value_vs_params_frontier.png"
frontier_runtime_plot_path = OUT_DIRS["optimization"] / "optimization_runtime_vs_params_frontier.png"


def _parse_solution_json(payload):
    if pd.isna(payload):
        return {}
    try:
        parsed = json.loads(payload)
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def _resolve_ground_truth_callable(gt_cfg):
    if not gt_cfg.get("enabled", False):
        return None
    callable_name = gt_cfg.get("callable_name")
    fn = globals().get(callable_name)
    if fn is None:
        raise ValueError(f"Ground-truth callable '{callable_name}' was not found in the script namespace.")
    return fn


def _plot_mean_std(ax, x, mean, std, label, alpha=0.15, mult=1.0):
    x = np.asarray(x, dtype=float)
    mean = np.asarray(mean, dtype=float)
    std = np.nan_to_num(np.asarray(std, dtype=float), nan=0.0)
    ax.plot(x, mean, linewidth=2, label=label)
    ax.fill_between(x, mean - mult * std, mean + mult * std, alpha=alpha)


def _summarize_optimization_subset(subset_df, param_metric):
    summary_specs = {
        "n_runs": ("model_id", "count"),
        "n_solved": ("has_solution", "sum"),
        "n_timed_out": ("timed_out", "sum"),
        "objective_mean": ("objective_value", "mean"),
        "objective_std": ("objective_value", "std"),
        "budget_sum_mean": ("budget_sum", "mean"),
        "budget_sum_std": ("budget_sum", "std"),
        "runtime_mean": ("runtime_sec", "mean"),
        "runtime_std": ("runtime_sec", "std"),
        "wall_time_mean": ("wall_time_sec", "mean"),
        "wall_time_std": ("wall_time_sec", "std"),
        "relu_binary_count_mean": ("relu_binary_count", "mean"),
        "relu_binary_count_std": ("relu_binary_count", "std"),
    }
    if "ground_truth" in subset_df.columns:
        summary_specs.update({
            "ground_truth_mean": ("ground_truth", "mean"),
            "ground_truth_std": ("ground_truth", "std"),
            "bias_mean": ("bias", "mean"),
            "bias_std": ("bias", "std"),
        })

    return (
        subset_df
        .groupby(param_metric, as_index=False)
        .agg(**summary_specs)
        .sort_values(param_metric)
        .reset_index(drop=True)
    )


def _save_solution_quality_and_runtime_plots(subset_df, subset_label, summary_path, value_path, runtime_path):
    if len(subset_df) == 0:
        print(f"No rows available for {subset_label} plots.")
        return pd.DataFrame()

    param_metric = analysis_cfg.get("param_metric", "effective_weight_size")
    if param_metric not in subset_df.columns:
        raise ValueError(f"param_metric='{param_metric}' was not found in the analysis dataframe.")

    summary_df = _summarize_optimization_subset(subset_df, param_metric)
    summary_df.to_csv(summary_path, index=False)
    display_cols = [param_metric, "n_runs", "n_solved", "n_timed_out", "objective_mean", "runtime_mean"]
    display(summary_df[display_cols])

    band_alpha = float(analysis_cfg.get("std_band_alpha", 0.15))
    band_mult = float(analysis_cfg.get("std_band_multiplier", 1.0))
    x = summary_df[param_metric].astype(float).values

    # Solution-quality plot. Rows with no incumbent solution naturally have NaN objective values.
    value_mask = summary_df["objective_mean"].notna().values
    if value_mask.any():
        fig, ax = plt.subplots(figsize=(10, 6))
        _plot_mean_std(
            ax, x[value_mask],
            summary_df.loc[value_mask, "objective_mean"].values,
            summary_df.loc[value_mask, "objective_std"].values,
            label="NN / Gurobi optimum",
            alpha=band_alpha,
            mult=band_mult,
        )
        if "ground_truth_mean" in summary_df.columns and summary_df["ground_truth_mean"].notna().any():
            gt_mask = summary_df["ground_truth_mean"].notna().values
            _plot_mean_std(
                ax, x[gt_mask],
                summary_df.loc[gt_mask, "ground_truth_mean"].values,
                summary_df.loc[gt_mask, "ground_truth_std"].values,
                label="Ground truth",
                alpha=band_alpha,
                mult=band_mult,
            )
            bias_mask = summary_df["bias_mean"].notna().values
            if bias_mask.any():
                _plot_mean_std(
                    ax, x[bias_mask],
                    summary_df.loc[bias_mask, "bias_mean"].values,
                    summary_df.loc[bias_mask, "bias_std"].values,
                    label="Bias = NN optimum - ground truth",
                    alpha=band_alpha,
                    mult=band_mult,
                )
        ax.set_xlabel(param_metric)
        ax.set_ylabel("objective value")
        ax.set_title(f"Average solution quality vs parameter count ({subset_label})")
        ax.grid(alpha=0.3)
        xscale_value = analysis_cfg.get("value_plot_xscale", "linear")
        if xscale_value in {"linear", "log"}:
            ax.set_xscale(xscale_value)
        yscale_value = analysis_cfg.get("value_plot_yscale", "linear")
        if yscale_value in {"linear", "log"}:
            ax.set_yscale(yscale_value)
        ax.legend()
        plt.tight_layout()
        if analysis_cfg.get("save_png", True):
            fig.savefig(value_path, dpi=200, bbox_inches="tight")
            print("Saved value plot to:", value_path)
        plt.close(fig)

    # Runtime plot includes successful, timed-out, and no-solution runs when runtime is available.
    runtime_metrics = analysis_cfg.get("runtime_metrics", ["wall_time_sec", "runtime_sec"])
    runtime_label_map = {
        "runtime_sec": ("runtime_mean", "runtime_std", "Gurobi runtime"),
        "wall_time_sec": ("wall_time_mean", "wall_time_std", "Wall time"),
    }
    fig, ax = plt.subplots(figsize=(10, 5))
    something_plotted = False
    for metric_name in runtime_metrics:
        if metric_name not in runtime_label_map:
            continue
        mean_col, std_col, label = runtime_label_map[metric_name]
        valid = summary_df[mean_col].notna().values
        if valid.any():
            _plot_mean_std(
                ax, x[valid],
                summary_df.loc[valid, mean_col].values,
                summary_df.loc[valid, std_col].values,
                label=label,
                alpha=band_alpha,
                mult=band_mult,
            )
            something_plotted = True
    if something_plotted:
        ax.set_xlabel(param_metric)
        ax.set_ylabel("seconds")
        ax.set_title(f"Average runtime vs parameter count ({subset_label})")
        ax.grid(alpha=0.3)
        xscale_runtime = analysis_cfg.get("runtime_plot_xscale", "linear")
        if xscale_runtime in {"linear", "log"}:
            ax.set_xscale(xscale_runtime)
        yscale_runtime = analysis_cfg.get("runtime_plot_yscale", "log")
        if yscale_runtime in {"linear", "log"}:
            ax.set_yscale(yscale_runtime)
        ax.legend()
        plt.tight_layout()
        if analysis_cfg.get("save_png", True):
            fig.savefig(runtime_path, dpi=200, bbox_inches="tight")
            print("Saved runtime plot to:", runtime_path)
        plt.close(fig)
    else:
        plt.close(fig)
        print(f"No runtime columns were available for {subset_label}.")

    return summary_df


if len(OPT_RESULTS_DF) == 0:
    print("No optimization results are available. Skipping Stage 6.")
else:
    plot_df = OPT_RESULTS_DF.copy()

    # Attach model/training metadata not already present in the optimization CSV.
    meta_cols = [
        "seed", "arch_label", "prune_rate", "effsize", "total_params", "stage",
        "train_runtime_sec", "prune_finetune_runtime_sec", "total_training_runtime_sec",
    ]
    available_meta_cols = [c for c in meta_cols if c in COMBINED_DF.columns]
    merge_meta_cols = [c for c in available_meta_cols if c not in plot_df.columns or c in {"seed", "arch_label", "prune_rate"}]
    meta_df = COMBINED_DF[available_meta_cols].drop_duplicates(subset=["seed", "arch_label", "prune_rate"]).copy()
    extra_meta_cols = [c for c in meta_df.columns if c not in plot_df.columns or c in {"seed", "arch_label", "prune_rate"}]
    plot_df = plot_df.merge(meta_df[extra_meta_cols], on=["seed", "arch_label", "prune_rate"], how="left")

    if "is_frontier" not in plot_df.columns:
        frontier_keys = FRONTIER_DF[["arch_label", "prune_rate"]].drop_duplicates().assign(is_frontier=True)
        plot_df = plot_df.merge(frontier_keys, on=["arch_label", "prune_rate"], how="left")
    plot_df["is_frontier"] = plot_df["is_frontier"].fillna(False).astype(bool)
    plot_df["has_solution"] = plot_df.get("has_solution", plot_df["objective_value"].notna()).fillna(False).astype(bool)
    plot_df["timed_out"] = plot_df.get("timed_out", plot_df["status"].eq("TIME_LIMIT")).fillna(False).astype(bool)

    plot_df["solution_dict"] = plot_df["solution_json"].apply(_parse_solution_json)
    budget_vars = []
    for spec in CONFIG["optimization"].get("budget_constraints", []):
        budget_vars.extend(spec.get("vars", []))
    budget_vars = list(dict.fromkeys(budget_vars))
    plot_df["budget_sum"] = plot_df["solution_dict"].apply(
        lambda d: float(sum(float(d.get(v, 0.0)) for v in budget_vars)) if d else np.nan
    )

    gt_fn = _resolve_ground_truth_callable(gt_cfg)
    if gt_fn is not None:
        plot_df["ground_truth"] = plot_df.apply(
            lambda row: float(gt_fn(row["solution_dict"], gt_cfg)) if row["has_solution"] else np.nan,
            axis=1,
        )
        plot_df["bias"] = plot_df["objective_value"] - plot_df["ground_truth"]
    else:
        plot_df["ground_truth"] = np.nan
        plot_df["bias"] = np.nan

    plot_df.to_csv(analysis_csv_path, index=False)
    print("Saved enriched all-model optimization results to:", analysis_csv_path)

    allowed_statuses = analysis_cfg.get("allowed_statuses", [])
    analysis_rows = plot_df.copy()
    if allowed_statuses and "status" in analysis_rows.columns:
        analysis_rows = analysis_rows[analysis_rows["status"].isin(allowed_statuses)].copy()

    ALL_OPT_SUMMARY_DF = _save_solution_quality_and_runtime_plots(
        analysis_rows,
        subset_label="all models",
        summary_path=all_summary_csv_path,
        value_path=all_value_plot_path,
        runtime_path=all_runtime_plot_path,
    )
    FRONTIER_OPT_SUMMARY_DF = _save_solution_quality_and_runtime_plots(
        analysis_rows[analysis_rows["is_frontier"]].copy(),
        subset_label="frontier models",
        summary_path=frontier_summary_csv_path,
        value_path=frontier_value_plot_path,
        runtime_path=frontier_runtime_plot_path,
    )



# =========================
# Plot 1: pruning rate vs mean / median validation MSE
# one line = one architecture/configuration
# =========================

import matplotlib.pyplot as plt

try:
    pruning_plot_df = AVG_DF.copy()
except NameError:
    pruning_plot_df = pd.read_csv(avg_csv_path)

plot_dir = OUT_DIRS["root"] / "extra_plots"
plot_dir.mkdir(parents=True, exist_ok=True)
pruning_plot_df = pruning_plot_df.sort_values(["size", "prune_rate"]).copy()


def plot_pruning_mse_by_architecture(plot_df, y_col, statistic_label, file_prefix):
    if y_col not in plot_df.columns:
        print(f"Skipping {statistic_label} pruning plot because '{y_col}' is unavailable.")
        return

    configs = plot_df["arch_label"].drop_duplicates().tolist()
    chunk_size = 10
    for fig_id, start in enumerate(range(0, len(configs), chunk_size), start=1):
        selected_configs = configs[start:start + chunk_size]
        if not selected_configs:
            continue

        fig, ax = plt.subplots(figsize=(8, 5))
        for cfg in selected_configs:
            sub = plot_df[plot_df["arch_label"] == cfg].sort_values("prune_rate")
            ax.plot(
                sub["prune_rate"],
                sub[y_col],
                marker="o",
                linewidth=2,
                label=str(cfg),
            )

        ax.set_xlabel("Pruning rate")
        ax.set_ylabel(f"{statistic_label} validation MSE")
        ax.set_yscale("log")
        ax.set_title(f"{statistic_label} validation MSE vs pruning rate")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10, ncol=2)
        plt.tight_layout()

        save_path = plot_dir / f"{file_prefix}_group{fig_id}.png"
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        print("Saved:", save_path)


plot_pruning_mse_by_architecture(
    pruning_plot_df,
    y_col="val_mse",
    statistic_label="Mean",
    file_prefix="pruning_vs_mean_val_mse",
)
plot_pruning_mse_by_architecture(
    pruning_plot_df,
    y_col="val_mse_median",
    statistic_label="Median",
    file_prefix="pruning_vs_median_val_mse",
)



# =========================
# Plot 2: Pareto frontier of size-MSE trade-off
# all points in gray, frontier in red
# =========================

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# If AVG_DF already exists, use it
try:
    plot_df = AVG_DF.copy()
except NameError:
    #plot_df = pd.read_csv(avg_csv_path)
    plot_df = pd.read_csv(avg_csv_path)

# ---- choose columns ----
# Replace these if your actual column names are different
x_col = "effective_weight_size"        # or "effective_size", "num_params", etc.
y_col = "val_mse"    # or "testf_mse"
label_col = "arch_label"

# Keep needed columns only
plot_df = plot_df[[x_col, y_col, label_col]].dropna().copy()

# Sort by x first (smaller size is better)
plot_df = plot_df.sort_values(by=[x_col, y_col]).reset_index(drop=True)

# ---- compute Pareto frontier ----
# Since both x and y are "smaller is better":
# a point is on the frontier if its y is lower than all previous points
frontier_indices = []
best_y_so_far = np.inf

for i, row in plot_df.iterrows():
    if row[y_col] < best_y_so_far:
        frontier_indices.append(i)
        best_y_so_far = row[y_col]

frontier_df = plot_df.loc[frontier_indices].copy()

# ---- make plot ----
plt.figure(figsize=(9, 6))

# all points
plt.scatter(
    plot_df[x_col],
    plot_df[y_col],
    color="gray",
    alpha=0.6,
    s=50,
    label="All configurations"
)

# frontier points + line
plt.plot(
    frontier_df[x_col],
    frontier_df[y_col],
    color="red",
    linewidth=2.5,
    marker="o",
    markersize=8,
    label="Selected frontier models"
)


plt.xscale("log")   # like your example
plt.yscale("log")   # like your example

plt.xlabel("Number of Parameters")
plt.ylabel("Mean Validation MSE")
plt.title("Pareto Frontier of Size–MSE Trade-off")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()

plot_dir = OUT_DIRS["root"] / "extra_plots"
plot_dir.mkdir(parents=True, exist_ok=True)
save_path = plot_dir / "pareto_frontier_size_mse.png"
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.close()

print("Saved:", save_path)


