"""Using boto3, instead of awscli, to tail logs. Based on https://github.com/aws/aws-cli/blob/v2/awscli/customizations/logs/tail.py"""

from collections import defaultdict
import sys
import time

import boto3
from botocore.exceptions import ClientError, ParamValidationError
from env import config_data


SLEEP = 5

def tail_logs():
    access_key_id = config_data["AWS_ACCESS_KEY_ID"]
    secret_access_key = config_data["AWS_SECRET_ACCESS_KEY"]
    client = boto3.client('logs', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')

    # this can be `boto3.client(logs)` instead of using `session`
    filter_logs_events_kwargs = {
        "logGroupName": "/aws/sagemaker/TrainingJobs",
        "logStreamNames": "put-green-black-work/algo-1-1692170805",
        "interleaved": True,
        "startTime": int(time.time()) * 1000
    }
    return _filter_log_events(client, filter_logs_events_kwargs)

def _filter_log_events(client, filter_logs_events_kwargs):
    try:
        for event in _do_filter_log_events(client, filter_logs_events_kwargs):
            yield event
    except KeyboardInterrupt:
        # The only way to exit from the --follow is to Ctrl-C. So
        # we should exit the iterator rather than having the
        # KeyboardInterrupt propogate to the rest of the command.
        return

def _get_latest_events_and_timestamp(event_ids_per_timestamp):
    if event_ids_per_timestamp:
        # Keep only ids of the events with the newest timestamp
        newest_timestamp = max(event_ids_per_timestamp.keys())
        event_ids_per_timestamp = defaultdict(
            set, {newest_timestamp: event_ids_per_timestamp[newest_timestamp]}
        )
    return event_ids_per_timestamp

def _reset_filter_log_events_params(fle_kwargs, event_ids_per_timestamp):
    # Remove nextToken and update startTime for the next request
    # with the timestamp of the newest event
    if event_ids_per_timestamp:
        fle_kwargs['startTime'] = max(
            event_ids_per_timestamp.keys()
        )
    fle_kwargs.pop('nextToken', None)

def _do_filter_log_events(client, filter_logs_events_kwargs):
    event_ids_per_timestamp = defaultdict(set)
    while True:
        try:
            response = client.filter_log_events(
                **filter_logs_events_kwargs)
        except (ClientError, ParamValidationError):
            sys.exit("Invalid MFA one time pass code")

        for event in response['events']:
            # For the case where we've hit the last page, we will be
            # reusing the newest timestamp of the received events to keep polling.
            # This means it is possible that duplicate log events with same timestamp
            # are returned back which we do not want to yield again.
            # We only want to yield log events that we have not seen.
            if event['eventId'] not in event_ids_per_timestamp[event['timestamp']]:
                event_ids_per_timestamp[event['timestamp']].add(event['eventId'])
                yield event
        event_ids_per_timestamp = _get_latest_events_and_timestamp(
            event_ids_per_timestamp
        )
        if 'nextToken' in response:
            filter_logs_events_kwargs['nextToken'] = response['nextToken']
        else:
            _reset_filter_log_events_params(
                filter_logs_events_kwargs,
                event_ids_per_timestamp
            )
            time.sleep(SLEEP)