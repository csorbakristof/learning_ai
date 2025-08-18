using LogAnalyzer.Core;

namespace LogAnalyzer.Tests;

public class EmailExtractionTests
{
    private readonly LogAnalyzerService _service;
    private readonly List<LogEntry> _testEntries;

    public EmailExtractionTests()
    {
        _service = new LogAnalyzerService();
        
        // Setup test data with emails
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

    #region Basic Email Extraction Tests

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
            new LogEntry { Level = "INFO", User = "user1", Message = "No email here", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "ERROR", User = "user2", Message = "Just a regular message", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "DEBUG", User = "user3", Message = "System startup", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entriesWithoutEmails);

        // Assert
        Assert.NotNull(emails);
        Assert.Empty(emails);
    }

    [Fact]
    public void ExtractEmailAddresses_WithDuplicateEmails_ReturnsUniqueEmails()
    {
        // Arrange
        var entriesWithDuplicates = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user1", Message = "Contact admin@test.com for help", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "ERROR", User = "user2", Message = "Error occurred, email admin@test.com", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "DEBUG", User = "user3", Message = "Sent notification to admin@test.com", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "INFO", User = "user4", Message = "Also notify support@test.com", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entriesWithDuplicates);

        // Assert
        Assert.Equal(2, emails.Count);
        Assert.Contains("admin@test.com", emails);
        Assert.Contains("support@test.com", emails);
    }

    #endregion

    #region Theory Tests for Various Email Formats

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
            new LogEntry { Level = "INFO", User = "user", Message = message, Timestamp = "2024-01-01 10:00:00" }
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
    [InlineData("Almost email but not: user@domain")]
    public void ExtractEmailAddresses_InvalidFormats_DoesNotExtract(string message)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = message, Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert
        Assert.Empty(emails);
    }

    #endregion

    #region Multiple Emails and Edge Cases

    [Fact]
    public void ExtractEmailAddresses_MultipleEmailsInOneMessage_ExtractsAll()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Level = "INFO", 
                User = "user", 
                Message = "Send notifications to admin@company.com, support@company.com, and backup@company.com", 
                Timestamp = "2024-01-01 10:00:00" 
            }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert
        Assert.Equal(3, emails.Count);
        Assert.Contains("admin@company.com", emails);
        Assert.Contains("support@company.com", emails);
        Assert.Contains("backup@company.com", emails);
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

    [Fact]
    public void ExtractEmailAddresses_WithSpecialCharactersInEmails_ExtractsCorrectly()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = "Email with dash: test-user@example.com", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Email with underscore: test_user@example.com", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Email with numbers: user123@example.com", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Email with plus: user+tag@example.com", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert
        Assert.Equal(4, emails.Count);
        Assert.Contains("test-user@example.com", emails);
        Assert.Contains("test_user@example.com", emails);
        Assert.Contains("user123@example.com", emails);
        Assert.Contains("user+tag@example.com", emails);
    }

    [Fact]
    public void ExtractEmailAddresses_LargeDataset_PerformsWell()
    {
        // Arrange
        var largeDataset = new List<LogEntry>();
        for (int i = 0; i < 1000; i++)
        {
            largeDataset.Add(new LogEntry 
            { 
                Level = "INFO",
                User = $"user{i}",
                Message = i % 2 == 0 ? $"Email user{i}@company.com sent" : "No email in this message",
                Timestamp = $"2024-01-01 {i / 3600:D2}:{(i % 3600) / 60:D2}:{i % 60:D2}"
            });
        }

        // Act
        var stopwatch = System.Diagnostics.Stopwatch.StartNew();
        var emails = _service.ExtractEmailAddresses(largeDataset);
        stopwatch.Stop();

        // Assert
        Assert.Equal(500, emails.Count); // Half should have emails
        Assert.True(stopwatch.ElapsedMilliseconds < 2000, $"Email extraction took {stopwatch.ElapsedMilliseconds}ms, should be under 2000ms");
    }

    [Fact]
    public void ExtractEmailAddresses_ComplexEmailFormats_ExtractsCorrectly()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = "Subdomain email: user@mail.company.com", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Country domain: user@company.co.uk", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Long TLD: user@company.museum", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Numeric domain: user@123company.com", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert
        Assert.Equal(4, emails.Count);
        Assert.Contains("user@mail.company.com", emails);
        Assert.Contains("user@company.co.uk", emails);
        Assert.Contains("user@company.museum", emails);
        Assert.Contains("user@123company.com", emails);
    }

    #endregion
}
