# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Building and Testing
- `cog build` - Build the Cog model container
- `cog predict` - Run a prediction locally (uses default parameters)
- `python predict.py` - Run the predictor directly for local testing

### Development
- The model runs locally without GPU requirements
- Dependencies are managed via `cog.yaml` (Pillow, numpy, cog)
- Output images are saved to `/tmp/color_field_painting.png`

## Architecture

This is a Cog-based procedural art generation model that creates abstract expressionist paintings with vertical "zip" lines over color fields.

### Core Components
- **Predictor class** (`predict.py`): Main Cog predictor implementing `cog.BasePredictor`
- **Color palette system**: Themed color generation (classic, warm, cool, monochrome, complementary, random)
- **Zip positioning algorithm**: Asymmetric vs symmetric placement of vertical bands
- **Edge rendering**: Hard edges (classic) vs soft edges with gradient blending

### Key Technical Details
- Uses PIL/Pillow for image generation and manipulation
- Procedural generation with numpy for soft edge calculations
- No ML model - purely algorithmic art generation
- Color intensity adjustment and hex color parsing
- Zip width ranges and positioning constraints to avoid visual conflicts

### Input Parameters
The model accepts 11 parameters including dimensions, colors, zip configuration, and aesthetic options. The `seed` parameter enables reproducible generation.

### Color Field Painting Logic
1. Generate base color field background
2. Calculate zip line positions (respecting asymmetric constraints)
3. Render vertical zip bands with specified width and edge properties
4. Apply color intensity and palette theme adjustments