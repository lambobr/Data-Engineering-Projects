from google.cloud import storage
from transform import tweets_json
from datetime import datetime
from google.cloud import bigquery
import os

#credentials
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/airflow/.config/gcloud/application_default_credentials.json'

# constants
UTC_DATETIME = str(datetime.utcnow())[0:15]  #append current UTC datetime to filename
FILENAME = tweets_json
PROJECT = "still-emissary-369616"
LOCATION = "asia-southeast1"
BUCKET = "twitter_etl"      # GCS bucket
URI = f"gs://twitter_etl/elonmusk_tweets-{UTC_DATETIME}.json"   # uri of GCS file
TABLE_ID_STAGING = "still-emissary-369616.ETL_projects.elonmusk_tweets_staging"     # bigquery staging table name
TABLE_ID = "still-emissary-369616.ETL_projects.elonmusk_tweets"      # bigquery final table name


def load_data_to_cloud_storage(filename, project, bucket, utc):
    storage_client = storage.Client(project=project)    #project name in GCP
    bucket = storage_client.bucket(bucket_name=bucket)   #name of bucket in GCS
    blob = bucket.blob(f'elonmusk_tweets-{utc}.json')  #assign file name
    blob.upload_from_string(data=filename,content_type='json') #upload data in GCS


def load_data_to_bigquery_staging(project, location, table_id_staging, uri):
    # Construct a BigQuery client object
    client = bigquery.Client(project=project, location=location)

    job_config = bigquery.LoadJobConfig(
        # schema=[
        #     bigquery.SchemaField("tweet_date", "TIMESTAMP"),
        #     bigquery.SchemaField("tweet", "STRING"),
        #     bigquery.SchemaField("crypto", "FLOAT64")
        # ],
        autodetect=True,  #autodetect schema
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition='WRITE_TRUNCATE'
    )

    load_job = client.load_table_from_uri(
        source_uris=uri, destination=table_id_staging, location=location, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.
    #destination_table = client.get_table(table_id_staging)  # Make an API request.


def query(project,location):
    client = bigquery.Client(project=project, location=location)

    # take only new tweets which are not already present in the final table
    try:
        query = """
            SELECT *
            FROM `still-emissary-369616.ETL_projects.elonmusk_tweets_staging`
            EXCEPT DISTINCT
            SELECT *
            FROM `still-emissary-369616.ETL_projects.elonmusk_tweets`
        """
        results_df = client.query(query).to_dataframe()

    except:
        query = """
                    SELECT *
                    FROM `still-emissary-369616.ETL_projects.elonmusk_tweets_staging`
                """
        results_df = client.query(query).to_dataframe()

    print(f'Count of new tweets: {results_df.shape[0]}')
    return results_df


def load_data_to_bigquery_final(project, location, table_id, dataframe):
    # Construct a BigQuery client object
    client = bigquery.Client(project=project, location=location)

    job_config = bigquery.LoadJobConfig(
        # schema=[
        #     bigquery.SchemaField("date", "TIMESTAMP"),
        #     bigquery.SchemaField("tweet", "STRING"),
        #     bigquery.SchemaField("crypto", "FLOAT64")
        # ],
        autodetect=True,  #autodetect schema
        write_disposition='WRITE_APPEND'
    )

    load_job = client.load_table_from_dataframe(
        dataframe=dataframe, destination=table_id, location=location, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    print("Count of total tweets stored: {}".format(destination_table.num_rows))


if __name__ == '__main__':
    load_data_to_cloud_storage(filename=FILENAME, project=PROJECT, bucket=BUCKET, utc=UTC_DATETIME)
    load_data_to_bigquery_staging(project=PROJECT, location=LOCATION, table_id_staging=TABLE_ID_STAGING, uri=URI)
    results_df = query(project=PROJECT, location=LOCATION)
    load_data_to_bigquery_final(project=PROJECT, location=LOCATION, table_id=TABLE_ID, dataframe=results_df)

