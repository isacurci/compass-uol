import boto3
import os
from dotenv import load_dotenv

load_dotenv()

print("ACCESS_KEY:", os.getenv('AWS_ACCESS_KEY_ID'))
print("SECRET_KEY:", os.getenv('AWS_SECRET_ACCESS_KEY'))

s3_client = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

response = s3_client.put_object(
    Bucket='data-lake-isa1',
    Key='teste/teste.json',
    Body='{"teste": true}',
    ContentType='application/json'
)

print("Sucesso:", response)
