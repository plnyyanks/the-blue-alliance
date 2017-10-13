import datetime


class FMSAPIOffseasonsWithDataSyncParser(object):

    EVENT_TYPES = {
        'offseasonwithazuresync'
    }

    def __init__(self, season, existing_offseasons):
        self.season = season
        self.existing_offseasons = existing_offseasons

    def parse(self, response):
        valid_events = filter(lambda e: e['type'].lower() in self.EVENT_TYPES, response['Events'])

        events_to_mark_official = []
        events_to_link_key = []
        events_to_create_suggestion = []

        for event in valid_events:
            first_event_code = event['code'].lower()
            existing_event = next(e for e in self.existing_offseasons if e.event_short == first_event_code or e.first_code == first_event_code)

            if existing_event.event_short == first_event_code and

    def is_event_probably_the_same(self, tba_event, first_event):
        """
        The event from the FIRST API is probably the same as the TBA event if...
         - Their start/end dates are within 24 hours
         - They're in the same state
        """
        return 
