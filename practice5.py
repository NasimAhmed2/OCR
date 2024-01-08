import boto3
import json
import os
import time
aws_region = 'ap-southeast-2'
# Set AWS credentials using environment variables
os.environ['AWS_ACCESS_KEY_ID'] = 'AKIA2UC3BGWC46O5LKBX'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
# Initialize the Textract client
textract_client = boto3.client('textract', region_name=aws_region)

# Specify the S3 bucket and object (document) to analyze
bucket = 'textract-blueconsulting'
document = 'output_page.pdf'

# Start the Textract analysis
response = textract_client.analyze_document(
    Document={'S3Object': {'Bucket': bucket, 'Name': document}},FeatureTypes=['FORMS']
)
Blocks=response['Blocks']
# print(Blocks)
# get key and value maps
key_map = {}
value_map = {}
block_map = {}
for block in Blocks:
    block_id = block['Id']
    block_map[block_id] = block
    if block['BlockType'] == "KEY_VALUE_SET":
        if 'KEY' in block['EntityTypes']:
            key_map[block_id] = block
        else:
            value_map[block_id] = block

print(key_map,value_map,block_map)
# # Get the JobId for checking the status or getting the results later
# job_id = response['JobId']
# print(f'Textract JobId: {job_id}')

# # Wait for the job to complete
# while True:
#     results = textract_client.get_document_text_detection(JobId=job_id)
#     job_status = results['JobStatus']

#     if job_status in ['SUCCEEDED', 'FAILED']:
#         break

#     print(f'Job status: {job_status}. Waiting for completion...')
#     time.sleep(5)  # Wait for 5 seconds before checking again

# # Assuming 'results' is the Textract response

# # Assuming 'results' is the Textract response

# # key_value_pairs = {}

# # for i, block in enumerate(results.get('Blocks', [])):
# #     if block.get('BlockType') == 'LINE':
# #         key = block.get('Text')
# #         value = ''  # Initialize an empty string for the value
# #         # Find the associated 'WORD' block (assuming it's the next block)
# #         next_block_index = i + 1
# #         if next_block_index < len(results.get('Blocks', [])):
# #             next_block = results['Blocks'][next_block_index]
# #             if next_block.get('BlockType') == 'WORD':
# #                 value = next_block.get('Text')
# #         key_value_pairs[key] = value

# # print(key_value_pairs)

# key_value_pairs = {}
# current_key = None

# for block in results.get('Blocks', []):
#     block_type = block.get('BlockType')
    
#     if block_type == 'LINE':
#         text = block.get('Text', '')
#         print(text)
#         # Check if the line ends with a colon, indicating it's a potential key
#         if text.endswith(':'):
#             current_key = text.strip(':').strip()  # Extract the key without the colon
#         else:
#             # If there's a current key, and the block type is 'WORD', set it as the value
#             if current_key and block_type == 'WORD':
#                 key_value_pairs[current_key] = text
#                 current_key = None

# # Print the resulting key-value pairs
# for key, value in key_value_pairs.items():
#     print(f'{key}: {value}')