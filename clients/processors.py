from django.conf import settings

from PIL import Image


class WatermarkProcessor:

    """
        Pastes watermark to avatar image before adding to database
    """

    def process(self, avatar):
        watermark = Image.open(settings.WATERMARK_URL)

        # Avatar and watermark sizes
        wm_width = watermark.width
        wm_height = watermark.height

        avatar_width = avatar.width
        avatar_height = avatar.height

        # Watermark position to paste in avatar image
        wm_position = (avatar_width - wm_width, avatar_height - wm_height)

        # New avatar with watermark processing
        wm_avatar = Image.new("RGBA", avatar.size)
        wm_avatar.paste(avatar, (0, 0))
        wm_avatar.paste(watermark, wm_position, mask=watermark)

        return wm_avatar
