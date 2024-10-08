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

from fmriprep_denoise.visualization import degrees_of_freedom_loss 
from fmriprep_denoise.visualization import connectivity_similarity
from fmriprep_denoise.visualization import motion_metrics

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


   #  fig = plot_motion_resid(
   #      dataset,
   #      fmriprep_version,
   #      metrics_path)
    
   #  output_file = metrics_path / f"{dataset}_motion_resid.png"
   #  fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
   #  print(f"Figure saved to {output_file}")
    
    
   #  fig =  plot_distance_dependence(
   #          dataset,
   #          fmriprep_version,
   #          metrics_path)
    
   #  output_file = metrics_path / f"{dataset}_distance_dependence.png"
   #  fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
   #  print(f"Figure saved to {output_file}")
 
   #  figs = plot_network_modularity(
   #          dataset,
   #          fmriprep_version,
   #          metrics_path,
   #          by_group=False
   #         )
   # # Check if figs is a list (multiple figures) or a single figure
   #  if isinstance(figs, list):
   #      # Loop through the list of figures and save each one
   #      for i, fig in enumerate(figs):
   #          output_file = metrics_path / f"{dataset}_network_modularity_{i}.png"
   #          fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save each figure with high resolution
   #          print(f"Figure {i} saved to {output_file}")
   #  else:
   #      # If it's a single figure, save it directly
   #      output_file = metrics_path / f"{dataset}_network_modularity.png"
   #      figs.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
   #      print(f"Figure saved to {output_file}")        
   
    
   #  fig, groups = plot_dof_dataset(
   #                  fmriprep_version, 
   #                  metrics_path
   #      )
   #  print(f"groups {groups}")
   #  output_file = metrics_path / f"{dataset}_dof_dataset.png"
   #  fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
   #  print(f"Figure saved to {output_file}")
  
    
  
   #  fig = plot_vol_scrubbed_dataset(
   #      fmriprep_version, 
   #      metrics_path
   #  )
   #  output_file = metrics_path / f"{dataset}_vol_scrubbed.png"
   #  fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
   #  print(f"Figure saved to {output_file}")
    
    
    #DEGREES OF FREEDOM LOST
    datasets_list= [dataset]
    criteria_name = None
    confounds_phenotype = degrees_of_freedom_loss.load_data(metrics_path, datasets_list, criteria_name, fmriprep_version) 
    fig = degrees_of_freedom_loss.plot_stats(confounds_phenotype, plot_subgroup=False)
    output_file = metrics_path / f"{dataset}_plotstats_dof.png"
    fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
    print(f"Figure saved to {output_file}")
    
    #CONNECTIVITY SIMILARITY
    datasets_list= [dataset]
    average_connectomes = connectivity_similarity.load_data(metrics_path, datasets_list, fmriprep_version) 
    fig = connectivity_similarity.plot_stats(average_connectomes, horizontal=False)
    output_file = metrics_path / f"{dataset}_connectivitysimilarity.png"
    fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
    print(f"Figure saved to {output_file}")

    #MOTION METRICS
    datasets_list= [dataset]
    criteria_name = None
    measures = ["p_values","fdr_p_values","median","distance", "modularity", "modularity_motion"]
    for measure_name in measures:
        data, measure = motion_metrics.load_data(metrics_path, datasets_list, criteria_name, fmriprep_version, measure_name)
        fig = motion_metrics.plot_stats(data, measure, group="full_sample")
        output_file = metrics_path / f"{dataset}_motionmetrics_{measure_name}.png"
        fig.savefig(output_file, dpi=300, bbox_inches='tight')  # Save figure with high resolution
        print(f"Figure saved to {output_file}")

    
  


    
if __name__ == "__main__":
    main()
