from datetime import datetime
import os
import uuid

def lambda_handler(event, context):
    day_of_year = datetime.now().timetuple().tm_yday
    bucket_name = os.environ['BUCKET_NAME']
    object_key = str(day_of_year) + '.mp3'

    return {
        "uid": str(uuid.uuid4()),
        "updateDate": datetime.now().isoformat(),
        "titleText": "Diário Estoico",
        "mainText": "",
        "streamUrl": f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
      }