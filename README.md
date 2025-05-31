![Sample Output](./@sample.png)

# Zip Line Color Field Generator

A Cog model that generates abstract expressionist paintings featuring prominent vertical "zip" lines over large color fields. This model specializes in creating hard-edge compositions where bold vertical bands divide and define color spaces, exploring the dynamic tension between division and unity.

## Features

- **Prominent Zip Lines**: Creates bold vertical bands that serve as both divisions and connections between color areas
- **Color Field Foundation**: Large, flat color areas provide the foundation for zip line compositions
- **Multiple Zip Configurations**: Generate 0-5 vertical zips with customizable widths and placement
- **Asymmetric Zip Placement**: Option for tension-creating asymmetric zip positioning
- **Hard vs Soft Zip Edges**: Choose between crisp hard edges or subtle soft transitions
- **Reproducible Results**: Seed control for consistent generation

## Model Inputs

- `width` (int, default: 1024): Width of the generated image
- `height` (int, default: 768): Height of the generated image  
- `primary_color` (str, default: "random"): Background color (hex code or "random")
- `zip_color` (str, default: "random"): Color for vertical zip lines (hex code or "random")
- `num_zips` (int, 0-5, default: 2): Number of vertical zip lines
- `zip_width_range` (str, default: "5-20"): Range for zip widths in pixels (format: "min-max")
- `color_intensity` (float, 0.1-1.0, default: 0.8): Color saturation intensity
- `asymmetric` (bool, default: true): Whether to place zips asymmetrically
- `edge_softness` (int, 0-5, default: 0): Edge softness (0 = hard edges)
- `color_palette` (str, default: "classic"): Color theme
- `seed` (int, optional): Random seed for reproducible results

## Color Palettes

- **classic**: Traditional abstract expressionist colors (deep reds, blues, whites)
- **warm**: Warm color schemes (reds, oranges, yellows)
- **cool**: Cool color schemes (blues, greens, purples)
- **monochrome**: Grayscale variations
- **complementary**: High contrast complementary colors
- **random**: Completely random color generation

## About Zip Lines in Abstract Expressionism

The "zip" is a vertical band of color that cuts through a color field, creating spatial relationships and emotional tension. These bold vertical elements serve multiple purposes: they can divide the canvas into distinct areas, create a sense of scale and proportion, or act as pathways for the eye to travel across the composition. The zip technique became particularly prominent in mid-20th century abstract expressionism, where artists used these vertical interventions to explore themes of transcendence, division, and unity through pure color and geometric form.

## Usage

```python
# Basic usage
predictor.predict(
    width=1024,
    height=768,
    primary_color="#8B0000",  # Dark red
    zip_color="#FFFFFF",      # White
    num_zips=1,
    asymmetric=True,
    color_palette="classic"
)

# Random generation
predictor.predict(
    primary_color="random",
    zip_color="random",
    num_zips=2,
    color_palette="random",
    seed=42  # For reproducible results
)
```

## Technical Details

The model uses procedural generation techniques to create images that emphasize the power of zip lines in color field composition:

1. **Color Field Foundation**: Large flat areas of color provide the base canvas
2. **Zip Line Generation**: Vertical bands are strategically positioned to create visual impact
3. **Color Relationships**: Palettes designed to maximize the contrast and harmony between field and zip
4. **Edge Definition**: Sharp zip edges maintain the bold, geometric precision that defines the style

## Installation

1. Install [Cog](https://github.com/replicate/cog)
2. Clone this repository
3. Run `cog predict` or build with `cog build`

## Example Outputs

The model generates images that showcase the dramatic impact of zip lines cutting through color fields, suitable for:
- Digital art collections
- Abstract backgrounds
- Color study references
- Meditation and mindfulness applications
- Educational purposes studying abstract expressionism

## License

This model generates original artworks inspired by zip line color field painting techniques, emphasizing the dramatic visual impact of vertical bands cutting through color spaces.