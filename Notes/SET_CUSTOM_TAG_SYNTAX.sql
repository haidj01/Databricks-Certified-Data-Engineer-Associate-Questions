ALTER TABLE any_bronze_table
SET TAGS(
  'demo_tag_quality'='bronze'
  'demo_tag_department'='sales'
);

ALTER TABLE any_bronze_table
SET TAGS('system.Certified');
