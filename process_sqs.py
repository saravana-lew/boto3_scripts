#!/usr/bin/env python3

import boto3
import time

# Configuration
QUEUE_URL = "https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>"
POLL_INTERVAL = 10  # Poll every 10 seconds

def process_message(message):
    """Process the SQS message."""
    print(f"Processing message: {message['Body']}")
    # Add custom processing logic here

def main():
    sqs = boto3.client('sqs')

    while True:
        try:
            # Receive messages
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10
            )

            if 'Messages' in response:
                for message in response['Messages']:
                    process_message(message)

                    # Delete the message after processing
                    sqs.delete_message(
                        QueueUrl=QUEUE_URL,
                        ReceiptHandle=message['ReceiptHandle']
                    )
                    print("Message processed and deleted.")
            else:
                print("No messages received. Waiting...")

        except Exception as e:
            print(f"Error: {e}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()