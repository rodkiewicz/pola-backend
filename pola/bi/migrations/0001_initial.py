# Generated by Django 3.1.6 on 2021-02-20 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_email_max_length'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('ai_pics', '0009_auto_20210117_0154'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('company', '0023_auto_20210215_0756'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('pola', '0007_auto_20180527_0848'),
        ('product', '0015_remove_product_company'),
        ('report', '0008_auto_20201012_0309'),
        ('reversion', '0001_squashed_0004_auto_20160611_1202'),
        ('sessions', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
        ('socialaccount', '0003_extra_data_default_dict'),
        ('users', '0003_auto_20201012_0332'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
CREATE OR REPLACE VIEW bi_new_product_by_hour AS
SELECT
    extract(hour from created_at) as dd,
    COUNT(*) FILTER(WHERE product_product.company_id is NULL) rozpoznaana,
    COUNT(*) FILTER(WHERE product_product.company_id is not NULL) nieroznanaa,
    COUNT(*) wszystkie
FROM
    product_product
WHERE
      product_product.created_at >= NOW() - INTERVAL '1 month'
GROUP BY extract(hour from created_at)
ORDER BY dd DESC
LIMIT 100;
            """,
            reverse_sql="DROP VIEW IF EXISTS bi_new_product_by_hour;"

        ),
        migrations.RunSQL(
            sql="""
CREATE OR REPLACE VIEW bi_stats_queries_uq_users_by_week AS
SELECT
	seq::date,
	COUNT(DISTINCT pola_query."client") count_uq_user,
	COUNT(1) count_request
FROM
	generate_series(
		(date_trunc('month', CURRENT_DATE) - INTERVAL '24 months')::timestamp,
		(date_trunc('month', CURRENT_DATE))::timestamp,
		'1 week'::interval
	) seq,
	pola_query
WHERE
	pola_query.timestamp BETWEEN seq::date AND (seq::date + INTERVAL '1 week')
GROUP BY seq
ORDER BY seq;
""",
            reverse_sql="DROP VIEW IF EXISTS bi_stats_queries_uq_users_by_week;"

        ),
        migrations.RunSQL(
            sql="""
CREATE OR REPLACE VIEW bi_queries_stats_intervals AS
SELECT
	COUNT(*) request_total,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '1 day') request_day,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '1 week') request_week,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '1 month') request_month,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '3 month') request_3_month,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '6 month') request_6_month,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '1 day' AND was_590 = true) request_day_was_590,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '1 week' AND was_590 = true) request_week_was_590,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '1 month' AND was_590 = true) request_month_was_590,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '3 month' AND was_590 = true) request_3_month_was_590,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '6 month' AND was_590 = true) request_6_month_was_590,
	COUNT(*) FILTER(WHERE was_590 = true) request_total_was_590,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '1 day' AND "was_plScore" = true) request_day_was_plScore,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '1 week' AND "was_plScore" = true) request_week_was_plScore,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '1 month' AND "was_plScore" = true) request_month_was_plScore,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '3 month' AND "was_plScore" = true) request_3_month_was_plScore,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '6 month' AND "was_plScore" = true) request_6_month_was_plScore,
	COUNT(*) FILTER(WHERE "was_plScore" = true) request_total_was_plScore,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '1 day' AND was_verified = true) request_day_was_verified,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '1 week' AND was_verified = true) request_week_was_verified,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '1 month' AND was_verified = true) request_month_was_verified,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '3 month' AND was_verified = true) request_3_month_was_verified,
	COUNT(*) FILTER(WHERE timestamp > NOW() - INTERVAL '6 month' AND was_verified = true) request_6_month_was_verified,
	COUNT(*) FILTER(WHERE was_verified = true) request_total_was_verified,
    COUNT(DISTINCT client) uq_user_total,
	COUNT(DISTINCT client) FILTER(WHERE timestamp > NOW() - INTERVAL '1 day') uq_user_day,
	COUNT(DISTINCT client) FILTER(WHERE timestamp > NOW() - INTERVAL '1 week') uq_user_week,
	COUNT(DISTINCT client) FILTER(WHERE timestamp > NOW() - INTERVAL '1 month') uq_user_month,
	COUNT(DISTINCT client) FILTER(WHERE timestamp > NOW() - INTERVAL '3 month') uq_user_3_month,
	COUNT(DISTINCT client) FILTER(WHERE timestamp > NOW() - INTERVAL '6 month') uq_user_6_month
FROM
	pola_query;
""",
            reverse_sql="DROP VIEW IF EXISTS bi_queries_stats_intervals;"
        ),
        migrations.RunSQL(
            sql="""
CREATE OR REPLACE VIEW bi_companies_by_query_group AS
SELECT
	CASE
		WHEN company_company.query_count > 75000 THEN '00. 75000>'
		WHEN company_company.query_count > 50000 THEN '01. 50000>'
		WHEN company_company.query_count > 30000 THEN '02. 30000>'
		WHEN company_company.query_count > 25000 THEN '03. 25000>'
		WHEN company_company.query_count > 20000 THEN '04. 20000>'
		WHEN company_company.query_count > 15000 THEN '05. 15000>'
		WHEN company_company.query_count > 10000 THEN '06. 10000>'
		WHEN company_company.query_count > 7500 THEN '07. 7500>'
		WHEN company_company.query_count > 5000 THEN '08. 5000>'
		WHEN company_company.query_count > 2500 THEN '09. 2500>'
		WHEN company_company.query_count > 1000 THEN '10. 1000>'
		WHEN company_company.query_count > 500 THEN '11. 500>'
		WHEN company_company.query_count > 250 THEN '12. 250>'
		WHEN company_company.query_count > 100 THEN '13. 100>'
		WHEN company_company.query_count > 50 THEN '14. 50>'
		WHEN company_company.query_count > 10 THEN '15. 10>'
		WHEN company_company.query_count > 5 THEN '16. 5>'
		ELSE '17. other'
	END query_count_group,
	SUM(query_count) sum_query_count,
	SUM(1) sum_total,
	SUM(company_company.verified::int) sum_verified,
	SUM(company_company.verified::int)::float / SUM(1)::float as percentage_verified,
	SUM(query_count)::float / (SELECT SUM(company_company.query_count) FROM company_company) percentage_query_count
FROM
	company_company
GROUP BY query_count_group
ORDER BY query_count_group ASC;
""",
            reverse_sql="DROP VIEW IF EXISTS bi_companies_by_query_group;"
        ),
        migrations.RunSQL(
            sql="""
CREATE OR REPLACE VIEW bi_product_by_time AS
SELECT
	seq,
	SUM(1) count_total,
	SUM((company_id IS NOT NULL)::int) count_with_company,
	SUM((code LIKE '590%')::int) count_590,
	SUM((company_id IS NOT NULL AND code LIKE '590%')::int) count_with_company_and_590,
	SUM((company_id IS NULL AND code LIKE '590%')::int) count_without_company_and_590,
	SUM((company_id IS NOT NULL)::int)::float / SUM(1) percentage_with_company,
	SUM((code LIKE '590%')::int)::float / SUM(1) percentage_590,
	SUM((company_id IS NOT NULL AND code LIKE '590%')::int)::float / SUM(1) percentage_wtih_company_and_590,
	SUM((company_id IS NULL AND code LIKE '590%')::int)::float / SUM(1) percentage_wtihout_company_and_590
FROM
	generate_series(
		(CURRENT_DATE - INTERVAL '24 months')::timestamp,
		(CURRENT_DATE)::timestamp,
		'1 week'::interval
	) seq
	LEFT JOIN
		product_product
	ON
		product_product.created_at BETWEEN seq AND (seq + INTERVAL '1 week')
GROUP BY seq
ORDER BY seq;
            """,
            reverse_sql="DROP VIEW IF EXISTS bi_product_by_time;"
        ),
        migrations.RunSQL(
            sql="""
CREATE OR REPLACE VIEW bi_queries_by_time AS
SELECT
	seq,
	COUNT(*) request_total,
	COUNT(*) FILTER(WHERE was_590 = true) request_was_590,
	COUNT(*) FILTER(WHERE "was_plScore" = true) request_was_plScore,
	COUNT(*) FILTER(WHERE was_verified = true) request_was_verified,
	COUNT(*) FILTER(WHERE was_590 = true)::float / COUNT(*) percetage_request_was_590,
	COUNT(*) FILTER(WHERE "was_plScore" = true)::float / COUNT(*) percetage_request_was_plScore,
	COUNT(*) FILTER(WHERE was_verified = true)::float / COUNT(*) percetage_request_was_verified,
    COUNT(DISTINCT client) uq_user
FROM
	generate_series(
		(CURRENT_DATE - INTERVAL '24 months')::timestamp,
		(CURRENT_DATE)::timestamp,
		'1 week'::interval
	) seq
	LEFT JOIN
		pola_query
	ON
		pola_query.timestamp BETWEEN seq AND (seq + INTERVAL '1 week')
GROUP BY seq
ORDER BY seq;
            """,
            reverse_sql="DROP VIEW IF EXISTS bi_queries_by_time;"

        ),
        migrations.RunSQL(
            sql="""
CREATE OR REPLACE VIEW bi_companies_with_count_group AS
SELECT
	CASE
		WHEN company_company.query_count > 75000 THEN '00. > 75000'
		WHEN company_company.query_count > 50000 THEN '01. > 50000'
		WHEN company_company.query_count > 30000 THEN '02. > 30000'
		WHEN company_company.query_count > 25000 THEN '03. > 25000'
		WHEN company_company.query_count > 20000 THEN '04. > 20000'
		WHEN company_company.query_count > 15000 THEN '05. > 15000'
		WHEN company_company.query_count > 10000 THEN '06. > 10000'
		WHEN company_company.query_count > 7500 THEN '07. > 7500'
		WHEN company_company.query_count > 5000 THEN '08. > 5000'
		WHEN company_company.query_count > 2500 THEN '09. > 2500'
		WHEN company_company.query_count > 1000 THEN '10. > 1000'
		WHEN company_company.query_count > 500 THEN '11. > 500'
		WHEN company_company.query_count > 250 THEN '12. > 250'
		WHEN company_company.query_count > 100 THEN '13. > 100'
		WHEN company_company.query_count > 50 THEN '14. > 50'
		WHEN company_company.query_count > 10 THEN '15. > 10'
		WHEN company_company.query_count > 5 THEN '16. > '
		ELSE '17. other'
	END query_count_group,
    company_company.*

FROM
	company_company
WHERE company_company.query_count > 1000
            """,
        reverse_sql="DROP VIEW IF EXISTS bi_companies_with_count_group;"
    ),
        migrations.RunSQL(
            sql="""
CREATE OR REPLACE VIEW bi_popular_not_verified_products AS
SELECT
*
FROM
product_product
WHERE
created_at >= NOW() - INTERVAL '1 month'
AND
company_id IS null
AND query_count > 0
ORDER BY query_count DESC
LIMIT 10000;
""",
    reverse_sql="DROP VIEW IF EXISTS bi_popular_not_verified_products;"
        )
    ]
