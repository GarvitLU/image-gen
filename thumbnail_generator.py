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
        # Remove common words and numbers
        text = re.sub(
            r'\b(introduction to|intro to|fundamentals|basics|beginner|complete|masterclass|course|101|the|a|an|and|or|but|in|on|at|to|for|of|with|by)\b',
            '',
            text,
            flags=re.IGNORECASE
        )
        # Remove any numbers at the beginning
        text = re.sub(r'^\d+\s*', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if not text:
            text = topic
        words = text.split()
        if len(words) <= 2:
            hook = f"Master {text}".strip()
        else:
            hook = ' '.join(words[:3])
        return hook.upper()
    
    def generate_prompt(self, topic, hook_text):
        """Create a clean thumbnail prompt with variety"""
        import random
        
        # Different style variations
        style_variations = [
            f"""
Design a YouTube-style thumbnail for "{topic}" with ONLY two elements:
1) the EXACT hook text: "{hook_text}"
2) a professional person portrait (waist-up or headshot)

Composition and style:
- Text on one side, person on the other; clear separation
- Background can be deep black/dark with contrast accents or vibrant gradient
- Add tasteful speaker cues: microphone or headset, natural hand gestures, subtle lighting
- Optional bold shapes behind text for contrast; minimal
- Big typography; subtle outline/shadow for readability
- Modern, premium, energetic look without clutter

Strict constraints:
- Render ONLY this text: "{hook_text}"
- Absolutely NO logos, icons, symbols, or badges of any kind
- NO timestamps, watermarks, corner tags, or UI elements
- NO small or fake text anywhere

Content rules:
- One person (max two); business-casual attire; confident expression
- Keep layout uncluttered; emphasize text and person only
- Use strong contrast to make the text pop
""",
            f"""
Create a professional course thumbnail for "{topic}" featuring:
1) the EXACT hook text: "{hook_text}"
2) a confident business professional (headshot or waist-up)

Design elements:
- Clean, modern layout with text prominently displayed
- Professional color scheme with gradients or solid backgrounds
- Subtle geometric shapes or patterns for visual interest
- Professional attire and confident body language
- High contrast for readability

Constraints:
- Render ONLY this text: "{hook_text}"
- NO logos, icons, or decorative elements
- NO watermarks or timestamps
- Clean, uncluttered design

Style: Corporate, professional, trustworthy
""",
            f"""
Design an engaging thumbnail for "{topic}" with:
1) the EXACT hook text: "{hook_text}"
2) a dynamic professional portrait

Visual style:
- Bold, modern typography with the text as the hero element
- Professional person with engaging expression and natural gestures
- Background with subtle gradients or professional patterns
- Clean composition with strong visual hierarchy
- Professional color palette with accent colors

Requirements:
- Render ONLY this text: "{hook_text}"
- NO additional text, logos, or decorative elements
- NO watermarks or timestamps
- Professional, trustworthy appearance

Focus: Clear communication of the course topic through text and professional imagery
"""
        ]
        
        return random.choice(style_variations)

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
                "negative_prompt": (
                    "logos, company logos, YouTube logo, Google logo, "
                    "Microsoft logo, Apple logo, Meta logo, LinkedIn logo, Twitter logo, "
                    "social media icons, badges, timestamps, watermarks, UI elements, overlays, fake text"
                ),
                "rendering_speed": "TURBO",
                "aspect_ratio": aspect_ratio,
                "quality": "standard"
            }
            
            response = requests.post(
                "https://api.ideogram.ai/v1/ideogram-v3/generate",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data and 'data' in data and len(data['data']) > 0:
                    image_url = data['data'][0]['url']
                    print('Thumbnail generated successfully!')
                    
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
        sanitized = re.sub(r'[^a-zA-Z0-9\s-]', '', topic.lower())
        sanitized = re.sub(r'\s+', '-', sanitized)
        return sanitized[:50]
    
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
        """Generate thumbnails for multiple course topics with variety"""
        if options is None:
            options = {}
        
        results = []
        import random
        
        # Different aspect ratios for variety
        aspect_ratios = ["16x9", "16x9", "16x9", "16x9", "16x9"]  # Mostly 16x9 but can add others
        
        for i, topic in enumerate(topics):
            try:
                # Add some variety to options
                current_options = options.copy()
                if i % 3 == 0:  # Every 3rd thumbnail gets different styling
                    current_options["aspect_ratio"] = random.choice(aspect_ratios)
                
                file_path = self.generate_thumbnail(topic, current_options)
                results.append({'topic': topic, 'file_path': file_path, 'success': True})
            except Exception as error:
                print(f'Failed to generate thumbnail for "{topic}": {error}')
                results.append({'topic': topic, 'error': str(error), 'success': False})
            
            # Random delay between 1-3 seconds to avoid rate limiting
            time.sleep(random.uniform(1, 3))
        
        return results


def main():
    """Main function to run the thumbnail generator"""
    try:
        generator = ThumbnailGenerator()
        
        course_topics = [
            "Grammar & Proofreading for Professionals",
"Inclusive Language in the Workplace",
"Problem Framing & Root Cause Analysis",
"Reverse Mentoring for Cross-Generational Learning",
"Role Clarity & Expectation Management",
"Running Effective Remote Meetings",
"Strategic Thinking for Individual Contributors",
"Writing for Executives: Briefs & Summaries"  

]
        
        print('🚀 Starting thumbnail generation...\n')
        
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