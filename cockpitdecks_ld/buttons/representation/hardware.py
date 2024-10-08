"""
Special represenations for web decks, to draw a "hardware" button
"""

import logging

from PIL import Image, ImageDraw

from cockpitdecks.resources.color import TRANSPARENT_PNG_COLOR
from cockpitdecks.buttons.representation.hardware import HardwareRepresentation, NO_ICON

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


class VirtualLLColoredButton(HardwareRepresentation):
    """Uniform color or texture icon

    Attributes:
        REPRESENTATION_NAME: "virtual-ll-coloredbutton"
    """

    REPRESENTATION_NAME = "virtual-ll-coloredbutton"

    def __init__(self, button: "Button"):
        HardwareRepresentation.__init__(self, button=button)

        self.knob_fill_color = self.hardware.get("knob-fill-color", "#21211f")
        self.knob_stroke_color = self.hardware.get("knob-stroke-color", "black")
        self.knob_stroke_width = self.hardware.get("knob-stroke-width", 1)

        self.off_color = self.hardware.get("off-color", (96, 96, 96))

        # This is the symbol that will be used (character 0 to 7)
        # Needs extension to allow for other symbols
        self.number = int(self.button.num_index if self.button.num_index is not None else 0)
        self.number_color = self.button._representation.render()

    def get_image(self):
        image = Image.new(mode="RGBA", size=(2 * self.radius, 2 * self.radius), color=TRANSPARENT_PNG_COLOR)
        draw = ImageDraw.Draw(image)
        # knob
        draw.ellipse(
            [1, 1] + [2 * self.radius - 1, 2 * self.radius - 1],
            fill=self.knob_fill_color,
            outline=self.knob_stroke_color,
            width=self.knob_stroke_width,
        )
        # marker
        self.number_color = self.button._representation.render()
        color = self.off_color if self.button.value == 0 else self.number_color
        if self.number == 0:  # special marker for 0
            size = int(self.radius * 0.9)
            draw.ellipse(
                [self.radius - int(size / 2), self.radius - int(size / 2)] + [self.radius + int(size / 2), self.radius + int(size / 2)],
                outline=color,
                width=2,
            )
            size = 4
            draw.ellipse([self.radius - int(size / 2), self.radius - int(size / 2)] + [self.radius + int(size / 2), self.radius + int(size / 2)], fill=color)
        else:
            font = self.get_font(self.get_attribute("font"), int(self.radius))  # (standard font)
            draw.text(
                (self.radius, self.radius),
                text=str(self.number),
                fill=color,
                font=font,
                anchor="mm",
                align="center",
            )
        return image

    def describe(self) -> str:
        return "The representation places a color button with number for LoupedeckLive colored button."
