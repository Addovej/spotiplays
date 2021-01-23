import asyncio
import re
from asyncio import Task
from asyncio.subprocess import Process
from logging import getLogger
from subprocess import PIPE, STDOUT
from typing import Optional

from api.v1.spotifyd.schemas import AccountSchema
from conf import settings
from models import Account, ActiveAccount

__all__ = (
    'spotifyd',
)

logger = getLogger('console')


class Spotifyd:
    _spotifyd: Optional[Process] = None
    _listener_task: Optional[Task] = None

    _account: Optional[AccountSchema] = None
    _auth: Optional[str] = None
    _cmd: Optional[str] = None
    _current_playback: Optional[dict] = None

    errors: list = []

    async def _init_account(self, account: AccountSchema = None) -> None:
        if account and account.is_verified():
            await ActiveAccount.set_active(account.id)
            self._account = account

        if self._account is None:
            active = await ActiveAccount.get_active()
            if active:
                account_db = await Account.get_by_id(active['account_id'])
                self._account = AccountSchema.parse_obj(account_db)

                logger.debug(f'Initialized account {self._account.name!r}.')

    def _build_cmd(self) -> None:
        if self._account and self._account.is_verified():
            # TODO: Remember volume and use as initial.
            cmd_list = settings.SPOTIFYD_CMD + [
                f'--config-path {settings.CONFIG_PATH}',
                f'--initial-volume {settings.INITIAL_VOLUME}',
                f'--username {self._account.username}',
                f'--password {self._account.password_decrypted()}'
            ]
            self._cmd = ' '.join(cmd_list)

    @property
    def cmd(self) -> Optional[str]:
        if self._cmd is None:
            self._build_cmd()

        return self._cmd

    @property
    def current_playback(self) -> dict:
        return self._current_playback

    @property
    def user(self) -> dict:
        if self._account:
            return self._account.dict(exclude={'password'})

        return {}

    async def _listener(self) -> None:
        logger.debug('Starting listen messages from spotifyd.')
        restart: bool = False

        while True:
            line = await self._spotifyd.stdout.readline()
            event = line.decode().strip()

            # To prevent infinity empty logs in error
            if not event:
                logger.error('Restarting spotifyd...')
                restart = True
                break

            if event.startswith('Authenticated'):
                self._auth, *_ = re.findall(r'"(.*?)"', event)
                logger.debug(f'Authenticated as {self._auth!r}')

            elif event.startswith('Loading <'):
                name, uri, *_ = re.findall(r'<(.*?)>', event)
                self._current_playback = {
                    'name': name,
                    'uri': uri
                }
                logger.debug(f'Current track: {name!r}[{uri}].')

            elif event.startswith('Caught panic with message:'):
                *_, msg = event.partition(': ')
                self.errors.append(msg)
                logger.error(event)

                if msg.startswith('Authentication failed'):
                    await Account.change_credentials_verification(
                        self._account.id,
                        {'state': 'FAILED', 'details': msg}
                    )

                break

            else:
                logger.debug(f'Spotifyd: {event}')

        logger.debug('Done with listen messages from spotifyd.')
        await self._terminate_or_restart(restart)

    async def start(self, account: AccountSchema = None) -> None:
        await self._init_account(account)

        if self.cmd is not None:
            logger.debug(
                f'Starting spotifyd for {self._account.name!r} account.'
            )

            self._spotifyd = await asyncio.create_subprocess_shell(
                self.cmd,
                stdin=PIPE, stdout=PIPE, stderr=STDOUT
            )
            self._listener_task = asyncio.create_task(self._listener())

    async def stop(self) -> None:
        self._stop_listener_task()
        self._terminate_spotifyd()
        self._reset_data()

    async def restart(self, account: AccountSchema = None) -> None:
        await self.stop()
        await self.start(account)

    async def _terminate_or_restart(self, restart: bool = False) -> None:
        self._terminate_spotifyd()

        if restart:
            await self.start()

    def _reset_data(self) -> None:
        logger.debug('Resetting data.')
        self._account = self._auth = self._cmd = self._current_playback = None

        self.errors = []

    def _stop_listener_task(self) -> None:
        if self._listener_task:
            logger.debug('Stopping listener task.')

            if self._listener_task.done():
                self._listener_task.result()
            else:
                self._listener_task.cancel()

            self._listener_task = None

    def _terminate_spotifyd(self) -> None:
        if self._spotifyd and self._spotifyd.returncode is None:
            logger.debug('Stopping spotifyd.')

            self._spotifyd.terminate()
            self._spotifyd = None


spotifyd = Spotifyd()
