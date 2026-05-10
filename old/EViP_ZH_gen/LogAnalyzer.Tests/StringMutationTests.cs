using Xunit;
using LogAnalyzer.Core;
using System.Collections.Generic;

namespace LogAnalyzer.Tests;

/// <summary>
/// Tests specifically designed to catch string literal mutations
/// </summary>
public class StringMutationTests
{
    private readonly LogAnalyzerService _service;

    public StringMutationTests()
    {
        _service = new LogAnalyzerService();
    }

    [Fact]
    public void ExtractEmailAddresses_DomainMustContainDot_RejectsNoDotDomains()
    {
        // This test specifically targets the !domainPart.Contains(".") condition
        // If the "." string gets mutated to "", the logic changes completely
        
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Level = "INFO", 
                User = "user", 
                Message = "Email: user@nodomain", // Domain without dot
                Timestamp = "2024-01-01 10:00:00" 
            },
            new LogEntry 
            { 
                Level = "INFO", 
                User = "user", 
                Message = "Email: user@stillnodot", // Another domain without dot
                Timestamp = "2024-01-01 10:01:00" 
            },
            new LogEntry 
            { 
                Level = "INFO", 
                User = "user", 
                Message = "Email: user@valid.domain", // Valid domain with dot
                Timestamp = "2024-01-01 10:02:00" 
            }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert - Only the email with a dot in domain should be valid
        // If "." gets mutated to "", then Contains("") would always return true
        // and the validation logic would be broken
        Assert.Single(emails);
        Assert.Contains("user@valid.domain", emails);
        Assert.DoesNotContain("user@nodomain", emails);
        Assert.DoesNotContain("user@stillnodot", emails);
    }

    [Fact]
    public void ExtractEmailAddresses_DomainDotValidation_SpecificStringChecks()
    {
        // Test various dot-related scenarios to ensure the "." string is used correctly
        var testCases = new[]
        {
            ("user@nodot", false),           // No dot at all
            ("user@a.", false),          // Ends with dot (caught by EndsWith("."))
            ("user@.a", false),          // Starts with dot (caught by StartsWith("."))
            ("user@domain.com", true),        // Valid: has dot in middle
            ("user@a.b.c", true),        // Valid: multiple dots
            ("user@sub.domain.com", true) // Valid: proper domain
        };

        foreach (var (email, shouldBeValid) in testCases)
        {
            // Arrange
            var entries = new List<LogEntry>
            {
                new LogEntry 
                { 
                    Level = "INFO", 
                    User = "user", 
                    Message = $"Contact: {email}", 
                    Timestamp = "2024-01-01 10:00:00" 
                }
            };

            // Act
            var emails = _service.ExtractEmailAddresses(entries);

            // Assert
            if (shouldBeValid)
            {
                Assert.Contains(email, emails);
            }
            else
            {
                Assert.DoesNotContain(email, emails);
            }
        }
    }

    [Fact]
    public void ExtractEmailAddresses_DotStringMutation_CatchesReplacementWithEmpty()
    {
        // This test is specifically designed to catch if "." gets replaced with ""
        // When Contains(".") becomes Contains(""), it would always return true
        
        // Arrange - emails that should be invalid but would become valid if "." -> ""
        var entries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Level = "INFO", 
                User = "user", 
                Message = "Email: invalid@nodot", 
                Timestamp = "2024-01-01 10:00:00" 
            }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert - Should be empty because domain has no dot
        // If "." gets mutated to "", this would incorrectly pass validation
        Assert.Empty(emails);
    }
}
