#!/usr/bin/env python3
"""
Git Commit Analysis Script

Analyzes git commit data and creates weekly visualizations for:
- All commits per week
- Pull requests per week

Usage:
    python git_analyzer.py <input_file> [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD]
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import argparse
import sys
from pathlib import Path
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.ticker import MaxNLocator
import numpy as np

# Set font preferences
plt.rcParams['font.family'] = ['Arial', 'sans-serif']


def parse_git_data(file_path):
    """
    Parse the git commit data from CSV format.
    
    Expected format: "hash","author","date","message"
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path, header=None, 
                        names=['hash', 'author', 'date', 'message'])
        
        # Parse the date column, handling mixed timezones by converting to UTC first
        df['date'] = pd.to_datetime(df['date'], utc=True)
        
        # Convert to naive datetime (remove timezone info) to avoid comparison issues
        df['date'] = df['date'].dt.tz_localize(None)
        
        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)
        
        return df
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        sys.exit(1)


def filter_by_date_range(df, start_date=None, end_date=None):
    """
    Filter dataframe by optional start and end dates.
    """
    if start_date:
        # Parse start_date and make it timezone-naive to match df['date']
        start_date = pd.to_datetime(start_date).tz_localize(None)
        df = df[df['date'] >= start_date]
    
    if end_date:
        # Parse end_date and make it timezone-naive to match df['date']
        end_date = pd.to_datetime(end_date).tz_localize(None)
        df = df[df['date'] <= end_date]
    
    return df


def group_by_weeks(df):
    """
    Group commits by weeks (Monday to Sunday) and count entries.
    Returns a series with week start dates as index and counts as values.
    """
    if len(df) == 0:
        return pd.Series(dtype=int)
    
    # Make a copy to avoid modifying the original dataframe
    df_copy = df.copy()
    
    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df_copy['date']):
        df_copy['date'] = pd.to_datetime(df_copy['date'])
    
    # Set the week to start on Monday
    df_copy['week'] = df_copy['date'].dt.to_period('W-MON')
    
    # Count commits per week
    weekly_counts = df_copy.groupby('week').size()
    
    # Convert period index to datetime (start of week)
    weekly_counts.index = weekly_counts.index.to_timestamp()
    
    return weekly_counts


def create_month_labels(date_range):
    """
    Create month labels in format "Mon\n'YY" for the 1st of each month.
    """
    if len(date_range) == 0:
        return [], []
    
    start_date = date_range.min()
    end_date = date_range.max()
    
    # Generate 1st of each month in the range
    current = datetime(start_date.year, start_date.month, 1)
    if current < start_date:
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    
    labels = []
    positions = []
    
    while current <= end_date:
        labels.append(f"{current.strftime('%b')}\n'{current.strftime('%y')}")
        positions.append(current)
        
        # Move to next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    
    return positions, labels


def plot_weekly_data(ax, weekly_data, ylabel, bar_color):
    """
    Plot weekly data as bars with custom month labels and rounded corners.
    """
    if len(weekly_data) == 0:
        ax.set_ylabel(ylabel)
        ax.text(0.5, 0.5, 'No data in date range', 
                transform=ax.transAxes, ha='center', va='center')
        return
    
    # Create bars with fixed corner radius (like CSS border-radius)
    bar_width = 5
    
    max_height = np.max(weekly_data)
    
    # Use the square of the full width of bars to maintain aspect ratio
    aspect_ratio = max_height/(bar_width+2)**2
    
    print(max_height, bar_width, aspect_ratio)
    
    for date, value in weekly_data.items():
        # Create rounded rectangle with consistent corner radius
        x = mdates.date2num(date)
        
        # Use fixed rounding parameters that create consistent corner appearance
        # Similar to CSS border-radius behavior
        rounding_size = 1.0 # Fixed moderate rounding
        
        fancy_rect = FancyBboxPatch((x - bar_width/2, 0), bar_width, value,
                                   boxstyle=f"round,rounding_size={rounding_size},pad=0.1", 
                                   facecolor=bar_color, alpha=1.0, 
                                   edgecolor='white', linewidth=0.5,
                                   mutation_aspect=aspect_ratio)
        ax.add_patch(fancy_rect)
    
    # Set axis limits
    if len(weekly_data) > 0:
        x_min = mdates.date2num(weekly_data.index.min()) - 7
        x_max = mdates.date2num(weekly_data.index.max()) + 7
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(0, weekly_data.max() * 1.1)
    
    # Customize the plot
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Set y-axis to show only integers
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Create custom month labels - this will override any automatic ticks
    positions, labels = create_month_labels(weekly_data.index)
    if positions:
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, fontsize=10)
    else:
        # Fallback to automatic monthly ticks if no custom labels
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n\'%y'))
    
    # Rotate x-axis labels for better readability
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha='center')


def main():
    parser = argparse.ArgumentParser(description='Analyze git commit data and create weekly visualizations')
    parser.add_argument('input_file', help='Path to the git data CSV file')
    parser.add_argument('--start-date', help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end-date', help='End date in YYYY-MM-DD format')
    parser.add_argument('--output', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    # Validate input file
    if not Path(args.input_file).exists():
        print(f"Error: File {args.input_file} does not exist")
        sys.exit(1)
    
    # Parse the git data
    print("Reading git data...")
    df = parse_git_data(args.input_file)
    print(f"Loaded {len(df)} commits")
    
    # Filter by date range if specified
    if args.start_date or args.end_date:
        print(f"Filtering by date range: {args.start_date} to {args.end_date}")
        df = filter_by_date_range(df, args.start_date, args.end_date)
        print(f"Filtered to {len(df)} commits")
    
    # Filter for PRs (commits with "Merge pull request" in message)
    pr_df = df[df['message'].str.contains('Merge pull request', case=False, na=False)]
    print(f"Found {len(pr_df)} pull request merges")
    
    # Group by weeks
    all_commits_weekly = group_by_weeks(df)
    pr_weekly = group_by_weeks(pr_df)
    
    # Create the plot with reduced figure size
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))
    
    # GitHub's actual light versions of green and blue
    github_light_green = '#57d193'  # GitHub's light green (lighter version of #238636)
    github_light_blue = '#54aeff'   # GitHub's light blue (lighter version of #0969da)
    
    # Plot all commits (no title)
    plot_weekly_data(ax1, all_commits_weekly, 
                    'Commits/Week', github_light_green)
    
    # Plot PRs (no title)
    plot_weekly_data(ax2, pr_weekly, 
                    'PRs/Week', github_light_blue)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save or show the plot
    if args.output:
        plt.savefig(args.output, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {args.output}")
    else:
        plt.show()
    
    # Print summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"Total commits: {len(df)}")
    print(f"Total PRs: {len(pr_df)}")
    print(f"Average commits per week: {all_commits_weekly.mean():.1f}")
    print(f"Average PRs per week: {pr_weekly.mean():.1f}")
    if len(all_commits_weekly) > 0:
        print(f"Max commits in a week: {all_commits_weekly.max()}")
    if len(pr_weekly) > 0:
        print(f"Max PRs in a week: {pr_weekly.max()}")


if __name__ == "__main__":
    main()