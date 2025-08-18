using Xunit;
using LogAnalyzer.Core;
using System.Collections.Generic;

namespace LogAnalyzer.Tests;

/// <summary>
/// Tests specifically designed to catch logical operator mutations (|| to && and vice versa)
/// </summary>
public class LogicalOperatorTests
{
    private readonly LogAnalyzerService _service;

    public LogicalOperatorTests()
    {
        _service = new LogAnalyzerService();
    }

    #region Email Validation Logical Operator Tests

    [Theory]
    [InlineData("a.@test.com")]           // Tests email.EndsWith(".") condition
    [InlineData("a@invalid")]             // Tests domain without dot condition  
    [InlineData("a@.invalid.com")]        // Tests domain.StartsWith(".") condition
    [InlineData("a@invalid.")]            // Tests domain.EndsWith(".") condition
    public void ExtractEmailAddresses_InvalidEmailFormats_ExcludesFromResults(string invalidEmail)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Level = "INFO", 
                User = "user", 
                Message = $"Contact: {invalidEmail} for support", 
                Timestamp = "2024-01-01 10:00:00" 
            }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert - These should be rejected due to OR conditions
        // If || becomes &&, these tests will fail because the logic changes
        Assert.DoesNotContain(invalidEmail, emails);
        Assert.Empty(emails);
    }

    [Theory]
    [InlineData("valid@test.com")]
    [InlineData("user.name@domain.org")]
    [InlineData("test123@example.co.uk")]
    public void ExtractEmailAddresses_ValidEmailFormats_IncludesInResults(string validEmail)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Level = "INFO", 
                User = "user", 
                Message = $"Contact: {validEmail} for support", 
                Timestamp = "2024-01-01 10:00:00" 
            }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert - These should be accepted
        Assert.Contains(validEmail, emails);
        Assert.Single(emails);
    }

    [Fact]
    public void ExtractEmailAddresses_LocalPartValidation_TestsAllConditions()
    {
        // Test each condition of the local part validation separately
        // Line 166: string.IsNullOrEmpty(localPart) || localPart.StartsWith(".") || localPart.EndsWith(".")
        
        var testCases = new List<LogEntry>
        {
            // This tests the localPart.StartsWith(".") condition  
            new LogEntry { Level = "INFO", User = "user", Message = "Email: a.invalid@domain.com", Timestamp = "2024-01-01 10:01:00" },
            
            // This tests the localPart.EndsWith(".") condition
            new LogEntry { Level = "INFO", User = "user", Message = "Email: invalid.a@domain.com", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(testCases);

        // Assert - All should be rejected due to OR logic
        // If || becomes &&, some of these might incorrectly pass
        Assert.Empty(emails);
    }

    [Fact]
    public void ExtractEmailAddresses_DomainPartValidation_TestsAllConditions()
    {
        // Test each condition of the domain part validation separately
        // Line 171: string.IsNullOrEmpty(domainPart) || domainPart.StartsWith(".") || domainPart.EndsWith(".") || !domainPart.Contains(".")
        
        var testCases = new List<LogEntry>
        {
            // This tests the string.IsNullOrEmpty(domainPart) condition
            new LogEntry { Level = "INFO", User = "user", Message = "Email: user@", Timestamp = "2024-01-01 10:00:00" },
            
            // This tests the domainPart.StartsWith(".") condition
            new LogEntry { Level = "INFO", User = "user", Message = "Email: user@.invalid.com", Timestamp = "2024-01-01 10:01:00" },
            
            // This tests the domainPart.EndsWith(".") condition
            new LogEntry { Level = "INFO", User = "user", Message = "Email: user@invalid.", Timestamp = "2024-01-01 10:02:00" },
            
            // This tests the !domainPart.Contains(".") condition
            new LogEntry { Level = "INFO", User = "user", Message = "Email: user@nodots", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(testCases);

        // Assert - All should be rejected due to OR logic
        // If || becomes &&, some of these might incorrectly pass
        Assert.Empty(emails);
    }

    #endregion

    #region IP Address Validation Logical Operator Tests

    [Theory]
    [InlineData("256.1.1.1")]      // num > 255 condition
    [InlineData("-1.1.1.1")]       // num < 0 condition  
    [InlineData("abc.1.1.1")]      // !int.TryParse condition
    [InlineData("1.1.1")]          // parts.Length != 4 (handled elsewhere)
    public void ExtractIPAddresses_InvalidIPParts_ExcludesFromResults(string invalidIP)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Level = "INFO", 
                User = "user", 
                Message = $"Server IP: {invalidIP}", 
                Timestamp = "2024-01-01 10:00:00" 
            }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entries);

        // Assert - Should be rejected due to OR conditions in validation
        // Line 222: !int.TryParse(part, out int num) || num < 0 || num > 255
        Assert.DoesNotContain(invalidIP, ips);
    }

    [Fact]
    public void ExtractIPAddresses_IPPartValidation_TestsAllConditions()
    {
        // Test the logical conditions separately: !int.TryParse(part, out int num) || num < 0 || num > 255
        
        var testCases = new List<LogEntry>
        {
            // Test !int.TryParse condition
            new LogEntry { Level = "INFO", User = "user", Message = "IP: abc.123.45.67", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 123.def.45.67", Timestamp = "2024-01-01 10:01:00" },
            
            // Test num > 255 condition
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 256.123.45.67", Timestamp = "2024-01-01 10:03:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 123.256.45.67", Timestamp = "2024-01-01 10:04:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 123.45.256.67", Timestamp = "2024-01-01 10:05:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 123.45.67.256", Timestamp = "2024-01-01 10:06:00" }
        };

        // Act
        var ips = _service.ExtractIPAddresses(testCases);

        // Assert - All should be rejected due to OR logic
        // If || becomes &&, some might incorrectly pass validation
        Assert.Empty(ips);
    }

    [Theory]
    [InlineData("192.168.1.1")]
    [InlineData("10.0.0.1")]  
    [InlineData("255.255.255.255")]
    [InlineData("0.0.0.0")]
    public void ExtractIPAddresses_ValidIPs_IncludesInResults(string validIP)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Level = "INFO", 
                User = "user", 
                Message = $"Server IP: {validIP}", 
                Timestamp = "2024-01-01 10:00:00" 
            }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Contains(validIP, ips);
        Assert.Single(ips);
    }

    #endregion
}
