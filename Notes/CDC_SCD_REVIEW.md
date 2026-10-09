```commandline
-- create a streming table called customers.
-- then use AUTO CDC to populate it
CREATE OR REFRESH STREAMING TABLE customers;

CREATE FLOW scd_type_1_flow AS
    AUTO CDC INTO customers                     -- apply insert,update and delete on customers table
    FROM STREAM source_streaming_table          -- Source Record that determine updates, inserts and deltes
    KEYS (CostomerId)                           -- column(s) that determine UNIQUELY IDENTIFY a row in the source and target table
    APPLY AS DELETE WHEN operation = "DELETE"   -- Specifiying the CDC event should be treated as DELETE
    SEQUENCE BY ProcessDate                     -- Specifies the order of CDC events in the source data
    COLUMNS * EXCEPT (operation)                -- specifies the subset of columns to include in tbe target
    STORED AS SCD TYPE 1;                       -- Whether to store records as SCD type1 or type2 
    


```