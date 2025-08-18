using LogAnalyzer.Core;

namespace LogAnalyzer.Tests;

public class FormatValidationTests
{
    private readonly LogAnalyzerService _service;

    public FormatValidationTests()
    {
        _service = new LogAnalyzerService();
    }

    #region Basic Format Tests

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

    [Fact]
    public void IsValidLogFormat_NullAndEmptyString_ReturnsFalse()
    {
        // Act & Assert
        Assert.False(_service.IsValidLogFormat(null));
        Assert.False(_service.IsValidLogFormat(string.Empty));
        Assert.False(_service.IsValidLogFormat("   "));
    }

    #endregion

    #region Theory Tests with InlineData

    [Theory]
    [InlineData("[2024-01-15 10:30:45] [INFO] [user] Message")]
    [InlineData("[2024-12-31 23:59:59] [WARNING] [admin] Year end message")]
    [InlineData("[2024-01-01 00:00:00] [ERROR] [system] New year error")]
    [InlineData("[2024-06-15 12:30:45] [DEBUG] [test.user] Mid year debug")]
    [InlineData("[2024-02-29 15:45:30] [ERROR] [leap.year] Leap year test")]
    public void IsValidLogFormat_VariousValidFormats_ReturnsTrue(string logLine)
    {
        // Act
        bool result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.True(result, $"Valid line should pass: {logLine}");
    }

    [Theory]
    [InlineData("[2024-13-15 10:30:45] [ERROR] [user] Invalid month")]
    [InlineData("[2024-01-32 10:30:45] [ERROR] [user] Invalid day")]
    [InlineData("[2024-01-15 25:30:45] [ERROR] [user] Invalid hour")]
    [InlineData("[2024-01-15 10:60:45] [ERROR] [user] Invalid minute")]
    [InlineData("[2024-01-15 10:30:60] [ERROR] [user] Invalid second")]
    [InlineData("[2024-02-30 10:30:45] [ERROR] [user] Invalid February date")]
    public void IsValidLogFormat_InvalidDateTimeFormats_ReturnsFalse(string logLine)
    {
        // Act
        bool result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.False(result, $"Invalid datetime should fail: {logLine}");
    }

    [Theory]
    [InlineData("[2024-01-15 10:30:45] [TRACE] [user] Invalid level")]
    [InlineData("[2024-01-15 10:30:45] [FATAL] [user] Invalid level")]
    [InlineData("[2024-01-15 10:30:45] [error] [user] Lowercase level")]
    [InlineData("[2024-01-15 10:30:45] [Error] [user] Mixed case level")]
    [InlineData("[2024-01-15 10:30:45] [CRITICAL] [user] Invalid level")]
    public void IsValidLogFormat_InvalidLogLevels_ReturnsFalse(string logLine)
    {
        // Act
        bool result = _service.IsValidLogFormat(logLine);

        // Assert
        Assert.False(result, $"Invalid log level should fail: {logLine}");
    }

    #endregion

    #region Edge Cases

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

    [Fact]
    public void IsValidLogFormat_MissingBrackets_ReturnsFalse()
    {
        // Arrange
        string[] invalidFormats = {
            "2024-01-15 10:30:45] [ERROR] [user] Missing opening bracket",
            "[2024-01-15 10:30:45 [ERROR] [user] Missing closing bracket",
            "[2024-01-15 10:30:45] ERROR] [user] Missing opening bracket for level",
            "[2024-01-15 10:30:45] [ERROR [user] Missing closing bracket for level",
            "[2024-01-15 10:30:45] [ERROR] user] Missing opening bracket for user",
            "[2024-01-15 10:30:45] [ERROR] [user Missing closing bracket for user"
        };

        // Act & Assert
        foreach (string invalidFormat in invalidFormats)
        {
            bool result = _service.IsValidLogFormat(invalidFormat);
            Assert.False(result, $"Format with missing brackets should fail: {invalidFormat}");
        }
    }

    [Fact]
    public void IsValidLogFormat_ValidLogLevels_ReturnsTrue()
    {
        // Arrange
        string[] validLevels = { "INFO", "WARNING", "ERROR", "DEBUG" };

        // Act & Assert
        foreach (string level in validLevels)
        {
            string logLine = $"[2024-01-15 10:30:45] [{level}] [user] Test message";
            bool result = _service.IsValidLogFormat(logLine);
            Assert.True(result, $"Valid level {level} should pass");
        }
    }

    [Fact]
    public void IsValidLogFormat_UsernameWithSpecialCharacters_ReturnsTrue()
    {
        // Arrange
        string[] validUsernames = {
            "[2024-01-15 10:30:45] [INFO] [john.doe] Message",
            "[2024-01-15 10:30:45] [INFO] [user_123] Message",
            "[2024-01-15 10:30:45] [INFO] [test-user] Message",
            "[2024-01-15 10:30:45] [INFO] [system] Message"
        };

        // Act & Assert
        foreach (string logLine in validUsernames)
        {
            bool result = _service.IsValidLogFormat(logLine);
            Assert.True(result, $"Valid username format should pass: {logLine}");
        }
    }

    #endregion
}
