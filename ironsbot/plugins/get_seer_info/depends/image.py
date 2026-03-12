from nonebot.adapters.onebot.v11 import MessageSegment as OneBotV11MessageSegment
from nonebot.params import Depends

from ironsbot.utils.image import GetImage

PET_IMAGE_URL_TEMPLATE = "https://newseer.61.com/web/monster/body/{}.png"
PetBodyImageGetter = GetImage(PET_IMAGE_URL_TEMPLATE, cls=OneBotV11MessageSegment)
PetBodyImage = Depends(PetBodyImageGetter)


MINTMARK_IMAGE_URL_TEMPLATE = "https://newseer.61.com/web/countermark/icon/{}.png"
MintmarkBodyImageGetter = GetImage(
    MINTMARK_IMAGE_URL_TEMPLATE, cls=OneBotV11MessageSegment
)
MintmarkBodyImage = Depends(MintmarkBodyImageGetter)


ELEMENT_TYPE_IMAGE_URL_TEMPLATE = "https://newseer.61.com/web/PetType/{}.png"
ElementTypeImageGetter = GetImage(
    ELEMENT_TYPE_IMAGE_URL_TEMPLATE, cls=OneBotV11MessageSegment
)
ElementTypeImage = Depends(ElementTypeImageGetter)

PREVIEW_IMAGE_URL_TEMPLATE = "https://raw.githubusercontent.com/WhY15w/seer-unity-preview-img-dumper/refs/heads/main/img/preview.png"
PreviewImageGetter = GetImage(PREVIEW_IMAGE_URL_TEMPLATE, cls=OneBotV11MessageSegment)
PreviewImage = Depends(PreviewImageGetter)
