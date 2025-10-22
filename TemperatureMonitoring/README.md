# Temperature Monitoring Data Processor

A Python console application for processing temperature sensor data from CSV files packed in ZIP archives. The application generates comprehensive visualizations and Excel reports for temperature monitoring analysis.

## Features

- **CSV Data Processing**: Parse CSV files with device names, timestamps, temperature, humidity, and battery data
- **ZIP File Support**: Extract and process multiple CSV files from ZIP archives
- **Data Visualization**: Generate timeline plots, multi-device comparisons, and statistical heatmaps
- **Excel Export**: Create detailed Excel reports with statistics and hourly averages
- **Comprehensive Testing**: Full unit test coverage with pytest
- **Logging**: Detailed logging for debugging and monitoring

## CSV File Format

The application expects CSV files with the following format:

```csv
T3_DeviceName
Time-Data=(A2/86400)+25569;Temp;Humi;Vbat
1791;13.72;86.58;2943
3593;13.57;86.7;2957
5396;13.5;86.88;2960
```

- **Line 1**: Device name (e.g., "T3_DeviceName")
- **Line 2**: Headers (Time-Data, Temp, Humi, Vbat)
- **Data Lines**: Timestamp (Excel format), Temperature (°C), Humidity (%), Battery (mV)

## Installation

### Quick Setup (Recommended)

1. **Clone or download** this project to your local machine

2. **Run the automated setup script**:
   ```powershell
   # Full setup with package verification
   .\setup.ps1
   
   # Quick setup without verification tests
   .\setup.ps1 -SkipTests
   
   # Show help and options
   .\setup.ps1 -Help
   ```

The setup script will automatically:
- Detect Python 3.8+ installation
- Create and activate a virtual environment
- Install all required dependencies
- Create necessary data and output directories
- Verify package installations (unless `-SkipTests` is used)

### Manual Installation

If you prefer manual setup or the automated script doesn't work:

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create data directories** (if not already present):
   ```bash
   mkdir -p data output
   ```

## Usage

### Console Application

After running the setup script, you can start the application directly:

```bash
# Process a ZIP file with full reports
python src/main.py data/temperature_data.zip

# Process without generating reports
python src/main.py data/temperature_data.zip --no-reports

# Set logging level
python src/main.py data/temperature_data.zip --log-level DEBUG
```

### GUI Application (if available)

To start the graphical user interface:

```bash
# Launch the GUI application
python launch_gui.py
```

The GUI provides:
- File selection dialog for ZIP files
- Visual progress indicators
- Interactive report generation options
- Real-time log display

## Program Outputs

The Temperature Monitoring application generates comprehensive reports and visualizations in the `output/` directory. Here's a complete summary of all outputs and their purposes:

### Individual Device Reports

**Timeline Visualization**
- **File**: `{device_name}_timeline.png`
- **Content**: Multi-panel timeline showing temperature, humidity, and battery voltage over time for a single device
- **Purpose**: Track individual device performance and identify patterns or anomalies

**Excel Data Report**
- **File**: `{device_name}_data.xlsx`
- **Content**: 
  - Raw data with converted timestamps
  - Statistical summary (min, max, mean, std deviation)
  - Hourly averages for trend analysis
- **Purpose**: Detailed data analysis and further processing in Excel

### Multi-Device Comparison Reports

**Temperature Comparison**
- **File**: `multi_device_temperature_comparison.png`
- **Content**: Overlaid temperature timelines for all devices with different colors
- **Purpose**: Compare temperature readings across multiple sensors to identify environmental variations

**Humidity Comparison**
- **File**: `multi_device_humidity_comparison.png`
- **Content**: Overlaid humidity timelines for all devices
- **Purpose**: Analyze humidity patterns and correlations between different monitoring locations

**Battery Level Comparison**
- **File**: `multi_device_battery_mv_comparison.png`
- **Content**: Battery voltage timelines showing power consumption patterns
- **Purpose**: Monitor device health and predict maintenance needs

### Statistical Analysis

**Statistics Heatmap**
- **File**: `statistics_heatmap.png`
- **Content**: Color-coded matrix showing statistical measures (mean, std, min, max) for all devices
- **Purpose**: Quick visual comparison of device performance characteristics

**Combined Excel Report**
- **File**: `all_devices_data.xlsx`
- **Content**: 
  - Consolidated data from all devices
  - Cross-device statistical comparisons
  - Summary statistics table
- **Purpose**: Comprehensive analysis and reporting for all monitored devices

### Log Files

**Application Log**
- **File**: `temperature_monitoring.log`
- **Content**: 
  - Processing steps and timestamps
  - Error messages and warnings
  - Data validation results
  - Performance metrics
- **Purpose**: Debugging, monitoring, and audit trail

### Console Output

During execution, the application displays:
- **Processing Status**: Files being processed and progress indicators
- **Data Summary**: Device count, data points, and time range
- **Validation Results**: Invalid data lines and error counts
- **Report Generation**: Files created and their locations
- **Statistics Overview**: Quick summary of key metrics for each device

### Error Handling Outputs

When issues occur, the application generates:
- **Error Messages**: Clear descriptions of problems encountered
- **Warning Messages**: Non-fatal issues (e.g., malformed data lines)
- **Skipped Files**: List of files that couldn't be processed
- **Validation Reports**: Details about data quality issues

All outputs are designed to provide both immediate insights and detailed data for further analysis, making the application suitable for both quick monitoring and comprehensive research purposes.

### Python API

```python
from src.main import TemperatureMonitoringApp

app = TemperatureMonitoringApp()
device_data_list = app.process_zip_file("data/temperature_data.zip")
app.print_summary(device_data_list)
```

### Individual Components

```python
# Process CSV files
from src.temperature_processor import TemperatureDataProcessor
processor = TemperatureDataProcessor()
data = processor.process_zip_file("data/sensors.zip")

# Create visualizations
from src.visualizer import TemperatureVisualizer
visualizer = TemperatureVisualizer()
visualizer.create_temperature_timeline(data[0])

# Export to Excel
from src.excel_exporter import ExcelExporter
exporter = ExcelExporter()
exporter.export_device_data(data[0])
```

## Generated Reports

The application generates the following outputs in the `output/` directory:

### Visualizations
- `{device_name}_timeline.png`: Individual device timeline plots
- `multi_device_temperature_comparison.png`: Temperature comparison across devices
- `multi_device_humidity_comparison.png`: Humidity comparison across devices
- `multi_device_battery_mv_comparison.png`: Battery level comparison across devices
- `statistics_heatmap.png`: Statistical overview heatmap

### Excel Reports
- `{device_name}_data.xlsx`: Individual device data with statistics and hourly averages
- `all_devices_data.xlsx`: Combined report for all devices

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_temperature_processor.py

# Run with verbose output
pytest -v
```

## Project Structure

```
TemperatureMonitoring/
├── src/
│   ├── main.py                 # Main application entry point
│   ├── temperature_processor.py # Core CSV/ZIP processing
│   ├── visualizer.py           # Data visualization
│   └── excel_exporter.py       # Excel report generation
├── tests/
│   ├── test_temperature_processor.py
│   ├── test_visualizer.py
│   └── test_excel_exporter.py
├── data/                       # Input data directory
├── output/                     # Generated reports directory
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project configuration
├── specification.md           # Project specifications
└── README.md                  # This file
```

## Dependencies

- **pandas**: Data manipulation and analysis
- **matplotlib**: Basic plotting and visualization
- **seaborn**: Statistical data visualization
- **openpyxl**: Excel file creation and formatting
- **pytest**: Testing framework
- **pytest-cov**: Test coverage reporting
- **numpy**: Numerical computing support

## Development

### Adding New Features

1. Create new modules in the `src/` directory
2. Add corresponding tests in the `tests/` directory
3. Update requirements.txt if new dependencies are needed
4. Update this README with usage examples

### Code Style

- Follow PEP 8 standards
- Use type hints for all functions
- Include comprehensive docstrings
- Write testable, modular code

## Logging

The application logs to both console and file (`temperature_monitoring.log`):

- **INFO**: Normal operation messages
- **WARNING**: Non-fatal issues (e.g., skipped invalid data lines)
- **ERROR**: Serious problems that prevent processing
- **DEBUG**: Detailed debugging information

## Error Handling

The application handles common error scenarios:

- Invalid ZIP files
- Malformed CSV data
- Missing files
- Empty datasets
- File permission issues

## License

This project is provided as-is for temperature monitoring data analysis purposes.

## Support

For questions or issues, please refer to the specification.md file or check the log files for detailed error information.
