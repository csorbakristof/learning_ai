using LogAnalyzer.Core;

namespace LogAnalyzer.Tests;

public class IPAddressExtractionTests
{
    private readonly LogAnalyzerService _service;
    private readonly List<LogEntry> _testEntries;

    public IPAddressExtractionTests()
    {
        _service = new LogAnalyzerService();
        
        // Setup test data with IP addresses
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

    #region Basic IP Extraction Tests

    [Fact]
    public void ExtractIPAddresses_WithIPs_ReturnsCorrectIPs()
    {
        // Act
        var ips = _service.ExtractIPAddresses(_testEntries);

        // Assert
        Assert.Contains("192.168.1.100", ips);
        Assert.Contains("10.0.0.5", ips);
        Assert.Equal(2, ips.Count);
    }

    [Fact]
    public void ExtractIPAddresses_WithNoIPs_ReturnsEmptyList()
    {
        // Arrange
        var entriesWithoutIPs = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user1", Message = "No IP here", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "ERROR", User = "user2", Message = "Just a regular message", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "DEBUG", User = "user3", Message = "System startup", Timestamp = "2024-01-01 10:02:00" }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entriesWithoutIPs);

        // Assert
        Assert.NotNull(ips);
        Assert.Empty(ips);
    }

    [Fact]
    public void ExtractIPAddresses_WithInvalidIPs_FiltersCorrectly()
    {
        // Arrange
        var entriesWithInvalidIPs = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user1", Message = "Invalid IP: 256.1.1.1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "ERROR", User = "user2", Message = "Another invalid: 192.168.300.1", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "DEBUG", User = "user3", Message = "Valid IP: 192.168.1.1", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "INFO", User = "user4", Message = "Valid IP-like pattern: 1.2.3.4", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entriesWithInvalidIPs);

        // Assert
        Assert.Equal(2, ips.Count);
        Assert.Contains("192.168.1.1", ips);
        Assert.Contains("1.2.3.4", ips);
    }

    #endregion

    #region Theory Tests for Various IP Formats

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
            new LogEntry { Level = "INFO", User = "user", Message = message, Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Single(ips);
        Assert.Contains(expectedIP, ips);
    }

    [Theory]
    [InlineData("Invalid IP: 256.1.1.1")]
    [InlineData("Invalid IP: 1.256.1.1")]
    [InlineData("Invalid IP: 1.1.256.1")]
    [InlineData("Invalid IP: 1.1.1.256")]
    [InlineData("Invalid IP: 192.168.1")]
    [InlineData("Not an IP: 192-168-1-1")]
    [InlineData("Incomplete: 192.168.")]
    public void ExtractIPAddresses_InvalidFormats_DoesNotExtract(string message)
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = message, Timestamp = "2024-01-01 10:00:00" }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Empty(ips);
    }

    #endregion

    #region Multiple IPs and Edge Cases

    [Fact]
    public void ExtractIPAddresses_MultipleIPsInOneMessage_ExtractsAll()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry 
            { 
                Level = "INFO", 
                User = "user", 
                Message = "Traffic from 192.168.1.1, 10.0.0.1, and 172.16.0.1", 
                Timestamp = "2024-01-01 10:00:00" 
            }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Equal(3, ips.Count);
        Assert.Contains("192.168.1.1", ips);
        Assert.Contains("10.0.0.1", ips);
        Assert.Contains("172.16.0.1", ips);
    }

    [Fact]
    public void ExtractIPAddresses_WithDuplicateIPs_ReturnsUniqueIPs()
    {
        // Arrange
        var entriesWithDuplicates = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user1", Message = "Connection from 192.168.1.1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "ERROR", User = "user2", Message = "Attack from 192.168.1.1", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "DEBUG", User = "user3", Message = "Response to 192.168.1.1", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "INFO", User = "user4", Message = "Also from 10.0.0.1", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entriesWithDuplicates);

        // Assert
        Assert.Equal(2, ips.Count);
        Assert.Contains("192.168.1.1", ips);
        Assert.Contains("10.0.0.1", ips);
    }

    [Fact]
    public void ExtractIPAddresses_EmptyList_ReturnsEmptyList()
    {
        // Arrange
        var emptyEntries = new List<LogEntry>();

        // Act
        var ips = _service.ExtractIPAddresses(emptyEntries);

        // Assert
        Assert.NotNull(ips);
        Assert.Empty(ips);
    }

    [Fact]
    public void ExtractIPAddresses_WithNullEntries_ThrowsException()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => _service.ExtractIPAddresses(null));
    }

    [Fact]
    public void ExtractIPAddresses_PrivateIPRanges_ExtractsCorrectly()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = "Class A private: 10.1.1.1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Class B private: 172.16.1.1", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Class C private: 192.168.1.1", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Public IP: 8.8.8.8", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Equal(4, ips.Count);
        Assert.Contains("10.1.1.1", ips);
        Assert.Contains("172.16.1.1", ips);
        Assert.Contains("192.168.1.1", ips);
        Assert.Contains("8.8.8.8", ips);
    }

    [Fact]
    public void ExtractIPAddresses_LargeDataset_PerformsWell()
    {
        // Arrange
        var largeDataset = new List<LogEntry>();
        for (int i = 0; i < 1000; i++)
        {
            largeDataset.Add(new LogEntry 
            { 
                Level = "INFO",
                User = $"user{i}",
                Message = i % 2 == 0 ? $"Connection from 192.168.1.{i % 255}" : "No IP in this message",
                Timestamp = $"2024-01-01 {i / 3600:D2}:{(i % 3600) / 60:D2}:{i % 60:D2}"
            });
        }

        // Act
        var stopwatch = System.Diagnostics.Stopwatch.StartNew();
        var ips = _service.ExtractIPAddresses(largeDataset);
        stopwatch.Stop();

        // Assert
        Assert.True(ips.Count > 0);
        Assert.True(stopwatch.ElapsedMilliseconds < 2000, $"IP extraction took {stopwatch.ElapsedMilliseconds}ms, should be under 2000ms");
    }

    [Fact]
    public void ExtractIPAddresses_BoundaryValues_HandlesCorrectly()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = "Min IP: 0.0.0.0", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Max IP: 255.255.255.255", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Localhost: 127.0.0.1", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Broadcast: 255.255.255.255", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Equal(3, ips.Count); // Should have unique IPs only
        Assert.Contains("0.0.0.0", ips);
        Assert.Contains("255.255.255.255", ips);
        Assert.Contains("127.0.0.1", ips);
    }

    [Fact]
    public void ExtractIPAddresses_AllValidIPPatterns_ExtractsCorrectly()
    {
        // Arrange
        var entries = new List<LogEntry>
        {
            new LogEntry { Level = "INFO", User = "user", Message = "Valid IP: 192.168.1.1", Timestamp = "2024-01-01 10:00:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Application 1.2.3.4 released", Timestamp = "2024-01-01 10:01:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Software connects to 10.0.0.1", Timestamp = "2024-01-01 10:02:00" },
            new LogEntry { Level = "INFO", User = "user", Message = "Server at 172.16.0.1", Timestamp = "2024-01-01 10:03:00" }
        };

        // Act
        var ips = _service.ExtractIPAddresses(entries);

        // Assert
        Assert.Equal(4, ips.Count);
        Assert.Contains("192.168.1.1", ips);
        Assert.Contains("1.2.3.4", ips);
        Assert.Contains("10.0.0.1", ips);
        Assert.Contains("172.16.0.1", ips);
    }

    #endregion
}
