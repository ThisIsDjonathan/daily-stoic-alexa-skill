from datetime import datetime
import os
import uuid

def lambda_handler(event, context):
    day_of_year = datetime.now().timetuple().tm_yday
    s3_bucket_name = os.environ['S3_BUCKET_NAME']
    object_key = str(day_of_year) + '.mp3'
    audio_url = f"https://{s3_bucket_name}.s3.amazonaws.com/audios/portuguese/{object_key}"

    return {
        "uid": str(uuid.uuid4()),
        "updateDate": datetime.now().isoformat(),
        "titleText": "Diário Estoico",
        "mainText": "",
        "streamUrl": audio_url
      }