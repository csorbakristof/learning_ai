# Overview

detect_heating.py loads the JSON database and creates statistics about the status of the heating. There are two separate heating zones monitored by the devices T8_Z1 (zone 1) and T6_Z2 (zone 2). The heating is active if these devices indicate a temperature higher than 30 degrees Celsius. (temperature >= 30, hardcoded constant) The cycle finishes when the temperature drops below 30. If the time between two cycles would be shorter than 15 minutes, it should be considered as a single cycle (gap handling).

Data processing:
- Process every data point for the given devices in the database. Missing data should be "inactive heating".
- All timestamps are in the same timezone so do not take that into account. Weekdays and weekend days are not separated.
- If a heating cycle covers the midnight, it should belong to the first day.

Outputs:
- heating_cycles.json contains for both zones all time intervals when the heating is active. Format:
```
{
  "T8_Z1": [
    {"start": "2024-10-01T08:30:00", "end": "2024-10-01T10:15:00"},
    {"start": "2024-10-01T18:00:00", "end": "2024-10-01T22:30:00"}
  ],
  "T6_Z2": [...]
}
```
- heating_cycle_per_day_Z1.png and heating_cycle_per_day_Z2.png are diagrams showing for zone 1 and 2 the number of cycles per day. (Simple diagram with day (date) on horizontal axis and number of cycles on vertical axis.) 
