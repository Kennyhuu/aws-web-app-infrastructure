import boto3
import urllib.parse

s3_client  = boto3.client('s3')
sns_client = boto3.client('sns')

SNS_TOPIC_ARN = 'arn:aws:sns:REGION:ACCOUNT_ID:WordCountTopic'

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = urllib.parse.unquote_plus(
                 event['Records'][0]['s3']['object']['key'],
                 encoding='utf-8'
             )

    print(f'Processing file: s3://{bucket}/{key}')

    response     = s3_client.get_object(Bucket=bucket, Key=key)
    file_content = response['Body'].read().decode('utf-8')

    word_count = len(file_content.split())

    print(f'Word count in {key}: {word_count}')

    message = f'The word count in the {key} file is {word_count}.'

    sns_client.publish(
        TopicArn = SNS_TOPIC_ARN,
        Subject  = 'Word Count Result',
        Message  = message
    )

    return {
        'statusCode': 200,
        'body': message
    }