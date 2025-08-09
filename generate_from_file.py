from thumbnail_generator import ThumbnailGenerator
from pathlib import Path
import re

def generate_from_file():
    """Generate thumbnails from course names in a text file"""
    try:
        print('📚 Course Thumbnail Generator from File\n')
        
        generator = ThumbnailGenerator()
        
        # Read course names from the text file
        courses_file = 'course.txt'
        
        if not Path(courses_file).exists():
            print(f"❌ File '{courses_file}' not found!")
            print(f"📝 Please create '{courses_file}' with your course names (one per line)")
            return
        
        with open(courses_file, 'r', encoding='utf-8') as file:
            file_content = file.read()
        
        course_topics = []
        for line in file_content.split('\n'):
            if line.strip():
                # Remove numbers at the beginning of each line
                cleaned_line = re.sub(r'^\d+\s*', '', line.strip())
                course_topics.append(cleaned_line)
        
        if not course_topics:
            print(f"❌ No course names found in '{courses_file}'")
            print('📝 Please add your course names to the file (one per line)')
            return
        
        print(f"📖 Found {len(course_topics)} courses in '{courses_file}':")
        for index, topic in enumerate(course_topics, 1):
            print(f"{index}. {topic}")
        
        print('\n🚀 Starting thumbnail generation...\n')
        
        # Generate thumbnails with professional styling
        results = generator.generate_multiple_thumbnails(course_topics, {
            "aspect_ratio": "16x9"
        })
        
        print('\n📊 Results Summary:')
        success_count = 0
        failure_count = 0
        
        for index, result in enumerate(results, 1):
            if result['success']:
                success_count += 1
                print(f"✅ {index}. {result['topic']}")
                print(f"   📁 Saved to: {result['file_path']}")
            else:
                failure_count += 1
                print(f"❌ {index}. {result['topic']}")
                print(f"   💥 Error: {result['error']}")
            print('')  # Empty line for readability
        
        print(f"\n🎯 Summary: {success_count} successful, {failure_count} failed")
        
        if success_count > 0:
            print('\n📂 Check the "thumbnails" folder for your generated images!')
            print('🎨 Thumbnails are styled to match professional course management systems')
        
    except Exception as error:
        print(f'❌ Script failed: {error}')
        exit(1)


if __name__ == "__main__":
    generate_from_file() 