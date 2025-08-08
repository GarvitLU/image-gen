import os
import requests
import re
from pathlib import Path
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

class ThumbnailGenerator:
    def __init__(self):
        self.api_key = os.getenv('IDEOGRAM_API_KEY')
        self.output_dir = os.getenv('OUTPUT_DIR', './thumbnails')
        
        if not self.api_key:
            raise ValueError('IDEOGRAM_API_KEY is required. Please set it in your .env file.')
        
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Ensure the output directory exists"""
        try:
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            print(f"Output directory ensured: {self.output_dir}")
        except Exception as error:
            print(f"Error creating output directory: {error}")
    
    def generate_hook_text(self, topic: str) -> str:
        """Create a short 2-4 word hook from the topic; uppercase for strong impact"""
        text = topic
        # Remove common filler words
        text = re.sub(r'\b(introduction to|intro to|fundamentals|basics|beginner|complete|masterclass|course|101)\b', '', text, flags=re.IGNORECASE)
        # Collapse spaces
        text = re.sub(r'\s+', ' ', text).strip()
        if not text:
            text = topic
        # Prefer 'Master <Topic>' if topic is noun-y
        words = text.split()
        if len(words) <= 2:
            hook = f"Master {text}".strip()
        else:
            # Take top 2-3 keywords
            hook = ' '.join(words[:3])
        return hook.upper()
    
    def generate_prompt(self, topic, hook_text):
        """Create a clean thumbnail: EXACT hook text + person only (no logos/UI)"""
        return f"""Design a YouTube-style thumbnail for "{topic}" with ONLY two elements:
        1) the EXACT hook text: "{hook_text}" (render this as the ONLY text)
        2) a professional person portrait (waist-up or headshot) looking at camera

        Composition and style:
        - Text on one side, person on the other; clear separation
        - Vibrant, colorful background (solid or subtle gradient) with strong contrast
        - Big typography; subtle outline/shadow allowed for readability
        - Modern, minimal, premium look

        Strict constraints:
        - Render ONLY this text: "{hook_text}". Do not add any other words, numbers, badges, subtitles, or symbols
        - ZERO logos or branding (YouTube, TED, Microsoft, Python or any icons)
        - NO timestamps/durations (e.g., 5:29, 11:48, 2:02:21)
        - NO badges, playlists, counters (e.g., 9 videos), watermarks, corner tags
        - NO labels like "Ex-Microsoft", "Variables & Data Types", or topic outlines
        - NO UI elements: buttons, menus, share icons, play buttons, dots, progress bars, carousels, profile chips
        - NO random small or fake text anywhere

        Content rules:
        - One person (max two); business-casual attire; friendly, confident expression
        - Keep layout uncluttered; emphasize the hook text and the person only
        """
    
    def generate_thumbnail(self, topic, options=None):
        """Generate a single thumbnail for a course topic"""
        if options is None:
            options = {}
        
        try:
            print(f"Generating thumbnail for: {topic}")
            
            hook_text = self.generate_hook_text(topic)
            prompt = self.generate_prompt(topic, hook_text)
            aspect_ratio = options.get("aspect_ratio", "16x9")
            
            print('Sending request to Ideogram API...')
            
            headers = {
                "api-key": self.api_key,
                "Content-Type": "application/json"
            }
            
            data = {
                "prompt": prompt,
                "rendering_speed": "TURBO",  # Fastest rendering
                "aspect_ratio": aspect_ratio,
                "quality": "standard"  # Faster than high quality
            }
            
            response = requests.post(
                "https://api.ideogram.ai/v1/ideogram-v3/generate",
                headers=headers,
                json=data,
                timeout=30  # Reduced timeout for faster failure detection
            )
            
            if response.status_code == 200:
                data = response.json()
                if data and 'data' in data and len(data['data']) > 0:
                    image_url = data['data'][0]['url']
                    print('Thumbnail generated successfully!')
                    
                    # Download and save the image
                    file_name = self.sanitize_filename(topic)
                    file_path = Path(self.output_dir) / f"{file_name}.png"
                    
                    self.download_and_save_image(image_url, file_path)
                    
                    print(f"Thumbnail saved to: {file_path}")
                    return str(file_path)
                else:
                    raise ValueError('No image data received from API')
            else:
                print(f"API Error: {response.status_code}")
                print(f"Response: {response.text}")
                raise ValueError(f"API request failed with status {response.status_code}")
                
        except Exception as error:
            print(f'Error generating thumbnail: {error}')
            raise error
    
    def sanitize_filename(self, topic):
        """Sanitize the topic name for use as a filename"""
        # Remove special characters and replace spaces with hyphens
        sanitized = re.sub(r'[^a-zA-Z0-9\s-]', '', topic.lower())
        sanitized = re.sub(r'\s+', '-', sanitized)
        return sanitized[:50]  # Limit length
    
    def download_and_save_image(self, image_url, file_path):
        """Download and save the image from URL"""
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            print(f"Image downloaded and saved to: {file_path}")
        except Exception as error:
            print(f'Error downloading image: {error}')
            raise error
    
    def generate_multiple_thumbnails(self, topics, options=None):
        """Generate thumbnails for multiple course topics"""
        if options is None:
            options = {}
        
        results = []
        
        for topic in topics:
            try:
                file_path = self.generate_thumbnail(topic, options)
                results.append({'topic': topic, 'file_path': file_path, 'success': True})
            except Exception as error:
                print(f'Failed to generate thumbnail for "{topic}": {error}')
                results.append({'topic': topic, 'error': str(error), 'success': False})
            
            # Add a small delay between requests to be respectful to the API
            time.sleep(1)
        
        return results


def main():
    """Main function to run the thumbnail generator"""
    try:
        generator = ThumbnailGenerator()
        
        # Test with only 2 courses
        course_topics = [
            "Machine Learning Fundamentals",
            "Effective Business Communication"
        ]
        
        print('🚀 Starting thumbnail generation (testing 2 courses)...\n')
        
        # Generate thumbnails for all topics
        results = generator.generate_multiple_thumbnails(course_topics, {
            "aspect_ratio": "16x9"
        })
        
        print('\n📊 Generation Results:')
        for result in results:
            if result['success']:
                print(f"✅ {result['topic']}: {result['file_path']}")
            else:
                print(f"❌ {result['topic']}: {result['error']}")
        
    except Exception as error:
        print(f'❌ Script failed: {error}')
        exit(1)


if __name__ == "__main__":
    main() 