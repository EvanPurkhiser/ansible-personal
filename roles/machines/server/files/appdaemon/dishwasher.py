# -*- coding: utf-8 -*-

import hassapi as hass
import collections

from dateutil import parser
from datetime import datetime, timedelta

from utils import time_ago

# The cutoff current that we consider the dishwasher to be "off"
THRESHOLD = 0.1

Value = collections.namedtuple("Value", ["date", "value"])


class Dishwasher(hass.Hass):
    last_notification = None

    def initialize(self):
        self.listen_state(self.power_update, entity="sensor.dishwasher_current")
        self.power_update()

    @property
    def current_history(self):
        """
        Most recent entries first
        """
        history = list(
            map(
                lambda v: Value(
                    parser.parse(v["last_updated"]),
                    float(0 if v["state"] == "unknown" else v["state"]),
                ),
                self.get_history(entity_id="sensor.dishwasher_current", days=1)[0],
            )
        )
        history.reverse()
        return history

    def power_update(self, *args, **kwargs):
        ln = self.last_notification
        now = datetime.now().astimezone()

        # We already recently reported the dishwasher as having finished
        if ln is not None and now - timedelta(minutes=30) > ln:
            return

        history = self.current_history

        # Locate the most recent point the current was above the threshold
        try:
            last_index = next(i for i, v in enumerate(history) if v.value > THRESHOLD)
        except StopIteration:
            # No history of the machine being run
            return

        # Dishwasher is still running if most recent entry is above the threshold
        if last_index == 0:
            return

        last = history[last_index]

        # We want at least 5 minutes of below threshold before reporting
        if last.date > now - timedelta(minutes=5):
            return

        # Verify that it has a power history from ~ 10-20m ago
        time_ago_10 = now - timedelta(minutes=15)
        time_ago_20 = now - timedelta(minutes=25)

        try:
            ten_min_ago_event = next(
                value
                for _, value in enumerate(history[last_index:])
                if value.date < time_ago_10 and value.date > time_ago_20
            )
        except StopIteration:
            # Probably not enough data
            return

        if ten_min_ago_event.value < THRESHOLD:
            return

        # If the last high value was before the last notification it's already
        # been reported.
        if ln is not None and last.date < ln:
            return

        finished_human = time_ago(last.date, now=now)

        self.send_msg(f"💦 Dishwasher finished cleaning! ({finished_human})")
        self.last_notification = now

    def send_msg(self, msg, **kwargs):
        self.call_service("telegram_bot/send_message", message=msg, **kwargs)
