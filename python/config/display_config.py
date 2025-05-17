"""
Display configuration for bezels and visual options
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

class BezelStyle(Enum):
    """Available bezel styles"""
    NONE = "none"
    COCO1 = "coco1"  # Color Computer 1/2 - Color Video Receiver
    COCO3 = "coco3"  # Color Computer 3 - CM-8 monitor
    MODERN = "modern"  # Clean modern frame
    CYBERPUNK = "cyberpunk"  # For Chen's sci-fi theme

@dataclass
class DisplayConfig:
    """Display and visual settings"""
    # Screen settings
    window_width: int = 1024
    window_height: int = 768
    fullscreen: bool = False
    
    # Bezel settings
    bezel_style: BezelStyle = BezelStyle.NONE
    bezel_opacity: float = 1.0  # 0.0 to 1.0
    
    # CRT effects
    scanlines: bool = False
    scanline_intensity: float = 0.3
    crt_curvature: float = 0.0  # 0.0 = flat, 1.0 = maximum curve
    phosphor_glow: bool = False
    
    # Color settings
    color_temperature: float = 6500  # Kelvin - affects color warmth
    contrast: float = 1.0
    brightness: float = 1.0
    saturation: float = 1.0
    
    # Retro effects
    screen_flicker: bool = False
    flicker_intensity: float = 0.1
    vignette: bool = False
    vignette_intensity: float = 0.3
    
    def to_json(self) -> dict:
        """Convert to JSON-serializable dict"""
        return {
            'window_width': self.window_width,
            'window_height': self.window_height,
            'fullscreen': self.fullscreen,
            'bezel_style': self.bezel_style.value,
            'bezel_opacity': self.bezel_opacity,
            'scanlines': self.scanlines,
            'scanline_intensity': self.scanline_intensity,
            'crt_curvature': self.crt_curvature,
            'phosphor_glow': self.phosphor_glow,
            'color_temperature': self.color_temperature,
            'contrast': self.contrast,
            'brightness': self.brightness,
            'saturation': self.saturation,
            'screen_flicker': self.screen_flicker,
            'flicker_intensity': self.flicker_intensity,
            'vignette': self.vignette,
            'vignette_intensity': self.vignette_intensity
        }
    
    @classmethod
    def from_json(cls, data: dict) -> 'DisplayConfig':
        """Create from JSON data"""
        if 'bezel_style' in data:
            data['bezel_style'] = BezelStyle(data['bezel_style'])
        return cls(**data)

# Preset configurations
PRESETS = {
    "authentic_coco1": DisplayConfig(
        bezel_style=BezelStyle.COCO1,
        scanlines=True,
        scanline_intensity=0.4,
        crt_curvature=0.3,
        phosphor_glow=True,
        color_temperature=5500,  # Warmer, like old CRTs
        screen_flicker=True,
        flicker_intensity=0.05,
        vignette=True
    ),
    
    "authentic_coco3": DisplayConfig(
        bezel_style=BezelStyle.COCO3,
        scanlines=True,
        scanline_intensity=0.3,
        crt_curvature=0.2,
        phosphor_glow=True,
        color_temperature=6200,
        vignette=True
    ),
    
    "modern_clean": DisplayConfig(
        bezel_style=BezelStyle.MODERN,
        bezel_opacity=0.8,
        window_width=1920,
        window_height=1080
    ),
    
    "cyberpunk": DisplayConfig(
        bezel_style=BezelStyle.CYBERPUNK,
        scanlines=True,
        scanline_intensity=0.2,
        phosphor_glow=True,
        color_temperature=8000,  # Cooler, blue-ish
        contrast=1.2,
        saturation=1.3,
        screen_flicker=True,
        flicker_intensity=0.02
    )
}