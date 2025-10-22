#!/usr/bin/env python3
"""
Heating Detection System

Analyzes temperature data to detect heating cycles for two zones:
- Zone 1: T8_Z1 device
- Zone 2: T6_Z2 device

Heating is considered active when temperature >= 30°C.
Gaps shorter than 15 minutes between cycles are merged into a single cycle.
"""

import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
HEATING_THRESHOLD = 30.0  # Degrees Celsius
MIN_GAP_MINUTES = 15     # Minimum gap between cycles to consider them separate
ZONE_DEVICES = {
    'T8_Z1': 'Zone 1',
    'T6_Z2': 'Zone 2'
}


class HeatingDetector:
    """Detects heating cycles from temperature monitoring data."""
    
    def __init__(self, json_db_path: str = "data/temperature_database.json", 
                 output_dir: str = "output"):
        self.json_db_path = Path(json_db_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.database = self._load_database()
        
    def _load_database(self) -> Dict:
        """Load the JSON database."""
        if not self.json_db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.json_db_path}")
        
        with open(self.json_db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_device_data(self, device_name: str) -> pd.DataFrame:
        """Get device data as a sorted DataFrame."""
        if device_name not in self.database.get('devices', {}):
            raise ValueError(f"Device '{device_name}' not found in database")
        
        records = self.database['devices'][device_name].get('records', [])
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
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        logger.info(f"Loaded {len(df)} records for device {device_name}")
        return df
    
    def _detect_raw_cycles(self, df: pd.DataFrame) -> List[Tuple[datetime, datetime]]:
        """Detect raw heating cycles before gap merging."""
        if df.empty:
            return []
        
        cycles = []
        in_cycle = False
        cycle_start = None
        
        for _, row in df.iterrows():
            timestamp = row['timestamp']
            temperature = row['temperature']
            is_heating = temperature >= HEATING_THRESHOLD
            
            if is_heating and not in_cycle:
                # Start of new cycle
                cycle_start = timestamp
                in_cycle = True
            elif not is_heating and in_cycle:
                # End of cycle
                if cycle_start:
                    cycles.append((cycle_start, timestamp))
                in_cycle = False
                cycle_start = None
        
        # Handle case where data ends while in a cycle
        if in_cycle and cycle_start:
            cycles.append((cycle_start, df.iloc[-1]['timestamp']))
        
        return cycles
    
    def _merge_cycles_with_gaps(self, raw_cycles: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]:
        """Merge cycles with gaps shorter than MIN_GAP_MINUTES."""
        if not raw_cycles:
            return []
        
        merged_cycles = []
        current_start, current_end = raw_cycles[0]
        
        for i in range(1, len(raw_cycles)):
            next_start, next_end = raw_cycles[i]
            gap_duration = (next_start - current_end).total_seconds() / 60  # minutes
            
            if gap_duration <= MIN_GAP_MINUTES:
                # Merge cycles - extend current cycle to include the next one
                current_end = next_end
            else:
                # Gap is too large, finalize current cycle and start new one
                merged_cycles.append((current_start, current_end))
                current_start, current_end = next_start, next_end
        
        # Add the final cycle
        merged_cycles.append((current_start, current_end))
        
        return merged_cycles
    
    def detect_heating_cycles(self, device_name: str) -> List[Dict[str, str]]:
        """
        Detect heating cycles for a specific device.
        
        Returns:
            List of cycles with start/end timestamps in ISO format
        """
        logger.info(f"Detecting heating cycles for {device_name}...")
        
        df = self._get_device_data(device_name)
        if df.empty:
            return []
        
        # Step 1: Detect raw cycles
        raw_cycles = self._detect_raw_cycles(df)
        logger.info(f"Found {len(raw_cycles)} raw cycles for {device_name}")
        
        # Step 2: Merge cycles with short gaps
        merged_cycles = self._merge_cycles_with_gaps(raw_cycles)
        logger.info(f"After merging gaps <= {MIN_GAP_MINUTES}min: {len(merged_cycles)} cycles for {device_name}")
        
        # Step 3: Convert to required format
        cycles = []
        for start, end in merged_cycles:
            cycles.append({
                'start': start.isoformat(),
                'end': end.isoformat()
            })
        
        return cycles
    
    def analyze_all_zones(self) -> Dict[str, List[Dict[str, str]]]:
        """Analyze heating cycles for all configured zones."""
        all_cycles = {}
        
        for device_name in ZONE_DEVICES.keys():
            try:
                cycles = self.detect_heating_cycles(device_name)
                all_cycles[device_name] = cycles
                
                if cycles:
                    total_duration = sum(
                        (pd.to_datetime(cycle['end']) - pd.to_datetime(cycle['start'])).total_seconds() / 3600
                        for cycle in cycles
                    )
                    logger.info(f"{device_name}: {len(cycles)} cycles, total {total_duration:.1f} hours")
                else:
                    logger.info(f"{device_name}: No heating cycles detected")
                    
            except Exception as e:
                logger.error(f"Error analyzing {device_name}: {e}")
                all_cycles[device_name] = []
        
        return all_cycles
    
    def save_cycles_json(self, cycles_data: Dict[str, List[Dict[str, str]]]) -> str:
        """Save heating cycles to JSON file."""
        output_path = self.output_dir / "heating_cycles.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(cycles_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved heating cycles to: {output_path}")
        return str(output_path)
    
    def _calculate_cycles_per_day(self, cycles: List[Dict[str, str]]) -> Dict[str, int]:
        """Calculate number of cycles per day."""
        cycles_per_day = {}
        
        for cycle in cycles:
            start_time = pd.to_datetime(cycle['start'])
            # Assign cycle to the day it started (as per specification)
            day_key = start_time.strftime('%Y-%m-%d')
            cycles_per_day[day_key] = cycles_per_day.get(day_key, 0) + 1
        
        return cycles_per_day
    
    def create_daily_cycle_chart(self, device_name: str, cycles: List[Dict[str, str]]) -> str:
        """Create a chart showing cycles per day for a device."""
        cycles_per_day = self._calculate_cycles_per_day(cycles)
        
        if not cycles_per_day:
            logger.warning(f"No cycles to plot for {device_name}")
            return ""
        
        # Convert to DataFrame for easier plotting
        dates = list(cycles_per_day.keys())
        counts = list(cycles_per_day.values())
        
        df_plot = pd.DataFrame({
            'date': pd.to_datetime(dates),
            'cycles': counts
        }).sort_values('date')
        
        # Create the plot
        plt.figure(figsize=(14, 6))
        plt.plot(df_plot['date'], df_plot['cycles'], 'b-', marker='o', linewidth=2, markersize=4)
        
        plt.title(f'Heating Cycles Per Day - {device_name} ({ZONE_DEVICES.get(device_name, "Unknown Zone")})')
        plt.xlabel('Date')
        plt.ylabel('Number of Cycles')
        plt.grid(True, alpha=0.3)
        
        # Format x-axis
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.WeekdayLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
        
        plt.tight_layout()
        
        # Save the plot
        zone_id = device_name.split('_')[-1]  # Extract Z1 or Z2
        save_path = self.output_dir / f"heating_cycle_per_day_{zone_id}.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved daily cycles chart: {save_path}")
        return str(save_path)
    
    def generate_summary_report(self, cycles_data: Dict[str, List[Dict[str, str]]]) -> str:
        """Generate a summary report of heating analysis."""
        report_lines = []
        report_lines.append("HEATING DETECTION ANALYSIS SUMMARY")
        report_lines.append("=" * 50)
        report_lines.append(f"Heating threshold: >= {HEATING_THRESHOLD}°C")
        report_lines.append(f"Gap merging threshold: <= {MIN_GAP_MINUTES} minutes")
        report_lines.append("")
        
        for device_name, cycles in cycles_data.items():
            zone_name = ZONE_DEVICES.get(device_name, "Unknown Zone")
            report_lines.append(f"{device_name} ({zone_name}):")
            
            if not cycles:
                report_lines.append("  No heating cycles detected")
                report_lines.append("")
                continue
            
            # Calculate statistics
            total_cycles = len(cycles)
            durations = []
            cycles_per_day = self._calculate_cycles_per_day(cycles)
            
            for cycle in cycles:
                start = pd.to_datetime(cycle['start'])
                end = pd.to_datetime(cycle['end'])
                duration_hours = (end - start).total_seconds() / 3600
                durations.append(duration_hours)
            
            total_heating_hours = sum(durations)
            avg_cycle_duration = total_heating_hours / total_cycles if total_cycles > 0 else 0
            max_cycles_per_day = max(cycles_per_day.values()) if cycles_per_day else 0
            avg_cycles_per_day = sum(cycles_per_day.values()) / len(cycles_per_day) if cycles_per_day else 0
            
            report_lines.append(f"  Total cycles: {total_cycles}")
            report_lines.append(f"  Total heating time: {total_heating_hours:.1f} hours")
            report_lines.append(f"  Average cycle duration: {avg_cycle_duration:.1f} hours")
            report_lines.append(f"  Max cycles per day: {max_cycles_per_day}")
            report_lines.append(f"  Average cycles per day: {avg_cycles_per_day:.1f}")
            report_lines.append(f"  Date range: {min(cycles_per_day.keys())} to {max(cycles_per_day.keys())}")
            report_lines.append("")
        
        # Save report
        report_path = self.output_dir / "heating_analysis_summary.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        logger.info(f"Saved summary report: {report_path}")
        return str(report_path)


def main():
    """Main function to run heating detection analysis."""
    try:
        detector = HeatingDetector()
        
        print("Heating Detection Analysis")
        print("=" * 40)
        print(f"Threshold: >= {HEATING_THRESHOLD}°C")
        print(f"Gap merging: <= {MIN_GAP_MINUTES} minutes")
        print(f"Zones: {', '.join(f'{k} ({v})' for k, v in ZONE_DEVICES.items())}")
        print()
        
        # Analyze all zones
        print("Analyzing heating cycles...")
        cycles_data = detector.analyze_all_zones()
        
        # Save JSON output
        json_path = detector.save_cycles_json(cycles_data)
        print(f"✓ Saved cycles data: {Path(json_path).name}")
        
        # Generate daily cycle charts
        print("\nGenerating daily cycle charts...")
        for device_name, cycles in cycles_data.items():
            if cycles:
                chart_path = detector.create_daily_cycle_chart(device_name, cycles)
                if chart_path:
                    print(f"✓ Saved chart: {Path(chart_path).name}")
            else:
                print(f"⚠ No cycles to chart for {device_name}")
        
        # Generate summary report
        report_path = detector.generate_summary_report(cycles_data)
        print(f"✓ Saved summary: {Path(report_path).name}")
        
        print(f"\nAll outputs saved in: {detector.output_dir}")
        
    except FileNotFoundError:
        print("ERROR: Temperature database not found!")
        print("Please ensure data/temperature_database.json exists.")
    except Exception as e:
        print(f"ERROR: {e}")
        logger.error(f"Heating detection error: {e}")


if __name__ == "__main__":
    main()