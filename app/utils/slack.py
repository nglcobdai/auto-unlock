import time

from requests.exceptions import RequestException
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Slack:
    def __init__(self, token: str):
        self.client = WebClient(token)
        self.channels = self.get_channels()
        self.mx_retry = 3
        self.retry = 0

    def get_channels(self, exclude_archived=True, **kwargs):
        """Get channel list

        Returns:
            list: Channel list
        """
        channels = self.client.conversations_list(
            exclude_archived=exclude_archived, **kwargs
        )
        return channels["channels"]

    def get_channel_id(self, channel):
        """Get channel ID

        Args:
            channel (str): Slack channel name

        Returns:
            str: Channel ID
        """
        channel_id = None
        for ch in self.channels:
            if ch["name"] == channel:
                channel_id = ch["id"]
                break
        if not channel_id:
            # `response`を空の辞書にするか、モックしたデータを使用する
            mock_response = {"ok": False, "error": "channel_not_found"}
            raise SlackApiError("Channel not found", response=mock_response)
        return channel_id

    def post_text(self, channel, text, **kwargs):
        """Post a message to a channel

        Args:
            channel (str): Slack channel name
            text (str): Message text

        Returns:
            dict: API response
        """
        try:
            return self._post_text(channel, text, **kwargs)
        except (RequestException, SlackApiError) as e:
            if self.retry >= self.mx_retry:
                raise e
            time.sleep(10)  # Wait 10 seconds
            self.retry += 1
            return self.post_text(channel, e, **kwargs)

    def _post_text(self, channel, text, **kwargs):
        """Post a message to a channel

        Args:
            channel (str): Slack channel name
            text (str): Message text

        Returns:
            dict: API response
        """
        try:
            response = self.client.chat_postMessage(
                channel=self.get_channel_id(channel),
                text=self._validate_text(text),
                **kwargs,
            )
            return response
        except SlackApiError as e:
            raise e

    def post_file(self, channel, files, **kwargs):
        """Post a file to a channel

        Args:
            channel (str): Slack channel name
            files (List[Dict]): List of files to upload
                [
                    {
                        "file": "README.md",
                        "title": "README"
                    },
                ]
            initial_comment (str, optional): Initial comment(None).

        Returns:
            dict: API response
        """
        response = self.client.files_upload_v2(
            channel=self.get_channel_id(channel), file_uploads=files, **kwargs
        )
        return response

    def _validate_text(self, text):
        """Validate text

        Args:
            text (str): Text

        Returns:
            bool: True if valid
        """
        if not text:
            return " "
        if len(text) == 0:
            return " "
        if len(text) > 3000:
            return text[:3000]
        return text
