# BME AUT Topic Collector

A Python application that scrapes course topic information from the BME Department of Automation and Applied Informatics website using Selenium and BeautifulSoup.

## Overview

This application automatically retrieves and catalogs university course topics from various BME AUT web pages, extracting detailed information for each topic and storing it in a structured JSON format.

## Authentication Required

**Important**: This application requires user authentication to access course dropdown information. The course association dropdowns (`ddlCourseGroup` and `ddlCourse`) are only visible to logged-in users.

### Login Process
1. The application will open a browser window to the BME AUT website
2. Click "Bejelentkezés" (Login) in the top menu
3. Enter your BME credentials and log in
4. Return to the terminal and press ENTER to continue
5. The application will then proceed with scraping

### Headless Mode Limitation
- **Cannot use `--headless` mode** for full functionality
- Headless mode prevents user login interaction
- Course information will be missing without authentication
- Use headless mode only for testing basic topic extraction

- **Multi-source scraping**: Collects topics from BSc and MSc programs across different engineering disciplines
- **Dynamic content handling**: Uses Selenium to handle JavaScript-generated content and dropdown interactions
- **Comprehensive data extraction**: 
  - Topic titles and URLs
  - External partner information
  - Student limits
  - Advisor lists
  - Course associations with codes and names
- **Robust error handling**: Gracefully handles network issues, missing elements, and parsing errors
- **Flexible output**: Saves data in JSON format with validation
- **Logging**: Comprehensive logging for debugging and monitoring

## Data Sources

The application scrapes topics from the following BME AUT pages:

### BSc Level
- **IT Engineer (Mérnök Informatikus)**
  - Project Laboratory: `https://www.aut.bme.hu/Education/BScInfo/Onlab`
  - Thesis Project: `https://www.aut.bme.hu/Education/BScInfo/Szakdolgozat`
- **Electrical Engineer (Villamosmérnök)**
  - Project Laboratory: `https://www.aut.bme.hu/Education/BScVillany/Onlab`
  - Thesis Project: `https://www.aut.bme.hu/Education/BScVillany/Szakdolgozat`
- **Mechatronics Engineer (Mechatronikai mérnök)**
  - Thesis Project: `https://www.aut.bme.hu/Education/BScMechatronika/Szakdolgozat`

### MSc Level
- **IT Engineer (Mérnök Informatikus)**
  - Project Laboratory: `https://www.aut.bme.hu/Education/MScInfo/Onlab`
  - Thesis Project: `https://www.aut.bme.hu/Education/MScInfo/Diploma`
- **Electrical Engineer (Villamosmérnök)**
  - Project Laboratory: `https://www.aut.bme.hu/Education/MScVillany/Onlab`
  - Thesis Project: `https://www.aut.bme.hu/Education/MScVillany/Diploma`
- **Mechatronics Engineer (Mechatronikai mérnök)**
  - Project Task: `https://www.aut.bme.hu/Education/MScMechatronika/Onlab`
  - Thesis Project: `https://www.aut.bme.hu/Education/MScMechatronika/Diploma`

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required dependencies (they should already be available in the project):
   ```bash
   pip install selenium requests beautifulsoup4 lxml webdriver-manager
   ```
3. Chrome browser should be installed (ChromeDriver will be managed automatically)

## Usage

### Basic Usage

Run the application with default settings (authentication required):
```bash
python main.py
```

**Note**: The application will open a browser window and wait for you to log in before continuing.

### Command Line Options

```bash
# Run with verbose logging (recommended)
python main.py --verbose

# Save to custom filename
python main.py --output my_topics.json

# Run in headless mode (LIMITED - no course information)
python main.py --headless

# Combine options (authentication still required unless headless)
python main.py --verbose --output results.json
```

### Command Line Options

```bash
# Run with verbose logging
python main.py --verbose

# Save to custom filename
python main.py --output my_topics.json

# Run in headless mode (no browser window)
python main.py --headless

# Validate an existing JSON file
python main.py --validate-only path/to/topics.json

# Combine options
python main.py --headless --verbose --output results.json
```

### Output

The application generates a JSON file (`topics.json` by default) in the `../data/` directory containing an array of topic objects with the following structure:

```json
[
  {
    "title": "Topic Title",
    "url": "https://www.aut.bme.hu/Task/...",
    "is_external": true,
    "external_partner": "Company Name or null",
    "student_limit": 2,
    "advisors": [
      "Advisor Name 1",
      "Advisor Name 2"
    ],
    "courses": [
      {
        "course_code": "BMEVIAUAL01",
        "course_name": "Course Name as seen in dropdown"
      }
    ],
    "source_category_url": "https://www.aut.bme.hu/Education/BScInfo/Onlab"
  }
]
```

## Configuration

The application can be configured by modifying `config.py`:

- **CATEGORY_URLS**: URLs to scrape
- **SELENIUM_CONFIG**: WebDriver settings (headless mode, timeouts, window size)
- **OUTPUT_DIR**: Output directory for JSON files
- **Wait times**: Delays for page loading and dropdown interactions

## Error Handling

The application includes robust error handling for:

- **Network issues**: HTTP errors, timeouts, connection problems
- **Missing elements**: Pages without expected content or structure
- **Data parsing errors**: Invalid or unexpected data formats
- **WebDriver issues**: Browser automation problems

Errors are logged with details and the application continues processing other items when possible.

## Logging

The application creates detailed logs including:
- Progress information
- Error messages with context
- Performance metrics
- Validation results

Logs are written to both console and log files with timestamps.

## Technical Details

### Architecture
- **topic_scraper.py**: Main scraping logic and data extraction
- **config.py**: Configuration constants and settings
- **main.py**: Command-line interface and application entry point

### Dependencies
- **Selenium**: Browser automation for dynamic content
- **BeautifulSoup**: HTML parsing for static content
- **Requests**: HTTP client for initial page fetching
- **WebDriver Manager**: Automatic ChromeDriver management

### Process Flow
1. Initialize WebDriver with Chrome
2. For each category URL:
   - Fetch the category page using requests
   - Parse HTML to find topic links under "Kiírt témák" heading
   - For each topic link:
     - Navigate using Selenium to handle dynamic content
     - Extract basic information (title, external partner, student limit, advisors)
     - Interact with dropdowns to extract course information
     - Compile data into structured format
3. Save all collected data to JSON file
4. Validate output and display statistics

## Troubleshooting

### Common Issues

1. **ChromeDriver issues**: The application uses webdriver-manager to automatically handle ChromeDriver installation
2. **Slow performance**: Increase wait times in config.py if pages load slowly
3. **Missing data**: Check logs for specific parsing errors on individual pages
4. **Network timeouts**: Increase timeout values in SELENIUM_CONFIG

### Debug Mode
Run with `--verbose` flag to see detailed logging information for troubleshooting.

## Contributing

When modifying the scraper:
1. Update the corresponding configuration in `config.py`
2. Test with a small subset of URLs first
3. Ensure error handling covers new scenarios
4. Update this README if adding new features
