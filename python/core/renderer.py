"""
Renderer module with bezel and CRT effect support
"""

import pygame
import numpy as np
from pathlib import Path
from typing import Optional, Tuple

from config.display_config import DisplayConfig, BezelStyle

class Renderer:
    """
    Handles game rendering with optional bezels and effects
    """
    
    def __init__(self, config: DisplayConfig):
        self.config = config
        self.bezel_surface: Optional[pygame.Surface] = None
        self.game_surface: Optional[pygame.Surface] = None
        self.screen: Optional[pygame.Surface] = None
        
        # Calculate game area within bezel
        self.game_rect = pygame.Rect(0, 0, 640, 480)  # Base game resolution
        self.bezel_rect = pygame.Rect(0, 0, config.window_width, config.window_height)
        
    def init_display(self):
        """Initialize pygame display"""
        pygame.init()
        
        if self.config.fullscreen:
            self.screen = pygame.display.set_mode(
                (0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF
            )
            self.bezel_rect.size = self.screen.get_size()
        else:
            self.screen = pygame.display.set_mode(
                (self.config.window_width, self.config.window_height),
                pygame.DOUBLEBUF
            )
            
        pygame.display.set_caption("Dungeons of Daggorath")
        
        # Create game surface
        self.game_surface = pygame.Surface((640, 480))
        
        # Load bezel if configured
        if self.config.bezel_style != BezelStyle.NONE:
            self.load_bezel()
            
    def load_bezel(self):
        """Load bezel artwork"""
        bezel_path = Path("assets/bezels") / f"{self.config.bezel_style.value}.png"
        
        if bezel_path.exists():
            self.bezel_surface = pygame.image.load(str(bezel_path))
            self.bezel_surface = pygame.transform.scale(
                self.bezel_surface, self.bezel_rect.size
            )
            
            # Calculate game area within bezel (assumes bezel has transparent center)
            # This would need actual bezel dimensions
            if self.config.bezel_style == BezelStyle.COCO1:
                # Color Video Receiver dimensions (example)
                padding = 120
                self.game_rect = pygame.Rect(
                    padding, padding,
                    self.bezel_rect.width - padding * 2,
                    self.bezel_rect.height - padding * 2
                )
            elif self.config.bezel_style == BezelStyle.COCO3:
                # CM-8 monitor dimensions (example)
                padding = 100
                self.game_rect = pygame.Rect(
                    padding, padding,
                    self.bezel_rect.width - padding * 2,
                    self.bezel_rect.height - padding * 2
                )
                
    def apply_crt_effects(self, surface: pygame.Surface) -> pygame.Surface:
        """Apply CRT effects to game surface"""
        result = surface.copy()
        
        if self.config.scanlines:
            self.apply_scanlines(result)
            
        if self.config.phosphor_glow:
            self.apply_phosphor_glow(result)
            
        if self.config.crt_curvature > 0:
            result = self.apply_curvature(result)
            
        if self.config.vignette:
            self.apply_vignette(result)
            
        return result
    
    def apply_scanlines(self, surface: pygame.Surface):
        """Apply scanline effect"""
        # Create scanline overlay
        overlay = pygame.Surface(surface.get_size())
        overlay.fill((0, 0, 0))
        
        # Draw horizontal lines
        for y in range(0, surface.get_height(), 3):
            pygame.draw.line(overlay, (255, 255, 255), (0, y), (surface.get_width(), y))
            
        # Blend with original
        overlay.set_alpha(int(255 * self.config.scanline_intensity))
        surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_SUB)
        
    def apply_phosphor_glow(self, surface: pygame.Surface):
        """Apply phosphor persistence effect"""
        # Simple glow simulation - would need shader for better effect
        glow = pygame.transform.smoothscale(
            surface, 
            (surface.get_width() // 4, surface.get_height() // 4)
        )
        glow = pygame.transform.smoothscale(
            glow,
            surface.get_size()
        )
        glow.set_alpha(64)
        surface.blit(glow, (0, 0), special_flags=pygame.BLEND_ADD)
        
    def apply_curvature(self, surface: pygame.Surface) -> pygame.Surface:
        """Apply CRT curvature distortion"""
        # Simplified barrel distortion - proper implementation would use shader
        # This is a placeholder for the concept
        return surface
        
    def apply_vignette(self, surface: pygame.Surface):
        """Apply vignette darkening at edges"""
        overlay = pygame.Surface(surface.get_size())
        overlay.fill((0, 0, 0))
        
        # Create radial gradient (simplified)
        center = (surface.get_width() // 2, surface.get_height() // 2)
        max_radius = max(center)
        
        for radius in range(max_radius, max_radius // 2, -5):
            alpha = int((radius / max_radius) * 255 * self.config.vignette_intensity)
            pygame.draw.circle(overlay, (0, 0, 0, alpha), center, radius)
            
        surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_SUB)
        
    def adjust_colors(self, surface: pygame.Surface):
        """Apply color adjustments"""
        # This would ideally use shaders or pixel arrays
        # Placeholder for color temperature, contrast, etc.
        pass
        
    def render_frame(self, game_content: pygame.Surface):
        """Render a complete frame with all effects"""
        # Scale game content to fit game area
        scaled_game = pygame.transform.scale(game_content, self.game_rect.size)
        
        # Apply CRT effects if enabled
        if any([self.config.scanlines, self.config.phosphor_glow, 
                self.config.crt_curvature, self.config.vignette]):
            scaled_game = self.apply_crt_effects(scaled_game)
            
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Draw bezel if loaded
        if self.bezel_surface:
            self.screen.blit(self.bezel_surface, (0, 0))
            
        # Draw game content
        self.screen.blit(scaled_game, self.game_rect)
        
        # Apply screen-wide effects
        if self.config.screen_flicker:
            flicker = np.random.uniform(
                1.0 - self.config.flicker_intensity,
                1.0 + self.config.flicker_intensity
            )
            # Would apply flicker here
            
        pygame.display.flip()
        
    def toggle_bezel(self):
        """Toggle through bezel styles"""
        styles = list(BezelStyle)
        current_index = styles.index(self.config.bezel_style)
        next_index = (current_index + 1) % len(styles)
        self.config.bezel_style = styles[next_index]
        
        if self.config.bezel_style != BezelStyle.NONE:
            self.load_bezel()
        else:
            self.bezel_surface = None