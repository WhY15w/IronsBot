from nonebot.plugin import PluginMetadata

from .config import Config
from .matchers import matcher_group as matcher_group

usage = """表情包相关命令

命令：
  土豆/今日土豆/随机土豆/🥔 <索引(可选)> — 随机或指定索引的土豆表情包

  小猪/今日小猪/随机小猪/🐷/🐖 <索引(可选)> — 随机或指定索引的小猪表情包

  咖波/今日咖波/随机咖波/capoo/猫猫虫 <索引(可选)> — 随机或指定索引的咖波表情包
"""

__plugin_meta__ = PluginMetadata(
    name="表情包",
    description="随机或是指定输出一张可爱表情包",
    usage=usage,
    config=Config,
    supported_adapters={"~onebot.v11"},
)
