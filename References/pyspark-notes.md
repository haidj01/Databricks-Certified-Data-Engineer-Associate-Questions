# PySpark Notes

## 1. What is Spark

- Open-source **unified computing engine** with a set of libraries for parallel data processing on a computer cluster.
- Processes data **in memory** — up to ~100x faster than Hadoop MapReduce for iterative workloads (~10x for disk-based). The 100x figure comes from specific benchmarks, not a universal guarantee.

### Components

| Layer | Contents |
|---|---|
| Low-level API | RDD, Distributed Variables (**Broadcast**, **Accumulator**) |
| Structured API | DataFrame, Dataset, SQL |
| Library ecosystem | Structured Streaming, MLlib / Advanced Analytics, GraphX |

> **PySpark note:** `Dataset` is Scala/Java only (compile-time type safety). In Python you only use **DataFrame**.

---

## 2. How Spark Works

### Nodes

- **Driver**
  - Heart of the application; entry point is the **SparkSession**.
  - Maintains information about executors.
  - Analyzes, distributes, and schedules work.
- **Executor**
  - Executes tasks assigned by the driver.
  - Reports execution status back to the driver.

### Job / Stage / Task

- **Action → 1 Job.**
- A job is split into **stages** at **shuffle boundaries**.
- Within a stage, **task count = partition count**.

### Key points

1. Each task works on exactly **one partition** at a time.
2. Tasks run **in parallel**.
3. Executors are **JVM processes** running on cluster machines.
4. Executors host **cores**; each core runs **1 task** at a time.

### Partition

- Data is divided into chunks called **partitions** to enable parallel processing.
- `spark.sql.shuffle.partitions` — number of partitions after a shuffle. **Default = 200.** A classic tuning knob (and exam favorite).

---

## 3. Transformations & Actions

### Transformation

- **Narrow** — each input partition contributes to **at most one** output partition. No shuffle. (`select`, `filter`, `withColumn`)
- **Wide** — one **output** partition depends on **many input** partitions. Causes a **shuffle**. (`groupBy`, `join`, `distinct`, `repartition`)

> Memorize wide as "output depends on many inputs" — it maps directly to why a shuffle is needed.

### Action & Lazy Evaluation

- Transformations build a plan; an **action** triggers execution.
- Types of action:
  1. View data in the console (`show`)
  2. Collect data to the native language (`collect`, `take`)
  3. Write data to an output source (`write`)
- Spark waits until the last moment to execute the computation graph, so it can optimize, plan, and allocate resources properly.

---

## 4. Structured API — DataFrame

1. The most common Structured API; represented like a table.
2. Organized into **rows and columns**.
3. Has a **schema** — metadata describing the columns.
4. Data is stored in **partitions**.
5. **Immutable** — every transformation returns a new DataFrame.

---

## 5. Structured API Execution Plan

### Logical planning

Unresolved logical plan → (check **catalog**) → resolved logical plan → **Catalyst Optimizer** → optimized logical plan

Catalyst optimizations to know:
- **Predicate pushdown** — push filters down to the data source so less data is read.
- **Column pruning** — read only the columns actually referenced.

### Physical planning

Optimized logical plan → several physical plans → **cost model** picks the best one → **Whole-Stage Code Generation** → RDD operations → executed on the cluster.

**DAG** = Directed Acyclic Graph, the illustration of the execution plan.

---

## 6. Extra for Databricks DE Associate

### Adaptive Query Execution (AQE)

Re-optimizes the plan **at runtime** using actual shuffle statistics. Enabled by default in Spark 3.x.

- Dynamically **coalesces shuffle partitions** (fixes the "200 tiny partitions" problem).
- Switches **sort-merge join → broadcast hash join** when one side turns out to be small.
- **Skew join handling** — splits oversized partitions.

### Partition vs. shuffle partition

- **Partition** — how data is currently split across the cluster.
- **Shuffle partition** — how many partitions are produced *after* a wide transformation, controlled by `spark.sql.shuffle.partitions` (default 200), and adjusted automatically when AQE is on.
