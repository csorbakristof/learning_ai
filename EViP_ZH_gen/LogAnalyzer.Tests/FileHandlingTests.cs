using LogAnalyzer.Core;

namespace LogAnalyzer.Tests;

public class FileHandlingTests
{
    private readonly LogAnalyzerService _service;

    public FileHandlingTests()
    {
        _service = new LogAnalyzerService();
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
            Assert.Equal(3, result.Count); // Should only return valid entries
            
            Assert.Equal("ERROR", result[0].Level);
            Assert.Equal("john.doe", result[0].User);
            Assert.Contains("192.168.1.100", result[0].Message);
            
            Assert.Equal("INFO", result[1].Level);
            Assert.Equal("jane.smith", result[1].User);
            Assert.Contains("john.doe@company.com", result[1].Message);
            
            Assert.Equal("WARNING", result[2].Level);
            Assert.Equal("admin", result[2].User);
        }
        finally
        {
            if (File.Exists(testFilePath))
                File.Delete(testFilePath);
        }
    }

    [Fact]
    public void ReadLogFile_NonExistentFile_ThrowsFileNotFoundException()
    {
        // Arrange
        string nonExistentFilePath = "non_existent_file_12345.log";

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
[Invalid] [Format] Missing timestamp
Missing brackets completely
2024-01-15 10:30:45 ERROR user Message without brackets";
        
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
[Invalid timestamp] [ERROR] [user] Invalid timestamp format
[2024-01-15 10:33:05] [DEBUG] [system] Valid entry 4";
        
        File.WriteAllText(testFilePath, testContent);

        try
        {
            // Act
            var result = _service.ReadLogFile(testFilePath);

            // Assert
            Assert.NotNull(result);
            Assert.Equal(4, result.Count); // Should only return the 4 valid entries
            
            Assert.All(result, entry => Assert.False(string.IsNullOrEmpty(entry.Level)));
            Assert.All(result, entry => Assert.False(string.IsNullOrEmpty(entry.User)));
            Assert.All(result, entry => Assert.False(string.IsNullOrEmpty(entry.Message)));
        }
        finally
        {
            if (File.Exists(testFilePath))
                File.Delete(testFilePath);
        }
    }

    [Fact]
    public void ReadLogFile_LargeFile_PerformsReasonably()
    {
        // Arrange
        string testFilePath = Path.GetTempFileName();
        var lines = new List<string>();
        
        // Create 1000 valid log entries
        for (int i = 0; i < 1000; i++)
        {
            int hour = 10 + (i / 3600);
            int minute = (i % 3600) / 60;
            int second = i % 60;
            lines.Add($"[2024-01-15 {hour:D2}:{minute:D2}:{second:D2}] [INFO] [user{i}] Test message {i}");
        }
        
        File.WriteAllLines(testFilePath, lines);

        try
        {
            // Act
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();
            var result = _service.ReadLogFile(testFilePath);
            stopwatch.Stop();

            // Assert
            Assert.Equal(1000, result.Count);
            Assert.True(stopwatch.ElapsedMilliseconds < 5000, $"File reading took {stopwatch.ElapsedMilliseconds}ms, should be under 5000ms");
        }
        finally
        {
            if (File.Exists(testFilePath))
                File.Delete(testFilePath);
        }
    }
}
