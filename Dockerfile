# ─── Build Stage ───────────────────────────────────────────────
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

COPY dashboard/JobSearchDashboard/JobSearchDashboard.csproj dashboard/JobSearchDashboard/
RUN dotnet restore dashboard/JobSearchDashboard/JobSearchDashboard.csproj

COPY dashboard/JobSearchDashboard/ dashboard/JobSearchDashboard/
RUN dotnet publish dashboard/JobSearchDashboard/JobSearchDashboard.csproj \
    -c Release -o /app/publish --no-restore

# ─── Runtime Stage ─────────────────────────────────────────────
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime
WORKDIR /app

# Copy published output
COPY --from=build /app/publish .

# Create data directory for job tracker CSV
RUN mkdir -p /data/documents

# Environment
ENV ASPNETCORE_ENVIRONMENT=Production
ENV ASPNETCORE_URLS=http://+:10000
ENV TrackerCsv=/data/documents/job_tracker.csv

EXPOSE 10000
ENTRYPOINT ["dotnet", "JobSearchDashboard.dll"]
