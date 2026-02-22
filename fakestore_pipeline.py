# Databricks notebook source
# MAGIC %md
# MAGIC **🥉 STEP 1 — Bronze Layer** 

# COMMAND ----------

bronze_products = spark.read.option("multiline", "true") \
    .json("/Volumes/workspace/default/products/products.json")

bronze_products.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("bronze_products")

   

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

display(spark.table("bronze_products"))

# COMMAND ----------

# MAGIC %md
# MAGIC **🥈 STEP 2 — Silver Layer (Cleaning & Struct Flattening)**

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE silver_products AS
# MAGIC SELECT
# MAGIC     id AS product_id,
# MAGIC     title,
# MAGIC     category,
# MAGIC     price,
# MAGIC     rating.rate AS rating_rate,
# MAGIC     rating.count AS rating_count
# MAGIC FROM bronze_products;

# COMMAND ----------

display(spark.table("silver_products"))

# COMMAND ----------

# MAGIC %sql
# MAGIC select distinct category from silver_products;

# COMMAND ----------

# MAGIC %md
# MAGIC **🏅 STEP 3 — Gold Layer (Business Metrics)**

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE gold_category_metrics AS
# MAGIC SELECT
# MAGIC     category,
# MAGIC     COUNT(*) AS total_products,
# MAGIC     ROUND(AVG(price),2) AS avg_price,
# MAGIC     ROUND(SUM(price),2) AS total_catalog_value,
# MAGIC     ROUND(AVG(rating_rate),2) AS avg_rating,
# MAGIC     SUM(rating_count) AS total_rating_votes
# MAGIC FROM silver_products
# MAGIC GROUP BY category
# MAGIC ORDER BY total_catalog_value DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC **📊 STEP 4 — Visualization**

# COMMAND ----------

display(
    spark.sql("""
        SELECT category, total_catalog_value
        FROM gold_category_metrics
        ORDER BY total_catalog_value DESC
    """)
)

# COMMAND ----------

# MAGIC %md
# MAGIC **📊 STEP 4 — Visualization**

# COMMAND ----------

display(
    spark.sql("""
        SELECT category, avg_rating
        FROM gold_category_metrics
        ORDER BY avg_rating DESC
    """)
)

# COMMAND ----------

# MAGIC %md
# MAGIC **⭐ STEP 5 — Create a Strong Analytical Output (Product Scoring Model)**

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE gold_product_scoring AS
# MAGIC SELECT
# MAGIC     product_id,
# MAGIC     title,
# MAGIC     category,
# MAGIC     price,
# MAGIC     rating_rate,
# MAGIC     rating_count,
# MAGIC     ROUND(
# MAGIC         (rating_rate * 0.6) +
# MAGIC         (LOG10(rating_count + 1) * 0.3) +
# MAGIC         (price/1000 * 0.1),
# MAGIC     3) AS product_score
# MAGIC FROM silver_products
# MAGIC ORDER BY product_score DESC;

# COMMAND ----------

display(
    spark.sql("""
        SELECT title, category, product_score
        FROM gold_product_scoring
        ORDER BY product_score DESC
    """)
)
