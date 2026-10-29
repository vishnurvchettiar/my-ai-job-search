using JobSearchDashboard.Models;
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;

namespace JobSearchDashboard.Services;

public class JobApplicationService
{
    private readonly string _csvPath;
    private List<JobApplication> _apps = new();
    private int _nextId = 1;

    public JobApplicationService(IConfiguration config)
    {
        _csvPath = config["TrackerCsv"] ?? Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
            "Desktop", "my-ai-job-search", "documents", "job_tracker.csv");
        LoadFromCsv();
    }

    private void LoadFromCsv()
    {
        _apps.Clear();
        if (!File.Exists(_csvPath)) return;
        try
        {
            using var reader = new StreamReader(_csvPath);
            using var csv = new CsvReader(reader, new CsvConfiguration(CultureInfo.InvariantCulture)
            {
                HeaderValidated = null,
                MissingFieldFound = null
            });
            var records = csv.GetRecords<dynamic>().ToList();
            int id = 1;
            foreach (var r in records)
            {
                var dict = (IDictionary<string, object>)r;
                _apps.Add(new JobApplication
                {
                    Id = id++,
                    Company     = GetVal(dict, "Company"),
                    Role        = GetVal(dict, "Role"),
                    Url         = GetVal(dict, "URL"),
                    Status      = GetVal(dict, "Status", "applied"),
                    FitScore    = double.TryParse(GetVal(dict, "FitScore"), out var s) ? s : 0,
                    Salary      = GetVal(dict, "Salary"),
                    Notes       = GetVal(dict, "Notes"),
                    DateApplied = DateTime.TryParse(GetVal(dict, "Date"), out var d) ? d : DateTime.Today,
                });
            }
            _nextId = _apps.Count + 1;
        }
        catch { /* If CSV is malformed, start fresh */ }
    }

    private static string GetVal(IDictionary<string, object> d, string key, string def = "")
        => d.TryGetValue(key, out var v) ? v?.ToString() ?? def : def;

    public List<JobApplication> GetAll() => _apps.OrderByDescending(a => a.DateApplied).ToList();

    public List<JobApplication> GetByStatus(string status)
        => _apps.Where(a => a.Status == status).OrderByDescending(a => a.DateApplied).ToList();

    public void Add(JobApplication app)
    {
        app.Id = _nextId++;
        _apps.Add(app);
        SaveToCsv();
    }

    public void Update(JobApplication app)
    {
        var existing = _apps.FirstOrDefault(a => a.Id == app.Id);
        if (existing != null)
        {
            existing.Status = app.Status;
            existing.Notes = app.Notes;
            existing.FitScore = app.FitScore;
            existing.InterviewDate = app.InterviewDate;
            existing.ColdEmailSent = app.ColdEmailSent;
            existing.CvTailored = app.CvTailored;
            existing.CoverLetterDone = app.CoverLetterDone;
        }
        SaveToCsv();
    }

    public void Delete(int id)
    {
        _apps.RemoveAll(a => a.Id == id);
        SaveToCsv();
    }

    private void SaveToCsv()
    {
        var dir = Path.GetDirectoryName(_csvPath);
        if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);
        using var writer = new StreamWriter(_csvPath);
        using var csv = new CsvWriter(writer, CultureInfo.InvariantCulture);
        csv.WriteHeader<CsvRow>();
        csv.NextRecord();
        foreach (var app in _apps)
        {
            csv.WriteRecord(new CsvRow
            {
                Date = app.DateApplied.ToString("yyyy-MM-dd"),
                Company = app.Company,
                Role = app.Role,
                URL = app.Url,
                Status = app.Status,
                FitScore = app.FitScore > 0 ? app.FitScore.ToString("F1") : "",
                Salary = app.Salary,
                Notes = app.Notes
            });
            csv.NextRecord();
        }
    }

    // Stats
    public int TotalCount => _apps.Count;
    public int InterviewCount => _apps.Count(a => a.Status == "interview");
    public int OfferCount => _apps.Count(a => a.Status == "offer");
    public int ColdEmailCount => _apps.Count(a => a.Status.StartsWith("cold_email"));
    public double AvgFitScore => _apps.Where(a => a.FitScore > 0).Select(a => a.FitScore).DefaultIfEmpty(0).Average();
    public double ResponseRate => TotalCount == 0 ? 0 : (double)(InterviewCount + OfferCount) / TotalCount * 100;
}

public class CsvRow
{
    public string Date { get; set; } = "";
    public string Company { get; set; } = "";
    public string Role { get; set; } = "";
    public string URL { get; set; } = "";
    public string Status { get; set; } = "";
    public string FitScore { get; set; } = "";
    public string Salary { get; set; } = "";
    public string Notes { get; set; } = "";
}
