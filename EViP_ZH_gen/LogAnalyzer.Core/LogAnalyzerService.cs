using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

namespace LogAnalyzer.Core;

/// <summary>
/// Service for analyzing log files and extracting information
/// </summary>
public class LogAnalyzerService
{
    /// <summary>
    /// Reads a log file and returns valid log entries
    /// </summary>
    /// <param name="filePath">Path to the log file</param>
    /// <returns>List of valid log entries</returns>
    public List<LogEntry> ReadLogFile(string filePath)
    {
        if (!File.Exists(filePath))
        {
            throw new FileNotFoundException($"Log file not found: {filePath}");
        }

        var logEntries = new List<LogEntry>();
        var lines = File.ReadAllLines(filePath);

        foreach (var line in lines)
        {
            if (IsValidLogFormat(line))
            {
                var entry = ParseLogLine(line);
                if (entry != null)
                {
                    logEntries.Add(entry);
                }
            }
        }

        return logEntries;
    }

    /// <summary>
    /// Validates if a log line matches the expected format
    /// </summary>
    /// <param name="logLine">Log line to validate</param>
    /// <returns>True if valid format, false otherwise</returns>
    public bool IsValidLogFormat(string logLine)
    {
        if (string.IsNullOrEmpty(logLine))
            return false;

        // Pattern: [YYYY-MM-DD HH:mm:ss] [LEVEL] [USER] Message
        // The regex pattern checks for:
        // - Square brackets with date and time
        // - Square brackets with log level (INFO, WARNING, ERROR, DEBUG)
        // - Square brackets with user name
        // - Message text
        var pattern = @"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(INFO|WARNING|ERROR|DEBUG)\] \[([^\]]+)\] (.+)$";
        
        var match = Regex.Match(logLine, pattern);
        if (!match.Success)
            return false;

        // Validate the timestamp format more strictly
        string timestampStr = match.Groups[1].Value;
        return DateTime.TryParseExact(timestampStr, "yyyy-MM-dd HH:mm:ss", null, DateTimeStyles.None, out _);
    }

    /// <summary>
    /// Filters log entries by level
    /// </summary>
    /// <param name="entries">Log entries to filter</param>
    /// <param name="level">Level to filter by (case-insensitive)</param>
    /// <returns>Filtered log entries</returns>
    public IEnumerable<LogEntry> FilterByLevel(IEnumerable<LogEntry> entries, string level)
    {
        if (string.IsNullOrWhiteSpace(level))
            return Enumerable.Empty<LogEntry>();

        return entries.Where(entry => string.Equals(entry.Level, level, StringComparison.OrdinalIgnoreCase));
    }

    /// <summary>
    /// Counts the number of error entries
    /// </summary>
    /// <param name="entries">Log entries to count</param>
    /// <returns>Number of error entries</returns>
    public int CountErrorEntries(IEnumerable<LogEntry> entries)
    {
        if (entries == null)
            throw new ArgumentNullException(nameof(entries));

        return entries.Count(entry => string.Equals(entry.Level, "ERROR", StringComparison.OrdinalIgnoreCase));
    }

    /// <summary>
    /// Gets user activity summary (count of entries per user)
    /// </summary>
    /// <param name="entries">Log entries to analyze</param>
    /// <returns>Dictionary with user names as keys and entry counts as values</returns>
    public Dictionary<string, int> GetUserActivitySummary(IEnumerable<LogEntry> entries)
    {
        if (entries == null)
            throw new ArgumentNullException(nameof(entries));

        return entries
            .Where(entry => !string.IsNullOrWhiteSpace(entry.User))
            .GroupBy(entry => entry.User)
            .ToDictionary(group => group.Key, group => group.Count());
    }

    /// <summary>
    /// Extracts unique email addresses from log entries
    /// </summary>
    /// <param name="entries">Log entries to search</param>
    /// <returns>List of unique email addresses</returns>
    public List<string> ExtractEmailAddresses(IEnumerable<LogEntry> entries)
    {
        if (entries == null)
            throw new ArgumentNullException(nameof(entries));

        // More strict email pattern that excludes common invalid cases
        var emailPattern = @"\b[A-Za-z0-9][A-Za-z0-9._%+-]*[A-Za-z0-9]@[A-Za-z0-9][A-Za-z0-9.-]*[A-Za-z0-9]\.[A-Za-z]{2,}\b";
        
        var emails = new HashSet<string>();
        
        foreach (var entry in entries)
        {
            if (string.IsNullOrEmpty(entry.Message))
                continue;
                
            var matches = Regex.Matches(entry.Message, emailPattern);
            foreach (Match match in matches)
            {
                string email = match.Value;
                // Additional validation to exclude emails with consecutive dots
                if (!email.Contains("..") && IsValidEmailStructure(email))
                {
                    emails.Add(email);
                }
            }
        }
        
        return emails.ToList();
    }

    private bool IsValidEmailStructure(string email)
    {
        // Additional checks for email validity
        if (email.StartsWith(".") || email.EndsWith("."))
            return false;
        if (email.StartsWith("@") || email.EndsWith("@"))
            return false;
        if (email.Count(c => c == '@') != 1)
            return false;
        
        var parts = email.Split('@');
        if (parts.Length != 2)
            return false;
            
        // Check local part (before @)
        string localPart = parts[0];
        if (string.IsNullOrEmpty(localPart) || localPart.StartsWith(".") || localPart.EndsWith("."))
            return false;
            
        // Check domain part (after @)
        string domainPart = parts[1];
        if (string.IsNullOrEmpty(domainPart) || domainPart.StartsWith(".") || domainPart.EndsWith(".") || !domainPart.Contains("."))
            return false;
            
        return true;
    }

    /// <summary>
    /// Extracts unique IPv4 addresses from log entries
    /// </summary>
    /// <param name="entries">Log entries to search</param>
    /// <returns>List of unique IP addresses</returns>
    public List<string> ExtractIPAddresses(IEnumerable<LogEntry> entries)
    {
        if (entries == null)
            throw new ArgumentNullException(nameof(entries));

        // IPv4 pattern: 4 numbers (0-255) separated by dots, with word boundaries
        var ipPattern = @"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b";
        
        var ips = new HashSet<string>();
        
        foreach (var entry in entries)
        {
            if (string.IsNullOrEmpty(entry.Message))
                continue;
                
            var matches = Regex.Matches(entry.Message, ipPattern);
            foreach (Match match in matches)
            {
                string ip = match.Value;
                // Additional validation to ensure it's a valid IP address
                if (IsValidIPAddress(ip))
                {
                    ips.Add(ip);
                }
            }
        }
        
        return ips.ToList();
    }

    private bool IsValidIPAddress(string ip)
    {
        // Ensure we have exactly 4 parts
        var parts = ip.Split('.');
        if (parts.Length != 4)
            return false;

        // Validate each part is a valid number 0-255
        foreach (var part in parts)
        {
            if (!int.TryParse(part, out int num) || num < 0 || num > 255)
                return false;
        }

        return true;
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
            
            return null;
        }
        catch
        {
            return null;
        }
    }
}
