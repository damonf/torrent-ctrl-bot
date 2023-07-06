from telegram.ext.filters import MessageFilter


class FilterMagnet(MessageFilter):
    def filter(self, message):
        return message.text.startswith("magnet:")
