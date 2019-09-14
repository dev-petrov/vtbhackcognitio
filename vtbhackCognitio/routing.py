from channels.routing import URLRouter, ProtocolTypeRouter
from django.conf.urls import url
from .apps.api.consumers import MessageConsumer


application = ProtocolTypeRouter({
    'websocket':URLRouter([
    url(r'^api/get_comments/$', MessageConsumer),
])
}) 