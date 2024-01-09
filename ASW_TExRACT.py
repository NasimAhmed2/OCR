import boto3
from collections import defaultdict
import os
import json
import pandas as pd

def get_kv_map(bucket, key):
    # process using image bytes
    aws_region = 'ap-southeast-2'
    # Set AWS credentials using environment variables
    os.environ['AWS_ACCESS_KEY_ID'] = 'your aws access key'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'your aws secret key'
    # Initialize the Textract client
    client = boto3.client('textract', region_name=aws_region)
    response = client.analyze_document(Document={'S3Object': {'Bucket': bucket, "Name": key}}, FeatureTypes=['FORMS','TABLES'])

    # Get the text blocks
    blocks = response['Blocks']
    # print(f'BLOCKS: {blocks}')

    # get key and value maps
    key_map = {}
    value_map = {}
    block_map = {}
    table_blocks = []
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET":
            if 'KEY' in block['EntityTypes']:
                key_map[block_id] = block
            else:
                value_map[block_id] = block
        elif block['BlockType'] == "TABLE":
            table_blocks.append(block)

    return key_map, value_map, block_map, table_blocks


def get_kv_relationship(key_map, value_map, block_map):
    kvs = defaultdict(list)
    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map)
        val = get_text(value_block, block_map)
        kvs[key].append(val)
    return kvs


def find_value_block(key_block, value_map):
    for relationship in key_block['Relationships']:
        if relationship['Type'] == 'VALUE':
            for value_id in relationship['Ids']:
                value_block = value_map[value_id]
    return value_block


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X'

    return text
# Specify the S3 bucket and object (document) to analyze

def organize_key_values(key_map, value_map, block_map):
    organized_dict = {}
    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map).strip()
        val = get_text(value_block, block_map).strip()
        key = key.replace('.', '').replace(':', '')
        organized_dict[key] = val
    return organized_dict

def get_text_table(result, blocks_map):
    text = ''
    confident_level = 0
    number_of_words = 0
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                        confident_level += float(word['Confidence'])
                        number_of_words += 1
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X'
                            confident_level += float(word['Confidence'])
                            number_of_words += 1

    confident_level = confident_level if confident_level == 0  else (confident_level / number_of_words)
    # return { "value": text, "confident" : confident_level }
    return text

# extracting tables data
def process_table_data(blocks_map, table_blocks):
    
    table_data = []
    for index, table in enumerate(table_blocks):
        
        data = generate_table(table, blocks_map, index + 1)
        table_data.append(data)
        # logger.info(f'Table text: {data}')
    return table_data[0]


def generate_table(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)
   
    table_data = []
    for row_index, cols in rows.items():
        data = []
        for col_index, text in cols.items():
            data.append(text)        
        table_data.append(data)
    return table_data


def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        rows[row_index] = {}

                    rows[row_index][col_index] = get_text_table(
                        cell, blocks_map)
    return rows

def lambda_handler(event, context):
    
    key_map, value_map, block_map, table_blocks = get_kv_map( event, context)

    # Get Key Value relationship
    # kvs = get_kv_relationship(key_map, value_map, block_map)
    organized_dict = organize_key_values(key_map, value_map, block_map)
    json_data = json.dumps(organized_dict, indent=2)
    table = process_table_data(block_map, table_blocks)
    datafrmae = pd.DataFrame(table[1:],columns=table[0:1])
    print("\n\n== FOUND KEY : VALUE pairs ===\n")
    print(json_data)
    print(datafrmae)
    # for key, value in organized_dict.items():
    #     print(f'{key}: {value}')

bucket = 'textract-blueconsulting'
document = 'output_pdf16_page1.pdf'
lambda_handler(bucket, document)
