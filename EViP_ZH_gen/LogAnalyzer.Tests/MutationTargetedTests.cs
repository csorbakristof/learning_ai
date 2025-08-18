using Xunit;
using LogAnalyzer.Core;
using System.Collections.Generic;
using System.Linq;

namespace LogAnalyzer.Tests;

/// <summary>
/// Tests designed to catch specific types of mutations that commonly survive
/// </summary>
public class MutationTargetedTests
{
    private readonly LogAnalyzerService _service;

    public MutationTargetedTests()
    {
        _service = new LogAnalyzerService();
    }

    #region Arithmetic Operator Mutations

    [Fact]
    public void CountErrorEntries_ExactCount_VerifiesArithmeticOperations()
    {
        // Arrange - Create exact number to catch +1/-1 mutations
        var entries = new List<LogEntry>();
        for (int i = 0; i < 7; i++) // Specific number to catch mutations
        {
            entries.Add(new LogEntry 
            { 
                Level = "ERROR", 
                User = $"user{i}", 
                Message = $"Error {i}", 
                Timestamp = "2024-01-01 10:00:00" 
            });
        }

        // Act
        var count = _service.CountErrorEntries(entries);

        // Assert - Test exact count to catch increment/decrement mutations
        Assert.Equal(7, count);
        Assert.NotEqual(6, count); // Catch count-1 mutations
        Assert.NotEqual(8, count); // Catch count+1 mutations
    }

    #endregion

    #region Comparison Operator Mutations

    [Fact]
    public void FilterByLevel_ComparisonOperators_TestsAllConditions()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "ERROR", User = "user1", Message = "msg1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user2", Message = "msg2", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "WARNING", User = "user3", Message = "msg3", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act & Assert - Test equality vs inequality mutations
        var errorResults = _service.FilterByLevel(entries, "ERROR").ToList();
        var infoResults = _service.FilterByLevel(entries, "INFO").ToList();
        var warningResults = _service.FilterByLevel(entries, "WARNING").ToList();
        var debugResults = _service.FilterByLevel(entries, "DEBUG").ToList();

        // Verify exact matches
        Assert.Single(errorResults);
        Assert.Equal("ERROR", errorResults[0].Level);
        
        Assert.Single(infoResults);
        Assert.Equal("INFO", infoResults[0].Level);
        
        Assert.Single(warningResults);
        Assert.Equal("WARNING", warningResults[0].Level);
        
        Assert.Empty(debugResults); // No DEBUG entries
    }

    #endregion

    #region Logical Operator Mutations (AND/OR)

    [Fact]
    public void IsValidLogFormat_LogicalOperators_TestsAndOrConditions()
    {
        // Test cases that would fail if && becomes || or vice versa
        
        // Valid format - all conditions must be true (tests AND logic)
        var validLog = "[2024-01-01 10:00:00] [INFO] [user] Message";
        Assert.True(_service.IsValidLogFormat(validLog));

        // Invalid cases - any single failure should make entire validation fail
        var invalidTimestamp = "[invalid-time] [INFO] [user] Message";
        var invalidLevel = "[2024-01-01 10:00:00] [INVALID] [user] Message";
        var invalidUser = "[2024-01-01 10:00:00] [INFO] [] Message";
        var invalidMessage = "[2024-01-01 10:00:00] [INFO] [user]";

        // These should all be false - testing that ALL conditions must be met
        Assert.False(_service.IsValidLogFormat(invalidTimestamp));
        Assert.False(_service.IsValidLogFormat(invalidLevel));
        Assert.False(_service.IsValidLogFormat(invalidUser));
        Assert.False(_service.IsValidLogFormat(invalidMessage));
    }

    #endregion

    #region Negation Operator Mutations

    [Fact]
    public void FilterByLevel_NegationOperators_TestsNotConditions()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "ERROR", User = "user1", Message = "msg1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user2", Message = "msg2", Timestamp = "2024-01-01 10:01:00" }
        };

        // Act - Test with level that should NOT match
        var nonExistentResults = _service.FilterByLevel(entries, "DEBUG");
        var existingResults = _service.FilterByLevel(entries, "ERROR");

        // Assert - Verify negation logic
        Assert.Empty(nonExistentResults); // Should be empty (not non-empty)
        Assert.NotEmpty(existingResults); // Should not be empty
    }

    #endregion

    #region String Method Mutations

    [Theory]
    [InlineData("")]
    [InlineData(null)]
    public void FilterByLevel_StringNullOrEmpty_TestsStringMethods(string level)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "ERROR", User = "user", Message = "msg", Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var results = _service.FilterByLevel(entries, level);

        // Assert - Should be empty for null/empty input
        Assert.Empty(results);
    }

    [Fact]
    public void GetUserActivitySummary_StringWhiteSpace_TestsIsNullOrWhiteSpace()
    {
        // Arrange - Mix of null, empty, whitespace, and valid users
        var entries = new List<LogEntry>
        {
            new LogEntry { User = "valid", Level = "INFO", Message = "msg1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { User = null, Level = "INFO", Message = "msg2", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { User = "", Level = "INFO", Message = "msg3", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { User = "   ", Level = "INFO", Message = "msg4", Timestamp = "2024-01-01 10:03:00" },
            new LogEntry { User = "\t", Level = "INFO", Message = "msg5", Timestamp = "2024-01-01 10:04:00" }
        };

        // Act
        var result = _service.GetUserActivitySummary(entries);

        // Assert - Only valid user should be included
        Assert.Single(result);
        Assert.True(result.ContainsKey("valid"));
        Assert.Equal(1, result["valid"]);
    }

    #endregion

    #region Conditional Expression Mutations

    [Fact]
    public void ExtractEmailAddresses_ConditionalExpressions_TestsTernaryOperators()
    {
        // Arrange - Test patterns that might use conditional expressions internally
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = "Contact: test@example.com for help", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "No email in this message", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Multiple emails: first@test.com and second@test.com", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act
        var emails = _service.ExtractEmailAddresses(entries);

        // Assert - Test exact conditions that might use ternary operators
        Assert.Equal(3, emails.Count);
        Assert.Contains("test@example.com", emails);
        Assert.Contains("first@test.com", emails);
        Assert.Contains("second@test.com", emails);
    }

    #endregion

    #region Loop Boundary Mutations

    [Fact]
    public void ExtractIPAddresses_LoopBoundaries_TestsIterationLogic()
    {
        // Arrange - Create data that tests loop boundaries
        var entries = new List<LogEntry>();
        
        // Add entries with IPs at different positions to test loop logic
        for (int i = 0; i < 5; i++)
        {
            entries.Add(new LogEntry 
            { 
                Level = "INFO", 
                User = $"user{i}", 
                Message = $"Server {i} has IP 192.168.1.{i + 1}", 
                Timestamp = "2024-01-01 10:00:00" 
            });
        }

        // Act
        var ips = _service.ExtractIPAddresses(entries);

        // Assert - Verify all IPs are found (tests loop completion)
        Assert.Equal(5, ips.Count);
        for (int i = 1; i <= 5; i++)
        {
            Assert.Contains($"192.168.1.{i}", ips);
        }
    }

    #endregion

    #region Return Value Mutations

    [Fact]
    public void IsValidLogFormat_ReturnValueMutations_TestsBooleanReturns()
    {
        // Test cases specifically designed to catch return value mutations
        
        // Case that should definitely return true
        var validCase = "[2024-01-01 10:00:00] [ERROR] [user.name] Valid message here";
        Assert.True(_service.IsValidLogFormat(validCase));
        
        // Case that should definitely return false
        var invalidCase = "This is not a valid log format at all";
        Assert.False(_service.IsValidLogFormat(invalidCase));
        
        // Edge case that tests the boundary between true/false
        var almostValidCase = "[2024-01-01 10:00:00] [ERROR] [user.name]"; // Missing message
        Assert.False(_service.IsValidLogFormat(almostValidCase));
    }

    #endregion
}
