# Data Processing Pipeline for Employment and Wage Statistics

## Overview

This repository contains an ETL (Extract, Transform, Load) pipeline designed to process and analyze Canadian employment and wage statistics. The primary end-use of this data is for visualization in Power BI, where you can find interactive dashboards showcasing trends and insights derived from the data.

## Project Structure

### 1. update_csv.py: The main Python script that performs the ETL process:

- Extracts employment and wage data from Statistics Canada.
- Transforms the data by cleaning, aggregating, and calculating key metrics.
- Loads the transformed data into CSV files for further analysis.

### 2. CSV Files:

- processed_stats_canada_data.csv: Contains cleaned and aggregated employment statistics.
- processed_participation_rates.csv: Provides participation rates for males and females, including differences.
- processed_wages_data.csv: Contains cleaned and aggregated wage statistics.
- gender_pay_gap.csv: Provides gender pay gap calculations across different wage types.

## GitHub Actions

The repository includes a GitHub Actions workflow to automate the script execution:

- Cron Schedule: Runs daily at midnight UTC.
- Push Trigger: Executes when changes are pushed to the main branch.
- Manual Trigger: Can be manually initiated from the GitHub Actions tab.

## Power BI Visualizations

The processed data is used to create various visualizations in Power BI, including:

- Trends in employment and wage statistics over time.
- Gender participation rates and their differences.
- Analysis of the gender pay gap across different types of wages.
