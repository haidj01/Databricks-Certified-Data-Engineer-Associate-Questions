# Databricks Certified Data Engineer Associate
## Week 9–10 Study Guide: Official Documentation References

**Week Focus:** Domain 4 & 5: Lakeflow Jobs (16%) + Implementing CI/CD (10%)  
**Updated:** August 2026  
**Exam Version:** May 2026 Exam Guide

---

## Table of Contents

- [Lakeflow Jobs Fundamentals](#lakeflow-jobs-fundamentals)
- [Task Types](#task-types)
- [Job DAG & Dependencies](#job-dag--dependencies)
- [Control Flow & Branching](#control-flow--branching)
- [Triggers & Scheduling](#triggers--scheduling)
- [Job Monitoring & Management](#job-monitoring--management)
- [Serverless Jobs (NEW 2026)](#serverless-jobs-new-2026)
- [Git Folders](#git-folders)
- [Declarative Automation Bundles (DABs)](#declarative-automation-bundles-dabs)
- [Bundle Configuration & Deployment](#bundle-configuration--deployment)
- [Databricks CLI](#databricks-cli)
- [CI/CD Best Practices](#cicd-best-practices)
- [Release Notes & Updates](#release-notes--updates)

---

## Lakeflow Jobs Fundamentals

### Lakeflow Jobs Overview

| Topic | URL | Notes |
|-------|-----|-------|
| **Lakeflow Jobs Introduction** | https://docs.databricks.com/en/jobs/index.html | Core concept |
| **Lakeflow Jobs (formerly Workflows)** | https://docs.databricks.com/en/jobs/index.html | Renamed 2026 |
| **Job vs Cluster Concepts** | https://docs.databricks.com/en/jobs/index.html | Key differences |
| **Job vs All-Purpose Cluster** | https://docs.databricks.com/en/jobs/index.html | Use case guide |
| **Lakeflow Jobs Architecture** | https://docs.databricks.com/en/jobs/index.html | How it works |

### Creating & Managing Jobs

| Topic | URL | Notes |
|-------|-----|-------|
| **Create a Lakeflow Job** | https://docs.databricks.com/en/jobs/jobs-quickstart.html | Quick start |
| **Job Configuration** | https://docs.databricks.com/en/jobs/index.html | Settings & options |
| **Job Naming & Description** | https://docs.databricks.com/en/jobs/index.html | Best practices |
| **Job Permissions** | https://docs.databricks.com/en/jobs/index.html | Access control |
| **Clone a Job** | https://docs.databricks.com/en/jobs/index.html | Duplicate job |
| **Edit a Running Job** | https://docs.databricks.com/en/jobs/index.html | Update parameters |
| **Delete a Job** | https://docs.databricks.com/en/jobs/index.html | Cleanup |

### Job UI & Navigation

| Topic | URL | Notes |
|-------|-----|-------|
| **Lakeflow Jobs UI** | https://docs.databricks.com/en/jobs/index.html | Web interface |
| **Jobs Sidebar & Tabs** | https://docs.databricks.com/en/jobs/index.html | UI components |
| **Job Details Page** | https://docs.databricks.com/en/jobs/index.html | Runs, config, history |
| **Runs Tab** | https://docs.databricks.com/en/jobs/index.html | Execution history |

---

## Task Types

### Core Task Types

| Topic | URL | Notes |
|-------|-----|-------|
| **Notebook Task** | https://docs.databricks.com/en/jobs/task-types.html | Execute notebook |
| **SQL Task** | https://docs.databricks.com/en/jobs/task-types.html | Run SQL query/file |
| **Python Task** | https://docs.databricks.com/en/jobs/task-types.html | Execute Python script |
| **JAR Task** | https://docs.databricks.com/en/jobs/task-types.html | Run JAR file |
| **Python Wheel Task** | https://docs.databricks.com/en/jobs/task-types.html | Package distribution |
| **Spark Submit Task** | https://docs.databricks.com/en/jobs/task-types.html | spark-submit command |

### Specialized Task Types

| Topic | URL | Notes |
|-------|-----|-------|
| **Pipeline Task (Lakeflow)** | https://docs.databricks.com/en/jobs/task-types.html | Run Lakeflow pipeline |
| **Dashboard Task (NEW)** | https://docs.databricks.com/en/jobs/task-types.html | Refresh dashboard |
| **dbt Task** | https://docs.databricks.com/en/jobs/task-types.html | Run dbt project |
| **AI Runtime Task (NEW)** | https://docs.databricks.com/en/jobs/task-types.html | Generative AI models |
| **SQL Alert Task (NEW)** | https://docs.databricks.com/en/release-notes/dev-tools/bundles.html | Monitor/alert |

### Notebook Task Specifics

| Topic | URL | Notes |
|-------|-----|-------|
| **Notebook Parameters** | https://docs.databricks.com/en/jobs/task-types.html | Pass parameters |
| **Base Parameters** | https://docs.databricks.com/en/jobs/task-types.html | Databricks variables |
| **Notebook Widget Integration** | https://docs.databricks.com/en/notebooks/index.html | Interactive parameters |
| **dbutils.widgets.get()** | https://docs.databricks.com/en/notebooks/index.html | Retrieve parameters |

### SQL Task Specifics

| Topic | URL | Notes |
|-------|-----|-------|
| **SQL File vs Query** | https://docs.databricks.com/en/jobs/task-types.html | Configuration options |
| **SQL Warehouse Selection** | https://docs.databricks.com/en/jobs/task-types.html | Compute selection |
| **Alert on Results** | https://docs.databricks.com/en/jobs/task-types.html | Output handling |

### Python Task Specifics

| Topic | URL | Notes |
|-------|-----|-------|
| **Python Script Execution** | https://docs.databricks.com/en/jobs/task-types.html | File or inline |
| **Command Line Arguments** | https://docs.databricks.com/en/jobs/task-types.html | Pass args |
| **Dependencies** | https://docs.databricks.com/en/jobs/task-types.html | Libraries & wheels |

---

## Job DAG & Dependencies

### DAG Basics

| Topic | URL | Notes |
|-------|-----|-------|
| **DAG (Directed Acyclic Graph)** | https://docs.databricks.com/en/jobs/index.html | Job structure |
| **Multiple Tasks in One Job** | https://docs.databricks.com/en/jobs/index.html | Define tasks |
| **Task Definitions** | https://docs.databricks.com/en/jobs/index.html | Task configuration |

### Task Dependencies

| Topic | URL | Notes |
|-------|-----|-------|
| **depends_on Clause** | https://docs.databricks.com/en/jobs/task-dependencies.html | Define dependencies |
| **Serial Execution** | https://docs.databricks.com/en/jobs/task-dependencies.html | Sequential tasks |
| **Parallel Execution** | https://docs.databricks.com/en/jobs/task-dependencies.html | Concurrent tasks |
| **Fan-Out Pattern** | https://docs.databricks.com/en/jobs/task-dependencies.html | One → multiple |
| **Fan-In Pattern** | https://docs.databricks.com/en/jobs/task-dependencies.html | Multiple → one |

### DAG Visualization

| Topic | URL | Notes |
|-------|-----|-------|
| **View DAG in UI** | https://docs.databricks.com/en/jobs/index.html | Graph visualization |
| **DAG Execution Flow** | https://docs.databricks.com/en/jobs/task-dependencies.html | Runtime behavior |
| **Task Status** | https://docs.databricks.com/en/jobs/index.html | Running, succeeded, failed |

---

## Control Flow & Branching

### Conditionals (if/else)

| Topic | URL | Notes |
|-------|-----|-------|
| **Conditional Tasks** | https://docs.databricks.com/en/jobs/control-flow.html | if/else branching |
| **run_if Clause** | https://docs.databricks.com/en/jobs/control-flow.html | Task condition |
| **Task Outcomes** | https://docs.databricks.com/en/jobs/control-flow.html | Success/failure evaluation |

### Retries & Error Handling

| Topic | URL | Notes |
|-------|-----|-------|
| **max_retries** | https://docs.databricks.com/en/jobs/control-flow.html | Retry count |
| **min_retry_interval_secs** | https://docs.databricks.com/en/jobs/control-flow.html | Retry delay |
| **timeout_seconds** | https://docs.databricks.com/en/jobs/control-flow.html | Task timeout |
| **on_failure** | https://docs.databricks.com/en/jobs/control-flow.html | Failure handler |

### For Each Loop

| Topic | URL | Notes |
|-------|-----|-------|
| **For Each Task** | https://docs.databricks.com/en/jobs/control-flow.html | Iterate over values |
| **Iteration Variable** | https://docs.databricks.com/en/jobs/control-flow.html | Loop parameter |
| **Dynamic Task Generation** | https://docs.databricks.com/en/jobs/control-flow.html | Variable-length loop |

### Email Notifications

| Topic | URL | Notes |
|-------|-----|-------|
| **on_success Email** | https://docs.databricks.com/en/jobs/control-flow.html | Success notification |
| **on_failure Email** | https://docs.databricks.com/en/jobs/control-flow.html | Failure notification |
| **Email Recipients** | https://docs.databricks.com/en/jobs/control-flow.html | Configure recipients |

---

## Triggers & Scheduling

### Scheduled Triggers

| Topic | URL | Notes |
|-------|-----|-------|
| **Cron Schedule** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Cron syntax |
| **Cron Expression Format** | https://docs.databricks.com/en/jobs/schedule-jobs.html | minute hour day-of-month etc. |
| **Pause/Resume Schedule** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Enable/disable |
| **Timezone Support** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Timezone handling |

### File Arrival Triggers

| Topic | URL | Notes |
|-------|-----|-------|
| **File Arrival Trigger** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Event-based |
| **S3 File Arrival** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Cloud storage |
| **Azure Blob Storage** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Event notification |
| **GCS File Arrival** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Google Cloud |

### Table Update Triggers

| Topic | URL | Notes |
|-------|-----|-------|
| **Table Update Trigger** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Data-driven |
| **Monitor Delta Table** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Trigger on write |
| **Polling Configuration** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Check frequency |

### Manual Triggers

| Topic | URL | Notes |
|-------|-----|-------|
| **On Demand Execution** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Manual run |
| **Run Job Now** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Immediate execution |
| **Run with Parameters** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Override settings |

### Trigger Best Practices

| Topic | URL | Notes |
|-------|-----|-------|
| **Polling vs Events** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Tradeoffs |
| **Timezone & Scheduling** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Global considerations |

---

## Job Monitoring & Management

### Monitoring Lakeflow Jobs

| Topic | URL | Notes |
|-------|-----|-------|
| **Monitor Lakeflow Jobs** | https://docs.databricks.com/en/jobs/monitor.html | Overview page |
| **Run History** | https://docs.databricks.com/en/jobs/monitor.html | Past executions |
| **Run Details** | https://docs.databricks.com/en/jobs/monitor.html | Drill-down metrics |

### Metrics & Logs

| Topic | URL | Notes |
|-------|-----|-------|
| **Job Execution Metrics** | https://docs.databricks.com/en/jobs/monitor.html | Duration, start time |
| **Task Execution Time** | https://docs.databricks.com/en/jobs/monitor.html | Per-task metrics |
| **Task Logs** | https://docs.databricks.com/en/jobs/monitor.html | Output/error logs |
| **Log Retention** | https://docs.databricks.com/en/jobs/monitor.html | How long stored |

### Spark UI Integration

| Topic | URL | Notes |
|-------|-----|-------|
| **View Spark UI from Job Run** | https://docs.databricks.com/en/jobs/monitor.html | Access Spark UI |
| **Spark Driver & Executors** | https://docs.databricks.com/en/jobs/monitor.html | Compute resources |
| **Job Cluster Tracking** | https://docs.databricks.com/en/jobs/monitor.html | Instance details |

### Job Status & Health

| Topic | URL | Notes |
|-------|-----|-------|
| **Job Run Status** | https://docs.databricks.com/en/jobs/monitor.html | Running, success, failure |
| **Failed Task Identification** | https://docs.databricks.com/en/jobs/monitor.html | Which task failed? |
| **Partial Success** | https://docs.databricks.com/en/jobs/control-flow.html | Some tasks complete |

### System Tables for Jobs

| Topic | URL | Notes |
|-------|-----|-------|
| **Jobs System Tables** | https://docs.databricks.com/en/admin/system-tables/jobs.html | Query job history |
| **Query Run Metrics** | https://docs.databricks.com/en/admin/system-tables/jobs.html | Analytics |
| **Audit Trail** | https://docs.databricks.com/en/admin/system-tables/jobs.html | Compliance |

---

## Serverless Jobs (NEW 2026)

### Serverless Jobs Overview

| Topic | URL | Notes |
|-------|-----|-------|
| **Serverless Jobs Introduction** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | 2026 feature |
| **Serverless Compute for Jobs** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | Default in UC |
| **Serverless vs Job Cluster** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | Comparison |

### Serverless Configuration

| Topic | URL | Notes |
|-------|-----|-------|
| **Enable Serverless Jobs** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | Setup steps |
| **Serverless Task Configuration** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | Task settings |
| **Compute Requirements** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | No explicit cluster needed |

### Serverless Benefits & Tradeoffs

| Topic | URL | Notes |
|-------|-----|-------|
| **Fast Startup** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | < 3 seconds |
| **Cost Model** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | Per-second execution |
| **Automatic Scaling** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | Built-in |
| **Limitations** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | When not suitable |

---

## Git Folders

### Git Folders Basics

| Topic | URL | Notes |
|-------|-----|-------|
| **Git Folders Overview** | https://docs.databricks.com/en/repos/index.html | Git integration |
| **Formerly Databricks Repos** | https://docs.databricks.com/en/repos/what-happened-repos.html | Renamed feature |
| **What Happened to Repos?** | https://docs.databricks.com/en/repos/what-happened-repos.html | Migration guide |

### Creating & Cloning Git Folders

| Topic | URL | Notes |
|-------|-----|-------|
| **Create Git Folder** | https://docs.databricks.com/en/repos/create-repo.html | From GitHub |
| **Clone Repository** | https://docs.databricks.com/en/repos/create-repo.html | Link to repo |
| **Connect GitHub Account** | https://docs.databricks.com/en/repos/create-repo.html | Authentication |
| **Support Git Providers** | https://docs.databricks.com/en/repos/create-repo.html | GitHub, GitLab, etc. |

### Git Operations in Databricks

| Topic | URL | Notes |
|-------|-----|-------|
| **Git Folder Structure** | https://docs.databricks.com/en/repos/git-operations.html | File organization |
| **View Files in Git Folder** | https://docs.databricks.com/en/repos/git-operations.html | Notebook browser |
| **Commit Changes** | https://docs.databricks.com/en/repos/git-operations.html | Save to repo |
| **Push to Remote** | https://docs.databricks.com/en/repos/git-operations.html | Sync with GitHub |
| **Pull from Remote** | https://docs.databricks.com/en/repos/git-operations.html | Get latest |
| **Branches** | https://docs.databricks.com/en/repos/git-operations.html | Create/switch branches |
| **Checkout Branch** | https://docs.databricks.com/en/repos/git-operations.html | Switch versions |

### Pull Requests & Code Review

| Topic | URL | Notes |
|-------|-----|-------|
| **Pull Requests from Databricks** | https://docs.databricks.com/en/repos/git-operations.html | Create PR |
| **Review in GitHub** | https://docs.databricks.com/en/repos/git-operations.html | Standard PR flow |
| **Merge PR** | https://docs.databricks.com/en/repos/git-operations.html | Accept changes |

---

## Declarative Automation Bundles (DABs)

### DABs Overview

| Topic | URL | Notes |
|-------|-----|-------|
| **Declarative Automation Bundles Overview** | https://docs.databricks.com/en/dev-tools/bundles/index.html | IaC for Databricks |
| **Formerly Databricks Asset Bundles** | https://docs.databricks.com/en/dev-tools/bundles/index.html | Renamed (March 2026) |
| **DABs Purpose** | https://docs.databricks.com/en/dev-tools/bundles/index.html | Why use DABs? |
| **YAML Configuration** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Bundle syntax |

### Bundle Structure

| Topic | URL | Notes |
|-------|-----|-------|
| **Bundle Root Directory** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Project structure |
| **databricks.yml** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Main config file |
| **Environment Folders** | https://docs.databricks.com/en/dev-tools/bundles/config.html | dev, staging, prod |
| **Resources** | https://docs.databricks.com/en/dev-tools/bundles/resources.html | Jobs, pipelines, models |

### Bundle Configuration

| Topic | URL | Notes |
|-------|-----|-------|
| **Bundle Config Syntax** | https://docs.databricks.com/en/dev-tools/bundles/config.html | YAML structure |
| **Variables in Bundles** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Parameterization |
| **Variable Definition** | https://docs.databricks.com/en/dev-tools/bundles/config.html | default, prompt, value |
| **Variable Substitution** | https://docs.databricks.com/en/dev-tools/bundles/config.html | ${var.name} syntax |
| **Environment Override** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Override per env |

### Bundle Resources

| Topic | URL | Notes |
|-------|-----|-------|
| **Jobs Resource** | https://docs.databricks.com/en/dev-tools/bundles/resources.html | Define jobs in DAB |
| **Pipeline Resource** | https://docs.databricks.com/en/dev-tools/bundles/resources.html | Lakeflow pipelines |
| **Model Resource** | https://docs.databricks.com/en/dev-tools/bundles/resources.html | ML models |
| **Dashboard Resource** | https://docs.databricks.com/en/dev-tools/bundles/resources.html | SQL dashboards |
| **Notebook Resource** | https://docs.databricks.com/en/dev-tools/bundles/resources.html | Notebooks |

### Environment Management

| Topic | URL | Notes |
|-------|-----|-------|
| **Environments in DABs** | https://docs.databricks.com/en/dev-tools/bundles/config.html | dev/test/prod |
| **Environment-Specific Config** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Override settings |
| **Include Paths** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Modular config |
| **Validation per Environment** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Pre-deployment check |

### DAB Templates

| Topic | URL | Notes |
|-------|-----|-------|
| **Bundle Templates** | https://docs.databricks.com/en/dev-tools/bundles/tutorials.html | Starter examples |
| **Example Bundles** | https://docs.databricks.com/en/dev-tools/bundles/tutorials.html | Reference projects |
| **Best Practices** | https://docs.databricks.com/en/dev-tools/bundles/tutorials.html | Design patterns |

---

## Bundle Configuration & Deployment

### Deploying Bundles

| Topic | URL | Notes |
|-------|-----|-------|
| **Deploy Process** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Full workflow |
| **Test Deploy (Dry Run)** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Plan without executing |
| **Deploy to Workspace** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Apply changes |
| **Incremental Deploy** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Update only changes |

### Deployment Hooks

| Topic | URL | Notes |
|-------|-----|-------|
| **Pre-Deploy Hooks** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Before deployment |
| **Post-Deploy Hooks** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | After deployment |
| **Script Execution** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Custom logic |

### Rollback & Troubleshooting

| Topic | URL | Notes |
|-------|-----|-------|
| **Bundle Validation** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Syntax check |
| **Deployment Errors** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Common issues |
| **Rollback Strategy** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Undo changes |

---

## Databricks CLI

### CLI Setup & Authentication

| Topic | URL | Notes |
|-------|-----|-------|
| **Databricks CLI Installation** | https://docs.databricks.com/en/dev-tools/cli/index.html | Setup guide |
| **Configure Authentication** | https://docs.databricks.com/en/dev-tools/cli/index.html | Token, PAT, etc. |
| **CLI Profile Configuration** | https://docs.databricks.com/en/dev-tools/cli/index.html | Multiple profiles |
| **Environment Variables** | https://docs.databricks.com/en/dev-tools/cli/index.html | Auth via env |

### Bundle Commands

| Topic | URL | Notes |
|-------|-----|-------|
| **bundle validate** | https://docs.databricks.com/en/dev-tools/cli/index.html | Check syntax |
| **bundle deploy** | https://docs.databricks.com/en/dev-tools/cli/index.html | Deploy to workspace |
| **bundle run** | https://docs.databricks.com/en/dev-tools/cli/index.html | Execute job from bundle |
| **bundle destroy** | https://docs.databricks.com/en/dev-tools/cli/index.html | Remove deployed resources |

### Other CLI Commands

| Topic | URL | Notes |
|-------|-----|-------|
| **jobs** Command | https://docs.databricks.com/en/dev-tools/cli/index.html | Job management |
| **runs** Command | https://docs.databricks.com/en/dev-tools/cli/index.html | Run history |
| **fs** Command | https://docs.databricks.com/en/dev-tools/cli/index.html | File operations |
| **configure** Command | https://docs.databricks.com/en/dev-tools/cli/index.html | Set up CLI |

### CLI Scripting

| Topic | URL | Notes |
|-------|-----|-------|
| **CLI in Scripts** | https://docs.databricks.com/en/dev-tools/cli/index.html | Automation |
| **Exit Codes** | https://docs.databricks.com/en/dev-tools/cli/index.html | Error handling |
| **JSON Output** | https://docs.databricks.com/en/dev-tools/cli/index.html | Parse results |

---

## CI/CD Best Practices

### CI/CD Pipeline with Git Folders

| Topic | URL | Notes |
|-------|-----|-------|
| **CI/CD Overview** | https://docs.databricks.com/en/repos/ci-cd.html | Databricks workflow |
| **Development Branch** | https://docs.databricks.com/en/repos/ci-cd.html | Local development |
| **Testing Branch** | https://docs.databricks.com/en/repos/ci-cd.html | Pre-production |
| **Production Branch** | https://docs.databricks.com/en/repos/ci-cd.html | Live deployment |

### Branch Strategy

| Topic | URL | Notes |
|-------|-----|-------|
| **Feature Branching** | https://docs.databricks.com/en/repos/ci-cd.html | Per-feature development |
| **Pull Request Workflow** | https://docs.databricks.com/en/repos/ci-cd.html | Code review process |
| **Merge to Staging** | https://docs.databricks.com/en/repos/ci-cd.html | Pre-production test |
| **Merge to Production** | https://docs.databricks.com/en/repos/ci-cd.html | Final deployment |

### Integration with Lakeflow Jobs

| Topic | URL | Notes |
|-------|-----|-------|
| **Job Definition from Git** | https://docs.databricks.com/en/repos/ci-cd.html | Source control jobs |
| **Deploy Jobs via DABs** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Infrastructure as code |
| **Environment Promotion** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | dev → staging → prod |

### Testing & Validation

| Topic | URL | Notes |
|-------|-----|-------|
| **Unit Testing Notebooks** | https://docs.databricks.com/en/repos/ci-cd.html | Test framework |
| **Integration Testing** | https://docs.databricks.com/en/repos/ci-cd.html | End-to-end tests |
| **Data Validation** | https://docs.databricks.com/en/repos/ci-cd.html | Quality checks |
| **Pre-Deployment Tests** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Validation before deploy |

### Automation Tools

| Topic | URL | Notes |
|-------|-----|-------|
| **GitHub Actions + Databricks** | https://docs.databricks.com/en/repos/ci-cd.html | External CI/CD |
| **Jenkins Integration** | https://docs.databricks.com/en/repos/ci-cd.html | Jenkins pipelines |
| **GitLab CI/CD** | https://docs.databricks.com/en/repos/ci-cd.html | GitLab runners |
| **CLI in CI/CD** | https://docs.databricks.com/en/dev-tools/cli/index.html | Automate with CLI |

### Best Practices

| Topic | URL | Notes |
|-------|-----|-------|
| **Version Pinning** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Lock dependencies |
| **Secrets Management** | https://docs.databricks.com/en/dev-tools/cli/index.html | Credential security |
| **Audit & Logging** | https://docs.databricks.com/en/repos/ci-cd.html | Track changes |
| **Rollback Procedures** | https://docs.databricks.com/en/repos/ci-cd.html | Undo deployments |

---

## Release Notes & Updates

### Lakeflow Jobs Updates

| Topic | URL | Notes |
|-------|-----|-------|
| **Serverless Jobs (2026)** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | NEW feature |
| **Dashboard Task (NEW)** | https://docs.databricks.com/en/release-notes/dev-tools/bundles.html | Refresh dashboards |
| **AI Runtime Task (NEW)** | https://docs.databricks.com/en/release-notes/dev-tools/bundles.html | Generative AI |
| **SQL Alert Task (NEW)** | https://docs.databricks.com/en/release-notes/dev-tools/bundles.html | Monitoring alerts |
| **Query-Based Connectors** | https://docs.databricks.com/en/jobs/task-types.html | NEW pipeline task |

### DABs & CI/CD Updates

| Topic | URL | Notes |
|-------|-----|-------|
| **DABs Renamed (March 2026)** | https://docs.databricks.com/en/dev-tools/bundles/index.html | Asset → Automation Bundles |
| **Template Library** | https://docs.databricks.com/en/dev-tools/bundles/tutorials.html | Starter examples |
| **Environment Support** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Multi-env management |

### Git Folders Updates

| Topic | URL | Notes |
|-------|-----|-------|
| **Repos Renamed to Git Folders** | https://docs.databricks.com/en/repos/what-happened-repos.html | Name change only |
| **GitLab Support** | https://docs.databricks.com/en/repos/create-repo.html | Third-party providers |
| **Bitbucket Support** | https://docs.databricks.com/en/repos/create-repo.html | Additional providers |

### Runtime Support

| Topic | URL | Notes |
|-------|-----|-------|
| **Databricks Runtime 17.0** | https://docs.databricks.com/en/release-notes/runtime/17.0.html | Latest features |
| **Databricks Runtime 16.4 LTS** | https://docs.databricks.com/en/release-notes/runtime/16.4lts.html | Long-term support |

---

## Week 9–10 Decision Framework

### When to Use Lakeflow Jobs vs Pipelines

| Scenario | Use | Advantage | Reference |
|----------|-----|-----------|-----------|
| **Scheduled ETL task** | Lakeflow Job | Simple, multi-task DAG | https://docs.databricks.com/en/jobs/index.html |
| **Incremental data processing** | Streaming Table | Exactly-once, low latency | https://docs.databricks.com/en/lakeflow/pipelines/streaming-tables.html |
| **Complex multi-stage pipeline** | Lakeflow Job with DAG | Flexible control flow | https://docs.databricks.com/en/jobs/task-dependencies.html |
| **Serverless, no-config compute** | Serverless Job (2026) | Cost-effective, instant start | https://docs.databricks.com/en/jobs/run-serverless-jobs.html |

### When to Use Git Folders vs DABs

| Scenario | Use | Advantage | Reference |
|----------|-----|-----------|-----------|
| **Version control notebooks/code** | Git Folders | Pure git, human-readable | https://docs.databricks.com/en/repos/index.html |
| **Declarative infra as code** | DABs | Automated deployment, variables | https://docs.databricks.com/en/dev-tools/bundles/index.html |
| **CI/CD automation** | DABs + CLI | Full pipeline automation | https://docs.databricks.com/en/dev-tools/bundles/deploy.html |
| **Code review workflow** | Git Folders | Standard GitHub flow | https://docs.databricks.com/en/repos/ci-cd.html |

---

## Exam Focus Areas (Domain 4–5)

### Domain 4: Heavily Tested Topics (20–25% of Domain 4 questions)

1. **Lakeflow Jobs Fundamentals** (10–12 questions)
   - Create, configure, manage jobs
   - Task types (notebook, SQL, Python, pipeline)
   - Permissions & access

2. **Task Dependencies & DAG** (8–10 questions)
   - Define depends_on relationships
   - Serial vs parallel execution
   - Fan-out/fan-in patterns

3. **Control Flow & Branching** (6–8 questions)
   - run_if conditions
   - Retries & timeouts
   - For Each loops

4. **Triggers & Scheduling** (8–10 questions)
   - Cron syntax
   - File/table triggers
   - Scheduling best practices

5. **Serverless Jobs (NEW 2026)** (5–7 questions)
   - Advantages (speed, cost)
   - When to use serverless
   - Configuration

### Domain 5: Heavily Tested Topics (20–25% of Domain 5 questions)

6. **Git Folders & Branching** (6–8 questions)
   - Create, clone, commit
   - Push/pull operations
   - Branch management

7. **DABs Configuration** (8–10 questions)
   - YAML syntax
   - Variables & environments
   - Resource definitions

8. **Bundle Deployment** (6–8 questions)
   - Validate & deploy
   - Environment overrides
   - Rollback procedures

9. **Databricks CLI** (5–7 questions)
   - Setup & authentication
   - Bundle commands
   - Script automation

10. **CI/CD Workflow** (5–7 questions)
    - Branch strategy
    - PR workflow
    - Environment promotion

### Exam Tip Questions

**Q: You want to run 10 data quality checks in parallel, then 1 final merge job. Which pattern?**
→ Answer: Fan-out (10 parallel) → Fan-in (1 merge task)  
→ Reference: https://docs.databricks.com/en/jobs/task-dependencies.html

**Q: A notebook task fails 3 times. Should you retry indefinitely?**
→ Answer: No; use max_retries (typically 2-3) with min_retry_interval_secs  
→ Reference: https://docs.databricks.com/en/jobs/control-flow.html

**Q: Which task type runs a Lakeflow Spark Declarative Pipeline?**
→ Answer: Pipeline Task  
→ Reference: https://docs.databricks.com/en/jobs/task-types.html

**Q: File lands at 2am UTC but your team is in EST. How to schedule?**
→ Answer: Use cron with timezone support (e.g., `0 7 * * * America/New_York`)  
→ Reference: https://docs.databricks.com/en/jobs/schedule-jobs.html

**Q: You want to deploy to dev, staging, and prod. Which should you use?**
→ Answer: DABs with environment-specific config files  
→ Reference: https://docs.databricks.com/en/dev-tools/bundles/config.html

**Q: Should you commit notebooks directly to main branch?**
→ Answer: No; use feature branches + PR workflow for code review  
→ Reference: https://docs.databricks.com/en/repos/ci-cd.html

**Q: How do you parameterize values in a DAB for different environments?**
→ Answer: Use variables with environment-specific overrides in databricks.yml  
→ Reference: https://docs.databricks.com/en/dev-tools/bundles/config.html

**Q: Serverless Jobs available in all workspaces?**
→ Answer: Default in UC-enabled workspaces (2026); config required for others  
→ Reference: https://docs.databricks.com/en/jobs/run-serverless-jobs.html

---

## Summary Statistics

| Category | Count | Notes |
|----------|-------|-------|
| **Total URLs** | **110+** | Domain 4–5 complete |
| **Domain 4 URLs** | **60+** | Lakeflow Jobs |
| **Domain 5 URLs** | **50+** | CI/CD & Bundles |
| **Core Topics** | 13 | Jobs, DAG, Triggers, Git, DABs, etc. |
| **Sub-Topics** | 85+ | Task types, control flow, etc. |
| **Release Notes** | 5 | NEW features 2026 |

---

## How to Use This Reference

1. **Search by Topic** — Use Ctrl+F for specific task types, commands
2. **Verify Against Exam Guide** — Cross-check with official May 2026 exam guide
3. **Deep Dive on Weak Areas** — Click URL to read full Databricks documentation
4. **Print for Offline Study** — Save as PDF for reference without network
5. **Bookmark Priority URLs** — Focus on heavily tested topics first

---

## Audit Notes

**Verified Date:** August 30, 2026  
**Exam Guide Version:** May 4, 2026 (Data Engineer Associate v2.0)  
**Domain Coverage:** Domain 4 & 5 (Lakeflow Jobs 16% + CI/CD 10% = 26% weight)

**Key Topics Verified:**
- ✅ Lakeflow Jobs (create, manage, monitor)
- ✅ Task types (Notebook, SQL, Python, JAR, Pipeline, Dashboard, dbt, etc.)
- ✅ Task dependencies & DAG patterns
- ✅ Control flow (conditionals, retries, loops)
- ✅ Triggers (cron, file arrival, table update)
- ✅ Serverless Jobs (NEW 2026)
- ✅ Git Folders (create, commit, branch, PR)
- ✅ Declarative Automation Bundles (DABs)
- ✅ Bundle configuration & deployment
- ✅ Databricks CLI
- ✅ CI/CD best practices
- ✅ Environment management (dev/staging/prod)

---

**Last Updated:** August 30, 2026  
**Next Review:** Monitor for advanced DAB features and Serverless Jobs enhancements
