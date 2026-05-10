using LogAnalyzer.Core;

class Program
{
    private static LogAnalyzerService _service = new LogAnalyzerService();
    private static List<LogEntry> _currentEntries = new List<LogEntry>();
    private static string _currentFilePath = string.Empty;

    static void Main(string[] args)
    {
        Console.WriteLine("=== Log Analyzer Application ===");
        Console.WriteLine("Welcome to the Log File Analyzer!");
        Console.WriteLine();

        bool exit = false;
        while (!exit)
        {
            ShowMenu();
            var choice = Console.ReadLine();

            switch (choice)
            {
                case "1":
                    LoadLogFile();
                    break;
                case "2":
                    ShowAllEntries();
                    break;
                case "3":
                    FilterByLevel();
                    break;
                case "4":
                    ShowErrorCount();
                    break;
                case "5":
                    ShowUserActivitySummary();
                    break;
                case "6":
                    ExtractEmailAddresses();
                    break;
                case "7":
                    ExtractIPAddresses();
                    break;
                case "8":
                    exit = true;
                    Console.WriteLine("Thank you for using Log Analyzer. Goodbye!");
                    break;
                default:
                    Console.WriteLine("Invalid choice. Please try again.");
                    break;
            }

            if (!exit)
            {
                Console.WriteLine("\nPress any key to continue...");
                Console.ReadKey();
                Console.Clear();
            }
        }
    }

    private static void ShowMenu()
    {
        Console.WriteLine("Please select an option:");
        Console.WriteLine("1. Load log file");
        Console.WriteLine("2. Show all entries");
        Console.WriteLine("3. Filter entries by level");
        Console.WriteLine("4. Show error count");
        Console.WriteLine("5. Show user activity summary");
        Console.WriteLine("6. Extract email addresses");
        Console.WriteLine("7. Extract IP addresses");
        Console.WriteLine("8. Exit");
        Console.Write("\nEnter your choice (1-8): ");
    }

    private static void LoadLogFile()
    {
        Console.WriteLine("\n=== Load Log File ===");
        Console.Write("Enter the path to the log file (or press Enter for 'sample.log'): ");
        string filePath = Console.ReadLine()?.Trim() ?? string.Empty;
        
        if (string.IsNullOrEmpty(filePath))
        {
            filePath = "sample.log";
        }

        try
        {
            _currentEntries = _service.ReadLogFile(filePath);
            _currentFilePath = filePath;
            Console.WriteLine($"Successfully loaded {_currentEntries.Count} log entries from '{filePath}'");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error loading file: {ex.Message}");
            _currentEntries.Clear();
            _currentFilePath = string.Empty;
        }
    }

    private static void ShowAllEntries()
    {
        Console.WriteLine("\n=== All Log Entries ===");
        
        if (!_currentEntries.Any())
        {
            Console.WriteLine("No log entries loaded. Please load a log file first.");
            return;
        }

        Console.WriteLine($"Showing all {_currentEntries.Count} entries from '{_currentFilePath}':");
        Console.WriteLine();

        foreach (var entry in _currentEntries)
        {
            Console.WriteLine($"[{entry.Timestamp}] [{entry.Level}] [{entry.User}] {entry.Message}");
        }
    }

    private static void FilterByLevel()
    {
        Console.WriteLine("\n=== Filter by Level ===");
        
        if (!_currentEntries.Any())
        {
            Console.WriteLine("No log entries loaded. Please load a log file first.");
            return;
        }

        Console.WriteLine("Available levels: INFO, WARNING, ERROR, DEBUG");
        Console.Write("Enter the level to filter by: ");
        string level = Console.ReadLine()?.Trim() ?? string.Empty;

        if (string.IsNullOrEmpty(level))
        {
            Console.WriteLine("No level specified.");
            return;
        }

        var filteredEntries = _service.FilterByLevel(_currentEntries, level);
        var entriesList = filteredEntries.ToList();

        Console.WriteLine($"\nFound {entriesList.Count} entries with level '{level}':");
        Console.WriteLine();

        foreach (var entry in entriesList)
        {
            Console.WriteLine($"[{entry.Timestamp}] [{entry.Level}] [{entry.User}] {entry.Message}");
        }
    }

    private static void ShowErrorCount()
    {
        Console.WriteLine("\n=== Error Count ===");
        
        if (!_currentEntries.Any())
        {
            Console.WriteLine("No log entries loaded. Please load a log file first.");
            return;
        }

        int errorCount = _service.CountErrorEntries(_currentEntries);
        Console.WriteLine($"Total number of ERROR entries: {errorCount}");
        Console.WriteLine($"Percentage of total entries: {(double)errorCount / _currentEntries.Count * 100:F1}%");
    }

    private static void ShowUserActivitySummary()
    {
        Console.WriteLine("\n=== User Activity Summary ===");
        
        if (!_currentEntries.Any())
        {
            Console.WriteLine("No log entries loaded. Please load a log file first.");
            return;
        }

        var userActivity = _service.GetUserActivitySummary(_currentEntries);

        Console.WriteLine($"Activity summary for {userActivity.Count} users:");
        Console.WriteLine();

        foreach (var kvp in userActivity.OrderByDescending(x => x.Value))
        {
            Console.WriteLine($"{kvp.Key}: {kvp.Value} entries");
        }
    }

    private static void ExtractEmailAddresses()
    {
        Console.WriteLine("\n=== Extract Email Addresses ===");
        
        if (!_currentEntries.Any())
        {
            Console.WriteLine("No log entries loaded. Please load a log file first.");
            return;
        }

        var emails = _service.ExtractEmailAddresses(_currentEntries);

        Console.WriteLine($"Found {emails.Count} unique email addresses:");
        Console.WriteLine();

        foreach (var email in emails.OrderBy(e => e))
        {
            Console.WriteLine($"- {email}");
        }
    }

    private static void ExtractIPAddresses()
    {
        Console.WriteLine("\n=== Extract IP Addresses ===");
        
        if (!_currentEntries.Any())
        {
            Console.WriteLine("No log entries loaded. Please load a log file first.");
            return;
        }

        var ipAddresses = _service.ExtractIPAddresses(_currentEntries);

        Console.WriteLine($"Found {ipAddresses.Count} unique IP addresses:");
        Console.WriteLine();

        foreach (var ip in ipAddresses.OrderBy(i => i))
        {
            Console.WriteLine($"- {ip}");
        }
    }
}
