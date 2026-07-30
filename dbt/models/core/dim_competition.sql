CREATE TABLE IF NOT EXISTS `sports-analytics-ml.dev_core.dim_competition`
(
    competition_key INT64 NOT NULL,

    provider_name STRING NOT NULL,
    
    provider_competition_id INT64 NOT NULL,

    competition_name STRING NOT NULL,

    country_name STRING,

    competition_gender STRING,

    competition_youth BOOL,

    competition_international BOOL,

    competition_code STRING,

    created_at TIMESTAMP NOT NULL,

    updated_at TIMESTAMP NOT NULL
)
CLUSTER BY provider_name, provider_competition_id;