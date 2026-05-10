using LogAnalyzer.Core;
using System.Threading.Tasks;

namespace LogAnalyzer.Tests;

public class EdgeCasesAndIntegrationTests
{
    private readonly LogAnalyzerService _service;

    public EdgeCasesAndIntegrationTests()
    {
        _service = new LogAnalyzerService();
    }

    #region LogEntry Model Tests

    [Fact]
    public void LogEntry_Properties_CanBeSetAndRetrieved()
    {
        // Arrange
        var entry = new LogEntry
        {
            Timestamp = "2024-01-15 12:00:00",
            Level = "INFO",
            User = "test.user",
            Message = "Test message"
        };

        // Assert
        Assert.Equal("2024-01-15 12:00:00", entry.Timestamp);
        Assert.Equal("INFO", entry.Level);
        Assert.Equal("test.user", entry.User);
        Assert.Equal("Test message", entry.Message);
    }

    [Fact]
    public void LogEntry_DefaultValues_AreEmptyStrings()
    {
        // Arrange & Act
        var entry = new LogEntry();

        // Assert
        Assert.Equal(string.Empty, entry.Timestamp);
        Assert.Equal(string.Empty, entry.Level);
        Assert.Equal(string.Empty, entry.User);
        Assert.Equal(string.Empty, entry.Message);
    }

    #endregion

    #region Performance and Large Dataset Tests

    [Fact]
    public void AllMethods_WithVeryLargeDataset_PerformReasonably()
    {
        // Arrange
        var largeDataset = new List<LogEntry>();
        var random = new Random(42); // Fixed seed for reproducible results
        
        // Create 10,000+ entries
        for (int i = 0; i < 10000; i++)
        {
            var level = new[] { "INFO", "WARNING", "ERROR", "DEBUG" }[i % 4];
            var user = $"user{i % 100}";
            var hasEmail = i % 5 == 0;
            var hasIP = i % 3 == 0;
            
            var message = $"Message {i}";
            if (hasEmail) message += $" contact user{i}@company.com";
            if (hasIP) message += $" from {192 + (i % 64)}.{168}.{1}.{i % 255}";
            
            largeDataset.Add(new LogEntry
            {
                Timestamp = $"2024-01-{(i % 28) + 1:D2} {i / 3600:D2}:{(i % 3600) / 60:D2}:{i % 60:D2}",
                Level = level,
                User = user,
                Message = message
            });
        }

        // Act & Assert - Test all major methods
        var stopwatch = System.Diagnostics.Stopwatch.StartNew();
        
        var errorCount = _service.CountErrorEntries(largeDataset);
        var userActivity = _service.GetUserActivitySummary(largeDataset);
        var emails = _service.ExtractEmailAddresses(largeDataset);
        var ips = _service.ExtractIPAddresses(largeDataset);
        var filteredErrors = _service.FilterByLevel(largeDataset, "ERROR").ToList();
        
        stopwatch.Stop();

        // Assert performance
        Assert.True(stopwatch.ElapsedMilliseconds < 5000, $"Processing 10K entries took {stopwatch.ElapsedMilliseconds}ms, should be under 5000ms");
        
        // Assert correctness
        Assert.Equal(2500, errorCount); // 25% should be errors
        Assert.Equal(100, userActivity.Count); // 100 unique users
        Assert.True(emails.Count > 0, "Should extract some emails");
        Assert.True(ips.Count > 0, "Should extract some IPs");
        Assert.Equal(errorCount, filteredErrors.Count);
    }

    #endregion

    #region Special Characters and Unicode Tests

    [Fact]
    public void ExtractMethods_WithSpecialCharactersInMessages_HandleCorrectly()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Level = "INFO", 
                User = "test.user", 
                Message = "Special chars: áéíóöőúüű and email test@üzenet.hu", 
                Timestamp = "2024-01-01 10:00:00" 
            },
            new LogEntry 
            { 
                Level = "ERROR", 
                User = "ügyfél", 
                Message = "Unicode IP: 192.168.1.1 and special chars: àáâãäåæçèéêë", 
                Timestamp = "2024-01-01 10:01:00" 
            },
            new LogEntry 
            { 
                Level = "DEBUG", 
                User = "tëst-üser", 
                Message = "Emoji test 🚀 with email: rocket@space.com and IP: 10.0.0.1", 
                Timestamp = "2024-01-01 10:02:00" 
            }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);
        var ips = _service.ExtractIPAddresses(entries);
        var userActivity = _service.GetUserActivitySummary(entries);

        // Assert
        Assert.Contains("rocket@space.com", emails);
        Assert.Contains("192.168.1.1", ips);
        Assert.Contains("10.0.0.1", ips);
        Assert.True(userActivity.ContainsKey("ügyfél"));
        Assert.True(userActivity.ContainsKey("tëst-üser"));
    }

    #endregion

    #region Thread Safety Tests

    [Fact]
    public void AllMethods_ThreadSafety_BasicCheck()
    {
        // Arrange
        var testEntries = new List<LogEntry>();
        for (int i = 0; i < 1000; i++)
        {
            testEntries.Add(new LogEntry
            {
                Timestamp = $"2024-01-01 {i / 60:D2}:{i % 60:D2}:00",
                Level = i % 2 == 0 ? "ERROR" : "INFO",
                User = $"user{i % 10}",
                Message = $"Message {i} with email user{i}@test.com and IP 192.168.1.{i % 255}"
            });
        }

        // Act - Run methods concurrently
        var tasks = new List<Task<object>>();
        
        // Start multiple concurrent operations
        for (int i = 0; i < 10; i++)
        {
            tasks.Add(Task.Run(() => (object)_service.CountErrorEntries(testEntries)));
            tasks.Add(Task.Run(() => (object)_service.GetUserActivitySummary(testEntries)));
            tasks.Add(Task.Run(() => (object)_service.ExtractEmailAddresses(testEntries)));
            tasks.Add(Task.Run(() => (object)_service.ExtractIPAddresses(testEntries)));
            tasks.Add(Task.Run(() => (object)_service.FilterByLevel(testEntries, "ERROR").ToList()));
        }

        // Wait for all tasks to complete
        Task.WaitAll(tasks.ToArray());

        // Assert - All tasks should complete without exceptions
        Assert.All(tasks, task => Assert.True(task.IsCompletedSuccessfully));
        
        // Verify consistent results
        var errorCounts = tasks.Where(t => t.Result is int).Select(t => (int)t.Result).Distinct().ToList();
        Assert.Single(errorCounts); // All error counts should be the same
    }

    #endregion

    #region Integration Scenarios

    [Fact]
    public void CompleteWorkflow_FromFileToAnalysis_WorksCorrectly()
    {
        // Arrange - Create a comprehensive test file
        string testFilePath = Path.GetTempFileName();
        string testContent = @"[2024-01-15 10:30:45] [ERROR] [john.doe] Failed login from 192.168.1.100
[2024-01-15 10:31:20] [INFO] [jane.smith] User registered with email john.doe@company.com
[2024-01-15 10:32:10] [WARNING] [admin] Suspicious activity from 10.0.0.5
[2024-01-15 10:33:05] [ERROR] [bob.wilson] Database timeout, contact admin@company.com
[2024-01-15 10:34:15] [DEBUG] [system] Email sent to support@company.hu from 172.16.0.1
Invalid log line without proper format
[2024-01-15 10:35:20] [INFO] [jane.smith] System maintenance completed
Another invalid line
[2024-01-15 10:36:30] [ERROR] [john.doe] Connection failed to 203.0.113.5";
        
        File.WriteAllText(testFilePath, testContent);

        try
        {
            // Act - Complete workflow
            var entries = _service.ReadLogFile(testFilePath);
            var errorCount = _service.CountErrorEntries(entries);
            var userActivity = _service.GetUserActivitySummary(entries);
            var emails = _service.ExtractEmailAddresses(entries);
            var ips = _service.ExtractIPAddresses(entries);
            var errorEntries = _service.FilterByLevel(entries, "ERROR").ToList();

            // Assert - Verify complete workflow
            Assert.Equal(7, entries.Count); // Should skip 2 invalid lines
            Assert.Equal(3, errorCount); // 3 ERROR entries
            Assert.Equal(5, userActivity.Count); // 5 unique users
            Assert.Equal(2, userActivity["jane.smith"]); // jane.smith appears twice
            Assert.Equal(2, userActivity["john.doe"]); // john.doe appears twice
            
            Assert.Equal(3, emails.Count); // 3 unique emails
            Assert.Contains("john.doe@company.com", emails);
            Assert.Contains("admin@company.com", emails);
            Assert.Contains("support@company.hu", emails);
            
            Assert.Equal(4, ips.Count); // 4 unique IPs
            Assert.Contains("192.168.1.100", ips);
            Assert.Contains("10.0.0.5", ips);
            Assert.Contains("172.16.0.1", ips);
            Assert.Contains("203.0.113.5", ips);
            
            Assert.Equal(3, errorEntries.Count);
            Assert.All(errorEntries, entry => Assert.Equal("ERROR", entry.Level));
        }
        finally
        {
            if (File.Exists(testFilePath))
                File.Delete(testFilePath);
        }
    }

    [Fact]
    public void ErrorHandling_NullAndEmptyInputs_HandledGracefully()
    {
        // Test all methods with null/empty inputs
        var emptyList = new List<LogEntry>();
        
        // These should not throw
        Assert.Equal(0, _service.CountErrorEntries(emptyList));
        Assert.Empty(_service.GetUserActivitySummary(emptyList));
        Assert.Empty(_service.ExtractEmailAddresses(emptyList));
        Assert.Empty(_service.ExtractIPAddresses(emptyList));
        Assert.Empty(_service.FilterByLevel(emptyList, "ERROR"));
        
        // These should throw ArgumentNullException
        Assert.Throws<ArgumentNullException>(() => _service.CountErrorEntries(null));
        Assert.Throws<ArgumentNullException>(() => _service.GetUserActivitySummary(null));
        Assert.Throws<ArgumentNullException>(() => _service.ExtractEmailAddresses(null));
        Assert.Throws<ArgumentNullException>(() => _service.ExtractIPAddresses(null));
        Assert.Throws<ArgumentNullException>(() => _service.FilterByLevel(null, "ERROR"));
        
        // Format validation with null/empty
        Assert.False(_service.IsValidLogFormat(null));
        Assert.False(_service.IsValidLogFormat(""));
        Assert.False(_service.IsValidLogFormat("   "));
    }

    [Fact]
    public void MemoryUsage_LargeDatasets_DoesNotLeakMemory()
    {
        // This is a basic test to ensure no obvious memory leaks
        // In a real scenario, you'd use memory profiling tools
        
        long startMemory = GC.GetTotalMemory(true);
        
        // Process multiple large datasets
        for (int iteration = 0; iteration < 10; iteration++)
        {
            var dataset = new List<LogEntry>();
            for (int i = 0; i < 1000; i++)
            {
                dataset.Add(new LogEntry
                {
                    Timestamp = $"2024-01-01 10:{i % 60:D2}:00",
                    Level = "INFO",
                    User = $"user{i}",
                    Message = $"Test message {i}"
                });
            }
            
            // Process the dataset
            _service.CountErrorEntries(dataset);
            _service.GetUserActivitySummary(dataset);
            _service.ExtractEmailAddresses(dataset);
            _service.ExtractIPAddresses(dataset);
            
            // Clear references
            dataset.Clear();
            dataset = null;
        }
        
        GC.Collect();
        GC.WaitForPendingFinalizers();
        GC.Collect();
        
        long endMemory = GC.GetTotalMemory(false);
        long memoryIncrease = endMemory - startMemory;
        
        // Memory increase should be reasonable (less than 10MB)
        Assert.True(memoryIncrease < 10 * 1024 * 1024, $"Memory increased by {memoryIncrease / (1024 * 1024)}MB, should be less than 10MB");
    }

    #endregion
}
