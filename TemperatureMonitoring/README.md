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

1. **Clone or download** this project to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create data directories** (if not already present):
   ```bash
   mkdir -p data output
   ```

## Usage

### Command Line Interface

```bash
# Process a ZIP file with full reports
python src/main.py data/temperature_data.zip

# Process without generating reports
python src/main.py data/temperature_data.zip --no-reports

# Set logging level
python src/main.py data/temperature_data.zip --log-level DEBUG
```

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
