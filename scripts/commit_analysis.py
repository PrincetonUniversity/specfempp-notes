#!/usr/bin/env python3
"""
Git Commit Log Analysis Script
Analyzes commit data to create weekly bar charts for commits and pull requests.

Usage:
    python commit_analysis.py <csv_file> [start_date] [end_date]
    
    csv_file: Path to CSV file with commit data
    start_date: Optional start date in YYYYMMDD format (inclusive)
    end_date: Optional end date in YYYYMMDD format (inclusive)

Example:
    python commit_analysis.py commits.csv
    python commit_analysis.py commits.csv 20250601
    python commit_analysis.py commits.csv 20250601 20250630
"""

import pandas as pd
import re
import sys
from datetime import datetime
import matplotlib.pyplot as plt

def parse_date_filter(date_str):
    """Parse date string in YYYYMMDD format."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y%m%d')
    except ValueError:
        raise ValueError(f"Invalid date format '{date_str}'. Use YYYYMMDD format.")

def load_and_process_data(csv_file_path, start_date=None, end_date=None):
    """Load CSV file and process commit data with optional date filtering."""
    
    # Read CSV file with pandas
    try:
        # Read CSV without headers, assuming 4 columns: hash, author, date, message
        df = pd.read_csv(csv_file_path, header=None, names=['hash', 'author', 'date_str', 'message'])
        print(f"Loaded {len(df)} rows from CSV file")
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file '{csv_file_path}' not found.")
    except Exception as e:
        raise Exception(f"Error reading CSV file: {e}")
    
    # Clean up quoted strings
    df['hash'] = df['hash'].str.strip('"')
    df['author'] = df['author'].str.strip('"')
    df['date_str'] = df['date_str'].str.strip('"')
    df['message'] = df['message'].str.strip('"')
    
    # Parse dates
    def parse_git_date(date_str):
        """Parse git date format and remove timezone."""
        try:
            # Remove timezone info (e.g., ' -0400')
            date_clean = re.sub(r' [-+]\d{4}$', '', str(date_str))
            return pd.to_datetime(date_clean, format='%a %b %d %H:%M:%S %Y')
        except:
            return pd.NaT
    
    df['date'] = df['date_str'].apply(parse_git_date)
    
    # Remove rows with invalid dates
    initial_count = len(df)
    df = df.dropna(subset=['date'])
    if len(df) < initial_count:
        print(f"Warning: Dropped {initial_count - len(df)} rows with invalid dates")
    
    # Apply date filtering
    if start_date:
        df = df[df['date'].dt.date >= start_date.date()]
        print(f"Filtered to dates >= {start_date.strftime('%Y-%m-%d')}: {len(df)} commits")
    
    if end_date:
        df = df[df['date'].dt.date <= end_date.date()]
        print(f"Filtered to dates <= {end_date.strftime('%Y-%m-%d')}: {len(df)} commits")
    
    # Identify pull requests
    pr_pattern = r'Merge pull request #(\d+)'
    df['is_pr'] = df['message'].str.contains(pr_pattern, regex=True, na=False)
    
    # Add week start column (Monday of each week)
    df['week_start'] = df['date'].dt.to_period('W-MON').dt.start_time
    
    return df

def analyze_weekly_data(df):
    """Analyze commits and PRs by week using pandas groupby."""
    
    # Group by week and count total commits
    weekly_commits = df.groupby('week_start').size()
    
    # Group by week and count PRs
    weekly_prs = df[df['is_pr']].groupby('week_start').size()
    
    # Ensure all weeks are represented in both series
    all_weeks = weekly_commits.index.union(weekly_prs.index)
    weekly_commits = weekly_commits.reindex(all_weeks, fill_value=0)
    weekly_prs = weekly_prs.reindex(all_weeks, fill_value=0)
    
    return weekly_commits, weekly_prs

def create_plots(weekly_commits, weekly_prs):
    """Create bar plots for commits and PRs side by side."""
    
    # Create subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Create month labels with year format
    dates = weekly_commits.index
    month_positions = []
    month_labels = []
    
    # Find the first occurrence of each month
    seen_months = set()
    for i, date in enumerate(dates):
        month_year = (date.year, date.month)
        if month_year not in seen_months:
            seen_months.add(month_year)
            month_positions.append(i)
            # Format as "Jan '25"
            month_labels.append(date.strftime("%b '%y"))
    
    # Plot commits
    bars1 = ax1.bar(range(len(weekly_commits)), weekly_commits.values, color='steelblue', alpha=0.7)
    ax1.set_ylabel('Commits/Week')
    ax1.grid(axis='y', alpha=0.3)
    
    # Plot PRs
    bars2 = ax2.bar(range(len(weekly_prs)), weekly_prs.values, color='darkgreen', alpha=0.7)
    ax2.set_ylabel('PRs/Week')
    ax2.grid(axis='y', alpha=0.3)
    
    # Set custom x-axis labels for both plots
    for ax in [ax1, ax2]:
        ax.set_xticks(month_positions)
        ax.set_xticklabels(month_labels)
        ax.tick_params(axis='x', rotation=0)
        # Force y-axis to show only whole numbers
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    plt.tight_layout()
    return fig

def print_summary(df, weekly_commits, weekly_prs):
    """Print summary statistics."""
    if len(df) == 0:
        print("No commits found matching the criteria.")
        return
    
    print(f"\nData Summary:")
    print(f"Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"Total commits: {len(df)}")
    print(f"Total PRs: {df['is_pr'].sum()}")
    print(f"Unique authors: {df['author'].nunique()}")
    print(f"Weeks with activity: {len(weekly_commits[weekly_commits > 0])}")
    
    # Top authors
    print(f"\nTop 5 authors by commit count:")
    author_counts = df['author'].value_counts().head()
    for author, count in author_counts.items():
        print(f"  {author}: {count} commits")

def main():
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python commit_analysis.py <csv_file> [start_date] [end_date]")
        print("       start_date and end_date should be in YYYYMMDD format")
        print("\nExample:")
        print("       python commit_analysis.py commits.csv")
        print("       python commit_analysis.py commits.csv 20250601")
        print("       python commit_analysis.py commits.csv 20250601 20250630")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    start_date = None
    end_date = None
    
    # Parse optional date arguments
    try:
        if len(sys.argv) >= 3:
            start_date = parse_date_filter(sys.argv[2])
            print(f"Start date filter: {start_date.strftime('%Y-%m-%d')}")
        
        if len(sys.argv) >= 4:
            end_date = parse_date_filter(sys.argv[3])
            print(f"End date filter: {end_date.strftime('%Y-%m-%d')}")
            
        if start_date and end_date and start_date > end_date:
            raise ValueError("Start date must be before or equal to end date")
            
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Load and process the data
    print(f"Loading commit data from '{csv_file_path}'...")
    try:
        df = load_and_process_data(csv_file_path, start_date, end_date)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    if len(df) == 0:
        print("No commits found matching the criteria.")
        sys.exit(1)
    
    # Analyze weekly data
    print("Analyzing weekly patterns...")
    weekly_commits, weekly_prs = analyze_weekly_data(df)
    
    # Print summary
    print_summary(df, weekly_commits, weekly_prs)
    
    # Create and show plots
    print("Creating plots...")
    fig = create_plots(weekly_commits, weekly_prs)
    plt.show()
    
    # Save the plot
    output_filename = f"weekly_git_activity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    fig.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved as '{output_filename}'")

if __name__ == "__main__":
    main()