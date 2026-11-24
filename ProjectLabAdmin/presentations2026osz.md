# Presentation Course Headcounts — 2026/27/1

Headcounts are based on the downloaded Neptun enrollment lists in
[`data/neptun_downloads_refresh_2026_11_24/`](./data/neptun_downloads_refresh_2026_11_24/).

## Reproducing the Neptun download

The lists were collected with `NeptunStudentDataCollector` in
[`app1_data_collector/dlnep_collector.py`](./app1_data_collector/dlnep_collector.py).
It opens the Neptun staff login in Chrome, then checks the course table for
courses whose code starts with `BMEVI`, whose requirement contains
`Évközi jegy`, and whose instructor field contains `Dr. Csorba Kristóf`.
Therefore, the actual selection is all matching courses in the logged-in
Neptun course list, not just courses explicitly named as project labs or thesis
courses.

To collect another semester's lists:

1. Open a PowerShell terminal and use the project's virtual environment.
2. Set the collector's download folder to a **new, empty, semester-specific
   folder**. The collector deletes existing Excel files in its configured
   download folder at the start of a run.
3. Run this from `ProjectLabAdmin`:

   ```powershell
   Set-Location 'E:\_learning_ai\ProjectLabAdmin\app1_data_collector'
   & '..\.venv\Scripts\python.exe' -c "from pathlib import Path; from dlnep_collector import NeptunStudentDataCollector; output = Path('..') / 'data' / 'neptun_downloads_YYYY_YY_T'; collector = NeptunStudentDataCollector(output); results = collector.collect_all_course_data(); print(f'Processed {len(results)} courses; downloaded {len(collector.downloaded_files)} files')"
   ```

   Replace `neptun_downloads_YYYY_YY_T` with a new folder name for the target
   semester (for example, `neptun_downloads_2027_28_1`).
4. Sign in yourself in the Chrome window, complete any required authentication,
   then press Enter in the PowerShell terminal when prompted. The collector
   navigates to the course list and exports each matching course roster as an
   Excel file.
5. Check the reported download count and confirm the new folder contains the
   expected `.xlsx` files before calculating headcounts.

Run the command in an interactive terminal so the login prompt can receive
Enter. Do not point the collector at a folder containing spreadsheets you want
to keep: its startup cleanup removes old Excel files there.

## Calculation and filtering criteria

1. Start with courses marked **Yes** for “Presentation required?” in
   [`course_metadata.md`](./course_metadata.md).
2. Exclude all BProf IT engineering courses: BProf students do not need to
   present for either of their courses. This overrides the metadata flags for
   `BMEVIAUBL00`, `BMEVIAUBL01`, and `BMEVIAUBT00`.
3. Count distinct Neptun student codes per included course, combining and
   deduplicating the course's downloaded groups. A student enrolled in more
   than one included course is counted once in each course; discipline totals
   sum those course headcounts and are not counts of globally unique students.
4. Keep courses with a headcount of zero in the course tables. Courses whose
   discipline is not identified in the available sources are listed separately
   and excluded from the IT, electrical, and mechatronics totals.

The totals below therefore represent course enrollments in presentation-required
courses, not unique students across all courses.

## By degree or discipline

### BSc IT engineering

| Course code | Headcount |
|---|---:|
| `BMEVIAUAL01` | 1 |
| `BMEVIAUAL04` | 11 |
| **BSc IT engineering total** | **12** |

### BSc electrical engineering

| Course code | Headcount |
|---|---:|
| `BMEVIAUAL03` | 0 |
| `BMEVIAUAL05` | 0 |
| **BSc electrical engineering total** | **0** |

### MSc IT engineering

| Course code | Headcount |
|---|---:|
| `BMEVIAUML10` | 24 |
| `BMEVIAUML11` | 35 |
| `BMEVIAUMT00` | 0 |
| `BMEVIAUMT10` | 21 |
| **MSc IT engineering total** | **80** |

### MSc electrical engineering

| Course code | Headcount |
|---|---:|
| `BMEVIAUML12` | 5 |
| `BMEVIAUML13` | 18 |
| `BMEVIAUMT12` | 12 |
| **MSc electrical engineering total** | **35** |

### MSc mechatronics engineering

| Course code | Headcount |
|---|---:|
| `BMEVIAUM039` | 4 |
| **MSc mechatronics engineering total** | **4** |

### Discipline not identified in the sources

These course codes were classified as unknown in the course metadata. Their
course-type labels and presentation flags are inferred from the codes.

| Course code | Headcount |
|---|---:|
| `BMEVIAUMSMDM01-00` | 0 |
| `BMEVIAUMSMPL01-00` | 3 |
| `BMEVIAUMSMPL02-00` | 0 |
| **Unclassified total** | **3** |

## Headcount totals by discipline

| Discipline | Included course levels | Total headcount |
|---|---|---:|
| IT engineering | BSc, MSc | **92** |
| Electrical engineering | BSc, MSc | **35** |
| Mechatronics engineering | MSc | **4** |
| Not identified in sources | MSc course codes with unverified discipline | **3** |
| **All presentation-required courses** |  | **134** |

# Room reservations for the presentations

| Room | Day | Time interval |
|---|---|---:|
| QBF14 | Monday | 8-16 |
| QBF15 | Monday | 10-16 |
| QBF14 | Tuesday | 8-12 |
| QBF15 | Tuesday | 8-12 |
| QBF14 | Wednesday | 8-16 |
| QBF15 | Wednesday | 8-16 |
