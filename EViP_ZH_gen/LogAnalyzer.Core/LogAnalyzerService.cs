using System.Text.RegularExpressions;

namespace LogAnalyzer.Core;

/// <summary>
/// Service class for analyzing log files and extracting information
/// </summary>
public class LogAnalyzerService
{
    /// <summary>
    /// Reads a log file and returns a list of log entries
    /// </summary>
    /// <param name="filePath">Path to the log file</param>
    /// <returns>List of parsed log entries</returns>
    public List<LogEntry> ReadLogFile(string filePath)
    {
        var entries = new List<LogEntry>();
        
        try
        {
            var lines = File.ReadAllLines(filePath);
            
            foreach (var line in lines)
            {
                if (IsValidLogFormat(line))
                {
                    var entry = ParseLogLine(line);
                    if (entry != null)
                    {
                        entries.Add(entry);
                    }
                }
            }
        }
        catch (FileNotFoundException)
        {
            throw new FileNotFoundException($"Log file not found: {filePath}");
        }
        catch (Exception ex)
        {
            throw new InvalidOperationException($"Error reading log file: {ex.Message}", ex);
        }
        
        return entries;
    }

    /// <summary>
    /// Filters log entries by the specified level
    /// </summary>
    /// <param name="entries">Log entries to filter</param>
    /// <param name="level">Log level to filter by</param>
    /// <returns>Filtered log entries</returns>
    public IEnumerable<LogEntry> FilterByLevel(IEnumerable<LogEntry> entries, string level)
    {
        return entries.Where(entry => 
            string.Equals(entry.Level, level, StringComparison.OrdinalIgnoreCase));
    }

    /// <summary>
    /// Counts the number of ERROR level entries
    /// </summary>
    /// <param name="entries">Log entries to analyze</param>
    /// <returns>Number of ERROR entries</returns>
    public int CountErrorEntries(IEnumerable<LogEntry> entries)
    {
        return entries.Count(entry => 
            string.Equals(entry.Level, "ERROR", StringComparison.OrdinalIgnoreCase));
    }

    /// <summary>
    /// Gets a summary of user activity (user name and their entry count)
    /// </summary>
    /// <param name="entries">Log entries to analyze</param>
    /// <returns>Dictionary with user names as keys and entry counts as values</returns>
    public Dictionary<string, int> GetUserActivitySummary(IEnumerable<LogEntry> entries)
    {
        return entries
            .Where(entry => !string.IsNullOrEmpty(entry.User))
            .GroupBy(entry => entry.User)
            .ToDictionary(group => group.Key, group => group.Count());
    }

    /// <summary>
    /// Validates if a log line matches the expected format
    /// </summary>
    /// <param name="logLine">Log line to validate</param>
    /// <returns>True if the format is valid, false otherwise</returns>
    public bool IsValidLogFormat(string logLine)
    {
        // Pattern: [YYYY-MM-DD HH:mm:ss] [LEVEL] [USER] Message
        // The regex pattern checks for:
        // - Square brackets with date and time
        // - Square brackets with log level (INFO, WARNING, ERROR, DEBUG)
        // - Square brackets with user name
        // - Message text
        var pattern = @"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] \[(INFO|WARNING|ERROR|DEBUG)\] \[[^\]]+\] .+$";
        return Regex.IsMatch(logLine, pattern);
    }

    /// <summary>
    /// Extracts unique email addresses from log entries
    /// </summary>
    /// <param name="entries">Log entries to search</param>
    /// <returns>List of unique email addresses</returns>
    public List<string> ExtractEmailAddresses(IEnumerable<LogEntry> entries)
    {
        // Email pattern: characters + @ + domain + . + extension
        var emailPattern = @"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b";
        
        return entries
            .SelectMany(entry => Regex.Matches(entry.Message, emailPattern))
            .Select(match => match.Value)
            .Distinct()
            .ToList();
    }

    /// <summary>
    /// Extracts unique IPv4 addresses from log entries
    /// </summary>
    /// <param name="entries">Log entries to search</param>
    /// <returns>List of unique IP addresses</returns>
    public List<string> ExtractIPAddresses(IEnumerable<LogEntry> entries)
    {
        // IPv4 pattern: 4 numbers (0-255) separated by dots
        var ipPattern = @"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b";
        
        return entries
            .SelectMany(entry => Regex.Matches(entry.Message, ipPattern))
            .Select(match => match.Value)
            .Distinct()
            .ToList();
    }

    /// <summary>
    /// Parses a single log line into a LogEntry object
    /// </summary>
    /// <param name="logLine">Log line to parse</param>
    /// <returns>Parsed LogEntry or null if parsing fails</returns>
    private LogEntry? ParseLogLine(string logLine)
    {
        try
        {
            // Pattern to extract parts: [timestamp] [level] [user] message
            var pattern = @"^\[([^\]]+)\] \[([^\]]+)\] \[([^\]]+)\] (.+)$";
            var match = Regex.Match(logLine, pattern);
            
            if (match.Success)
            {
                return new LogEntry
                {
                    Timestamp = match.Groups[1].Value,
                    Level = match.Groups[2].Value,
                    User = match.Groups[3].Value,
                    Message = match.Groups[4].Value
                };
            }
        }
        catch (Exception)
        {
            // Return null if parsing fails
        }
        
        return null;
    }
}