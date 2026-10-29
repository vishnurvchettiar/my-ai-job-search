namespace JobSearchDashboard.Models;

public class JobApplication
{
    public int Id { get; set; }
    public string Company { get; set; } = "";
    public string Role { get; set; } = "";
    public string Url { get; set; } = "";
    public string Status { get; set; } = "applied";
    public double FitScore { get; set; }
    public string Salary { get; set; } = "";
    public string Notes { get; set; } = "";
    public DateTime DateApplied { get; set; } = DateTime.Today;
    public DateTime? InterviewDate { get; set; }
    public bool ColdEmailSent { get; set; }
    public bool CvTailored { get; set; }
    public bool CoverLetterDone { get; set; }

    public string StatusBadgeClass => Status switch
    {
        "applied"           => "badge-applied",
        "interview"         => "badge-interview",
        "offer"             => "badge-offer",
        "rejected"          => "badge-rejected",
        "cold_email_drafted"=> "badge-cold",
        "cold_email_sent"   => "badge-cold",
        "ready_to_send"     => "badge-ready",
        _                   => "badge-applied"
    };

    public string StatusIcon => Status switch
    {
        "applied"            => "📤",
        "interview"          => "🎤",
        "offer"              => "🎉",
        "rejected"           => "❌",
        "cold_email_drafted" => "✉️",
        "cold_email_sent"    => "📨",
        "ready_to_send"      => "⚡",
        _                    => "📋"
    };
}
