import dataclasses
import datetime
import uuid

from aiochclient import ChClient, Record

from application.settings import Settings


@dataclasses.dataclass
class RegisterAnalytics:
    ch_client: ChClient
    settings: Settings

    async def set_event(self, request_data: str, status_code: int, error_message: str) -> None:
        event_time = datetime.datetime.now()
        event_time_str = event_time.strftime("%Y-%m-%d %H:%M:%S")
        query = f"""
            INSERT INTO {self.settings.CH_DB}.user_registration_events (
            id,
            request_data,
            status_code,
            error_message,
            event_time
        ) VALUES (
            '{uuid.uuid4()}',
            '{request_data}',
            {status_code},
            '{error_message}',
            '{event_time_str}'
        );
        """
        try:
            await self.ch_client.execute(query=query)
        except Exception as e:
            print(e)

    async def get_events(self) -> list[Record]:
        query = f"SELECT * FROM {self.settings.CH_DB}.user_registration_events"  # noqa: S608
        return await self.ch_client.fetch(query=query)
