using LogAnalyzer.Core;

namespace LogAnalyzer.Tests;

public class UserActivityAnalysisTests
{
    private readonly LogAnalyzerService _service;
    private readonly List<LogEntry> _testEntries;

    public UserActivityAnalysisTests()
    {
        _service = new LogAnalyzerService();
        
        // Setup test data for user activity analysis
        _testEntries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Timestamp = "2024-01-15 10:30:45", 
                Level = "ERROR", 
                User = "john.doe", 
                Message = "Failed login attempt" 
            },
            new LogEntry 
            { 
                Timestamp = "2024-01-15 10:31:20", 
                Level = "INFO", 
                User = "jane.smith", 
                Message = "User registered" 
            },
            new LogEntry 
            { 
                Timestamp = "2024-01-15 10:32:10", 
                Level = "WARNING", 
                User = "admin", 
                Message = "Suspicious activity detected" 
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
                Message = "Email sent successfully" 
            }
        };
    }

    [Fact]
    public void GetUserActivitySummary_ReturnsCorrectCounts()
    {
        // Act
        var userActivity = _service.GetUserActivitySummary(_testEntries);

        // Assert
        Assert.Equal(5, userActivity.Count); // john.doe, jane.smith, admin, bob.wilson, system
        Assert.Equal(1, userActivity["john.doe"]);
        Assert.Equal(1, userActivity["jane.smith"]);
        Assert.Equal(1, userActivity["admin"]);
        Assert.Equal(1, userActivity["bob.wilson"]);
        Assert.Equal(1, userActivity["system"]);
    }

    [Fact]
    public void GetUserActivitySummary_EmptyList_ReturnsEmptyDictionary()
    {
        // Arrange
        var emptyEntries = new List<LogEntry>();

        // Act
        var userActivity = _service.GetUserActivitySummary(emptyEntries);

        // Assert
        Assert.NotNull(userActivity);
        Assert.Empty(userActivity);
    }

    [Fact]
    public void GetUserActivitySummary_EntriesWithEmptyUsers_ExcludesEmptyUsers()
    {
        // Arrange
        var entriesWithEmptyUsers = new List<LogEntry>
        {
            new LogEntry { User = "valid.user", Level = "INFO", Message = "Valid", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { User = "", Level = "ERROR", Message = "Empty user", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { User = null, Level = "WARNING", Message = "Null user", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { User = "another.user", Level = "DEBUG", Message = "Another valid", Timestamp = "2024-01-01 10:03:00" },
            new LogEntry { User = "   ", Level = "INFO", Message = "Whitespace user", Timestamp = "2024-01-01 10:04:00" }
        };

        // Act
        var userActivity = _service.GetUserActivitySummary(entriesWithEmptyUsers);

        // Assert
        Assert.Equal(2, userActivity.Count);
        Assert.True(userActivity.ContainsKey("valid.user"));
        Assert.True(userActivity.ContainsKey("another.user"));
        Assert.False(userActivity.ContainsKey(""));
        Assert.False(userActivity.ContainsKey("   "));
    }

    [Fact]
    public void GetUserActivitySummary_DuplicateUsers_CountsCorrectly()
    {
        // Arrange
        var entriesWithDuplicates = new List<LogEntry>
        {
            new LogEntry { User = "john.doe", Level = "INFO", Message = "Message 1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { User = "john.doe", Level = "ERROR", Message = "Message 2", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { User = "john.doe", Level = "WARNING", Message = "Message 3", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { User = "jane.smith", Level = "DEBUG", Message = "Message 4", Timestamp = "2024-01-01 10:03:00" },
            new LogEntry { User = "jane.smith", Level = "INFO", Message = "Message 5", Timestamp = "2024-01-01 10:04:00" },
            new LogEntry { User = "admin", Level = "ERROR", Message = "Message 6", Timestamp = "2024-01-01 10:05:00" }
        };

        // Act
        var userActivity = _service.GetUserActivitySummary(entriesWithDuplicates);

        // Assert
        Assert.Equal(3, userActivity.Count);
        Assert.Equal(3, userActivity["john.doe"]);
        Assert.Equal(2, userActivity["jane.smith"]);
        Assert.Equal(1, userActivity["admin"]);
    }

    [Fact]
    public void GetUserActivitySummary_WithNullEntries_ThrowsException()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => _service.GetUserActivitySummary(null));
    }

    [Fact]
    public void GetUserActivitySummary_LargeDataset_PerformsWell()
    {
        // Arrange
        var largeDataset = new List<LogEntry>();
        for (int i = 0; i < 10000; i++)
        {
            largeDataset.Add(new LogEntry 
            { 
                User = $"user{i % 100}", // 100 unique users
                Level = "INFO",
                Message = $"Message {i}",
                Timestamp = $"2024-01-01 {i / 3600:D2}:{(i % 3600) / 60:D2}:{i % 60:D2}"
            });
        }

        // Act
        var stopwatch = System.Diagnostics.Stopwatch.StartNew();
        var userActivity = _service.GetUserActivitySummary(largeDataset);
        stopwatch.Stop();

        // Assert
        Assert.Equal(100, userActivity.Count); // 100 unique users
        Assert.All(userActivity.Values, count => Assert.Equal(100, count)); // Each user should have 100 entries
        Assert.True(stopwatch.ElapsedMilliseconds < 2000, $"Analysis took {stopwatch.ElapsedMilliseconds}ms, should be under 2000ms");
    }

    [Fact]
    public void GetUserActivitySummary_CaseSensitiveUsers_TreatsAsDistinct()
    {
        // Arrange
        var entriesWithCaseDifferences = new List<LogEntry>
        {
            new LogEntry { User = "John.Doe", Level = "INFO", Message = "Message 1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { User = "john.doe", Level = "ERROR", Message = "Message 2", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { User = "JOHN.DOE", Level = "WARNING", Message = "Message 3", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act
        var userActivity = _service.GetUserActivitySummary(entriesWithCaseDifferences);

        // Assert
        Assert.Equal(3, userActivity.Count); // Should treat as 3 distinct users
        Assert.Equal(1, userActivity["John.Doe"]);
        Assert.Equal(1, userActivity["john.doe"]);
        Assert.Equal(1, userActivity["JOHN.DOE"]);
    }

    [Fact]
    public void GetUserActivitySummary_SingleUser_ReturnsCorrectCount()
    {
        // Arrange
        var singleUserEntries = new List<LogEntry>
        {
            new LogEntry { User = "solo.user", Level = "INFO", Message = "Message 1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { User = "solo.user", Level = "ERROR", Message = "Message 2", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { User = "solo.user", Level = "WARNING", Message = "Message 3", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { User = "solo.user", Level = "DEBUG", Message = "Message 4", Timestamp = "2024-01-01 10:03:00" },
            new LogEntry { User = "solo.user", Level = "INFO", Message = "Message 5", Timestamp = "2024-01-01 10:04:00" }
        };

        // Act
        var userActivity = _service.GetUserActivitySummary(singleUserEntries);

        // Assert
        Assert.Single(userActivity);
        Assert.Equal(5, userActivity["solo.user"]);
    }
}
