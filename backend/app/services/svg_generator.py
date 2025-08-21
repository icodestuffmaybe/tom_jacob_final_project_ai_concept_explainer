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
        # TODO: EXERCISE 1C - Implement SVG Flashcard Generation (Prompt Engineering Session)
        # INSTRUCTION: Create an AI prompt that generates educational SVG flashcards
        # 
        # STEPS TO IMPLEMENT:
        # 1. Handle the case when self.model is None (return fallback SVG)
        # 2. Extract core essence from the explanation using extract_core_essence()
        # 3. Create a comprehensive prompt for SVG generation using Session 1 techniques:
        #    - Persona prompting (assign AI role as designer)
        #    - Detailed format specification (SVG structure)
        #    - Clear visual design requirements
        #    - Specific output format (pure SVG code)
        # 4. Generate content and clean the response
        # 5. Return valid SVG content
        # 
        # PROMPT ENGINEERING TECHNIQUES (Session 1):
        # - Persona: "You are a minimalist designer..."
        # - Clear format specification: SVG dimensions, structure
        # - Detailed requirements: colors, layout, typography
        # - Output format: "Generate ONLY valid SVG code"
        # 
        # SVG REQUIREMENTS:
        # - Size: 800x600 pixels
        # - Dark theme: background #1a1a1a, text #f0f0f0
        # - Structure: Title, core content, visual element
        # - Educational and visually appealing
        # 
        # DESIGN PRINCIPLES:
        # - Minimalist and zen-inspired
        # - Clear typography (14px+ body, 24px+ title)
        # - Balanced layout with negative space
        # - Simple but meaningful visual elements
        
        # TODO: Remove this assertion once you implement the function
        assert False, "❌ EXERCISE 1C NOT IMPLEMENTED: Please implement generate_svg_flashcard() function in svg_generator.py"
        
        # TODO: Implement your solution here
        
        if not self.model:
            return self.get_fallback_svg(topic)
            
        # TODO: Extract core essence from explanation
        core_essence = await self.extract_core_essence(topic, explanation)
        
        # TODO: Create your SVG generation prompt using Session 1 techniques
        prompt = f"""
        # Your SVG generation prompt goes here
        # Remember to:
        # - Use persona prompting (designer role)
        # - Specify exact SVG format and dimensions
        # - Include design requirements (colors, layout)
        # - Request only SVG code as output
        # - Include the topic: {topic}
        # - Include the core_essence: {core_essence}
        """
        
        try:
            # TODO: Generate content using self.model.generate_content(prompt)
            # TODO: Clean the response using self.clean_svg_response()
            # TODO: Return the SVG content
            pass
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