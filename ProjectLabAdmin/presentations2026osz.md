# Presentation Course Headcounts — 2026/27/1

Headcounts are based on the downloaded Neptun enrollment lists in
[`data/neptun_downloads_refresh_2026_11_24/`](./data/neptun_downloads_refresh_2026_11_24/).
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

