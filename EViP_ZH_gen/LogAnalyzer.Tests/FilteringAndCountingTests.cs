using LogAnalyzer.Core;

namespace LogAnalyzer.Tests;

public class FilteringAndCountingTests
{
    private readonly LogAnalyzerService _service;
    private readonly List<LogEntry> _testEntries;

    public FilteringAndCountingTests()
    {
        _service = new LogAnalyzerService();
        
        // Setup test data for filtering and counting
        _testEntries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Timestamp = "2024-01-15 10:30:45", 
                Level = "ERROR", 
                User = "john.doe", 
                Message = "Failed login attempt from 192.168.1.100" 
            },
            new LogEntry 
            { 
                Timestamp = "2024-01-15 10:31:20", 
                Level = "INFO", 
                User = "jane.smith", 
                Message = "User registered with email john.doe@company.com" 
            },
            new LogEntry 
            { 
                Timestamp = "2024-01-15 10:32:10", 
                Level = "WARNING", 
                User = "admin", 
                Message = "Suspicious activity detected from 10.0.0.5" 
            },
            new LogEntry 
            { 
                Timestamp = "2024-01-15 10:33:05", 
                Level = "ERROR", 
                User = "bob.wilson", 
                Message = "Database connection timeout" 
            },
            new LogEntry 
            { 
                Timestamp = "2024-01-15 10:34:15", 
                Level = "DEBUG", 
                User = "system", 
                Message = "Email sent to support@company.hu successfully" 
            }
        };
    }

    #region Level Filtering Tests

    [Fact]
    public void FilterByLevel_WithValidLevel_ReturnsCorrectEntries()
    {
        // Act
        var errorEntries = _service.FilterByLevel(_testEntries, "ERROR").ToList();
        var infoEntries = _service.FilterByLevel(_testEntries, "INFO").ToList();
        var warningEntries = _service.FilterByLevel(_testEntries, "WARNING").ToList();
        var debugEntries = _service.FilterByLevel(_testEntries, "DEBUG").ToList();

        // Assert
        Assert.Equal(2, errorEntries.Count);
        Assert.All(errorEntries, entry => Assert.Equal("ERROR", entry.Level));
        
        Assert.Single(infoEntries);
        Assert.All(infoEntries, entry => Assert.Equal("INFO", entry.Level));
        
        Assert.Single(warningEntries);
        Assert.All(warningEntries, entry => Assert.Equal("WARNING", entry.Level));
        
        Assert.Single(debugEntries);
        Assert.All(debugEntries, entry => Assert.Equal("DEBUG", entry.Level));
    }

    [Fact]
    public void FilterByLevel_CaseInsensitive_ReturnsCorrectEntries()
    {
        // Act
        var errorEntriesLower = _service.FilterByLevel(_testEntries, "error").ToList();
        var errorEntriesUpper = _service.FilterByLevel(_testEntries, "ERROR").ToList();
        var errorEntriesMixed = _service.FilterByLevel(_testEntries, "Error").ToList();

        // Assert
        Assert.Equal(errorEntriesUpper.Count, errorEntriesLower.Count);
        Assert.Equal(errorEntriesUpper.Count, errorEntriesMixed.Count);
        Assert.Equal(2, errorEntriesLower.Count);
    }

    [Fact]
    public void FilterByLevel_NonExistentLevel_ReturnsEmpty()
    {
        // Act
        var result = _service.FilterByLevel(_testEntries, "NONEXISTENT").ToList();

        // Assert
        Assert.Empty(result);
    }

    [Fact]
    public void FilterByLevel_EmptyLevel_ReturnsEmpty()
    {
        // Act
        var result = _service.FilterByLevel(_testEntries, "").ToList();

        // Assert
        Assert.Empty(result);
    }

    [Fact]
    public void FilterByLevel_NullLevel_ReturnsEmpty()
    {
        // Act
        var result = _service.FilterByLevel(_testEntries, null).ToList();

        // Assert
        Assert.Empty(result);
    }

    [Fact]
    public void FilterByLevel_EmptyEntries_ReturnsEmpty()
    {
        // Arrange
        var emptyEntries = new List<LogEntry>();

        // Act
        var result = _service.FilterByLevel(emptyEntries, "ERROR").ToList();

        // Assert
        Assert.Empty(result);
    }

    [Fact]
    public void FilterByLevel_WhitespaceLevel_ReturnsEmpty()
    {
        // Act
        var result = _service.FilterByLevel(_testEntries, "   ").ToList();

        // Assert
        Assert.Empty(result);
    }

    [Fact]
    public void FilterByLevel_NullEntries_ThrowsException()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => _service.FilterByLevel(null, "ERROR"));
    }

    #endregion

    #region Error Counting Tests

    [Fact]
    public void CountErrorEntries_WithErrorEntries_ReturnsCorrectCount()
    {
        // Act
        int errorCount = _service.CountErrorEntries(_testEntries);

        // Assert
        Assert.Equal(2, errorCount); // john.doe and bob.wilson have ERROR entries
    }

    [Fact]
    public void CountErrorEntries_WithNoErrorEntries_ReturnsZero()
    {
        // Arrange
        var entriesWithoutErrors = _testEntries.Where(e => e.Level != "ERROR").ToList();

        // Act
        int errorCount = _service.CountErrorEntries(entriesWithoutErrors);

        // Assert
        Assert.Equal(0, errorCount);
    }

    [Fact]
    public void CountErrorEntries_EmptyList_ReturnsZero()
    {
        // Arrange
        var emptyEntries = new List<LogEntry>();

        // Act
        int errorCount = _service.CountErrorEntries(emptyEntries);

        // Assert
        Assert.Equal(0, errorCount);
    }

    [Fact]
    public void CountErrorEntries_CaseInsensitive_ReturnsCorrectCount()
    {
        // Arrange
        var mixedCaseEntries = new List<LogEntry>
        {
            new LogEntry { Level = "ERROR", User = "user1", Message = "Error 1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "error", User = "user2", Message = "Error 2", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "Error", User = "user3", Message = "Error 3", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "INFO", User = "user4", Message = "Info 1", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        int errorCount = _service.CountErrorEntries(mixedCaseEntries);

        // Assert
        Assert.Equal(3, errorCount); // Should count all ERROR variations
    }

    [Fact]
    public void CountErrorEntries_WithNullEntries_ThrowsException()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => _service.CountErrorEntries(null));
    }

    [Fact]
    public void CountErrorEntries_LargeDataset_PerformsWell()
    {
        // Arrange
        var largeDataset = new List<LogEntry>();
        for (int i = 0; i < 10000; i++)
        {
            largeDataset.Add(new LogEntry 
            { 
                Level = i % 4 == 0 ? "ERROR" : "INFO",
                User = $"user{i}",
                Message = $"Message {i}",
                Timestamp = $"2024-01-01 {i / 3600:D2}:{(i % 3600) / 60:D2}:{i % 60:D2}"
            });
        }

        // Act
        var stopwatch = System.Diagnostics.Stopwatch.StartNew();
        int errorCount = _service.CountErrorEntries(largeDataset);
        stopwatch.Stop();

        // Assert
        Assert.Equal(2500, errorCount); // 25% should be errors
        Assert.True(stopwatch.ElapsedMilliseconds < 1000, $"Counting took {stopwatch.ElapsedMilliseconds}ms, should be under 1000ms");
    }

    [Fact]
    public void CountErrorEntries_OnlyErrorEntries_ReturnsTotal()
    {
        // Arrange
        var onlyErrors = new List<LogEntry>
        {
            new LogEntry { Level = "ERROR", User = "user1", Message = "Error 1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "ERROR", User = "user2", Message = "Error 2", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "ERROR", User = "user3", Message = "Error 3", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act
        int errorCount = _service.CountErrorEntries(onlyErrors);

        // Assert
        Assert.Equal(3, errorCount);
    }

    #endregion
}
