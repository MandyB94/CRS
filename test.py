import boto3

# Initialize S3 client
s3 = boto3.client('s3')

# Define the bucket name
bucket_name = 'rahul-bucket-f13-proj'

# List objects in the bucket to verify paths
response = s3.list_objects_v2(Bucket=bucket_name)

# Print the list of objects in the bucket
if 'Contents' in response:
    for obj in response['Contents']:
        print(obj['Key'])
else:
    print("No objects found in the bucket.")
