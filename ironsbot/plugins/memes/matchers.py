import random
from collections.abc import AsyncGenerator, Callable
from dataclasses import dataclass
from typing import NoReturn

import nonebot
from nonebot import MatcherGroup
from nonebot.adapters import Message, MessageTemplate
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.exception import FinishedException
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Depends

from ironsbot.utils.cnb import CnbApi
from ironsbot.utils.rule import no_reply

from .config import meme_is_enabled, plugin_config

matcher_group = MatcherGroup()


def get_cnb_api(token: str, repo: str) -> Callable[[], AsyncGenerator[CnbApi, None]]:
    async def _get_cnb_api() -> AsyncGenerator[CnbApi, None]:
        async with CnbApi(token, repo=repo) as cnb:
            yield cnb

    return _get_cnb_api


@dataclass(frozen=True)
class ImageCommandConfig:
    """基于索引的图片命令配置。"""

    command: str
    aliases: set[str | tuple[str, ...]]
    max_index: int
    image_path_template: str
    message_template: str


def create_image_command(
    group: MatcherGroup,
    config: ImageCommandConfig,
    cnb_factory: Callable[..., AsyncGenerator[CnbApi, None]],
) -> type[Matcher]:
    """根据配置创建一个「随机/指定索引 + CnbApi 图片」的命令。"""
    matcher = group.on_command(config.command, aliases=config.aliases, rule=no_reply())
    template = MessageTemplate(config.message_template)

    async def _handler(
        m: Matcher,
        arg: Message = CommandArg(),
        cnb: CnbApi = Depends(cnb_factory),
    ) -> NoReturn:
        random_text = "自选"
        arg_str = arg.extract_plain_text()
        if arg_str.isdigit():
            index = int(arg_str)
        elif not arg_str:
            index = random.randint(1, config.max_index)
            random_text = "随机"
        else:
            raise FinishedException

        if not 1 <= index <= config.max_index:
            await m.finish(f"编号必须在1到{config.max_index}之间！")

        image = MessageSegment.image(
            await cnb.get_file(config.image_path_template.format(index=index))
        )
        await m.finish(
            template.format(
                random_text=random_text,
                index=index,
                total=config.max_index,
                image=image,
            )
        )

    matcher.append_handler(_handler)
    return matcher


# ============ 命令配置 ============

COMMANDS: list[ImageCommandConfig] = []

if plugin_config.cnb_token and plugin_config.cnb_repo:
    _cnb_factory = get_cnb_api(plugin_config.cnb_token, plugin_config.cnb_repo)

    if meme_is_enabled("tudou"):
        COMMANDS.append(
            ImageCommandConfig(
                command="土豆",
                aliases={"今日土豆", "随机土豆", "🥔"},
                max_index=2185,
                image_path_template="tudou/{index}.gif",
                message_template=(
                    "{random_text}土豆（{index}/{total}）\n🌈发【土豆x】直接出x号土豆\n{image}"
                ),
            )
        )
    if meme_is_enabled("pig"):
        COMMANDS.append(
            ImageCommandConfig(
                command="小猪",
                aliases={"今日小猪", "随机小猪", "🐷", "🐖"},
                max_index=166,
                image_path_template="pig/{index}.jpg",
                message_template=(
                    "{random_text}小猪（{index}/{total}）\n🌈发【小猪x】直接出x号小猪\n{image}"
                ),
            )
        )

    for _cmd in COMMANDS:
        create_image_command(matcher_group, _cmd, _cnb_factory)

else:
    nonebot.logger.warning("CNB 相关配置未设置，表情包命令将不会生效")
