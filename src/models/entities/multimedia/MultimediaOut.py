class MultimediaOut():

    def __init__(self, archive_url, archive_type) -> None:
        self.archive_url = archive_url
        self.archive_type = archive_type

    def to_JSON(self):
        return {
            'archive_url': self.archive_url,
            'archive_type': self.archive_type
        }