using LogAnalyzer.Core;

namespace LogAnalyzer.Tests;

public class LogAnalyzerServiceTests
{
    private readonly LogAnalyzerService _service;
    private readonly List<LogEntry> _testEntries;

    public LogAnalyzerServiceTests()
    {
        _service = new LogAnalyzerService();
        
        // Setup test data
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
    public void ReadLogFile_ValidFile_ReturnsCorrectEntries()
    {
        // Arrange - Create a temporary test file
        string testFilePath = Path.GetTempFileName();
        string testContent = @"[2024-01-15 10:30:45] [ERROR] [john.doe] Failed login attempt from 192.168.1.100
[2024-01-15 10:31:20] [INFO] [jane.smith] User registered with email john.doe@company.com
[2024-01-15 10:32:10] [WARNING] [admin] Suspicious activity detected
Invalid log line without proper format";
        
        File.WriteAllText(testFilePath, testContent);

        try
        {
            // Act
            var result = _service.ReadLogFile(testFilePath);

            // Assert
            Assert.NotNull(result);
            Assert.Equal(3, result.Count); // Only 3 valid entries (4th line is invalid)
            
            // Check that all returned entries have required properties
            foreach (var entry in result)
            {
                Assert.False(string.IsNullOrEmpty(entry.Timestamp));
                Assert.False(string.IsNullOrEmpty(entry.Level));
                Assert.False(string.IsNullOrEmpty(entry.User));
                Assert.False(string.IsNullOrEmpty(entry.Message));
            }
        }
        finally
        {
            // Clean up
            if (File.Exists(testFilePath))
                File.Delete(testFilePath);
        }
    }

    [Fact]
    public void ReadLogFile_NonExistentFile_ThrowsFileNotFoundException()
    {
        // Arrange
        string nonExistentFilePath = "non_existent_file.log";

        // Act & Assert
        Assert.Throws<FileNotFoundException>(() => _service.ReadLogFile(nonExistentFilePath));
    }

    [Fact]
    public void IsValidLogFormat_ValidFormat_ReturnsTrue()
    {
        // Arrange
        string validLogLine = "[2024-01-15 10:30:45] [ERROR] [john.doe] Failed login attempt from 192.168.1.100";

        // Act
        bool result = _service.IsValidLogFormat(validLogLine);

        // Assert
        Assert.True(result);
    }

    [Fact]
    public void IsValidLogFormat_InvalidFormat_ReturnsFalse()
    {
        // Arrange
        string[] invalidLogLines = {
            "Invalid log line without proper format",
            "[2024-01-15] [ERROR] Message without user",
            "2024-01-15 10:30:45 ERROR john.doe Message without brackets",
            "[2024-01-15 10:30:45] [INVALID_LEVEL] [user] Message",
            ""
        };

        // Act & Assert
        foreach (string invalidLine in invalidLogLines)
        {
            bool result = _service.IsValidLogFormat(invalidLine);
            Assert.False(result, $"Line should be invalid: {invalidLine}");
        }
    }

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
    public void FilterByLevel_WithValidLevel_ReturnsCorrectEntries()
    {
        // Act
        var errorEntries = _service.FilterByLevel(_testEntries, "ERROR").ToList();
        var infoEntries = _service.FilterByLevel(_testEntries, "INFO").ToList();

        // Assert
        Assert.Equal(2, errorEntries.Count);
        Assert.All(errorEntries, entry => Assert.Equal("ERROR", entry.Level));
        
        Assert.Single(infoEntries);
        Assert.All(infoEntries, entry => Assert.Equal("INFO", entry.Level));
    }

    [Fact]
    public void FilterByLevel_CaseInsensitive_ReturnsCorrectEntries()
    {
        // Act
        var errorEntriesLower = _service.FilterByLevel(_testEntries, "error").ToList();
        var errorEntriesUpper = _service.FilterByLevel(_testEntries, "ERROR").ToList();

        // Assert
        Assert.Equal(errorEntriesUpper.Count, errorEntriesLower.Count);
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
    public void ExtractEmailAddresses_WithEmails_ReturnsCorrectEmails()
    {
        // Act
        var emails = _service.ExtractEmailAddresses(_testEntries);

        // Assert
        Assert.Contains("john.doe@company.com", emails);
        Assert.Contains("support@company.hu", emails);
        Assert.Equal(2, emails.Count);
    }

    [Fact]
    public void ExtractEmailAddresses_WithNoEmails_ReturnsEmptyList()
    {
        // Arrange
        var entriesWithoutEmails = new List<LogEntry>
        {
            new LogEntry { Message = "No email in this message" },
            new LogEntry { Message = "Another message without email" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entriesWithoutEmails);

        // Assert
        Assert.Empty(emails);
    }

    [Fact]
    public void ExtractIPAddresses_WithIPs_ReturnsCorrectIPs()
    {
        // Act
        var ipAddresses = _service.ExtractIPAddresses(_testEntries);

        // Assert
        Assert.Contains("192.168.1.100", ipAddresses);
        Assert.Contains("10.0.0.5", ipAddresses);
        Assert.Equal(2, ipAddresses.Count);
    }

    [Fact]
    public void ExtractIPAddresses_WithNoIPs_ReturnsEmptyList()
    {
        // Arrange
        var entriesWithoutIPs = new List<LogEntry>
        {
            new LogEntry { Message = "No IP address in this message" },
            new LogEntry { Message = "Another message without IP" }
        };

        // Act
        var ipAddresses = _service.ExtractIPAddresses(entriesWithoutIPs);

        // Assert
        Assert.Empty(ipAddresses);
    }

    [Fact]
    public void ExtractIPAddresses_WithInvalidIPs_FiltersCorrectly()
    {
        // Arrange
        var entriesWithInvalidIPs = new List<LogEntry>
        {
            new LogEntry { Message = "Invalid IP: 999.999.999.999" },
            new LogEntry { Message = "Valid IP: 192.168.1.1 and invalid: 300.400.500.600" },
            new LogEntry { Message = "Another valid IP: 10.0.0.1" }
        };

        // Act
        var ipAddresses = _service.ExtractIPAddresses(entriesWithInvalidIPs);

        // Assert
        Assert.Contains("192.168.1.1", ipAddresses);
        Assert.Contains("10.0.0.1", ipAddresses);
        Assert.DoesNotContain("999.999.999.999", ipAddresses);
        Assert.DoesNotContain("300.400.500.600", ipAddresses);
        Assert.Equal(2, ipAddresses.Count);
    }
}