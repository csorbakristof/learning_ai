using Xunit;
using LogAnalyzer.Core;
using System.Collections.Generic;
using System.Linq;

namespace LogAnalyzer.Tests;

/// <summary>
/// Advanced tests targeting complex validation logic and edge cases in email/IP extraction
/// </summary>
public class AdvancedValidationTests
{
    private readonly LogAnalyzerService _service;

    public AdvancedValidationTests()
    {
        _service = new LogAnalyzerService();
    }

    #region Email Validation Edge Cases

    [Theory]
    [InlineData(".start@example.com")]     // Starts with dot
    [InlineData("end.@example.com")]       // Ends with dot
    [InlineData("@example.com")]          // Starts with @
    [InlineData("user@")]                 // Ends with @
    [InlineData("user@@example.com")]     // Multiple @
    [InlineData("user@.example.com")]     // Domain starts with dot
    [InlineData("user@example.com.")]     // Domain ends with dot
    [InlineData("user@example")]          // Domain without dot
    public void ExtractEmailAddresses_InvalidEmailFormats_DoesNotExtract(string invalidEmail)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = $"Contact: {invalidEmail}", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert
        Assert.DoesNotContain(invalidEmail, emails);
    }

    [Theory]
    [InlineData("user@example.com")]           // Standard email
    [InlineData("user.name@example.com")]      // Dot in local part
    [InlineData("user+tag@example.com")]       // Plus in local part
    [InlineData("user_name@example.com")]      // Underscore in local part
    [InlineData("user@sub.example.com")]       // Subdomain
    [InlineData("ab@cd.co")]                   // Minimum length valid email
    public void ExtractEmailAddresses_ValidEmailFormats_ExtractsCorrectly(string validEmail)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = $"Contact: {validEmail} for support", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert
        Assert.Contains(validEmail, emails);
    }

    [Fact]
    public void ExtractEmailAddresses_ConsecutiveDots_FiltersOut()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = "Invalid: user..name@example.com", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Valid: user.name@example.com", Timestamp = "2024-01-01 10:01:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert
        Assert.Single(emails);
        Assert.Contains("user.name@example.com", emails);
        Assert.DoesNotContain("user..name@example.com", emails);
    }

    #endregion

    #region IP Address Complex Validation

    [Fact]
    public void ExtractIPAddresses_MixedContent_ExtractsAllValidIPs()
    {
        // Arrange - Test various IP patterns including those that look like version numbers
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = "Application version 1.2.3.4 detected", Timestamp = "2024-01-01 10:00:00" }, // IP-like version
            new LogEntry { Level = "INFO", User = "user", Message = "Build 2.1.0.1-beta", Timestamp = "2024-01-01 10:01:00" }, // IP-like with suffix
            new LogEntry { Level = "INFO", User = "user", Message = "Server IP: 192.168.1.100", Timestamp = "2024-01-01 10:02:00" }, // actual IP
            new LogEntry { Level = "INFO", User = "user", Message = "Connected to 10.0.0.1", Timestamp = "2024-01-01 10:03:00" } // another actual IP
        };

        // Act
        var ips = _service.ExtractIPAddresses(entries);

        // Assert - Should extract all valid IP addresses regardless of context
        Assert.Contains("1.2.3.4", ips);
        Assert.Contains("2.1.0.1", ips);
        Assert.Contains("192.168.1.100", ips);
        Assert.Contains("10.0.0.1", ips);
        Assert.Equal(4, ips.Count);
    }

    [Theory]
    [InlineData("192.168.01.1")]   // Leading zero (should be valid)
    [InlineData("10.0.0.01")]      // Leading zero in last octet
    [InlineData("001.1.1.1")]      // Leading zeros in first octet
    public void ExtractIPAddresses_LeadingZeros_HandlesCorrectly(string ipWithZeros)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = $"IP: {ipWithZeros}", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entries);

        // Assert - Should handle leading zeros appropriately
        Assert.Single(ips);
        Assert.Contains(ipWithZeros, ips);
    }

    [Fact]
    public void ExtractIPAddresses_EdgeCasePatterns_ValidatesCorrectly()
    {
        // Arrange - Test edge cases in IP detection
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = "IP at start: 10.0.0.1 of message", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Message ending with IP 10.0.0.2", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Multiple IPs: 10.0.0.3 and 10.0.0.4 here", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Wrapped (10.0.0.5) in parentheses", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Equal(5, ips.Count);
        Assert.Contains("10.0.0.1", ips);
        Assert.Contains("10.0.0.2", ips);
        Assert.Contains("10.0.0.3", ips);
        Assert.Contains("10.0.0.4", ips);
        Assert.Contains("10.0.0.5", ips);
    }

    #endregion

    #region Complex Log Format Validation

    [Theory]
    [InlineData("[2024-01-01 00:00:00] [INFO] [user] Message")]     // Midnight
    [InlineData("[2024-12-31 23:59:59] [ERROR] [admin] Last second")]  // Year end
    [InlineData("[2024-02-29 12:00:00] [DEBUG] [test] Leap year")]     // Leap year
    [InlineData("[2024-06-15 12:34:56] [WARNING] [user.name] Complex user")]
    public void IsValidLogFormat_ComplexValidFormats_ValidatesCorrectly(string logLine)
    {
        // Act
        var result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.True(result);
    }

    [Theory]
    [InlineData("[2024-13-01 10:00:00] [INFO] [user] Invalid month")]
    [InlineData("[2024-01-32 10:00:00] [INFO] [user] Invalid day")]
    [InlineData("[2024-01-01 25:00:00] [INFO] [user] Invalid hour")]
    [InlineData("[2024-01-01 10:61:00] [INFO] [user] Invalid minute")]
    [InlineData("[2024-01-01 10:00:61] [INFO] [user] Invalid second")]
    [InlineData("[2023-02-29 10:00:00] [INFO] [user] Invalid leap year")]
    public void IsValidLogFormat_InvalidDateTimeParts_ReturnsFalse(string logLine)
    {
        // Act
        var result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.False(result);
    }

    [Theory]
    [InlineData("[2024-01-01 10:00:00] [CUSTOM] [user] Custom level")]
    [InlineData("[2024-01-01 10:00:00] [info] [user] Lowercase level")]
    [InlineData("[2024-01-01 10:00:00] [Error] [user] Mixed case level")]
    public void IsValidLogFormat_InvalidLogLevels_ReturnsFalse(string logLine)
    {
        // Act
        var result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.False(result);
    }

    #endregion

    #region File Reading Edge Cases

    [Fact]
    public void ReadLogFile_MixedValidInvalidLines_ProcessesOnlyValid()
    {
        // Arrange
        var tempFile = Path.GetTempFileName();
        var lines = new[]
        {
            "[2024-01-01 10:00:00] [INFO] [user1] Valid line 1",
            "This is not a valid log line",
            "[2024-01-01 10:01:00] [ERROR] [user2] Valid line 2",
            "[invalid-timestamp] [INFO] [user3] Invalid timestamp",
            "[2024-01-01 10:02:00] [DEBUG] [user4] Valid line 3",
            "",  // Empty line
            "   ", // Whitespace only
            "[2024-01-01 10:03:00] [WARNING] [user5] Valid line 4"
        };
        
        try
        {
            File.WriteAllLines(tempFile, lines);

            // Act
            var entries = _service.ReadLogFile(tempFile);

            // Assert
            Assert.Equal(4, entries.Count); // Only valid lines
            Assert.All(entries, entry => 
            {
                Assert.NotNull(entry.Level);
                Assert.NotNull(entry.User);
                Assert.NotNull(entry.Message);
                Assert.NotNull(entry.Timestamp);
            });
        }
        finally
        {
            if (File.Exists(tempFile))
                File.Delete(tempFile);
        }
    }

    #endregion

    #region String Comparison Edge Cases

    [Fact]
    public void FilterByLevel_CaseSensitivityEdgeCases_HandlesCorrectly()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "ERROR", User = "user1", Message = "msg1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "error", User = "user2", Message = "msg2", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "Error", User = "user3", Message = "msg3", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "eRrOr", User = "user4", Message = "msg4", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var results = _service.FilterByLevel(entries, "ERROR").ToList();

        // Assert - Should find all variations due to case-insensitive comparison
        Assert.Equal(4, results.Count);
    }

    #endregion
}
