#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:21:00 2024

@author: angeles
"""

"""
"""
import argparse
from pathlib import Path
import matplotlib.pyplot as plt

# export PYTHONPATH=$(pwd)
from fmriprep_denoise.visualization import figures
from fmriprep_denoise.visualization.figures import (
    plot_motion_resid,
    plot_distance_dependence,
    plot_network_modularity,
    plot_dof_dataset,
    plot_vol_scrubbed_dataset
    ) 

from fmriprep_denoise.visualization.degrees_of_freedom_loss import (
    load_data,
    plot_stats
    ) 


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=(
            "Plot figures."
        ),
    )
    parser.add_argument(
        "--metricspath",
        action="store",
        type=str,
        help="path for folder with tsv outputs modularity, qcfc, and connectome.",
    )
    
    parser.add_argument(
        "--dataset_name", action="store", type=str, help="Dataset name."
    )
    
    parser.add_argument(
        "--fmriprepversion", action="store", type=str, help="fmriprep version"
    )
    
    return parser.parse_args()


def main():
    args = parse_args()
    print(vars(args))
    dataset = args.dataset_name
    fmriprep_version = args.fmriprepversion
    metrics_path = Path(args.metricspath)


    fig = plot_motion_resid(
        dataset,
        fmriprep_version,
        metrics_path)
    
    output_file = metrics_path / f"{dataset}_motion_resid.png"
    fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
    print(f"Figure saved to {output_file}")
    
    
    fig =  plot_distance_dependence(
            dataset,
            fmriprep_version,
            metrics_path)
    
    output_file = metrics_path / f"{dataset}_distance_dependence.png"
    fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
    print(f"Figure saved to {output_file}")
 
    figs = plot_network_modularity(
            dataset,
            fmriprep_version,
            metrics_path,
            by_group=False
           )
    
   # Check if figs is a list (multiple figures) or a single figure
    if isinstance(figs, list):
        # Loop through the list of figures and save each one
        for i, fig in enumerate(figs):
            output_file = metrics_path / f"{dataset}_network_modularity_{i}.png"
            fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save each figure with high resolution
            print(f"Figure {i} saved to {output_file}")
    else:
        # If it's a single figure, save it directly
        output_file = metrics_path / f"{dataset}_network_modularity.png"
        figs.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
        print(f"Figure saved to {output_file}")        
   
    
    fig, groups = plot_dof_dataset(
                    fmriprep_version, 
                    metrics_path
        )
    print(f"groups {groups}")
    output_file = metrics_path / f"{dataset}_dof_dataset.png"
    fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
    print(f"Figure saved to {output_file}")
  
    fig = plot_vol_scrubbed_dataset(
        fmriprep_version, 
        metrics_path
    )
    output_file = metrics_path / f"{dataset}_vol_scrubbed.png"
    fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
    print(f"Figure saved to {output_file}")
    
    datasets_list= [dataset]
    criteria_name = None
    confounds_phenotype = load_data(metrics_path, dataset, criteria_name, fmriprep_version)
    
    fig = plot_stats(confounds_phenotype, plot_subgroup=False)
    output_file = metrics_path / f"{dataset}_plotstats_dof.png"
    fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution

    print(f"Figure saved to {output_file}")
    


    
if __name__ == "__main__":
    main()
