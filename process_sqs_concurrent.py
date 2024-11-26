#!/usr/bin/env python3

import boto3
import time
from concurrent.futures import ThreadPoolExecutor

# Configuration
QUEUE_URL = "https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>"
POLL_INTERVAL = 10  # Poll every 10 seconds
MAX_THREADS = 5     # Number of worker threads

def process_message(message):
    """Process the SQS message."""
    try:
        print(f"Processing message: {message['Body']}")
        # Add custom processing logic here
        time.sleep(2)  # Simulate processing time
    except Exception as e:
        print(f"Error processing message: {e}")
    return message

def delete_message(sqs, message):
    """Delete the message from the SQS queue after processing."""
    try:
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=message['ReceiptHandle']
        )
        print(f"Deleted message: {message['MessageId']}")
    except Exception as e:
        print(f"Error deleting message: {e}")

def poll_and_process(sqs):
    """Poll the SQS queue and process messages in threads."""
    while True:
        try:
            # Receive messages
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=10,  # Fetch multiple messages at once
                WaitTimeSeconds=10
            )

            if 'Messages' in response:
                with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                    # Process messages concurrently
                    futures = {executor.submit(process_message, msg): msg for msg in response['Messages']}

                    for future in futures:
                        message = futures[future]
                        try:
                            # Wait for the processing to complete
                            future.result()
                            # Delete the message
                            delete_message(sqs, message)
                        except Exception as e:
                            print(f"Error in message processing: {e}")
            else:
                print("No messages received. Waiting...")
        except Exception as e:
            print(f"Polling error: {e}")

        time.sleep(POLL_INTERVAL)

def main():
    sqs = boto3.client('sqs')
    print("Starting SQS processor...")
    poll_and_process(sqs)

if __name__ == "__main__":
    main()