import re
from typing import Literal

from nonebot.adapters import Event
from nonebot.consts import ENDSWITH_KEY, STARTSWITH_KEY
from nonebot.rule import Rule
from nonebot.typing import T_State

BOT_COMMAND_ARG_KEY: Literal["_irons_bot_command_arg"] = "_irons_bot_command_arg"


class StartswithOrEndswithRule:
    """检查消息纯文本是否以指定字符串开头或结尾（OR 语义）。

    匹配成功后始终设置 STARTSWITH_KEY 和 ENDSWITH_KEY（未命中侧为空字符串），
    并设置 BOT_COMMAND_ARG_KEY 为去除前缀/后缀后的文本。
    """

    __slots__ = ("ignorecase", "prefix", "suffix")

    def __init__(
        self,
        prefix: tuple[str, ...],
        suffix: tuple[str, ...] | None = None,
        ignorecase: bool = False,
    ) -> None:
        self.prefix = prefix
        self.suffix = suffix if suffix is not None else prefix
        self.ignorecase = ignorecase

    def __repr__(self) -> str:
        return (
            f"StartswithOrEndswith("
            f"prefix={self.prefix}, suffix={self.suffix}, "
            f"ignorecase={self.ignorecase})"
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, StartswithOrEndswithRule)
            and frozenset(self.prefix) == frozenset(other.prefix)
            and frozenset(self.suffix) == frozenset(other.suffix)
            and self.ignorecase == other.ignorecase
        )

    def __hash__(self) -> int:
        return hash((frozenset(self.prefix), frozenset(self.suffix), self.ignorecase))

    async def __call__(self, event: Event, state: T_State) -> bool:
        try:
            text = event.get_plaintext()
        except Exception:
            return False

        flags = re.IGNORECASE if self.ignorecase else 0

        sw = re.match(
            f"^(?:{'|'.join(re.escape(p) for p in self.prefix)})",
            text,
            flags,
        )
        ew = re.search(
            f"(?:{'|'.join(re.escape(s) for s in self.suffix)})$",
            text,
            flags,
        )

        if not sw and not ew:
            return False

        state[STARTSWITH_KEY] = sw.group() if sw else ""
        state[ENDSWITH_KEY] = ew.group() if ew else ""
        state[BOT_COMMAND_ARG_KEY] = text.replace(state[STARTSWITH_KEY], "").replace(
            state[ENDSWITH_KEY], ""
        )
        return True


def startswith_or_endswith(
    prefix: str | tuple[str, ...],
    suffix: str | tuple[str, ...] | None = None,
    ignorecase: bool = True,
) -> Rule:
    """匹配消息开头或结尾为指定字符串的规则。

    Args:
        prefix: 前缀或前缀元组
        suffix: 后缀或后缀元组，为 None 时复用 prefix
        ignorecase: 是否忽略大小写
    """
    if isinstance(prefix, str):
        prefix = (prefix,)
    if isinstance(suffix, str):
        suffix = (suffix,)
    return Rule(StartswithOrEndswithRule(prefix, suffix, ignorecase))


class NoReply:
    """仅匹配没有回复消息的规则。"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "NoReply()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NoReply)

    def __hash__(self) -> int:
        return hash(())

    async def __call__(self, event: Event, _: T_State) -> bool:
        reply = getattr(event, "reply", None)
        return reply is None


def no_reply() -> Rule:
    return Rule(NoReply())
