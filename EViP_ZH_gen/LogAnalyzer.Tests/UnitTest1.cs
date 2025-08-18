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

    #region File Reading Tests

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
    public void ReadLogFile_EmptyFile_ReturnsEmptyList()
    {
        // Arrange
        string testFilePath = Path.GetTempFileName();
        File.WriteAllText(testFilePath, string.Empty);

        try
        {
            // Act
            var result = _service.ReadLogFile(testFilePath);

            // Assert
            Assert.NotNull(result);
            Assert.Empty(result);
        }
        finally
        {
            if (File.Exists(testFilePath))
                File.Delete(testFilePath);
        }
    }

    [Fact]
    public void ReadLogFile_FileWithOnlyInvalidEntries_ReturnsEmptyList()
    {
        // Arrange
        string testFilePath = Path.GetTempFileName();
        string testContent = @"Invalid line 1
Another invalid line
Yet another invalid line without proper format
[Invalid] [Format] Missing timestamp";
        
        File.WriteAllText(testFilePath, testContent);

        try
        {
            // Act
            var result = _service.ReadLogFile(testFilePath);

            // Assert
            Assert.NotNull(result);
            Assert.Empty(result);
        }
        finally
        {
            if (File.Exists(testFilePath))
                File.Delete(testFilePath);
        }
    }

    [Fact]
    public void ReadLogFile_FileWithMixedValidAndInvalidEntries_ReturnsOnlyValidEntries()
    {
        // Arrange
        string testFilePath = Path.GetTempFileName();
        string testContent = @"[2024-01-15 10:30:45] [ERROR] [john.doe] Valid entry 1
Invalid line without format
[2024-01-15 10:31:20] [INFO] [jane.smith] Valid entry 2
Another invalid line
[2024-01-15 10:32:10] [WARNING] [admin] Valid entry 3
[Invalid timestamp] [ERROR] [user] Invalid timestamp format";
        
        File.WriteAllText(testFilePath, testContent);

        try
        {
            // Act
            var result = _service.ReadLogFile(testFilePath);

            // Assert
            Assert.NotNull(result);
            Assert.Equal(3, result.Count);
            Assert.All(result, entry => Assert.False(string.IsNullOrEmpty(entry.Message)));
        }
        finally
        {
            if (File.Exists(testFilePath))
                File.Delete(testFilePath);
        }
    }

    #endregion

    #region Format Validation Tests

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
            "",
            null
        };

        // Act & Assert
        foreach (string invalidLine in invalidLogLines)
        {
            bool result = _service.IsValidLogFormat(invalidLine);
            Assert.False(result, $"Line should be invalid: {invalidLine}");
        }
    }

    [Theory]
    [InlineData("[2024-01-15 10:30:45] [INFO] [user] Message")]
    [InlineData("[2024-12-31 23:59:59] [WARNING] [admin] Year end message")]
    [InlineData("[2024-01-01 00:00:00] [ERROR] [system] New year error")]
    [InlineData("[2024-06-15 12:30:45] [DEBUG] [test.user] Mid year debug")]
    public void IsValidLogFormat_VariousValidFormats_ReturnsTrue(string logLine)
    {
        // Act
        bool result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.True(result);
    }

    [Theory]
    [InlineData("[2024-13-15 10:30:45] [ERROR] [user] Invalid month")]
    [InlineData("[2024-01-32 10:30:45] [ERROR] [user] Invalid day")]
    [InlineData("[2024-01-15 25:30:45] [ERROR] [user] Invalid hour")]
    [InlineData("[2024-01-15 10:60:45] [ERROR] [user] Invalid minute")]
    [InlineData("[2024-01-15 10:30:60] [ERROR] [user] Invalid second")]
    public void IsValidLogFormat_InvalidDateTimeFormats_ReturnsFalse(string logLine)
    {
        // Act
        bool result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.False(result);
    }

    [Theory]
    [InlineData("[2024-01-15 10:30:45] [TRACE] [user] Invalid level")]
    [InlineData("[2024-01-15 10:30:45] [FATAL] [user] Invalid level")]
    [InlineData("[2024-01-15 10:30:45] [error] [user] Lowercase level")]
    [InlineData("[2024-01-15 10:30:45] [Error] [user] Mixed case level")]
    public void IsValidLogFormat_InvalidLogLevels_ReturnsFalse(string logLine)
    {
        // Act
        bool result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.False(result);
    }

    [Fact]
    public void IsValidLogFormat_EmptyUser_ReturnsFalse()
    {
        // Arrange
        string logLine = "[2024-01-15 10:30:45] [ERROR] [] Message with empty user";

        // Act
        bool result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.False(result);
    }

    [Fact]
    public void IsValidLogFormat_EmptyMessage_ReturnsFalse()
    {
        // Arrange
        string logLine = "[2024-01-15 10:30:45] [ERROR] [user]";

        // Act
        bool result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.False(result);
    }

    #endregion

    #region Level Filtering Tests

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
    public void CountErrorEntries_WithNullEntries_ReturnsZero()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => _service.CountErrorEntries(null));
    }

    #endregion

    #region User Activity Tests

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
            new LogEntry { User = "another.user", Level = "DEBUG", Message = "Another valid", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var userActivity = _service.GetUserActivitySummary(entriesWithEmptyUsers);

        // Assert
        Assert.Equal(2, userActivity.Count);
        Assert.True(userActivity.ContainsKey("valid.user"));
        Assert.True(userActivity.ContainsKey("another.user"));
        Assert.False(userActivity.ContainsKey(""));
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
            new LogEntry { User = "jane.smith", Level = "DEBUG", Message = "Message 4", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var userActivity = _service.GetUserActivitySummary(entriesWithDuplicates);

        // Assert
        Assert.Equal(2, userActivity.Count);
        Assert.Equal(3, userActivity["john.doe"]);
        Assert.Equal(1, userActivity["jane.smith"]);
    }

    [Fact]
    public void GetUserActivitySummary_WithNullEntries_ThrowsException()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => _service.GetUserActivitySummary(null));
    }

    #endregion

    #region Email Extraction Tests

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
            new LogEntry { Message = "No email in this message", User = "user1", Level = "INFO", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Message = "Another message without email", User = "user2", Level = "ERROR", Timestamp = "2024-01-01 10:01:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entriesWithoutEmails);

        // Assert
        Assert.Empty(emails);
    }

    [Fact]
    public void ExtractEmailAddresses_WithDuplicateEmails_ReturnsUniqueEmails()
    {
        // Arrange
        var entriesWithDuplicates = new List<LogEntry>
        {
            new LogEntry { Message = "Email to john.doe@company.com sent", User = "user1", Level = "INFO", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Message = "Another email to john.doe@company.com", User = "user2", Level = "ERROR", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Message = "Email to admin@test.org", User = "user3", Level = "WARNING", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entriesWithDuplicates);

        // Assert
        Assert.Equal(2, emails.Count);
        Assert.Contains("john.doe@company.com", emails);
        Assert.Contains("admin@test.org", emails);
    }

    [Theory]
    [InlineData("Contact support@example.com for help", "support@example.com")]
    [InlineData("User john.doe123@test-domain.org registered", "john.doe123@test-domain.org")]
    [InlineData("Email admin_user@sub.domain.co.uk", "admin_user@sub.domain.co.uk")]
    [InlineData("Send to user+tag@gmail.com", "user+tag@gmail.com")]
    [InlineData("Backup to system.backup@company.info", "system.backup@company.info")]
    public void ExtractEmailAddresses_VariousValidFormats_ExtractsCorrectly(string message, string expectedEmail)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Message = message, User = "user", Level = "INFO", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert
        Assert.Single(emails);
        Assert.Contains(expectedEmail, emails);
    }

    [Theory]
    [InlineData("Invalid email @example.com")]
    [InlineData("Invalid email user@")]
    [InlineData("Invalid email user@.com")]
    [InlineData("Invalid email user@@example.com")]
    [InlineData("Not an email: user.example.com")]
    public void ExtractEmailAddresses_InvalidFormats_DoesNotExtract(string message)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Message = message, User = "user", Level = "INFO", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert
        Assert.Empty(emails);
    }

    [Fact]
    public void ExtractEmailAddresses_MultipleEmailsInOneMessage_ExtractsAll()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Message = "Send report to admin@company.com and backup@storage.net", 
                User = "user", 
                Level = "INFO", 
                Timestamp = "2024-01-01 10:00:00" 
            }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert
        Assert.Equal(2, emails.Count);
        Assert.Contains("admin@company.com", emails);
        Assert.Contains("backup@storage.net", emails);
    }

    [Fact]
    public void ExtractEmailAddresses_EmptyList_ReturnsEmptyList()
    {
        // Arrange
        var emptyEntries = new List<LogEntry>();

        // Act
        var emails = _service.ExtractEmailAddresses(emptyEntries);

        // Assert
        Assert.NotNull(emails);
        Assert.Empty(emails);
    }

    [Fact]
    public void ExtractEmailAddresses_WithNullEntries_ThrowsException()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => _service.ExtractEmailAddresses(null));
    }

    #endregion

    #region IP Address Extraction Tests

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
            new LogEntry { Message = "No IP address in this message", User = "user1", Level = "INFO", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Message = "Another message without IP", User = "user2", Level = "ERROR", Timestamp = "2024-01-01 10:01:00" }
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
            new LogEntry { Message = "Invalid IP: 999.999.999.999", User = "user1", Level = "ERROR", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Message = "Valid IP: 192.168.1.1 and invalid: 300.400.500.600", User = "user2", Level = "INFO", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Message = "Another valid IP: 10.0.0.1", User = "user3", Level = "WARNING", Timestamp = "2024-01-01 10:02:00" }
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

    [Theory]
    [InlineData("Connection from 192.168.1.100", "192.168.1.100")]
    [InlineData("Server at 10.0.0.1 responding", "10.0.0.1")]
    [InlineData("External request from 203.0.113.5", "203.0.113.5")]
    [InlineData("Firewall blocked 172.16.254.1", "172.16.254.1")]
    [InlineData("Localhost 127.0.0.1 accessed", "127.0.0.1")]
    [InlineData("Edge case 0.0.0.0", "0.0.0.0")]
    [InlineData("Max IP 255.255.255.255", "255.255.255.255")]
    public void ExtractIPAddresses_VariousValidIPs_ExtractsCorrectly(string message, string expectedIP)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Message = message, User = "user", Level = "INFO", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var ipAddresses = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Single(ipAddresses);
        Assert.Contains(expectedIP, ipAddresses);
    }

    [Theory]
    [InlineData("Invalid IP: 256.1.1.1")]
    [InlineData("Invalid IP: 1.256.1.1")]
    [InlineData("Invalid IP: 1.1.256.1")]
    [InlineData("Invalid IP: 1.1.1.256")]
    [InlineData("Invalid IP: 192.168.1")]
    [InlineData("Not an IP: 192-168-1-1")]
    public void ExtractIPAddresses_InvalidFormats_DoesNotExtract(string message)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Message = message, User = "user", Level = "INFO", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var ipAddresses = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Empty(ipAddresses);
    }

    [Fact]
    public void ExtractIPAddresses_MultipleIPsInOneMessage_ExtractsAll()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Message = "Traffic from 192.168.1.100 to 10.0.0.5 detected", 
                User = "user", 
                Level = "INFO", 
                Timestamp = "2024-01-01 10:00:00" 
            }
        };

        // Act
        var ipAddresses = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Equal(2, ipAddresses.Count);
        Assert.Contains("192.168.1.100", ipAddresses);
        Assert.Contains("10.0.0.5", ipAddresses);
    }

    [Fact]
    public void ExtractIPAddresses_WithDuplicateIPs_ReturnsUniqueIPs()
    {
        // Arrange
        var entriesWithDuplicates = new List<LogEntry>
        {
            new LogEntry { Message = "Connection from 192.168.1.100", User = "user1", Level = "INFO", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Message = "Another connection from 192.168.1.100", User = "user2", Level = "ERROR", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Message = "Traffic to 10.0.0.1", User = "user3", Level = "WARNING", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act
        var ipAddresses = _service.ExtractIPAddresses(entriesWithDuplicates);

        // Assert
        Assert.Equal(2, ipAddresses.Count);
        Assert.Contains("192.168.1.100", ipAddresses);
        Assert.Contains("10.0.0.1", ipAddresses);
    }

    [Fact]
    public void ExtractIPAddresses_EmptyList_ReturnsEmptyList()
    {
        // Arrange
        var emptyEntries = new List<LogEntry>();

        // Act
        var ipAddresses = _service.ExtractIPAddresses(emptyEntries);

        // Assert
        Assert.NotNull(ipAddresses);
        Assert.Empty(ipAddresses);
    }

    [Fact]
    public void ExtractIPAddresses_WithNullEntries_ThrowsException()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => _service.ExtractIPAddresses(null));
    }

    #endregion

    #region Edge Cases and Integration Tests

    [Fact]
    public void LogEntry_Properties_CanBeSetAndRetrieved()
    {
        // Arrange
        var logEntry = new LogEntry();

        // Act
        logEntry.Timestamp = "2024-01-15 10:30:45";
        logEntry.Level = "ERROR";
        logEntry.User = "john.doe";
        logEntry.Message = "Test message";

        // Assert
        Assert.Equal("2024-01-15 10:30:45", logEntry.Timestamp);
        Assert.Equal("ERROR", logEntry.Level);
        Assert.Equal("john.doe", logEntry.User);
        Assert.Equal("Test message", logEntry.Message);
    }

    [Fact]
    public void LogEntry_DefaultValues_AreEmptyStrings()
    {
        // Act
        var logEntry = new LogEntry();

        // Assert
        Assert.Equal(string.Empty, logEntry.Timestamp);
        Assert.Equal(string.Empty, logEntry.Level);
        Assert.Equal(string.Empty, logEntry.User);
        Assert.Equal(string.Empty, logEntry.Message);
    }

    [Fact]
    public void AllMethods_WithVeryLargeDataset_PerformReasonably()
    {
        // Arrange - Create a large dataset
        var largeDataset = new List<LogEntry>();
        for (int i = 0; i < 10000; i++)
        {
            largeDataset.Add(new LogEntry
            {
                Timestamp = $"2024-01-15 10:{i % 60:D2}:{i % 60:D2}",
                Level = i % 4 == 0 ? "ERROR" : i % 4 == 1 ? "INFO" : i % 4 == 2 ? "WARNING" : "DEBUG",
                User = $"user{i % 100}",
                Message = $"Message {i} with email user{i}@company.com and IP 192.168.1.{i % 255}"
            });
        }

        // Act & Assert - Should complete without timeout
        var filterResult = _service.FilterByLevel(largeDataset, "ERROR");
        var errorCount = _service.CountErrorEntries(largeDataset);
        var userActivity = _service.GetUserActivitySummary(largeDataset);
        var emails = _service.ExtractEmailAddresses(largeDataset);
        var ips = _service.ExtractIPAddresses(largeDataset);

        // Verify results are reasonable
        Assert.True(filterResult.Count() > 0);
        Assert.True(errorCount > 0);
        Assert.True(userActivity.Count > 0);
        Assert.True(emails.Count > 0);
        Assert.True(ips.Count > 0);
    }

    [Fact]
    public void ExtractMethods_WithSpecialCharactersInMessages_HandleCorrectly()
    {
        // Arrange
        var entriesWithSpecialChars = new List<LogEntry>
        {
            new LogEntry 
            { 
                Message = "Email: test@domain.com; IP: 192.168.1.1; Special chars: !@#$%^&*()", 
                User = "user", 
                Level = "INFO", 
                Timestamp = "2024-01-01 10:00:00" 
            },
            new LogEntry 
            { 
                Message = "Simple email: admin@example.com and IP 10.0.0.1 with émojis 🎉", 
                User = "user", 
                Level = "INFO", 
                Timestamp = "2024-01-01 10:01:00" 
            }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entriesWithSpecialChars);
        var ips = _service.ExtractIPAddresses(entriesWithSpecialChars);

        // Assert
        Assert.Contains("test@domain.com", emails);
        Assert.Contains("admin@example.com", emails);
        Assert.Contains("192.168.1.1", ips);
        Assert.Contains("10.0.0.1", ips);
    }

    [Fact]
    public void AllMethods_ThreadSafety_BasicCheck()
    {
        // Arrange
        var tasks = new List<Task>();
        var results = new List<bool>();
        var lockObject = new object();

        // Act - Run multiple operations concurrently
        for (int i = 0; i < 10; i++)
        {
            tasks.Add(Task.Run(() =>
            {
                try
                {
                    var filterResult = _service.FilterByLevel(_testEntries, "ERROR");
                    var errorCount = _service.CountErrorEntries(_testEntries);
                    var userActivity = _service.GetUserActivitySummary(_testEntries);
                    var emails = _service.ExtractEmailAddresses(_testEntries);
                    var ips = _service.ExtractIPAddresses(_testEntries);

                    lock (lockObject)
                    {
                        results.Add(true);
                    }
                }
                catch
                {
                    lock (lockObject)
                    {
                        results.Add(false);
                    }
                }
            }));
        }

        Task.WaitAll(tasks.ToArray());

        // Assert - All operations should complete successfully
        Assert.Equal(10, results.Count);
        Assert.All(results, result => Assert.True(result));
    }

    #endregion
}