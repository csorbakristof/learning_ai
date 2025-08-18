using Xunit;
using LogAnalyzer.Core;
using System.Collections.Generic;

namespace LogAnalyzer.Tests;

/// <summary>
/// Advanced tests to catch remaining stubborn mutations that focus on edge cases
/// </summary>
public class AdvancedMutationTests
{
    private readonly LogAnalyzerService _service;

    public AdvancedMutationTests()
    {
        _service = new LogAnalyzerService();
    }

    [Fact]
    public void CountErrorEntries_StatementMutation_MustReturnValue()
    {
        // This targets the statement mutation on line 94
        // Statement mutations often remove the return statement entirely
        
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "ERROR", User = "user1", Message = "Error 1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user2", Message = "Info 1", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "ERROR", User = "user3", Message = "Error 2", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act
        var result = _service.CountErrorEntries(entries);

        // Assert - These assertions will fail if the return statement is removed
        Assert.IsType<int>(result);  // Must return an int
        Assert.True(result >= 0);    // Must be non-negative
        Assert.Equal(2, result);     // Must return the correct count
        
        // Additional checks to catch statement removal
        Assert.NotEqual(default(int), result); // Should not be default value
        Assert.InRange(result, 0, entries.Count()); // Must be in valid range
    }

    [Fact]
    public void GetUserActivitySummary_StatementMutation_MustReturnDictionary()
    {
        // This targets the statement mutation on line 107
        
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "alice", Message = "Message 1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "ERROR", User = "bob", Message = "Message 2", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "INFO", User = "alice", Message = "Message 3", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act
        var result = _service.GetUserActivitySummary(entries);

        // Assert - These will fail if the return statement is removed
        Assert.NotNull(result);                           // Must return a value
        Assert.IsType<Dictionary<string, int>>(result);   // Must return correct type
        Assert.True(result.Count > 0);                    // Must have contents
        Assert.Equal(2, result.Count);                    // Correct number of users
        Assert.Equal(2, result["alice"]);                 // Correct count for alice
        Assert.Equal(1, result["bob"]);                   // Correct count for bob
        
        // Additional validation
        Assert.All(result.Values, count => Assert.True(count > 0)); // All counts positive
    }

    [Fact]
    public void ExtractEmailAddresses_ComplexLogicalConditions_ComprehensiveTest()
    {
        // Target the remaining logical mutations by testing complex combinations
        // This should catch mutations where || becomes && in email validation
        
        var complexTestCases = new List<LogEntry>
        {
            // Test combination of conditions that should ALL fail individually
            new LogEntry { Level = "INFO", User = "user", Message = "Email: @missinglocal.com", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Email: .startsdot@domain.com", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Email: endsdot.@domain.com", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Email: user@", Timestamp = "2024-01-01 10:03:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Email: user@.startsdot.com", Timestamp = "2024-01-01 10:04:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Email: user@endsdot.", Timestamp = "2024-01-01 10:05:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Email: user@nodot", Timestamp = "2024-01-01 10:06:00" },
            
            // One valid email for contrast
            new LogEntry { Level = "INFO", User = "user", Message = "Valid: user@valid.domain.com", Timestamp = "2024-01-01 10:07:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(complexTestCases);

        // Assert
        Assert.Single(emails); // Only one valid email should be found
        Assert.Contains("user@valid.domain.com", emails);
        
        // Verify none of the invalid ones are included
        Assert.DoesNotContain("@missinglocal.com", emails);
        Assert.DoesNotContain(".startsdot@domain.com", emails);
        Assert.DoesNotContain("endsdot.@domain.com", emails);
        Assert.DoesNotContain("user@", emails);
        Assert.DoesNotContain("user@.startsdot.com", emails);
        Assert.DoesNotContain("user@endsdot.", emails);
        Assert.DoesNotContain("user@nodot", emails);
    }

    [Fact]
    public void ExtractIPAddresses_ComplexLogicalConditions_ComprehensiveTest()
    {
        // Target the remaining logical mutations in IP validation
        // This should catch mutations where || becomes && in IP validation
        
        var complexTestCases = new List<LogEntry>
        {
            // Test each condition that should individually cause failure
            new LogEntry { Level = "INFO", User = "user", Message = "IP: notanumber.1.2.3", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 256.1.2.3", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 1.notanumber.2.3", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 1.2.notanumber.3", Timestamp = "2024-01-01 10:03:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 1.2.3.notanumber", Timestamp = "2024-01-01 10:04:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 300.2.3.4", Timestamp = "2024-01-01 10:05:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 1.300.3.4", Timestamp = "2024-01-01 10:06:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 1.2.300.4", Timestamp = "2024-01-01 10:07:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "IP: 1.2.3.300", Timestamp = "2024-01-01 10:08:00" },
            
            // Valid IPs for contrast
            new LogEntry { Level = "INFO", User = "user", Message = "Valid: 192.168.1.1", Timestamp = "2024-01-01 10:09:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Valid: 10.0.0.1", Timestamp = "2024-01-01 10:10:00" }
        };

        // Act
        var ips = _service.ExtractIPAddresses(complexTestCases);

        // Assert
        Assert.Equal(2, ips.Count); // Only valid IPs should be found
        Assert.Contains("192.168.1.1", ips);
        Assert.Contains("10.0.0.1", ips);
        
        // Verify all invalid ones are rejected
        Assert.DoesNotContain("notanumber.1.2.3", ips);
        Assert.DoesNotContain("256.1.2.3", ips);
        Assert.DoesNotContain("300.2.3.4", ips);
    }
}
