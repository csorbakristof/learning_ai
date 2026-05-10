namespace LogAnalyzer.Core;

/// <summary>
/// Represents a single log entry with timestamp, level, message and user information
/// </summary>
public class LogEntry
{
    /// <summary>
    /// The timestamp of the log entry in text format
    /// </summary>
    public string Timestamp { get; set; } = string.Empty;

    /// <summary>
    /// The log level (INFO, WARNING, ERROR, DEBUG)
    /// </summary>
    public string Level { get; set; } = string.Empty;

    /// <summary>
    /// The log message content
    /// </summary>
    public string Message { get; set; } = string.Empty;

    /// <summary>
    /// The user name (optional)
    /// </summary>
    public string User { get; set; } = string.Empty;
}