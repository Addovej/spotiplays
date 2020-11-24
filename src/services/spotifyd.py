import asyncio
import re
from logging import getLogger
from subprocess import PIPE, STDOUT

logger = getLogger('console')


class Spotifyd:
    _spotifyd = None
    _listener_task = None

    _auth: str = None
    _current_playback: dict = None

    def __init__(self):
        self.cmd = '/usr/bin/spotifyd --no-daemon ' \
                   '--initial-volume 51 ' \
                   '--config-path /etc/spotifyd.conf'

    @property
    def current_playback(self) -> dict:
        return self._current_playback

    @property
    def user(self) -> str:
        return self._auth

    async def _listener(self) -> None:
        while True:
            line = await self._spotifyd.stdout.readline()
            event = line.decode().strip()

            if event.startswith('Authenticated'):
                self._auth, *_ = re.findall(r'"(.*?)"', event)
                logger.info(f'Authenticated as {self._auth!r}')
            elif event.startswith('Loading <'):
                name, uri, *_ = re.findall(r'<(.*?)>', event)
                self._current_playback = {
                    'name': name,
                    'uri': uri
                }
                logger.info(f'Current track: {name!r}[{uri}]')
            else:
                logger.info(f'Event: {event!r}')

    async def start(self):
        self._spotifyd = await asyncio.create_subprocess_shell(
            self.cmd,
            stdin=PIPE, stdout=PIPE, stderr=STDOUT
        )
        self._listener_task = asyncio.create_task(self._listener())

    async def stop(self) -> None:
        if self._listener_task.done():
            self._listener_task.result()
        else:
            self._listener_task.cancel()
        self._spotifyd.terminate()

    async def restart(self) -> None:
        await self.stop()
        await self.start()


spotifyd = Spotifyd()
