# Databricks Data Engineer Associate Certification Wiki - Schema

**Created:** 2026-09-09
**Purpose:** Personal knowledge base for Databricks Certified Data Engineer Associate exam preparation

## Wiki Structure

This wiki follows the LLM Wiki pattern with three layers:

### 1. Raw Sources (`/References`)
Immutable reference materials including:
- Official Databricks study guides (PDF)
- Practice exam questions
- Course materials and notebooks
- Supplementary documentation

### 2. The Wiki (`/Notes`)
LLM-generated knowledge base organized by topics:
- **Topics directory** - Subject-specific pages with concepts, examples, and cross-references
- **Index** - Content catalog organized by categories
- **Log** - Chronological learning progress

### 3. Schema (this file)
Configuration and workflow documentation

## Topic Categories

### Core Technologies
- **Delta Lake** - ACID transactions, time travel, optimization
- **Delta Live Tables (DLT)** - Pipeline creation, expectations, monitoring
- **Unity Catalog** - Governance, permissions, security

### Data Processing
- **Spark/PySpark** - DataFrames, transformations, optimization
- **Streaming** - Structured streaming, triggers, watermarks
- **Batch Processing** - Jobs, scheduling, performance

### Architecture & Patterns
- **Medallion Architecture** - Bronze, Silver, Gold layers
- **CDC & SCD** - Change data capture, slowly changing dimensions
- **Data Quality** - Expectations, constraints, monitoring

### Operations
- **Workflows** - Jobs, tasks, dependencies
- **Cost Optimization** - Clusters, auto-stop, serverless
- **Monitoring** - Metrics, alerts, debugging

## Workflows

### Ingest
Process reference materials (PDFs, documentation) to update 10-15 topic pages simultaneously:
1. Read source material
2. Extract key concepts
3. Update relevant topic pages
4. Add cross-references
5. Log progress in log.md

### Query
Answer questions from README or practice exams:
1. Search relevant topic pages
2. Synthesize answer with examples
3. Add cross-references to related topics
4. Optionally save as new topic section

### Lint
Health-check operations:
- Check for contradictions between topics
- Identify stale or outdated information
- Find orphaned pages without cross-references
- Detect missing cross-references
- Verify all 90 README questions have answers

## Page Structure

Each topic page should include:
- **Overview** - Brief description
- **Key Concepts** - Core ideas with definitions
- **Examples** - Code snippets and use cases
- **Common Pitfalls** - Mistakes to avoid
- **Exam Tips** - What to remember for the test
- **Cross-References** - Links to related topics
- **Sources** - References to original materials

## Maintenance

- Update log.md after each study session
- Cross-reference new insights across topics
- Track question coverage from README
- Mark completed vs. pending topics
