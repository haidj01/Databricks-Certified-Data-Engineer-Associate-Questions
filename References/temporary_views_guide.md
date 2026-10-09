# Databricks Temporary Views 완벽 가이드

**📅 Last Updated:** August 2026  
**🎯 Target:** Databricks Certified Data Engineer Associate Exam + 실무 참고  
**📚 Source:** [docs.databricks.com](https://docs.databricks.com)

---

## 📋 목차

1. [개요](#개요)
2. [VIEW 타입 비교](#view-타입-비교)
3. [생성 구문](#생성-구문)
4. [Spark Declarative Pipeline 사용](#spark-declarative-pipeline-사용)
5. [실전 예제](#실전-예제)
6. [자격증 시험 핵심](#자격증-시험-핵심)
7. [Q&A](#qa)

---

## 개요

### Temporary View란?

<cite index="31-1">TEMPORARY VIEW는 생성한 세션에서만 사용 가능하며, 세션이 종료되면 자동으로 drop되는 가상 테이블</cite>입니다.

**핵심 특징:**
- ✅ 메모리에 존재 (디스크 저장 안 함)
- ✅ 세션 종료 시 자동 삭제
- ✅ 다른 사용자 접근 불가
- ✅ 빠른 생성 & 쿼리

**사용 시나리오:**
- 데이터 탐색 및 EDA
- 중간 변환 결과 저장
- 복잡한 쿼리 분해
- Bronze → Silver 변환

---

## VIEW 타입 비교

| 구분 | **Stored VIEW** | **TEMPORARY VIEW** | **GLOBAL TEMP VIEW** |
|------|---|---|---|
| **범위** | Workspace | 세션 | 클러스터 |
| **수명** | 영구 | 세션 종료 시 삭제 | Spark 앱 종료 시 삭제 |
| **가시성** | 모든 사용자 | 생성자만 | 같은 클러스터 내 모든 노트북 |
| **저장 위치** | Unity Catalog 메타스토어 | 메모리 | 메모리 (`global_temp` 스키마) |
| **성능** | 중간 | 빠름 ⚡ | 빠름 ⚡ |
| **사용 시기** | 프로덕션 공유 | 개발/탐색 | 노트북 간 임시 공유 |
| **Drop 방법** | `DROP VIEW` | 자동 또는 `DROP VIEW` | 자동 또는 `DROP VIEW` |

---

## 생성 구문

### 1️⃣ SQL 방식

#### TEMPORARY VIEW

```sql
-- 기본 구문
CREATE TEMPORARY VIEW temp_view_name AS
SELECT * FROM source_table WHERE condition;

-- 명시적 REPLACE (기존 view 덮어쓰기)
CREATE OR REPLACE TEMPORARY VIEW temp_view_name AS
SELECT * FROM source_table;

-- 컬럼 명시 (옵션)
CREATE TEMPORARY VIEW temp_view_name (col1, col2, col3) AS
SELECT a, b, c FROM source_table;

-- COMMENT 추가
CREATE TEMPORARY VIEW temp_view_name 
COMMENT 'Silver layer: cleaned customer data' AS
SELECT 
  customer_id,
  UPPER(first_name) AS first_name,
  clean_email(email) AS email
FROM bronze_customers
WHERE is_active = true;
```

#### GLOBAL TEMPORARY VIEW

```sql
CREATE TEMPORARY VIEW global_temp.my_view AS
SELECT * FROM my_table;

-- 쿼리 시 반드시 global_temp 프리픽스 사용
SELECT * FROM global_temp.my_view;
```

---

### 2️⃣ PySpark 방식

#### createTempView (기존 view 있으면 에러)

```python
df = spark.read.table("bronze_transactions")

# 기본 사용
df.createTempView("temp_transactions")

# 재사용 불가 — 두 번째 실행 시 에러 발생
try:
    df.createTempView("temp_transactions")
except Exception as e:
    print(f"❌ {e}")  # AnalysisException: Temporary table already exists
```

#### createOrReplaceTempView (권장 ⭐)

```python
# 첫 생성
df.createOrReplaceTempView("temp_customers")

# 수정된 데이터로 재생성 — 에러 없음
df_filtered = df.filter(df.status == "active")
df_filtered.createOrReplaceTempView("temp_customers")

# SQL에서 사용
result = spark.sql("SELECT * FROM temp_customers WHERE age > 18")
result.show()
```

#### createGlobalTempView

```python
# Global Temp View 생성
df.createOrReplaceGlobalTempView("global_shared_view")

# 쿼리: global_temp 스키마 필수
spark.sql("SELECT * FROM global_temp.global_shared_view").show()

# 다른 노트북에서도 접근 가능 (같은 클러스터)
# Notebook B:
# spark.sql("SELECT * FROM global_temp.global_shared_view")
```

---

### 3️⃣ View 확인 & 정리

```python
# TEMPORARY VIEW 조회
spark.sql("SHOW VIEWS IN current_database()").show()

# VIEW 상세정보 조회
spark.sql("DESCRIBE FORMATTED temp_customers").show()

# VIEW 삭제
spark.catalog.dropTempView("temp_customers")  # True/False 반환

# 모든 TEMPORARY VIEW 삭제
for view in spark.catalog.listTempViews():
    spark.catalog.dropTempView(view[0])
    print(f"✓ Dropped: {view[0]}")
```

---

## Spark Declarative Pipeline 사용

### @dp.temporary_view 데코레이터

<cite index="31-1">Spark Declarative Pipeline에서 `@temporary_view` 데코레이터를 사용하여 임시 view를 정의하며, 결과는 view가 쿼리될 때 계산됨</cite>

#### 기본 문법

```python
from pyspark import pipelines as dp
from pyspark.sql import DataFrame

@dp.temporary_view
def basic_temp_view() -> DataFrame:
    return spark.table("source_data")

# 또는 이름 명시
@dp.temporary_view(name="custom_name")
def my_temp_view() -> DataFrame:
    return spark.read.table("samples.nyctaxi.trips")
```

#### 매개변수

```python
@dp.temporary_view(
    name="silver_customers",           # 옵션: 커스텀 이름
    comment="Cleaned customer records"  # 옵션: 설명
)
@dp.expect(...)  # 옵션: 데이터 품질 검증
def cleaned_customers() -> DataFrame:
    return spark.read.table("bronze.raw_customers")
```

#### 파이프라인 내 사용 범위

```python
from pyspark import pipelines as dp
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, upper, trim

# 1️⃣ TEMPORARY VIEW (중간 변환용)
@dp.temporary_view(name="bronze_raw")
def raw_data() -> DataFrame:
    return spark.read.table("source.raw_events")

# 2️⃣ TEMPORARY VIEW (정제 로직)
@dp.temporary_view(name="silver_clean")
def cleaned_data() -> DataFrame:
    """
    Bronze 데이터 정제
    - 공백 제거
    - NULL 처리
    - 타입 변환
    """
    return (
        spark.table("bronze_raw")
        .select(
            col("event_id"),
            upper(trim(col("event_name"))).alias("event_name"),
            col("event_timestamp")
        )
        .filter(col("event_id").isNotNull())
    )

# 3️⃣ MATERIALIZED VIEW (최종 결과 - 파이프라인 외부 접근 가능)
@dp.materialized_view(name="gold_events")
def final_events() -> DataFrame:
    """
    Gold layer: 최종 분석 테이블
    - silver_clean에서만 데이터 소스
    - 외부에서 쿼리 가능
    """
    return spark.table("silver_clean")

# ⚠️ bronze_raw, silver_clean은 파이프라인 내부에서만 사용 가능
# ✅ gold_events는 다른 노트북/쿼리에서 접근 가능
```

---

## 실전 예제

### 예제 1: 고객 데이터 정제 (PySpark)

```python
from pyspark.sql.functions import col, when, upper, trim, coalesce

# BRONZE: 원본 데이터
bronze_customers = spark.read.format("parquet").load("/data/raw/customers")

# SILVER: 정제 로직
cleaned_customers = (
    bronze_customers
    .select(
        col("customer_id"),
        upper(trim(col("name"))).alias("name"),
        coalesce(col("email"), "unknown@example.com").alias("email"),
        when(col("age") < 0, None).otherwise(col("age")).alias("age")
    )
    .filter(col("customer_id").isNotNull())
    .dropDuplicates(["customer_id"])
)

# TEMPORARY VIEW 생성 → 다른 변환에서 재사용
cleaned_customers.createOrReplaceTempView("temp_customers_clean")

# GOLD: 비즈니스 로직 추가
gold_customers = spark.sql("""
    SELECT
        customer_id,
        name,
        email,
        age,
        CASE 
            WHEN age < 18 THEN 'Minor'
            WHEN age BETWEEN 18 AND 65 THEN 'Adult'
            ELSE 'Senior'
        END AS age_group,
        CURRENT_TIMESTAMP() AS processed_at
    FROM temp_customers_clean
    WHERE age IS NOT NULL
""")

# GOLD 저장 (파이프라인 외부 접근 가능)
gold_customers.write.mode("overwrite").format("delta").save("/data/gold/customers")
```

### 예제 2: Spark Declarative Pipeline (multi-step transform)

```python
from pyspark import pipelines as dp
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, sum as spark_sum, count

# ──────────────────────────────────────────────
# BRONZE: 원본 데이터
# ──────────────────────────────────────────────
@dp.table
def raw_orders() -> DataFrame:
    """Kafka에서 실시간 주문 스트리밍"""
    return (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "orders_topic")
        .option("startingOffsets", "latest")
        .load()
        .select(
            col("value").cast("string").alias("json_data")
        )
    )

@dp.table
def raw_customers() -> DataFrame:
    """고객 정보 배치 로드"""
    return spark.read.table("external.customers")

# ──────────────────────────────────────────────
# SILVER: 데이터 정제 (TEMPORARY VIEW)
# ──────────────────────────────────────────────
@dp.temporary_view(
    name="silver_orders_clean",
    comment="Cleaned order records - internal use only"
)
def silver_orders() -> DataFrame:
    """
    주문 데이터 정제
    - NULL 체크
    - 타입 변환
    - 이상치 제거
    """
    from pyspark.sql.functions import from_json, schema_of_json
    
    # JSON 스키마 정의
    json_schema = "order_id INT, customer_id INT, amount DOUBLE, status STRING, order_date STRING"
    
    return (
        spark.table("raw_orders")
        .select(from_json(col("json_data"), json_schema).alias("data"))
        .select("data.*")
        .filter(col("amount") > 0)
        .filter(col("order_id").isNotNull())
    )

@dp.temporary_view(
    name="silver_customers_clean",
    comment="Cleaned customer records"
)
def silver_customers() -> DataFrame:
    """고객 데이터 정제"""
    return (
        spark.table("raw_customers")
        .select(
            col("customer_id"),
            col("name"),
            col("country")
        )
        .dropDuplicates(["customer_id"])
    )

# ──────────────────────────────────────────────
# GOLD: 최종 분석 테이블 (MATERIALIZED VIEW)
# ──────────────────────────────────────────────
@dp.materialized_view(
    name="gold_customer_orders",
    comment="Order summary by customer - for BI/Analytics"
)
def gold_customer_orders() -> DataFrame:
    """
    고객별 주문 요약
    - Temp view 2개 JOIN
    - 파이프라인 외부 접근 가능
    """
    return (
        spark.sql("""
            SELECT
                c.customer_id,
                c.name,
                c.country,
                COUNT(o.order_id) AS total_orders,
                SUM(o.amount) AS total_amount,
                AVG(o.amount) AS avg_order_value,
                CURRENT_TIMESTAMP() AS updated_at
            FROM silver_customers_clean c
            LEFT JOIN silver_orders_clean o
                ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.name, c.country
        """)
    )

@dp.materialized_view(
    name="gold_orders_by_status"
)
def gold_orders_status() -> DataFrame:
    """상태별 주문 통계"""
    return (
        spark.sql("""
            SELECT
                status,
                COUNT(*) AS order_count,
                SUM(amount) AS total_revenue,
                AVG(amount) AS avg_revenue
            FROM silver_orders_clean
            GROUP BY status
        """)
    )

# ⚠️ 범위:
# - silver_orders_clean, silver_customers_clean: 파이프라인 내부만
# - gold_customer_orders, gold_orders_by_status: 외부 접근 가능
```

### 예제 3: 복잡한 JOIN 및 Temp View 활용

```python
# 시나리오: 거래 데이터 + 환율 정보 → 통합 분석

# TEMP VIEW 1: 거래 데이터
transactions_df = spark.read.table("bronze.transactions")
transactions_df.createOrReplaceTempView("temp_txns")

# TEMP VIEW 2: 환율 정보
exchange_rates_df = spark.read.table("bronze.exchange_rates")
exchange_rates_df.createOrReplaceTempView("temp_rates")

# GOLD: 통합 쿼리 (두 TEMP VIEW 활용)
gold_global_transactions = spark.sql("""
    SELECT
        t.transaction_id,
        t.currency,
        t.amount,
        r.usd_rate,
        t.amount * r.usd_rate AS amount_usd,
        t.transaction_date
    FROM temp_txns t
    LEFT JOIN temp_rates r
        ON t.currency = r.currency
        AND t.transaction_date = r.rate_date
    WHERE r.usd_rate IS NOT NULL
""")

gold_global_transactions.write.mode("overwrite").format("delta").save("/gold/global_txns")

# 정리
spark.catalog.dropTempView("temp_txns")
spark.catalog.dropTempView("temp_rates")
```

---

## 자격증 시험 핵심

### 📌 시험에 나올 주요 개념

#### 1. **VIEW 타입 선택 문제**

**Q: 어떤 상황에 어떤 VIEW를 사용할까?**

| 상황 | 답 | 이유 |
|------|-----|------|
| "데이터가 세션 후에도 유지되어야 한다" | **Stored VIEW** | Persistent, 메타스토어 저장 |
| "탐색 중 중간 결과를 임시 저장하고 싶다" | **Temp VIEW** | 빠르고, 세션 종료 시 자동 삭제 |
| "다른 노트북에서도 접근해야 한다 (같은 클러스터)" | **Global Temp VIEW** | 클러스터 범위 공유 |
| "프로덕션 Gold layer" | **Materialized VIEW** | 영구, 최적화된 성능 |

#### 2. **Bronze → Silver → Gold 패턴**

```
Bronze (원본)
  ↓ TEMPORARY VIEW 또는 @dp.temporary_view
Silver (정제)
  ↓ TEMPORARY VIEW 또는 @dp.temporary_view
Gold (최종 결과)
  ↓
Stored VIEW 또는 Materialized View
  → 외부 BI/Analytics 접근
```

**시험 포인트:**
- Silver = 중간 변환 → TEMPORARY VIEW OK
- Gold = 최종 결과 → Stored/Materialized VIEW 권장
- Temp View는 "파이프라인 내부 전용"

#### 3. **PySpark API 차이**

| 메서드 | 기존 존재 | 재사용 가능 | 권장 |
|---|---|---|---|
| `createTempView()` | ❌ 에러 | ❌ | ❌ 비권장 |
| `createOrReplaceTempView()` | ✅ 덮어쓰기 | ✅ | ✅ **권장** |
| `createGlobalTempView()` | ❌ 에러 | ❌ | ❌ |
| `createOrReplaceGlobalTempView()` | ✅ | ✅ | ✅ 클러스터 공유 시 |

#### 4. **Spark Declarative Pipeline (Section 3)**

**시험 범위:**
- `@dp.temporary_view` vs `@dp.materialized_view` 구분
- Temp view = 파이프라인 내부용 (외부 접근 불가)
- Materialized view = 파이프라인 외부 접근 가능

**샘플 시험 문제:**
```
Q: 파이프라인에서 중간 변환 결과를 저장하고, 
   다른 변환에서만 참조할 수 있어야 합니다.
   어떤 데코레이터를 사용하시겠습니까?

A) @dp.table
B) @dp.temporary_view  ✅ 정답
C) @dp.materialized_view
D) @dp.view
```

---

### 🎯 시험 대비 체크리스트

- [ ] Stored/Temp/Global Temp 3가지 VIEW 범위 이해
- [ ] `createOrReplaceTempView()` vs `createTempView()` 차이 숙지
- [ ] Bronze → Silver → Gold에서 VIEW 활용 시점 파악
- [ ] `@dp.temporary_view` 데코레이터 문법 암기
- [ ] "파이프라인 내부 전용" vs "외부 접근 가능" 구분
- [ ] 실제 SQL/PySpark 코드 작성 연습
- [ ] Mock exam: Domain 3 문제 10회 풀이

---

## Q&A

### Q1. Temporary View vs DataFrame 캐싱의 차이?

```python
# 방법 1: DataFrame 캐싱
df = spark.read.table("large_table")
df.cache()
result1 = df.filter(...).collect()
result2 = df.select(...).collect()  # 캐시 재사용

# 방법 2: Temporary View
df.createOrReplaceTempView("temp_large")
result1 = spark.sql("SELECT ... FROM temp_large WHERE ...").collect()
result2 = spark.sql("SELECT ... FROM temp_large").collect()  # SQL 재사용
```

**차이:**
| 항목 | DataFrame Cache | Temp View |
|------|---|---|
| 메모리 효율 | 높음 (컬럼 선택형) | 중간 (전체 로드) |
| SQL 통합 | ❌ | ✅ |
| 다른 세션 접근 | ❌ | ❌ (Temp View도 세션 범위) |
| 사용 시기 | 반복 변환 | SQL 재사용 |

### Q2. Temp View 이름 충돌 시?

```python
# 같은 이름의 Temp View + Stored View 존재
spark.sql("CREATE TEMPORARY VIEW my_data AS SELECT * FROM source")
spark.sql("CREATE VIEW my_data AS SELECT * FROM other_source")

# 조회 시 우선순위: TEMPORARY VIEW > Stored VIEW
spark.sql("SELECT * FROM my_data")  # Temp View의 결과 반환

# 명시적 지정
spark.sql("SELECT * FROM catalog.schema.my_data")  # Stored View 강제 접근
```

### Q3. Global Temp View의 생명 주기?

```python
# Notebook A
df.createOrReplaceGlobalTempView("global_shared")

# Notebook B (같은 클러스터)
spark.sql("SELECT * FROM global_temp.global_shared")  # ✅ 접근 가능

# Notebook A 클러스터 중단 후
# Notebook B에서 같은 클러스터 재시작
spark.sql("SELECT * FROM global_temp.global_shared")  # ❌ 없음 (삭제됨)
```

**생명주기:**
- 생성: Spark 앱 시작 시
- 공유: 클러스터 내 모든 노트북
- 삭제: 클러스터 중단 또는 명시적 DROP

### Q4. Temp View 성능 최적화?

```python
# ✅ Good: 필요한 컬럼만 SELECT
filtered_data = (
    spark.read.table("large_table")
    .select("id", "name", "amount")  # 3개 컬럼만
    .filter(col("amount") > 1000)
)
filtered_data.createOrReplaceTempView("temp_filtered")

# ❌ Bad: 모든 컬럼 로드
raw_data = spark.read.table("large_table")
raw_data.createOrReplaceTempView("temp_raw")
spark.sql("SELECT id, name, amount FROM temp_raw WHERE amount > 1000")
```

**팁:** Temp View 생성 전 필터링 & 프로젝션 수행

### Q5. Temp View와 CTE의 차이?

```python
# Temp View: 여러 쿼리에서 재사용
df.createOrReplaceTempView("temp_sales")
spark.sql("SELECT COUNT(*) FROM temp_sales").show()  # Query 1
spark.sql("SELECT SUM(amount) FROM temp_sales").show()  # Query 2

# CTE: 단일 쿼리 내에서만 유효
spark.sql("""
    WITH cte_sales AS (
        SELECT * FROM sales WHERE year = 2024
    )
    SELECT COUNT(*), SUM(amount) FROM cte_sales
""")
```

**선택 기준:**
- 같은 변환을 **여러 쿼리에서** 사용 → **Temp View**
- 단일 복잡한 쿼리 내 **임시 단계** → **CTE**

---

## 참고 자료

- 📖 [Databricks Temporary View Docs](https://docs.databricks.com/aws/en/ldp/developer/ldp-sql-ref-create-temporary-view)
- 📖 [PySpark createOrReplaceTempView API](https://docs.databricks.com/aws/en/pyspark/reference/classes/dataframe/createorreplacetempview)
- 📖 [Spark Declarative Pipelines Guide](https://spark.apache.org/docs/latest/declarative-pipelines-programming-guide.html)
- 📖 [Databricks Certified Data Engineer Associate Exam Guide (May 2026)](https://www.databricks.com/learn/certification/data-engineer-associate)

---

## 요약

| 개념 | 핵심 포인트 |
|------|---|
| **Temporary View** | 세션 범위, 빠른 성능, 중간 변환용 |
| **Global Temporary View** | 클러스터 범위 공유, 다중 노트북 접근 |
| **Stored View** | 영구, 메타스토어, 프로덕션 공유 |
| **PySpark API** | `createOrReplaceTempView()` 권장 |
| **Spark DLP** | `@dp.temporary_view` = 내부용, `@dp.materialized_view` = 외부용 |
| **시험 핵심** | VIEW 타입 선택, Bronze→Silver→Gold 패턴, 데코레이터 차이 |

**최종 팁:** 실제 파이프라인 구축하며 3가지 VIEW 타입을 직접 사용해보면, 자격증 시험과 실무에서 모두 자신감이 생깁니다! 💪

---

**작성 일자:** 2026년 8월  
**버전:** 1.0  
**대상:** Databricks Certified Data Engineer Associate 수험자 및 데이터 엔지니어
