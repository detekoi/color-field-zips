import os
import random
from typing import List, Optional
import numpy as np
from PIL import Image, ImageDraw
from cog import BasePredictor, Input, Path


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # No model loading needed for procedural generation
        pass

    def predict(
        self,
        width: int = Input(default=1024, description="Width of the generated image"),
        height: int = Input(default=768, description="Height of the generated image"),
        primary_color: str = Input(
            default="random",
            description="Primary background color (hex code like #FF0000 or 'random')"
        ),
        zip_color: str = Input(
            default="random",
            description="Color for the vertical zip lines (hex code like #FFFFFF or 'random')"
        ),
        num_zips: int = Input(
            default=2,
            ge=0,
            le=5,
            description="Number of vertical zip lines (0-5)"
        ),
        zip_width_range: str = Input(
            default="5-20",
            description="Range for zip line widths in pixels (format: 'min-max')"
        ),
        color_intensity: float = Input(
            default=0.8,
            ge=0.1,
            le=1.0,
            description="Color saturation intensity (0.1-1.0)"
        ),
        asymmetric: bool = Input(
            default=True,
            description="Whether to place zips asymmetrically (more abstract expressionist style)"
        ),
        edge_softness: int = Input(
            default=0,
            ge=0,
            le=5,
            description="Softness of zip edges (0 = hard edges, 5 = soft)"
        ),
        color_palette: str = Input(
            default="classic",
            choices=["classic", "warm", "cool", "monochrome", "complementary", "random"],
            description="Color palette theme"
        ),
        seed: int = Input(default=None, description="Random seed for reproducible results"),
    ) -> Path:
        """Generate an abstract expressionist color field painting"""
        
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        # Parse zip width range
        try:
            min_width, max_width = map(int, zip_width_range.split('-'))
        except ValueError:
            min_width, max_width = 5, 20
        
        # Generate the image
        image = self._generate_painting(
            width, height, primary_color, zip_color, num_zips,
            min_width, max_width, color_intensity, asymmetric,
            edge_softness, color_palette
        )
        
        # Save the image
        output_path = "/tmp/color_field_painting.png"
        image.save(output_path, "PNG")
        
        return Path(output_path)
    
    def _generate_painting(
        self, width: int, height: int, primary_color: str, zip_color: str,
        num_zips: int, min_width: int, max_width: int, color_intensity: float,
        asymmetric: bool, edge_softness: int, color_palette: str
    ) -> Image.Image:
        """Generate the actual color field painting"""
        
        # Create base image
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        
        # Get color palette
        bg_color, zip_colors = self._get_color_palette(
            primary_color, zip_color, color_palette, color_intensity, num_zips
        )
        
        # Fill background
        draw.rectangle([0, 0, width, height], fill=bg_color)
        
        # Generate zip positions
        zip_positions = self._generate_zip_positions(width, num_zips, asymmetric)
        
        # Draw zips
        for i, x_pos in enumerate(zip_positions):
            zip_width = random.randint(min_width, max_width)
            zip_col = zip_colors[i % len(zip_colors)]
            
            # Calculate zip boundaries
            left = max(0, x_pos - zip_width // 2)
            right = min(width, x_pos + zip_width // 2)
            
            if edge_softness == 0:
                # Hard edges (classic style)
                draw.rectangle([left, 0, right, height], fill=zip_col)
            else:
                # Soft edges
                self._draw_soft_zip(image, left, right, height, zip_col, edge_softness)
        
        return image
    
    def _get_color_palette(
        self, primary_color: str, zip_color: str, palette_theme: str,
        intensity: float, num_zips: int
    ) -> tuple:
        """Generate color palette based on theme"""
        
        def adjust_intensity(color_tuple):
            """Adjust color intensity"""
            return tuple(int(c * intensity) for c in color_tuple)
        
        def hex_to_rgb(hex_color):
            """Convert hex to RGB"""
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Define palette themes
        palettes = {
            "classic": {
                "backgrounds": [(139, 0, 0), (0, 0, 139), (139, 69, 19), (25, 25, 112)],
                "zips": [(255, 255, 255), (255, 255, 0), (255, 140, 0), (220, 220, 220)]
            },
            "warm": {
                "backgrounds": [(178, 34, 34), (255, 69, 0), (205, 92, 92), (139, 69, 19)],
                "zips": [(255, 255, 255), (255, 215, 0), (255, 160, 122), (240, 230, 140)]
            },
            "cool": {
                "backgrounds": [(25, 25, 112), (0, 100, 0), (70, 130, 180), (72, 61, 139)],
                "zips": [(255, 255, 255), (173, 216, 230), (144, 238, 144), (221, 160, 221)]
            },
            "monochrome": {
                "backgrounds": [(50, 50, 50), (80, 80, 80), (35, 35, 35), (100, 100, 100)],
                "zips": [(255, 255, 255), (200, 200, 200), (150, 150, 150), (220, 220, 220)]
            },
            "complementary": {
                "backgrounds": [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)],
                "zips": [(0, 255, 255), (255, 0, 255), (255, 255, 0), (128, 0, 128)]
            }
        }
        
        # Handle custom colors
        if primary_color != "random":
            try:
                bg_color = adjust_intensity(hex_to_rgb(primary_color))
            except:
                bg_color = adjust_intensity((139, 0, 0))  # fallback
        else:
            if palette_theme == "random":
                # Random palette
                bg_color = adjust_intensity(tuple(random.randint(0, 255) for _ in range(3)))
            else:
                bg_color = adjust_intensity(random.choice(palettes[palette_theme]["backgrounds"]))
        
        # Generate zip colors
        zip_colors = []
        for i in range(max(1, num_zips)):
            if zip_color != "random":
                try:
                    zip_colors.append(adjust_intensity(hex_to_rgb(zip_color)))
                except:
                    zip_colors.append(adjust_intensity((255, 255, 255)))  # fallback
            else:
                if palette_theme == "random":
                    zip_colors.append(adjust_intensity(tuple(random.randint(0, 255) for _ in range(3))))
                else:
                    zip_colors.append(adjust_intensity(random.choice(palettes[palette_theme]["zips"])))
        
        return bg_color, zip_colors
    
    def _generate_zip_positions(self, width: int, num_zips: int, asymmetric: bool) -> List[int]:
        """Generate positions for vertical zip lines"""
        if num_zips == 0:
            return []
        
        positions = []
        
        if asymmetric:
            # Asymmetric placement
            # Avoid center and edges, create tension
            forbidden_zones = [
                (0, width * 0.1),  # left edge
                (width * 0.45, width * 0.55),  # center
                (width * 0.9, width)  # right edge
            ]
            
            attempts = 0
            while len(positions) < num_zips and attempts < 100:
                x = random.randint(int(width * 0.15), int(width * 0.85))
                
                # Check if position is in forbidden zone
                valid = True
                for start, end in forbidden_zones:
                    if start <= x <= end:
                        valid = False
                        break
                
                # Check minimum distance from other zips
                if valid:
                    for existing_x in positions:
                        if abs(x - existing_x) < width * 0.1:
                            valid = False
                            break
                
                if valid:
                    positions.append(x)
                
                attempts += 1
        else:
            # Symmetric placement
            if num_zips == 1:
                positions = [width // 2]
            else:
                margin = width * 0.2
                available_width = width - 2 * margin
                spacing = available_width / (num_zips - 1) if num_zips > 1 else 0
                
                for i in range(num_zips):
                    x = int(margin + i * spacing)
                    positions.append(x)
        
        return positions
    
    def _draw_soft_zip(self, image: Image.Image, left: int, right: int, 
                      height: int, color: tuple, softness: int) -> None:
        """Draw a zip with soft edges"""
        img_array = np.array(image)
        
        # Create gradient mask
        zip_width = right - left
        for x in range(left, right):
            # Calculate distance from edge
            dist_from_left = x - left
            dist_from_right = right - x
            edge_dist = min(dist_from_left, dist_from_right)
            
            # Calculate alpha based on distance and softness
            if edge_dist < softness:
                alpha = edge_dist / softness
            else:
                alpha = 1.0
            
            # Blend colors
            for y in range(height):
                original = img_array[y, x]
                blended = [
                    int(original[i] * (1 - alpha) + color[i] * alpha)
                    for i in range(3)
                ]
                img_array[y, x] = blended
        
        # Convert back to PIL image
        blended_image = Image.fromarray(img_array)
        image.paste(blended_image)


# Example usage for testing locally
if __name__ == "__main__":
    predictor = Predictor()
    predictor.setup()
    
    # Test generation
    result = predictor.predict(
        width=1024,
        height=768,
        primary_color="random",
        zip_color="random",
        num_zips=2,
        zip_width_range="10-25",
        color_intensity=0.8,
        asymmetric=True,
        edge_softness=0,
        color_palette="classic",
        seed=42
    )
    print(f"Generated image saved to: {result}")