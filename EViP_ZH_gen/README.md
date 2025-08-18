# LogAnalyzer - Log File Analysis Application

This is a complete C# .NET 8 solution for analyzing log files. The project was developed as part of the EViP (Programming Fundamentals) course examination, demonstrating C# syntax, IEnumerable, LINQ, regular expressions, and xUnit testing.

## Project Structure

The solution consists of three projects:

- **LogAnalyzer.Core** - Class Library containing the business logic
- **LogAnalyzer.Console** - Console Application providing an interactive user interface  
- **LogAnalyzer.Tests** - xUnit Test Project with comprehensive unit tests

## Features

### Core Functionality
- Read and parse log files with format validation
- Filter log entries by level (INFO, WARNING, ERROR, DEBUG)
- Count error entries and calculate statistics
- Analyze user activity patterns
- Extract email addresses and IP addresses using regex patterns
- Case-insensitive operations throughout

### Log File Format

The application expects log files in the following format:
```
[YYYY-MM-DD HH:mm:ss] [LEVEL] [USER] Message
```

**Example:**
```
[2024-01-15 10:30:45] [ERROR] [john.doe] Failed login attempt from 192.168.1.100
[2024-01-15 10:31:20] [INFO] [jane.smith] User registered with email john.doe@company.com
[2024-01-15 10:32:10] [WARNING] [admin] Suspicious activity detected from 10.0.0.5
```

**Valid Log Levels:** INFO, WARNING, ERROR, DEBUG

## Running the Application

### Console Application
```bash
cd LogAnalyzer.Console
dotnet run
```

Or from the solution root:
```bash
dotnet run --project LogAnalyzer.Console
```

### Running Tests
```bash
dotnet test
```

### Building the Solution
```bash
dotnet build
```

## Usage Guide

1. **Start the Application:** Run the console application
2. **Load Log File:** Choose option 1 and enter the path to your log file (or press Enter to use sample.log)
3. **Analyze Data:** Use the various menu options to analyze the loaded data:
   - View all entries
   - Filter by log level
   - Count errors
   - See user activity summary
   - Extract email addresses
   - Extract IP addresses

## Sample Data

The project includes `sample.log` with 24 log entries containing:
- Different log levels (INFO, WARNING, ERROR, DEBUG)
- Multiple users (john.doe, jane.smith, admin, bob.wilson, system, etc.)
- Email addresses in messages
- IP addresses in messages
- Some invalid format lines for testing

## Regular Expressions Used

### Log Format Validation
```regex
^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] \[(INFO|WARNING|ERROR|DEBUG)\] \[[^\]]+\] .+$
```

### Email Address Extraction
```regex
\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b
```

### IPv4 Address Extraction
```regex
\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b
```

## Architecture & Design Patterns

### LINQ Usage
- **Filtering:** `Where()` for log level filtering
- **Counting:** `Count()` for error counting
- **Grouping:** `GroupBy()` and `ToDictionary()` for user activity analysis
- **Data extraction:** `SelectMany()` and `Distinct()` for email/IP extraction
- **Sorting:** `OrderBy()` and `OrderByDescending()` for result presentation

### Error Handling
- File not found exceptions
- Invalid log format handling
- Robust parsing with graceful degradation
- Comprehensive input validation

### Testing Strategy
- **Unit Tests:** 14 comprehensive test cases covering all major functionality
- **Test Categories:**
  - File reading and validation
  - Format validation (valid and invalid cases)
  - Filtering operations
  - Data extraction and regex patterns
  - Error counting and user analysis
  - Edge cases and error conditions

## Technical Implementation

### Key Classes

**LogEntry Model:**
```csharp
public class LogEntry
{
    public string Timestamp { get; set; }
    public string Level { get; set; }
    public string Message { get; set; }
    public string User { get; set; }
}
```

**LogAnalyzerService Methods:**
- `ReadLogFile(string filePath)` - Read and parse log files
- `IsValidLogFormat(string logLine)` - Validate log entry format
- `FilterByLevel(IEnumerable<LogEntry> entries, string level)` - Filter by log level
- `CountErrorEntries(IEnumerable<LogEntry> entries)` - Count ERROR entries
- `GetUserActivitySummary(IEnumerable<LogEntry> entries)` - User activity statistics
- `ExtractEmailAddresses(IEnumerable<LogEntry> entries)` - Extract email addresses
- `ExtractIPAddresses(IEnumerable<LogEntry> entries)` - Extract IP addresses

## Requirements Fulfilled

✅ **Project Structure:** 3 projects with proper references  
✅ **Log Entry Model:** Complete with all required properties  
✅ **File Reading:** Robust file I/O with error handling  
✅ **Format Validation:** Regex-based validation  
✅ **LINQ Operations:** Filtering, counting, grouping, data extraction  
✅ **Regular Expressions:** Email and IP extraction patterns  
✅ **Console Interface:** Interactive menu-driven application  
✅ **Unit Testing:** Comprehensive test coverage with xUnit  
✅ **Sample Data:** 20+ log entries with various scenarios  
✅ **Documentation:** Complete README with usage instructions  

## Development Notes

- Built with .NET 8
- Uses C# 12 features where appropriate
- Follows clean code principles
- Comprehensive error handling
- Case-insensitive string comparisons
- Extensible architecture for future enhancements

## Testing Coverage

The test suite includes:
- Valid and invalid file reading scenarios
- Format validation edge cases
- LINQ operation correctness
- Regex pattern accuracy
- Error handling verification
- Data integrity checks

All tests pass successfully, ensuring reliable functionality across all features.
