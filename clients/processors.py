from PIL import Image

from django.conf import settings


class WatermarkProcessor:

    def process(self, avatar):
        watermark = Image.open(settings.WATERMARK_URL)

        wm_width = watermark.width
        wm_height = watermark.height

        avatar_width = avatar.width
        avatar_height = avatar.height

        wm_position = (avatar_width - wm_width, avatar_height - wm_height)

        # New avatar with watermark
        wm_avatar = Image.new("RGBA", avatar.size)
        wm_avatar.paste(avatar, (0, 0))
        wm_avatar.paste(watermark, wm_position, mask=watermark)

        return wm_avatar
