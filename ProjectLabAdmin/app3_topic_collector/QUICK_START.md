# Topic Collector - Quick Start Guide

## Overview
The BME AUT Topic Collector has been successfully created in the `app3_topic_collector` folder. It's designed to scrape course topic information from the BME Department of Automation and Applied Informatics website.

## Files Created
```
app3_topic_collector/
├── __init__.py                 # Package initialization
├── config.py                   # Configuration settings
├── topic_scraper.py           # Main scraping logic
├── main.py                    # Command-line interface
├── test_topic_collector.py    # Test suite
├── demo.py                    # Demo script
├── config_example.py          # Example configuration
└── README.md                  # Detailed documentation
```

## How to Run

### Option 1: Using the batch file (Recommended for Windows)
```bash
run_topic_collector.bat
```

### Option 2: Using VS Code task
- Press `Ctrl+Shift+P`
- Type "Tasks: Run Task"
- Select "Run Topic Collector"

### Option 3: Direct command line
```bash
cd app3_topic_collector
E:/_learning_ai/ProjectLabAdmin/.venv/Scripts/python.exe main.py
```

### Command Line Options
```bash
# Basic usage
python main.py

# Run with verbose logging
python main.py --verbose

# Run in headless mode (no browser window)
python main.py --headless

# Save to custom filename
python main.py --output my_topics.json

# Combine options
python main.py --headless --verbose --output results.json
```

## What It Does

The application:
1. **Scrapes 11 different BME AUT pages** for course topics
2. **Extracts comprehensive information** for each topic:
   - Title and URL
   - External partner information
   - Student limits
   - Advisor names
   - Associated course codes and names
3. **Saves everything to JSON format** in the `data/topics.json` file

## Test Results ✅

The application has been tested and verified:
- ✅ All 8 unit tests passed
- ✅ Found 93 topics from the first test category
- ✅ Parsing functions work correctly
- ✅ Configuration is valid
- ✅ Output format matches specification

## Expected Output

The application will create a `data/topics.json` file with structure like:
```json
[
  {
    "title": "Topic Title",
    "url": "https://www.aut.bme.hu/Task/...",
    "is_external": true,
    "external_partner": "Company Name or null",
    "student_limit": 2,
    "advisors": ["Dr. Advisor Name 1", "Dr. Advisor Name 2"],
    "courses": [
      {
        "course_code": "BMEVIAUAL01",
        "course_name": "Full Course Name"
      }
    ],
    "source_category_url": "https://www.aut.bme.hu/Education/BScInfo/Onlab"
  }
]
```

## Technical Notes

- **Uses Selenium** for dynamic content (course dropdowns)
- **Uses BeautifulSoup** for static HTML parsing
- **Automatically manages ChromeDriver** via webdriver-manager
- **Robust error handling** continues on individual failures
- **Comprehensive logging** for debugging and monitoring

## Performance

Based on initial testing:
- Found 93 topics in the first category alone
- With 11 categories total, expect 500-1000+ topics
- Full run may take 10-30 minutes depending on website response times
- Each topic requires individual page visits for detailed information

## Next Steps

1. **Run a test**: Use `python demo.py` to test basic functionality
2. **Full scrape**: Use `python main.py` when ready for complete data collection
3. **Monitor logs**: Check the generated log files for any issues
4. **Validate results**: The application includes built-in output validation

## Troubleshooting

- **Chrome not found**: Install Google Chrome browser
- **Slow performance**: Use `--headless` mode or increase wait times in config.py
- **Network issues**: Check internet connection and website availability
- **Missing data**: Check logs for specific parsing errors

The application is ready to use! Let me know if you need any modifications or have questions about the functionality.
