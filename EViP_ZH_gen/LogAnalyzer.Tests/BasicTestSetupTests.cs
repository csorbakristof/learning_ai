using LogAnalyzer.Core;

namespace LogAnalyzer.Tests;

public class BasicTestSetupTests
{
    private readonly LogAnalyzerService _service;
    private readonly List<LogEntry> _testEntries;

    public BasicTestSetupTests()
    {
        _service = new LogAnalyzerService();
        
        // Setup test data - 5 különböző típusú teszt LogEntry
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

    [Fact]
    public void LogAnalyzerService_CanBeInstantiated()
    {
        // Act & Assert
        Assert.NotNull(_service);
    }

    [Fact]
    public void TestData_ContainsFiveDifferentEntries()
    {
        // Assert
        Assert.Equal(5, _testEntries.Count);
        Assert.Contains(_testEntries, e => e.Level == "ERROR");
        Assert.Contains(_testEntries, e => e.Level == "INFO");
        Assert.Contains(_testEntries, e => e.Level == "WARNING");
        Assert.Contains(_testEntries, e => e.Level == "DEBUG");
    }

    [Fact]
    public void TestData_ContainsDifferentUsers()
    {
        // Assert
        var uniqueUsers = _testEntries.Select(e => e.User).Distinct().ToList();
        Assert.True(uniqueUsers.Count >= 4);
        Assert.Contains("john.doe", uniqueUsers);
        Assert.Contains("jane.smith", uniqueUsers);
        Assert.Contains("admin", uniqueUsers);
        Assert.Contains("system", uniqueUsers);
    }

    [Fact]
    public void TestData_ContainsEmailAndIPInMessages()
    {
        // Assert
        Assert.Contains(_testEntries, e => e.Message.Contains("@"));
        Assert.Contains(_testEntries, e => e.Message.Contains("192.168.1.100"));
        Assert.Contains(_testEntries, e => e.Message.Contains("10.0.0.5"));
    }

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

    [Fact]
    public void LogAnalyzerService_PublicMethods_AreAvailable()
    {
        // Assert - Check that all required methods exist
        var serviceType = typeof(LogAnalyzerService);
        
        Assert.NotNull(serviceType.GetMethod("ReadLogFile"));
        Assert.NotNull(serviceType.GetMethod("FilterByLevel"));
        Assert.NotNull(serviceType.GetMethod("CountErrorEntries"));
        Assert.NotNull(serviceType.GetMethod("GetUserActivitySummary"));
        Assert.NotNull(serviceType.GetMethod("IsValidLogFormat"));
        Assert.NotNull(serviceType.GetMethod("ExtractEmailAddresses"));
        Assert.NotNull(serviceType.GetMethod("ExtractIPAddresses"));
    }

    [Fact]
    public void TestSetup_ValidatesBasicFunctionality()
    {
        // Act & Assert - Basic smoke test
        Assert.DoesNotThrow(() => {
            var result = _service.FilterByLevel(_testEntries, "ERROR");
            Assert.NotNull(result);
        });
    }
}
