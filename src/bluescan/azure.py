from typing import Generator
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import (
    OperationStatusCodes,
    ReadResult,
)
from msrest.authentication import CognitiveServicesCredentials

import os
import argparse
import time


"""
Authenticate
Authenticates your credentials and creates a client.
"""
try:
    subscription_key = os.getenv("AZURE_CV_KEY")
    endpoint = os.getenv("AZURE_CV_URL")

    computervision_client = ComputerVisionClient(
        endpoint, CognitiveServicesCredentials(subscription_key)
    )
except Exception as e:
    print(e)
    print("It seems you haven't set up the Azure API key/URL")


def upload_and_analyse(image_path: str) -> ReadResult:
    """
    Call API with raw image uploading and get the results as a list

    :param image_path: path for an uploading image
    :return: A list of OCR results to be iterated
    """
    image_data = open(image_path, "rb")

    #
    # read_image_url = "https://cad-kenkyujo.com/wp-content/uploads/2020/03/c787ea6972868edbf0f08bb3cc04d79c.jpg"
    # read_response = computervision_client.read(read_image_url, language="ja", raw=True)
    #
    read_response = computervision_client.read_in_stream(
        image_data, language="ja", raw=True
    )

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ["notStarted", "running"]:
            break
        time.sleep(1)

    if read_result.status == OperationStatusCodes.succeeded:
        return read_result.analyze_result.read_results
    else:
        raise ValueError("Couldn't read the image on Azure.")


if __name__ == "__main__":
    """
    OCR: Read File using the Read API, extract text - remote
    This example will extract text in an image, then print results, line by line.
    This API call can also extract handwriting style text (not shown).
    """
    print("===== Read File - remote =====")

    # Get an image with text
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path")
    image_path = parser.parse_args().image_path

    try:
        results = upload_and_analyse(image_path)

        # Print the detected text, line by line
        for text_result in results:
            for line in text_result.lines:
                print(line.text)
                print(line.bounding_box)

    except Exception as e:
        print(e)
        print("Error: Failed to read on Azure!")
