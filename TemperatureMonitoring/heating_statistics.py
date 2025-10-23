#!/usr/bin/env python3
"""
Heating Statistics Analyzer

Analyzes heating patterns and their relationships to temperature differences.
Generates plots and statistics for heating cycle patterns.
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
INTERNAL_TEMP_DEVICE = 'T3_Kek'
EXTERNAL_TEMP_DEVICE = 'T2_Terasz'
HEATING_ZONE_DEVICE = 'T6_Z2'


class HeatingStatisticsAnalyzer:
    """Analyzes heating statistics and temperature patterns."""
    
    def __init__(self, 
                 temperature_db_path: str = "data/temperature_database.json",
                 heating_cycles_path: str = "output/heating_cycles.json",
                 output_dir: str = "output"):
        self.temperature_db_path = Path(temperature_db_path)
        self.heating_cycles_path = Path(heating_cycles_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.temperature_db = self._load_json(self.temperature_db_path)
        self.heating_cycles = self._load_json(self.heating_cycles_path)
        
    def _load_json(self, path: Path) -> Dict:
        """Load JSON file with error handling."""
        if not path.exists():
            if 'heating_cycles' in str(path):
                raise FileNotFoundError(
                    f"Heating cycles file not found: {path}\n"
                    f"Please run 'detect_heating.py' first to generate heating cycle data."
                )
            else:
                raise FileNotFoundError(f"File not found: {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_device_data_by_day(self, device_name: str) -> pd.DataFrame:
        """Get device temperature data grouped by day."""
        if device_name not in self.temperature_db.get('devices', {}):
            raise ValueError(f"Device '{device_name}' not found in database")
        
        records = self.temperature_db['devices'][device_name].get('records', [])
        if not records:
            logger.warning(f"No data found for device '{device_name}'")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df_data = []
        for record in records:
            df_data.append({
                'timestamp': pd.to_datetime(record['timestamp']),
                'temperature': record['temperature']
            })
        
        df = pd.DataFrame(df_data)
        df['date'] = df['timestamp'].dt.date
        
        return df
    
    def _calculate_daily_mean_temp_difference(self) -> pd.DataFrame:
        """Calculate daily mean temperature difference: mean(T3_Kek - T2_Terasz)."""
        logger.info(f"Calculating daily mean temperature difference: {INTERNAL_TEMP_DEVICE} - {EXTERNAL_TEMP_DEVICE}")
        
        # Get data for both devices
        df_internal = self._get_device_data_by_day(INTERNAL_TEMP_DEVICE)
        df_external = self._get_device_data_by_day(EXTERNAL_TEMP_DEVICE)
        
        if df_internal.empty or df_external.empty:
            logger.error("Missing temperature data for one or both devices")
            return pd.DataFrame()
        
        # NOTE: Devices have different sampling schedules, so we can't merge on timestamp
        # Instead, calculate daily mean for each device separately
        internal_daily_mean = df_internal.groupby('date').agg({
            'temperature': 'mean'
        }).reset_index()
        internal_daily_mean.columns = ['date', 'mean_temp_internal']
        
        external_daily_mean = df_external.groupby('date').agg({
            'temperature': 'mean'
        }).reset_index()
        external_daily_mean.columns = ['date', 'mean_temp_external']
        
        # Merge daily means
        daily_stats = pd.merge(
            internal_daily_mean,
            external_daily_mean,
            on='date',
            how='inner'
        )
        
        # Calculate difference of daily means
        daily_stats['mean_temp_diff'] = daily_stats['mean_temp_internal'] - daily_stats['mean_temp_external']
        
        # Keep only date and mean_temp_diff columns
        daily_stats = daily_stats[['date', 'mean_temp_diff']]
        daily_stats['date'] = pd.to_datetime(daily_stats['date'])
        
        logger.info(f"Calculated temperature differences for {len(daily_stats)} days")
        return daily_stats
    
    def _calculate_daily_heating_cycle_count(self) -> pd.DataFrame:
        """Calculate number of heating cycles per day from heating_cycles.json."""
        logger.info(f"Calculating daily heating cycle count for {HEATING_ZONE_DEVICE}")
        
        cycles = self.heating_cycles.get(HEATING_ZONE_DEVICE, [])
        if not cycles:
            logger.warning(f"No heating cycles found for {HEATING_ZONE_DEVICE}")
            return pd.DataFrame()
        
        # Count cycles per day
        cycle_counts = {}
        for cycle in cycles:
            start_time = pd.to_datetime(cycle['start'])
            day_key = start_time.date()
            cycle_counts[day_key] = cycle_counts.get(day_key, 0) + 1
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {'date': pd.to_datetime(date), 'cycle_count': count}
            for date, count in cycle_counts.items()
        ])
        
        df = df.sort_values('date').reset_index(drop=True)
        
        logger.info(f"Calculated cycle counts for {len(df)} days")
        return df
    
    def _merge_daily_data(self) -> pd.DataFrame:
        """Merge temperature difference and heating cycle count data."""
        df_temp_diff = self._calculate_daily_mean_temp_difference()
        df_cycles = self._calculate_daily_heating_cycle_count()
        
        if df_temp_diff.empty:
            logger.error("Cannot merge data: temperature data is empty")
            return pd.DataFrame()
        
        # Use left join to keep all days with temperature data
        # Days without heating cycles will get cycle_count = 0
        if df_cycles.empty:
            logger.warning("No heating cycles found, all days will have cycle_count = 0")
            df_temp_diff['cycle_count'] = 0
            df_merged = df_temp_diff
        else:
            df_merged = pd.merge(df_temp_diff, df_cycles, on='date', how='left')
            # Fill missing cycle counts with 0 (days with no heating)
            df_merged['cycle_count'] = df_merged['cycle_count'].fillna(0).astype(int)
        
        days_with_heating = (df_merged['cycle_count'] > 0).sum()
        days_without_heating = (df_merged['cycle_count'] == 0).sum()
        logger.info(f"Merged data contains {len(df_merged)} days total")
        logger.info(f"  - {days_with_heating} days with heating cycles")
        logger.info(f"  - {days_without_heating} days without heating (0 cycles)")
        return df_merged
    
    def generate_dual_axis_plot(self) -> Tuple[str, str]:
        """Generate dual-axis plot: temperature difference and heating cycle count over time."""
        logger.info("Generating dual-axis plot...")
        
        df = self._merge_daily_data()
        if df.empty:
            logger.error("No data available for plotting")
            return "", ""
        
        # Create figure and axis
        fig, ax1 = plt.subplots(figsize=(14, 6))
        
        # Plot temperature difference on left axis (blue)
        color_temp = 'tab:blue'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Mean Temperature Difference (°C)', color=color_temp)
        ax1.plot(df['date'], df['mean_temp_diff'], '.', color=color_temp, markersize=5, label='Temp Diff')
        ax1.tick_params(axis='y', labelcolor=color_temp)
        ax1.grid(True, alpha=0.3)
        
        # Create second y-axis for heating cycles (red)
        ax2 = ax1.twinx()
        color_cycles = 'tab:red'
        ax2.set_ylabel('Number of Heating Cycles', color=color_cycles)
        ax2.plot(df['date'], df['cycle_count'], '.', color=color_cycles, markersize=5, label='Heating Cycles')
        ax2.tick_params(axis='y', labelcolor=color_cycles)
        
        # Format x-axis
        ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=7))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        # Title
        plt.title(f'Mean Temperature Difference ({INTERNAL_TEMP_DEVICE} - {EXTERNAL_TEMP_DEVICE}) and Heating Cycles ({HEATING_ZONE_DEVICE})')
        
        fig.tight_layout()
        
        # Save plot
        plot_path = self.output_dir / "MeanDiff_And_HeatingCycleCount_Plot.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        logger.info(f"Saved dual-axis plot: {plot_path}")
        
        # Save CSV
        csv_path = self.output_dir / "MeanDiff_And_HeatingCycleCount_Plot.csv"
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved data CSV: {csv_path}")
        
        return str(plot_path), str(csv_path)
    
    def generate_xy_plot(self) -> Tuple[str, str]:
        """Generate X-Y scatter plot: temperature difference vs heating cycle count."""
        logger.info("Generating X-Y scatter plot...")
        
        df = self._merge_daily_data()
        if df.empty:
            logger.error("No data available for plotting")
            return "", ""
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Plot scatter
        ax.plot(df['mean_temp_diff'], df['cycle_count'], '.', markersize=8, color='tab:purple')
        
        ax.set_xlabel(f'Mean Temperature Difference (°C)\n({INTERNAL_TEMP_DEVICE} - {EXTERNAL_TEMP_DEVICE})')
        ax.set_ylabel(f'Number of Heating Cycles\n({HEATING_ZONE_DEVICE})')
        ax.set_title('Heating Cycles vs Temperature Difference')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        plot_path = self.output_dir / "MeanDiff_And_HeatingCycleCount_XY.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        logger.info(f"Saved X-Y plot: {plot_path}")
        
        # Save CSV (same data as dual-axis plot)
        csv_path = self.output_dir / "MeanDiff_And_HeatingCycleCount_XY.csv"
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved data CSV: {csv_path}")
        
        return str(plot_path), str(csv_path)
    
    def generate_summary_statistics(self) -> str:
        """Generate summary statistics report."""
        logger.info("Generating summary statistics...")
        
        df = self._merge_daily_data()
        if df.empty:
            logger.error("No data available for statistics")
            return ""
        
        report_lines = []
        report_lines.append("HEATING STATISTICS ANALYSIS SUMMARY")
        report_lines.append("=" * 60)
        report_lines.append(f"Internal Temperature Device: {INTERNAL_TEMP_DEVICE}")
        report_lines.append(f"External Temperature Device: {EXTERNAL_TEMP_DEVICE}")
        report_lines.append(f"Heating Zone Device: {HEATING_ZONE_DEVICE}")
        report_lines.append("")
        report_lines.append(f"Analysis Period: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
        report_lines.append(f"Total Days Analyzed: {len(df)}")
        report_lines.append("")
        
        # Temperature difference statistics
        report_lines.append("TEMPERATURE DIFFERENCE STATISTICS")
        report_lines.append("-" * 60)
        report_lines.append(f"Mean Temperature Difference: {df['mean_temp_diff'].mean():.2f} °C")
        report_lines.append(f"Median Temperature Difference: {df['mean_temp_diff'].median():.2f} °C")
        report_lines.append(f"Std Dev Temperature Difference: {df['mean_temp_diff'].std():.2f} °C")
        report_lines.append(f"Min Temperature Difference: {df['mean_temp_diff'].min():.2f} °C")
        report_lines.append(f"Max Temperature Difference: {df['mean_temp_diff'].max():.2f} °C")
        report_lines.append("")
        
        # Heating cycle statistics
        report_lines.append("HEATING CYCLE STATISTICS")
        report_lines.append("-" * 60)
        report_lines.append(f"Mean Cycles Per Day: {df['cycle_count'].mean():.2f}")
        report_lines.append(f"Median Cycles Per Day: {df['cycle_count'].median():.0f}")
        report_lines.append(f"Std Dev Cycles Per Day: {df['cycle_count'].std():.2f}")
        report_lines.append(f"Min Cycles Per Day: {df['cycle_count'].min():.0f}")
        report_lines.append(f"Max Cycles Per Day: {df['cycle_count'].max():.0f}")
        report_lines.append(f"Total Heating Cycles: {df['cycle_count'].sum():.0f}")
        report_lines.append("")
        
        # Correlation analysis
        correlation = df['mean_temp_diff'].corr(df['cycle_count'])
        report_lines.append("CORRELATION ANALYSIS")
        report_lines.append("-" * 60)
        report_lines.append(f"Correlation (Temp Diff vs Cycle Count): {correlation:.4f}")
        if abs(correlation) > 0.7:
            strength = "strong"
        elif abs(correlation) > 0.4:
            strength = "moderate"
        else:
            strength = "weak"
        direction = "negative" if correlation < 0 else "positive"
        report_lines.append(f"Interpretation: {strength} {direction} correlation")
        report_lines.append("")
        
        # Additional insights
        report_lines.append("KEY INSIGHTS")
        report_lines.append("-" * 60)
        
        # Days with highest cycle counts
        top_5_cycles = df.nlargest(5, 'cycle_count')[['date', 'cycle_count', 'mean_temp_diff']]
        report_lines.append("Days with Most Heating Cycles:")
        for _, row in top_5_cycles.iterrows():
            report_lines.append(f"  {row['date'].strftime('%Y-%m-%d')}: {row['cycle_count']:.0f} cycles, temp diff: {row['mean_temp_diff']:.1f}°C")
        report_lines.append("")
        
        # Days with lowest temperature difference
        lowest_5_diff = df.nsmallest(5, 'mean_temp_diff')[['date', 'mean_temp_diff', 'cycle_count']]
        report_lines.append("Days with Lowest Temperature Difference:")
        for _, row in lowest_5_diff.iterrows():
            report_lines.append(f"  {row['date'].strftime('%Y-%m-%d')}: {row['mean_temp_diff']:.1f}°C, {row['cycle_count']:.0f} cycles")
        report_lines.append("")
        
        # Save report
        report_path = self.output_dir / "heating_statistics.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        logger.info(f"Saved summary statistics: {report_path}")
        return str(report_path)
    
    def analyze_all(self):
        """Run complete analysis and generate all outputs."""
        print("Heating Statistics Analysis")
        print("=" * 60)
        print(f"Internal Temperature: {INTERNAL_TEMP_DEVICE}")
        print(f"External Temperature: {EXTERNAL_TEMP_DEVICE}")
        print(f"Heating Zone: {HEATING_ZONE_DEVICE}")
        print()
        
        try:
            # Generate dual-axis plot
            print("Generating dual-axis plot...")
            plot1_path, csv1_path = self.generate_dual_axis_plot()
            if plot1_path:
                print(f"✓ Dual-axis plot: {Path(plot1_path).name}")
                print(f"✓ Data CSV: {Path(csv1_path).name}")
            else:
                print("✗ Failed to generate dual-axis plot")
            print()
            
            # Generate X-Y plot
            print("Generating X-Y scatter plot...")
            plot2_path, csv2_path = self.generate_xy_plot()
            if plot2_path:
                print(f"✓ X-Y plot: {Path(plot2_path).name}")
                print(f"✓ Data CSV: {Path(csv2_path).name}")
            else:
                print("✗ Failed to generate X-Y plot")
            print()
            
            # Generate summary statistics
            print("Generating summary statistics...")
            stats_path = self.generate_summary_statistics()
            if stats_path:
                print(f"✓ Summary statistics: {Path(stats_path).name}")
            else:
                print("✗ Failed to generate summary statistics")
            print()
            
            print(f"All outputs saved in: {self.output_dir}")
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            print(f"ERROR: {e}")


def main():
    """Main function to run heating statistics analysis."""
    try:
        analyzer = HeatingStatisticsAnalyzer()
        analyzer.analyze_all()
        
    except FileNotFoundError as e:
        print(f"ERROR: Required file not found!")
        print(f"{e}")
        print("\nPlease ensure:")
        print("1. temperature_database.json exists (run main.py first)")
        print("2. heating_cycles.json exists (run detect_heating.py first)")
    except Exception as e:
        print(f"ERROR: {e}")
        logger.error(f"Heating statistics analysis error: {e}")


if __name__ == "__main__":
    main()
