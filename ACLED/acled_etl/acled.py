import requests
import datetime as dt
import json
from io import StringIO
import pandas as pd
import boto3
from botocore.exceptions import ClientError
import logging

log = logging.getLogger('acled')
S3_BUCKET = "acled-data"

def exec():
    # calculate last 7 days 
    today = dt.datetime.now()
    p7d = today - dt.timedelta(days=7)

    today_param = today.strftime("%Y-%m-%d")
    p7d_param = p7d.strftime("%Y-%m-%d")

    log.info(f"ACLED ETL running for dates {p7d_param} to {today_param}")

    access = json.loads(get_secret())
    token = access["API_TOKEN"]
    email = access["EMAIL_ADDRESS"]

    url2 = f'https://api.acleddata.com/acled/read.csv?key={token}&email={email}&first_event_date={p7d_param}&last_event_date={today_param}&region=1,2,3,4,5&limit=0'
    response = requests.post(url2)

    if not response.ok:
        log.error(f"Request to ACLED API failed with response code {response.status_code}: {response.text}")
        return

    data = StringIO(response.text)
    df = pd.read_csv(data)

    s3_endpoint = f"s3://{S3_BUCKET}/ACLED_EXPORT_{today_param}.csv"
    log.info(f"Writing dataframe with {len(df)} to {s3_endpoint}")
    try:
        df.to_csv(s3_endpoint)
    except Exception as ex:
        log.error(f"Unable save data to S3: {ex}")
        raise ex


def get_secret():
    log.debug("Retrieving ACLED access information from Secrets Manager")
    secret_name = "ACLED"
    region_name = "us-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        log.error(e)
        raise e

    return get_secret_value_response['SecretString']