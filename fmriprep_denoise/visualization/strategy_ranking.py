from itertools import product
import pandas as pd
from fmriprep_denoise.visualization import degrees_of_freedom_loss, motion_metrics
from fmriprep_denoise.visualization import utils
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection


strategy_order = list(utils.GRID_LOCATION.values())
#fmriprep_versions = ["fmriprep-20.2.1lts", "fmriprep-20.2.5lts"]
#datasets = ["ds000228", "ds000030"]


def load_data(path_root, datasets, fmriprep_versions, criteria_name="stringent"):
    mean_total_ranking = []
    for v, d in product(fmriprep_versions, datasets):
        dof = _rank_degrees_of_freedom(path_root, criteria_name, v, d)
        metrics = _rank_motion_metrics(path_root, datasets, criteria_name, v, d)
        df_data = pd.concat([dof, metrics], axis=1)
        mean_total_ranking.append(df_data)
    mean_total_ranking = pd.concat(mean_total_ranking).reset_index()
    mean_total_ranking = mean_total_ranking.melt(
        id_vars=["strategy", "version", "dataset"],
        var_name="metrics",
        value_name="ranking",
    )
    return pd.pivot_table(
        mean_total_ranking,
        columns="strategy",
        index=["dataset", "version", "metrics"],
        fill_value="ranking",
    )

def _rank_degrees_of_freedom(path_root, criteria_name, v, d):
    """Rank the loss of temporal degrees of freedom."""
    dof = degrees_of_freedom_loss.load_data(path_root, [d], criteria_name, v)
    current_ranking = {
            s: [dof[d]["confounds_stats"].loc[:, (s, "total")].mean()] for s in strategy_order
        }
    order = pd.DataFrame(current_ranking).T.sort_values(0)
    order.index = order.index.set_names(["strategy"])
    order = order.reset_index()
    order["version"] = v
    order["dataset"] = d
    order["loss_df"] = list(range(1, order.shape[0] + 1))
    order = order.drop(0, axis=1)
    order = order.set_index(["strategy", "version", "dataset"])
    return order


def _rank_motion_metrics(path_root, datasets, criteria_name, fmriprep_version, dataset):
    """Rank motion based metrics."""
    metrics = pd.DataFrame()
    for m in ["p_values", "median", "distance", "modularity"]:
        data, measure = motion_metrics.load_data(
                    path_root, datasets, criteria_name, fmriprep_version, measure_name=m
                )
        ascending = m != "modularity"
        r = (
                    data[dataset]
                    .query("groups=='full_sample'")
                    .groupby("strategy")[measure["label"]]
                    .describe()["mean"]
                    .sort_values(ascending=ascending)
                )
        rk = pd.DataFrame(list(range(1, len(strategy_order) + 1)), index=r.index, columns=[m])
        rk = rk.reset_index()
        rk["version"] = fmriprep_version
        rk["dataset"] = dataset
        rk = rk.set_index(["strategy", "version", "dataset"])
        metrics = pd.concat([metrics, rk], axis=1)
    return metrics


def plot_ranking(data,datasets,fmriprep_versions):
    
    """Plot the ranking of selected metrics as bubble heatmaps, adjusting for the number of datasets and versions."""
   
    # Set up the number of rows and columns based on datasets and fmriprep_versions
    n_rows = len(datasets)
    n_cols = len(fmriprep_versions)
   
   # Create subplots dynamically based on the number of datasets and versions
    if n_rows == 1 and n_cols == 1:
        fig, axs = plt.subplots(figsize=(9.6, 4.8), constrained_layout=True)  # single plot
        axs = np.array([[axs]])  # Wrap it into a 2D array to match the indexing later
    else:
        fig, axs = plt.subplots(
            n_rows, n_cols, figsize=(9.6 * n_cols, 4.8 * n_rows), 
            sharex=True, sharey=True, constrained_layout=True
        )
    
    # Ensure axs is 2D array even if there's a single row or column
    if n_rows == 1:
        axs = np.expand_dims(axs, axis=0)
    if n_cols == 1:
        axs = np.expand_dims(axs, axis=1)
   
    fig.suptitle(
       "Ranking of all strategies per dataset per fMRIPrep version",
       weight="heavy",
       fontsize="x-large",
    )
    
    for j, d in enumerate(datasets):
        for i, v in enumerate(fmriprep_versions):
            mat = data.xs(d, level="dataset", drop_level=True)
            mat = mat.xs(v, level="version", drop_level=True)
            mat = mat.droplevel(None, axis=1)
            mat = mat.loc[
                ["modularity", "distance", "median", "p_values", "loss_df"],
                strategy_order
            ]
            n_metrics, n_strategy = mat.shape

            x_strategy, y_metrics = np.meshgrid(np.arange(n_strategy), np.arange(n_metrics))

            r_ranking = (len(strategy_order) + 1 - mat) / (len(strategy_order) + 1) / 2
            circles = [
                plt.Circle((x, y), radius=r)
                for r, x, y in zip(r_ranking.values.flat,
                                   x_strategy.flat,
                                   y_metrics.flat)
            ]
            col = PatchCollection(circles, array=mat.values.flatten(), cmap="rocket_r")
            axs[i, j].add_collection(col)

            axs[i, j].set(
                xticks=np.arange(n_strategy),
                yticks=np.arange(n_metrics),
                xticklabels=mat.columns,
                yticklabels=[
                    "Average network modularity",
                    "DM-FC",
                    "QC-FC: median",
                    "QC-FC: significant",
                    "Loss of temporal degrees of freedom",
                ],
            )
            axs[i, j].set_xticklabels(mat.columns, rotation=45, ha="right")
            axs[i, j].set_xticks(np.arange(n_strategy + 1) - 0.5, minor=True)
            axs[i, j].set_yticks(np.arange(n_metrics + 1) - 0.5, minor=True)
            axs[i, j].grid(which="minor")
            axs[i, j].set_title(f"{d}: {v}")

    fig.colorbar(col, ax=axs.ravel().tolist())
    return fig
