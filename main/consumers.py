import logging
from channels import Group
from channels.sessions import channel_session

log = logging.getLogger(__name__)


@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    Group('display').add(message.reply_channel)

@channel_session
def ws_disconnect(message):
    Group('display').discard(message.reply_channel)