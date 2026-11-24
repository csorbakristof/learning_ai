# Neptun Course Metadata

Semester: **2026/27/1**  
Scope: **49 downloaded spreadsheets representing 28 distinct course codes** in
[`data/neptun_downloads_refresh_2026_11_24/`](./data/neptun_downloads_refresh_2026_11_24/).

“Presentation required” follows the requested rule: project-lab/project-task
courses require a presentation; BSc thesis courses and MSc Thesis 2
(`Diplomatervezés 2`) do not. Rows marked as inferred use course-code pairings
where an individual VIK course header was unavailable. “Yes” for the BProf
thesis course follows the stated exceptions literally: it is not a BSc thesis
or an MSc Thesis 2 course.

| Neptun course code | Official course title / course type | Degree or discipline | Presentation required? | Downloaded groups |
|---|---|---|---|---|
| `BMEVIAUAL01` | [Önálló laboratórium](https://portal.vik.bme.hu/kepzes/targyak/VIAUAL01/) | BSc IT engineering | Yes | AL, L |
| `BMEVIAUAL03` | [Önálló laboratórium](https://portal.vik.bme.hu/kepzes/targyak/VIAUAL03/) | BSc electrical engineering | Yes | AL, L |
| `BMEVIAUAL04` | BSc project laboratory (AUT category listing; no individual VIK header found) | BSc IT engineering | Yes | AL, L |
| `BMEVIAUAL05` | BSc project laboratory (AUT category listing; no individual VIK header found) | BSc electrical engineering | Yes | AL, L |
| `BMEVIAUAT00` | [Szakdolgozat-készítés](https://portal.vik.bme.hu/kepzes/targyak/VIAUAT00/) | BSc IT engineering | No | AGY, GY |
| `BMEVIAUAT01` | [Szakdolgozat-készítés](https://portal.vik.bme.hu/kepzes/targyak/VIAUAT01/) | BSc electrical engineering | No | AGY, Gy |
| `BMEVIAUAT02` | BSc thesis (AUT category listing; no individual VIK header found) | BSc IT engineering | No | AGY, GY |
| `BMEVIAUAT03` | BSc thesis (AUT category listing; no individual VIK header found) | BSc electrical engineering | No | AGY, GY |
| `BMEVIAUBL00` | [Önálló laboratórium](https://portal.vik.bme.hu/kepzes/targyak/VIAUBL00/) — cooperative education | IT engineering, BProf (`üzemmérnök-informatikus`) | Yes | L |
| `BMEVIAUBL01` | [Projektgyakorlat](https://portal.vik.bme.hu/kepzes/targyak/VIAUBL01/) — cooperative education | IT engineering, BProf (`üzemmérnök-informatikus`) | Yes | GY |
| `BMEVIAUBT00` | [Szakdolgozat-készítés](https://portal.vik.bme.hu/kepzes/targyak/VIAUBT00/) — BProf thesis project | IT engineering, BProf (`üzemmérnök-informatikus`) | Yes | GY |
| `BMEVIAUM039` | [Projektfeladat mechatronikusoknak](https://portal.vik.bme.hu/kepzes/targyak/VIAUM039/) | MSc mechatronics engineering | Yes | L |
| `BMEVIAUML10` | MSc project laboratory (AUT category listing; no individual VIK header found) | MSc IT engineering | Yes | AL, L |
| `BMEVIAUML11` | MSc project laboratory (AUT category listing; no individual VIK header found) | MSc IT engineering | Yes | AL, L |
| `BMEVIAUML12` | MSc project laboratory (AUT category listing; no individual VIK header found) | MSc electrical engineering | Yes | AL, L |
| `BMEVIAUML13` | MSc project laboratory (AUT category listing; no individual VIK header found) | MSc electrical engineering | Yes | AL, L |
| `BMEVIAUMSMDM01-00` | MSc thesis project 1 (inferred from code; no matching course header found) | Not identified in provided sources | Yes (inferred) | GY |
| `BMEVIAUMSMDM02-00` | MSc thesis project 2 (inferred from code; no matching course header found) | Not identified in provided sources | No (inferred) | GY |
| `BMEVIAUMSMPL01-00` | MSc project laboratory 1 (inferred from code; no matching course header found) | Not identified in provided sources | Yes (inferred) | L |
| `BMEVIAUMSMPL02-00` | MSc project laboratory 2 (inferred from code; no matching course header found) | Not identified in provided sources | Yes (inferred) | L |
| `BMEVIAUMT00` | [Diplomatervezés 1](https://portal.vik.bme.hu/kepzes/targyak/VIAUMT00/) | MSc IT engineering | Yes | AGY, Gy |
| `BMEVIAUMT01` | [Diplomatervezés 2](https://portal.vik.bme.hu/kepzes/targyak/VIAUMT01/) | MSc IT engineering | No | AGY, Gy |
| `BMEVIAUMT03` | [Diplomatervezés 2](https://portal.vik.bme.hu/kepzes/targyak/VIAUMT03/) | MSc electrical engineering | No | AGY, Gy |
| `BMEVIAUMT10` | MSc thesis course (stage inferred from paired codes; no individual VIK header found) | MSc IT engineering | Yes (inferred Thesis 1) | AGY, GY |
| `BMEVIAUMT11` | MSc thesis course (stage inferred from paired codes; no individual VIK header found) | MSc IT engineering | No (inferred Thesis 2) | AGY, GY |
| `BMEVIAUMT12` | MSc thesis course (stage inferred from paired codes; no individual VIK header found) | MSc electrical engineering | Yes (inferred Thesis 1) | AGY, GY |
| `BMEVIAUMT13` | MSc thesis course (stage inferred from paired codes; no individual VIK header found) | MSc electrical engineering | No (inferred Thesis 2) | AGY, GY |

## Classification notes and sources

- AUT category descriptions identify the relevant degree/discipline groups:
  [app3 topic collector README](./app3_topic_collector/README.md) and
  [topic collector specification](./specification/specification_topiccollector.md).
- The VIK course catalog and linked course headers were used for official
  titles and program labels:
  [VIK course catalog](https://portal.vik.bme.hu/kepzes/targyak/).
- The catalog/category pages reviewed did not identify a discipline or provide
  individual headers for the four `MSMDM`/`MSMPL` codes; their course-type and
  presentation labels above are code-based inferences, not verified catalog
  metadata.
- For `BMEVIAUMT10`–`13`, the AUT category lists identify the degree discipline;
  the Thesis 1/2 pairing is inferred because individual VIK headers were not
  found for those codes.
- The group values are the downloaded Neptun section/type suffixes. They are
  listed as downloaded, including differences in capitalization.
