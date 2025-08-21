import google.generativeai as genai
from app.core.config import settings

class SVGGenerator:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-pro')  # Using Pro version
        else:
            self.model = None
        
    async def generate_svg_flashcard(self, topic: str, explanation: str) -> str:
        if not self.model:
            return self.get_fallback_svg(topic)
            
        core_essence = await self.extract_core_essence(topic, explanation)
        
        prompt = f"""
        Create a Minimalist Educational SVG Flashcard
        You are a minimalist designer who specializes in explaining complex concepts simply using the Feynman technique. 
        Create an SVG flashcard (800x600 pixels) that teaches the following concept:

        TOPIC: {topic}

        CORE EXPLANATION: {core_essence}

        Content Structure:
        - Concept Title - Center at the top
        - Core Essence - A brief, deep analysis of what the concept really means
        - Simple Explanation - Break it down like you're explaining to a beginner, using everyday language
        - Real-World Example - A concrete, relatable analogy or example
        - Visual Element - A simple, zen-inspired graphic that represents the concept

        Design Style:
        - Aesthetic: Futuristic matrix style combined with zen minimalism
        - Color Scheme: Dark background (#1a1a1a) with chalk white text (#f0f0f0) for contrast
        - Layout: Clean grid-based design using golden ratio proportions
        - Typography: Minimum 14px font size for body text, 24px for title
        - Spacing: Generous use of negative space for "breathability"
        - Visual Inspiration: Song dynasty painting mood - simple, elegant, meaningful

        Layout Requirements:
        - Canvas: 800x600 pixels with 20px margins
        - Title centered at top (y=50)
        - Core essence in upper section (y=120-180)
        - Central zen graphic (y=200-400) - simple, symbolic illustration
        - Simple explanation at bottom (y=420-520)
        - Balance all elements harmoniously

        IMPORTANT: Generate ONLY valid SVG code starting with <svg> and ending with </svg>.
        No markdown, no explanations, just the SVG code.
        """
        
        try:
            response = self.model.generate_content(prompt)
            svg_content = self.clean_svg_response(response.text)
            return svg_content
        except Exception as e:
            print(f"Error generating SVG: {e}")
            return self.get_fallback_svg(topic)
    
    async def extract_core_essence(self, topic: str, explanation: str) -> str:
        if not self.model:
            return f"Core concept about {topic}"
            
        prompt = f"""
        From this explanation about "{topic}":
        {explanation[:500]}
        
        Extract:
        1. The single most important concept (one sentence)
        2. A simple analogy or real-world example
        3. Why this matters in everyday life
        
        Keep each point to one sentence maximum.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error extracting core essence: {e}")
            return f"Core concept about {topic}"
    
    def clean_svg_response(self, response: str) -> str:
        response = response.replace('```svg', '').replace('```', '')
        
        svg_start = response.find('<svg')
        svg_end = response.find('</svg>') + 6
        
        if svg_start != -1 and svg_end > svg_start:
            return response[svg_start:svg_end]
        
        return self.get_fallback_svg("Concept")
    
    def get_fallback_svg(self, topic: str = "Concept") -> str:
        return f'''<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="600" fill="#1a1a1a"/>
    <text x="400" y="50" font-size="24" fill="#f0f0f0" text-anchor="middle" font-family="Arial, sans-serif">
        {topic}
    </text>
    <circle cx="400" cy="250" r="50" fill="none" stroke="#f0f0f0" stroke-width="2"/>
    <text x="400" y="350" font-size="16" fill="#f0f0f0" text-anchor="middle" font-family="Arial, sans-serif">
        Learning in progress...
    </text>
    <text x="400" y="450" font-size="14" fill="#f0f0f0" text-anchor="middle" font-family="Arial, sans-serif">
        Visual representation will be generated
    </text>
    <text x="400" y="480" font-size="14" fill="#f0f0f0" text-anchor="middle" font-family="Arial, sans-serif">
        once Gemini API is configured
    </text>
</svg>'''