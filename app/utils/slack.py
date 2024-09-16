from slack_sdk import WebClient


class Slack:
    def __init__(self, token: str):
        self.client = WebClient(token)
        self.channels = self.get_channels()

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
        return channel_id

    def post_text(self, channel, text, **kwargs):
        """Post a message to a channel

        Args:
            channel (str): Slack channel name
            text (str): Message text

        Returns:
            dict: API response
        """
        response = self.client.chat_postMessage(
            channel=self.get_channel_id(channel),
            text=self._validate_text(text),
            **kwargs
        )
        return response

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
