from __future__ import annotations

import datetime as dt
from typing import Any


class Calendar:
    # Reference: https://developers.google.com/calendar/api/v3/reference/calendarList#resource-representations
    def __init__(
        self,
        kind: str,
        etag: str,
        id: str,
        summary: str,
        accessRole: str,
        defaultReminders: list[dict[str, str | int]],
        description: str = "",
        location: str = "",
        timeZone: str = "",
        summaryOverride: str = "",
        colorId: str = "",
        backgroundColor: str = "",
        foregroundColor: str = "",
        hidden: bool = False,
        selected: bool = False,
        notificationSettings: dict[str, str] = {},
        primary: bool = False,
        deleted: bool = False,
        conferenceProperties: dict[str, str] | None = None,
    ):
        self.kind: str = kind
        self.etag: str = etag
        self.id: str = id
        self.summary: str = summary
        self.access_role: str = accessRole
        self.default_reminders: list[dict[str, str | int]] = defaultReminders
        self.notification_settings: dict[str, str] = notificationSettings
        self.description: str = description
        self.location: str = location
        self.timeZone: str = timeZone
        self.summary_override: str = summaryOverride
        self.color_id: str = colorId
        self.background_color: str = backgroundColor
        self.foreground_color: str = foregroundColor
        self.hidden: bool = hidden
        self.selected: bool = selected
        self.primary: bool = primary
        self.deleted: bool = deleted
        self.conference_properties: dict[str, str] | None = conferenceProperties

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> Calendar:
        return cls(**data)

    def __repr__(self) -> str:
        return f"<Google Calendar: {self.summary}>"


class EventTime:
    def __init__(
        self,
        date: str = "",
        dateTime: str = "",
        timeZone: str = "",
    ):
        self.date: dt.datetime | None = (
            dt.datetime.fromisoformat(date) if date else None
        )
        self.date_time: dt.datetime | None = (
            dt.datetime.fromisoformat(dateTime) if dateTime else None
        )
        self.time_zone: str = timeZone

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> EventTime:
        return cls(**data)

    def __repr__(self) -> str:
        return f"<Google Calendar Event Time: {self.date_time}>"


class Event:
    # Reference: https://developers.google.com/calendar/api/v3/reference/events#resource-representations
    def __init__(
        self,
        kind: str,
        etag: str,
        id: str,
        htmlLink: str,
        created: str,
        updated: str,
        summary: str,
        creator: dict[str, str | bool],
        organizer: dict[str, str | bool],
        start: dict[str, str],
        end: dict[str, str],
        iCalUID: str,
        sequence: int,
        eventType: str,
        status: str = "",
        description: str = "",
        location: str = "",
        colorId: str = "",
        transparency: str = "",
        visibility: str = "",
        attendeesOmitted: bool = False,
        anyoneCanAddSelf: bool = False,
        guestsCanInviteOthers: bool = True,
        guestsCanModify: bool = False,
        guestsCanSeeOtherGuests: bool = True,
        privateCopy: bool = False,
        endTimeUnspecified: bool = False,
        recurringEventId: str = "",
        originalStartTime: dict[str, str] = {},
        attendees: list[dict[str, str | bool | int]] = [],
        extendedProperties: dict[str, Any] = {},
        hangoutLink: str = "",
        conferenceData: dict[str, Any] = {},
        gadget: dict[str, Any] = {},
        locked: bool = False,
        source: dict[str, str] = {},
        workingLocationProperties: dict[str, Any] = {},
        outOfOfficeProperties: dict[str, str] = {},
        focusTimeProperties: dict[str, str] = {},
        attachments: list[dict[str, str]] = [],
        recurrence: list[str] = [],
        reminders: dict[str, Any] = {},
    ):
        self.kind: str = kind
        self.etag: str = etag
        self.id: str = id
        self.htmlLink: str = htmlLink
        self.created: dt.datetime = dt.datetime.fromisoformat(created)
        self.updated: dt.datetime = dt.datetime.fromisoformat(updated)
        self.summary: str = summary
        self.creator: dict[str, str | bool] = creator
        self.organizer: dict[str, str | bool] = organizer
        self.start: EventTime = EventTime.from_response(start)
        self.end: EventTime = EventTime.from_response(end)
        self.end_time_unspecified: bool = endTimeUnspecified
        self.recurrence: list[str] = recurrence
        self.recurring_event_id: str = recurringEventId
        self.original_start_time: EventTime = EventTime.from_response(originalStartTime)
        self.ical_uid: str = iCalUID
        self.sequence: int = sequence
        self.attendees: list[dict[str, str | bool | int]] = attendees
        self.extended_properties: dict[str, Any] = extendedProperties
        self.hangout_link: str = hangoutLink
        self.conference_data: dict[str, Any] = conferenceData
        self.gadget: dict[str, Any] = gadget
        self.locked: bool = locked
        self.reminders: dict[str, Any] = reminders
        self.source: dict[str, str] = source
        self.working_location_properties: dict[str, Any] = workingLocationProperties
        self.out_of_office_properties: dict[str, str] = outOfOfficeProperties
        self.focus_time_properties: dict[str, str] = focusTimeProperties
        self.attachments: list[dict[str, str]] = attachments
        self.event_type: str = eventType
        self.status: str = status
        self.description: str = description
        self.location: str = location
        self.color_id: str = colorId
        self.transparency: str = transparency
        self.visibility: str = visibility
        self.attendees_omitted: bool = attendeesOmitted
        self.anyone_can_add_self: bool = anyoneCanAddSelf
        self.guests_can_invite_others: bool = guestsCanInviteOthers
        self.guests_can_modify: bool = guestsCanModify
        self.guests_can_see_other_guests: bool = guestsCanSeeOtherGuests
        self.private_copy: bool = privateCopy

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> Event:
        return cls(**data)

    def __repr__(self) -> str:
        return f"<Google Calendar Event: {self.summary}>"
