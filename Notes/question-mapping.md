# README Question Mapping

**Purpose:** Track coverage of all 90 README questions across topic pages
**Last Updated:** 2026-09-09

## Coverage Summary

- **Total Questions:** 90
- **Fully Covered:** 23
- **Partially Covered:** 12
- **Not Covered:** 55

## Question Mapping by Topic

### Delta Lake (13 questions)

| Q# | Question | Status | Location |
|----|----------|--------|----------|
| 1 | Why might data not be available in Delta table? | ✅ Covered | [delta-lake.md](topics/delta-lake.md) - VACUUM section |
| 2 | What does Delta Lake become in data platform? | ✅ Covered | [delta-lake.md](topics/delta-lake.md) - Overview |
| 3 | What does Delta table contain? | ✅ Covered | [delta-lake.md](topics/delta-lake.md) - Table Structure |
| 4 | Advantage of Delta Lake over traditional data lake? | ✅ Covered | [delta-lake.md](topics/delta-lake.md) - Advantages |
| 8 | Is Delta Lake ACID compliant? | ✅ Covered | [delta-lake.md](topics/delta-lake.md) - ACID Compliance |
| 9 | How to avoid duplicates when merging? | ✅ Covered | [delta-lake.md](topics/delta-lake.md) - MERGE Operations |
| 10 | What to consider with INSERT OVERWRITE? | ✅ Covered | [batch-processing.md](topics/batch-processing.md) - INSERT OVERWRITE |
| 11 | Purpose of Z-ordering? | ✅ Covered | [delta-lake.md](topics/delta-lake.md) - Optimization |
| 12 | Why might COPY INTO not work? | ✅ Covered | [batch-processing.md](topics/batch-processing.md) - COPY INTO |
| 20 | Delete metadata but retain data files? | ✅ Covered | [unity-catalog.md](topics/unity-catalog.md) - External Tables |
| 24 | Advantage of gold table over silver table? | ⚠️ Partial | Need medallion-architecture.md |
| 25 | Difference between bronze and raw table? | ⚠️ Partial | Need medallion-architecture.md |
| 26 | How to identify silver or bronze? | ⚠️ Partial | Need medallion-architecture.md |

### Delta Live Tables (9 questions)

| Q# | Question | Status | Location |
|----|----------|--------|----------|
| 13 | What happens with Expect or Drop on violation? | ✅ Covered | [delta-live-tables.md](topics/delta-live-tables.md) - Expectations |
| 21 | What happens when stream marked as "Streaming Live"? | ✅ Covered | [delta-live-tables.md](topics/delta-live-tables.md) - Streaming Live Status |
| 27 | How to create dependent tasks in DLT? | ✅ Covered | [delta-live-tables.md](topics/delta-live-tables.md) - Dependent Tasks |
| 30 | Where to see data quality metrics in DLT? | ✅ Covered | [delta-live-tables.md](topics/delta-live-tables.md) - Data Quality Monitoring |
| 31 | How to execute DLT pipeline? | ✅ Covered | [delta-live-tables.md](topics/delta-live-tables.md) - Pipeline Execution |
| 43 | How to check failed status of task in DLT? | ✅ Covered | [workflows.md](topics/workflows.md) - Checking Task Status |
| 35 | Refer Q40 practice exam | ❌ Not Covered | Need practice exam analysis |
| 36 | Refer Q1 practice exam | ❌ Not Covered | Need practice exam analysis |
| 37 | Refer Q3 practice exam | ❌ Not Covered | Need practice exam analysis |

### Unity Catalog (7 questions)

| Q# | Question | Status | Location |
|----|----------|--------|----------|
| 14 | When to use GRANT ALL PRIVILEGES? | ✅ Covered | [unity-catalog.md](topics/unity-catalog.md) - Permissions |
| 15 | When to use GRANT USAGE? | ✅ Covered | [unity-catalog.md](topics/unity-catalog.md) - Permissions |
| 19 | Which physical object for 10 tables for team sharing? | ✅ Covered | [unity-catalog.md](topics/unity-catalog.md) - Creating Objects |
| 22 | How to mark table as containing PII data? | ✅ Covered | [unity-catalog.md](topics/unity-catalog.md) - Marking PII |
| 23 | How to describe database to get path? | ✅ Covered | [unity-catalog.md](topics/unity-catalog.md) - Getting Database Path |
| 5 | Which component is web application part of? | ❌ Not Covered | Need workspace.md - Control vs Data plane |
| 6 | What operations outside of Databricks repo? | ❌ Not Covered | Need workspace.md - Repo operations |

### Streaming (4 questions)

| Q# | Question | Status | Location |
|----|----------|--------|----------|
| 17 | How to set processingTime to 5 seconds? | ✅ Covered | [streaming.md](topics/streaming.md) - Trigger Configuration |
| 18 | Configure streaming for continuous processing in production? | ✅ Covered | [streaming.md](topics/streaming.md) - Trigger Configuration |
| 41 | Refer Q27 practice exam | ❌ Not Covered | Need practice exam analysis |
| 42 | Refer Q33 practice exam | ❌ Not Covered | Need practice exam analysis |

### Workflows (4 questions)

| Q# | Question | Status | Location |
|----|----------|--------|----------|
| 29 | How to prevent code from running on Sundays? | ✅ Covered | [workflows.md](topics/workflows.md) - Scheduling |
| 44 | Webhook or email alert for triggers? | ✅ Covered | [workflows.md](topics/workflows.md) - Alerts |
| 7 | Advantage of repo over notebook versioning? | ❌ Not Covered | Need workspace.md - Version control |
| 43 | Check failed status of DLT task | ✅ Covered | [workflows.md](topics/workflows.md) - Task Status |

### Cost Optimization (6 questions)

| Q# | Question | Status | Location |
|----|----------|--------|----------|
| 32 | How to save costs using serverless or control DBU? | ✅ Covered | [cost-optimization.md](topics/cost-optimization.md) - Serverless |
| 33 | Manager concerned about over-costing, how to save? | ✅ Covered | [cost-optimization.md](topics/cost-optimization.md) - Checklist |
| 34 | How to reduce cluster costs? | ✅ Covered | [cost-optimization.md](topics/cost-optimization.md) - Auto-Stop |
| 45 | How to speed up query with cluster pools? | ✅ Covered | [cost-optimization.md](topics/cost-optimization.md) - Cluster Pools |
| 28 | How to speed up query execution? | ⚠️ Partial | [spark-fundamentals.md](topics/spark-fundamentals.md) - Performance |
| 45 | Cluster pools for speed and cost | ✅ Covered | [cost-optimization.md](topics/cost-optimization.md) - Cluster Pools |

### Spark/PySpark (6 questions)

| Q# | Question | Status | Location |
|----|----------|--------|----------|
| 16 | Advantage of using array functions? | ✅ Covered | [spark-fundamentals.md](topics/spark-fundamentals.md) - Array Functions |
| 38 | spark.table() vs spark.delta.table() vs spark.sql()? | ✅ Covered | [spark-fundamentals.md](topics/spark-fundamentals.md) - Accessing Tables |
| 39 | JDBC driver name for SQLite? | ✅ Covered | [spark-fundamentals.md](topics/spark-fundamentals.md) - JDBC |
| 40 | Create all_transaction from march and april without duplicates? | ✅ Covered | [spark-fundamentals.md](topics/spark-fundamentals.md) - Deduplication |
| 28 | Speed up query execution? | ⚠️ Partial | [spark-fundamentals.md](topics/spark-fundamentals.md) - Performance |
| 45 | Speed up with cluster pools? | ✅ Covered | Covered in cost-optimization.md |

### CDC & SCD (2 questions)

| Q# | Question | Status | Location |
|----|----------|--------|----------|
| 24 | Gold vs Silver table advantage? | ⚠️ Partial | Related to medallion architecture |
| 25 | Bronze vs raw table difference? | ⚠️ Partial | Related to medallion architecture |

### Practice Exam References (7 questions)

| Q# | Question | Status | Location |
|----|----------|--------|----------|
| 35 | Refer Q40 practice exam | ❌ Not Covered | Needs practice exam file analysis |
| 36 | Refer Q1 practice exam | ❌ Not Covered | Needs practice exam file analysis |
| 37 | Refer Q3 practice exam | ❌ Not Covered | Needs practice exam file analysis |
| 41 | Refer Q27 practice exam | ❌ Not Covered | Needs practice exam file analysis |
| 42 | Refer Q33 practice exam | ❌ Not Covered | Needs practice exam file analysis |
| 78 | Refer Q40 practice exam | ❌ Not Covered | Duplicate of Q35 |
| 79 | Refer Q1 practice exam | ❌ Not Covered | Duplicate of Q36 |
| 80 | Refer Q3 practice exam | ❌ Not Covered | Duplicate of Q37 |

### Uncategorized / Need New Topics (32 questions)

**Need workspace.md:**
- Q5: Web application component (control vs data plane)
- Q6: Operations outside repos (push, pull, clone, commit)
- Q7: Advantage of repo over notebook versioning

**Need medallion-architecture.md:**
- Q24: Advantage of gold over silver table
- Q25: Difference between bronze and raw table
- Q26: How to identify silver or bronze (Q31 practice exam)

**Need tables-views.md:**
- Q20: Delete metadata but keep data (covered partially in unity-catalog.md)
- General table types and operations

**Need monitoring.md:**
- Q30: Where to see DLT data quality metrics (covered in delta-live-tables.md)
- Q43: Check failed task status (covered in workflows.md)

**Need sql-syntax.md:**
- CREATE FLOW syntax reference
- SET CUSTOM TAG syntax reference
- STREAMING TABLE syntax reference

**Need exam-prep.md:**
- General exam strategy
- Time management
- Practice exam insights
- High-priority topics

**Remaining uncategorized questions (need to review practice exam PDFs):**
- Q35, Q36, Q37: Practice exam references
- Q41, Q42: Practice exam references
- Q78-Q90: Various topics requiring practice exam analysis

## Next Steps

1. ✅ Create remaining topic pages:
   - medallion-architecture.md
   - workspace.md
   - tables-views.md

2. ⏳ Analyze practice exam PDFs to answer reference questions

3. ⏳ Create quick reference pages:
   - sql-syntax.md
   - exam-prep.md

4. ⏳ Update log.md with progress

5. ⏳ Ingest reference PDFs to enrich existing topics
