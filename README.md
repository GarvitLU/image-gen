# Thumbnail Generator (Python Version)

A Python script that generates professional course thumbnails using the Ideogram API. The script creates context-aware, educational thumbnails based on course topics.

## Features

- 🎨 **Context-aware prompts**: Generates thumbnails specifically designed for educational content
- 📁 **Automatic file management**: Creates organized output directories and sanitizes filenames
- 🔄 **Batch processing**: Generate multiple thumbnails at once
- 🎯 **Professional design**: Optimized for YouTube and online learning platforms
- ⚡ **Medium quality**: Uses medium quality setting for faster generation (as per user preference)

## Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Get your Ideogram API key**:
   - Sign up at [Ideogram](https://ideogram.ai/)
   - Get your API key from the dashboard
   - Copy the API key

3. **Configure environment variables**:
   Create a `.env` file and add your API key:
   ```
   IDEOGRAM_API_KEY=your_actual_api_key_here
   OUTPUT_DIR=./thumbnails
   ```

## Usage

### Basic Usage

Run the main script to generate thumbnails for the example course topics:

```bash
python thumbnail_generator.py
```

### Generate from File

Use the file-based generator to read course names from a text file:

```bash
python generate_from_file.py
```

This will read course names from `course-test.txt` (one per line).

### Custom Usage

You can also import and use the `ThumbnailGenerator` class in your own scripts:

```python
from thumbnail_generator import ThumbnailGenerator

generator = ThumbnailGenerator()

# Generate a single thumbnail
file_path = await generator.generate_thumbnail("Machine Learning Basics", {
    "aspect_ratio": "16:9",
    "style": "cinematic"
})

# Generate multiple thumbnails
topics = [
    "Web Development",
    "Mobile App Development", 
    "Database Design"
]

results = generator.generate_multiple_thumbnails(topics, {
    "aspect_ratio": "16:9",
    "style": "cinematic"
})
```

## Configuration Options

### Thumbnail Options

- `aspect_ratio`: Image aspect ratio (default: "16:9")
- `style`: Generation style (default: "cinematic")
- `quality`: Image quality (default: "medium")

### Environment Variables

- `IDEOGRAM_API_KEY`: Your Ideogram API key (required)
- `OUTPUT_DIR`: Directory to save generated thumbnails (default: "./thumbnails")

## Output

Generated thumbnails are saved in the `thumbnails/` directory (or your custom `OUTPUT_DIR`) with sanitized filenames based on the course topic.

Example output structure:
```
thumbnails/
├── javascript-fundamentals.png
├── react-development.png
├── python-for-beginners.png
└── data-science-essentials.png
```

## API Reference

### ThumbnailGenerator Class

#### Constructor
```python
ThumbnailGenerator()
```

#### Methods

##### `generate_thumbnail(topic, options=None)`
Generates a single thumbnail for a course topic.

**Parameters:**
- `topic` (str): The course topic/title
- `options` (dict, optional): Generation options

**Returns:** str - Path to the generated image

##### `generate_multiple_thumbnails(topics, options=None)`
Generates thumbnails for multiple course topics.

**Parameters:**
- `topics` (list): List of course topics
- `options` (dict, optional): Generation options

**Returns:** list - List of results with success/error status

## Error Handling

The script includes comprehensive error handling:
- API key validation
- Network error handling
- File system error handling
- Graceful failure for individual thumbnails in batch operations

## Tips for Best Results

1. **Be specific with topics**: Use descriptive course titles
2. **Consider your audience**: The prompts are optimized for educational content
3. **Test different styles**: Try different style options for variety
4. **Monitor API usage**: Be mindful of your Ideogram API limits

## Troubleshooting

### Common Issues

1. **"IDEOGRAM_API_KEY is required"**
   - Make sure you've created a `.env` file with your API key

2. **"No image data received from API"**
   - Check your API key is valid
   - Verify your Ideogram account has sufficient credits

3. **Network errors**
   - Check your internet connection
   - Verify the Ideogram API is accessible

4. **ModuleNotFoundError**
   - Run `pip install -r requirements.txt` to install dependencies

## License

MIT License - feel free to use and modify as needed. 