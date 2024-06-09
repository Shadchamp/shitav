// Query to retrieve all systems and their associated CVEs
let systems = SecurityEvent
| where EventID == 4624 // Replace with the appropriate event ID for system logon events
| summarize LastLogonTime = max(TimeGenerated) by ComputerName;

let cves = SecurityAlert
| where VendorName == "CVE" // Replace with the appropriate vendor name for CVEs
| summarize CVEs = make_set(Title) by ComputerName;

// Join the systems and CVEs datasets
systems
| join kind=leftouter cves on ComputerName
| project ComputerName, LastLogonTime, CVEs