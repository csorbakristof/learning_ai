using Xunit;
using LogAnalyzer.Core;
using System.Collections.Generic;

namespace LogAnalyzer.Tests;

/// <summary>
/// Tests specifically targeting boundary conditions and edge cases to catch surviving mutations
/// </summary>
public class BoundaryConditionTests
{
    private readonly LogAnalyzerService _service;

    public BoundaryConditionTests()
    {
        _service = new LogAnalyzerService();
    }

    #region Array/Collection Boundary Tests

    [Fact]
    public void FilterByLevel_EmptyCollection_ReturnsEmpty()
    {
        // Arrange
        var emptyEntries = new List<LogEntry>();

        // Act
        var result = _service.FilterByLevel(emptyEntries, "ERROR");

        // Assert
        Assert.Empty(result);
    }

    [Fact]
    public void FilterByLevel_SingleEntry_ReturnsCorrectly()
    {
        // Arrange
        var singleEntry = new List<LogEntry>
        {
            new LogEntry { Level = "ERROR", User = "test", Message = "test", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var result = _service.FilterByLevel(singleEntry, "ERROR");

        // Assert
        Assert.Single(result);
        Assert.Equal("ERROR", result.First().Level);
    }

    [Fact]
    public void CountErrorEntries_ZeroErrors_ReturnsZero()
    {
        // Arrange
        var entriesWithoutErrors = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "test", Message = "test", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "WARNING", User = "test", Message = "test", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "DEBUG", User = "test", Message = "test", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act
        var count = _service.CountErrorEntries(entriesWithoutErrors);

        // Assert
        Assert.Equal(0, count);
    }

    [Fact]
    public void CountErrorEntries_OnlyErrors_ReturnsCorrectCount()
    {
        // Arrange
        var onlyErrors = new List<LogEntry>
        {
            new LogEntry { Level = "ERROR", User = "test1", Message = "error1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "ERROR", User = "test2", Message = "error2", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "ERROR", User = "test3", Message = "error3", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act
        var count = _service.CountErrorEntries(onlyErrors);

        // Assert
        Assert.Equal(3, count);
    }

    #endregion

    #region String Comparison Edge Cases

    [Theory]
    [InlineData("ERROR", "error")]
    [InlineData("Error", "ERROR")]
    [InlineData("ErRoR", "error")]
    public void FilterByLevel_CaseInsensitive_WorksCorrectly(string entryLevel, string filterLevel)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = entryLevel, User = "test", Message = "test", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var result = _service.FilterByLevel(entries, filterLevel);

        // Assert
        Assert.Single(result);
    }

    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    [InlineData("\t")]
    [InlineData("\n")]
    public void FilterByLevel_WhitespaceLevel_ReturnsEmpty(string level)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "ERROR", User = "test", Message = "test", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var result = _service.FilterByLevel(entries, level);

        // Assert
        Assert.Empty(result);
    }

    #endregion

    #region Regex Boundary Tests

    [Theory]
    [InlineData("192.168.1.255")] // Max valid IP octet
    [InlineData("0.0.0.0")]       // Min valid IP
    [InlineData("255.255.255.255")] // Max valid IP
    [InlineData("127.0.0.1")]     // Localhost
    public void ExtractIPAddresses_BoundaryValidIPs_ExtractsCorrectly(string ip)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "test", Message = $"Server IP is {ip}", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var result = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Single(result);
        Assert.Contains(ip, result);
    }

    [Theory]
    [InlineData("256.1.1.1")]     // First octet too high
    [InlineData("1.256.1.1")]     // Second octet too high
    [InlineData("1.1.256.1")]     // Third octet too high
    [InlineData("1.1.1.256")]     // Fourth octet too high
    [InlineData("192.168.1")]     // Too few octets
    [InlineData("192.168.1.1.1")] // Too many octets
    public void ExtractIPAddresses_BoundaryInvalidIPs_DoesNotExtract(string invalidIP)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "test", Message = $"Invalid IP: {invalidIP}", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var result = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Empty(result);
    }

    #endregion

    #region Logic Operator Edge Cases

    [Fact]
    public void GetUserActivitySummary_MixedValidAndInvalidUsers_CountsOnlyValid()
    {
        // Arrange - Test both valid AND invalid users together
        var mixedEntries = new List<LogEntry>
        {
            new LogEntry { User = "valid.user", Level = "INFO", Message = "msg1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { User = "", Level = "INFO", Message = "msg2", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { User = "valid.user", Level = "INFO", Message = "msg3", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { User = null, Level = "INFO", Message = "msg4", Timestamp = "2024-01-01 10:03:00" },
            new LogEntry { User = "another.user", Level = "INFO", Message = "msg5", Timestamp = "2024-01-01 10:04:00" }
        };

        // Act
        var result = _service.GetUserActivitySummary(mixedEntries);

        // Assert
        Assert.Equal(2, result.Count); // Only valid users counted
        Assert.Equal(2, result["valid.user"]); // User appears twice
        Assert.Equal(1, result["another.user"]); // User appears once
        Assert.False(result.ContainsKey("")); // Empty user not included
        // Don't check for null key directly as it throws exception
    }

    #endregion

    #region Timestamp Edge Cases

    [Theory]
    [InlineData("2024-01-01 00:00:00")] // Midnight
    [InlineData("2024-12-31 23:59:59")] // Last second of year
    [InlineData("2024-02-29 12:00:00")] // Leap year
    public void IsValidLogFormat_BoundaryTimestamps_ValidatesCorrectly(string timestamp)
    {
        // Arrange
        var logLine = $"[{timestamp}] [INFO] [user] Test message";

        // Act
        var result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.True(result);
    }

    [Theory]
    [InlineData("2024-01-01 24:00:00")] // Invalid hour
    [InlineData("2024-01-01 12:60:00")] // Invalid minute
    [InlineData("2024-01-01 12:00:60")] // Invalid second
    [InlineData("2024-02-30 12:00:00")] // Invalid date
    [InlineData("2023-02-29 12:00:00")] // Non-leap year
    public void IsValidLogFormat_InvalidBoundaryTimestamps_ReturnsFalse(string invalidTimestamp)
    {
        // Arrange
        var logLine = $"[{invalidTimestamp}] [INFO] [user] Test message";

        // Act
        var result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.False(result);
    }

    #endregion
}
