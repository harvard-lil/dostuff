import logging
from channels import Group
from channels.sessions import channel_session

log = logging.getLogger(__name__)


@channel_session
def ws_connect(message, room_name):
    message.reply_channel.send({"accept": True})
    Group('room-%s' % room_name).add(message.reply_channel)
    message.channel_session['room'] = room_name

@channel_session
def ws_disconnect(message):
    if 'room' in message.channel_session:
        Group('room-%s' % message.channel_session['room']).discard(message.reply_channel)