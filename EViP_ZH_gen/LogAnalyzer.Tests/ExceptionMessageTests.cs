using Xunit;
using LogAnalyzer.Core;
using System;
using System.Collections.Generic;
using System.IO;

namespace LogAnalyzer.Tests;

/// <summary>
/// Tests specifically designed to catch exception message and statement mutations
/// </summary>
public class ExceptionMessageTests
{
    private readonly LogAnalyzerService _service;

    public ExceptionMessageTests()
    {
        _service = new LogAnalyzerService();
    }

    [Fact]
    public void ReadLogFile_FileNotFound_ThrowsWithSpecificMessage()
    {
        // Arrange
        string nonExistentPath = "C:\\definitely\\does\\not\\exist\\file.log";

        // Act & Assert - This will catch string mutations in exception message
        var exception = Assert.Throws<FileNotFoundException>(() => _service.ReadLogFile(nonExistentPath));
        Assert.Contains("Log file not found:", exception.Message);
        Assert.Contains(nonExistentPath, exception.Message);
        
        // Ensure it's not just any FileNotFoundException
        Assert.NotEqual("", exception.Message);
        Assert.NotNull(exception.Message);
    }

    [Fact]
    public void CountErrorEntries_ValidInput_MustReturnNonNegativeCount()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "ERROR", User = "user1", Message = "msg1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user2", Message = "msg2", Timestamp = "2024-01-01 10:01:00" }
        };

        // Act
        var result = _service.CountErrorEntries(entries);

        // Assert - This catches statement removal mutations
        Assert.True(result >= 0, "Count must be non-negative");
        Assert.Equal(1, result); // Exact count verification
        
        // Additional checks to catch various mutations
        Assert.NotEqual(-1, result);
        Assert.NotEqual(int.MaxValue, result);
    }

    [Fact]
    public void GetUserActivitySummary_ValidInput_MustReturnDictionary()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "testuser", Message = "msg", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var result = _service.GetUserActivitySummary(entries);

        // Assert - This catches statement removal mutations
        Assert.NotNull(result);
        Assert.IsType<Dictionary<string, int>>(result);
        Assert.Single(result);
        Assert.True(result.ContainsKey("testuser"));
        Assert.Equal(1, result["testuser"]);
    }
}
