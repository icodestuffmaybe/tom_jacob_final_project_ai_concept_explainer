import google.generativeai as genai
from typing import List, Dict, Optional
import asyncio
import httpx
from app.core.config import settings

try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
    print("✅ DuckDuckGo search available")
except ImportError:
    DDGS_AVAILABLE = False
    print("⚠️ DuckDuckGo search not available")

class ExplanationService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-pro')  # Using Pro version
        else:
            self.model = None
        
    async def explain_concept(self, query: str) -> Dict:
        print(f"🔍 Processing query: {query}")
        
        print("📝 Extracting keywords...")
        keywords = await self.extract_keywords(query)
        print(f"   Keywords: {keywords}")
        
        print("🌐 Searching for sources...")
        sources = await self.search_sources(keywords)
        print(f"   Found {len(sources)} sources")
        
        if sources:
            print("📖 Summarizing sources...")
            source_summary = await self.summarize_sources(sources)
            print("🧠 Generating explanation with sources...")
            explanation = await self.generate_explanation_with_sources(
                query, source_summary, sources
            )
        else:
            print("🧠 Generating explanation without sources...")
            explanation = await self.generate_explanation_without_sources(query)
            sources = []
        
        print("✅ Explanation complete!")
        return {
            "explanation": explanation,
            "sources": sources,
            "keywords": keywords
        }
    
    async def extract_keywords(self, query: str) -> List[str]:
        # TODO: EXERCISE 2A - Implement Keyword Extraction (RAG Session)
        # INSTRUCTION: This function should extract 3-5 Wikipedia-searchable keywords from educational queries
        # 
        # STEPS TO IMPLEMENT:
        # 1. Handle the case when self.model is None (no API key) - provide intelligent fallback
        # 2. Create a prompt that asks the AI to extract Wikipedia-searchable keywords
        # 3. Include examples in your prompt (few-shot prompting from Session 1)
        # 4. Parse the AI response to extract keywords as a list
        # 5. Always include the original query as the first keyword
        # 6. Return max 5 keywords
        # 
        # PROMPT ENGINEERING TIPS (from Session 1):
        # - Use clear instructions
        # - Provide 2-3 examples
        # - Specify the exact output format you want
        # - Include the reasoning (why these keywords are good)
        # 
        # EXAMPLE PROMPT STRUCTURE:
        # """
        # Extract educational keywords from this query: "{query}"
        # 
        # Requirements:
        # - Return 3-5 keywords that would have Wikipedia articles
        # - Include main topic and related educational terms
        # - Use simple, common terms
        # 
        # Examples:
        # "What is photosynthesis?" → "photosynthesis, plants, biology, chlorophyll"
        # "Explain gravity" → "gravity, physics, Newton, force, mass"
        # 
        # Query: "{query}"
        # Keywords:
        # """
        
        # TODO: Remove this assertion once you implement the function
        assert False, "❌ EXERCISE 2A NOT IMPLEMENTED: Please implement extract_keywords() function in explanation_service.py"
        
        # TODO: Implement your solution here
        # Hint: Check if self.model exists, create appropriate prompt, handle response
        
        # FALLBACK IMPLEMENTATION (for when no API key):
        if not self.model:
            # TODO: Improve this fallback to be more intelligent
            # Consider: synonyms, educational terms, subject classification
            words = query.split()
            return [query] + words[:2]  # Include full query + first 2 words
            
        # TODO: Create your prompt here using Session 1 techniques
        prompt = f"""
        # Your prompt implementation goes here
        """
        
        try:
            # TODO: Generate content using self.model.generate_content()
            # TODO: Parse the response to extract keywords
            # TODO: Ensure original query is included
            # TODO: Return max 5 keywords
            pass
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            # Better fallback
            words = query.split()
            return [query] + words[:2]
    
    async def search_sources(self, keywords: List[str]) -> List[Dict]:
        sources = []
        
        # Try keywords in order until we find something
        for keyword in keywords[:3]:  # Try first 3 keywords
            print(f"   🔍 Searching for: '{keyword.strip()}'")
            
            # Try Wikipedia first
            wiki_results = await self.search_wikipedia(keyword.strip())
            if wiki_results:
                sources.extend(wiki_results[:1])
                print(f"   ✅ Found Wikipedia source for: '{keyword.strip()}'")
                break
            else:
                print(f"   ❌ No Wikipedia results for: '{keyword.strip()}'")
            
            # If Wikipedia fails, try DuckDuckGo
            if DDGS_AVAILABLE:
                ddg_results = await self.search_duckduckgo(keyword.strip())
                if ddg_results:
                    sources.extend(ddg_results[:1])
                    print(f"   ✅ Found DuckDuckGo source for: '{keyword.strip()}'")
                    break
                else:
                    print(f"   ❌ No DuckDuckGo results for: '{keyword.strip()}'")
        
        return sources[:2]  # Return max 2 sources (1 Wikipedia + 1 DuckDuckGo)
    
    async def search_wikipedia(self, keyword: str) -> List[Dict]:
        # TODO: EXERCISE 2B - Implement Wikipedia Search & Retrieval (RAG Session)
        # INSTRUCTION: Implement Wikipedia API integration for educational content retrieval
        # 
        # STEPS TO IMPLEMENT:
        # 1. Set up async HTTP client with proper timeout (5-10 seconds)
        # 2. Try direct page lookup first using Wikipedia REST API:
        #    URL: https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_keyword}
        # 3. Handle URL encoding for special characters using urllib.parse.quote()
        # 4. If direct lookup fails, try search API:
        #    URL: https://en.wikipedia.org/w/api.php with search parameters
        # 5. Extract relevant data: title, URL, snippet (limit to ~300 chars)
        # 6. Return structured format: List[Dict] with keys: title, url, snippet, source_type
        # 7. Handle errors gracefully - return empty list [] for failures
        # 
        # RAG TECHNIQUES (Session 2):
        # - API integration: Multiple endpoints for robust retrieval
        # - Content extraction: Get clean, relevant summaries
        # - Error handling: Graceful fallbacks for missing content
        # - Data processing: Structure data for AI consumption
        # 
        # EXAMPLE API USAGE:
        # Direct page: GET https://en.wikipedia.org/api/rest_v1/page/summary/Photosynthesis
        # Search: GET https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch=quantum%20physics&srlimit=1
        # 
        # EXPECTED RETURN FORMAT:
        # [
        #     {
        #         'title': 'Page Title',
        #         'url': 'https://en.wikipedia.org/wiki/Page_Title',
        #         'snippet': 'Article summary...',
        #         'source_type': 'wikipedia'
        #     }
        # ]
        
        # TODO: Remove this assertion once you implement the function
        assert False, "❌ EXERCISE 2B NOT IMPLEMENTED: Please implement search_wikipedia() function in explanation_service.py"
        
        # TODO: Implement your Wikipedia search solution here
        # Hint: Use httpx.AsyncClient, handle both direct page and search APIs
        
        # FALLBACK (for reference, but implement your own):
        print(f"   ⚠️ Wikipedia search not implemented yet for: {keyword}")
        return []
    
    async def search_duckduckgo(self, keyword: str) -> List[Dict]:
        """Search DuckDuckGo for educational content when Wikipedia fails"""
        if not DDGS_AVAILABLE:
            return []
            
        try:
            print(f"   🦆 Searching DuckDuckGo for: {keyword}")
            
            # Create educational search query
            educational_query = f"{keyword} educational explanation learning"
            
            # Use asyncio to run the synchronous DDGS search
            import asyncio
            
            def run_ddg_search():
                with DDGS() as ddgs:
                    # Search for educational content with filters
                    results = list(ddgs.text(
                        educational_query,
                        max_results=3,
                        region='us-en',
                        safesearch='moderate'
                    ))
                    return results
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            search_results = await loop.run_in_executor(None, run_ddg_search)
            
            if search_results:
                # Filter for educational domains
                educational_sources = []
                educational_domains = [
                    '.edu', '.org', 'khanacademy', 'coursera', 'edx',
                    'britannica', 'nationalgeographic', 'smithsonian',
                    'mit.edu', 'stanford.edu', 'harvard.edu', 'wikipedia',
                    'sciencedirect', 'nature.com', 'ieee.org'
                ]
                
                for result in search_results[:5]:  # Check first 5 results
                    url = result.get('href', '').lower()
                    title = result.get('title', '')
                    body = result.get('body', '')
                    
                    # Prioritize educational domains
                    is_educational = any(domain in url for domain in educational_domains)
                    
                    if is_educational or 'education' in body.lower() or 'learn' in body.lower():
                        educational_sources.append({
                            'title': title,
                            'url': result.get('href', ''),
                            'snippet': body[:300],
                            'source_type': 'duckduckgo_educational'
                        })
                        print(f"   ✅ DuckDuckGo found educational source: {title}")
                        break  # Take first good educational source
                
                return educational_sources[:1]  # Return max 1 source
            else:
                print(f"   ❌ DuckDuckGo: No results for {keyword}")
                
        except Exception as e:
            print(f"   ❌ DuckDuckGo search error for '{keyword}': {e}")
        
        return []
    
    async def summarize_sources(self, sources: List[Dict]) -> str:
        # TODO: EXERCISE 2C - Implement Source Integration & Summarization (RAG Session)
        # INSTRUCTION: Create multi-source content synthesis for AI prompts
        # 
        # STEPS TO IMPLEMENT:
        # 1. Handle the case when self.model is None (return empty string or fallback)
        # 2. Process the sources list to extract key information
        # 3. Create a prompt for AI summarization using techniques from Session 1:
        #    - Clear instructions for synthesis (not just copying)
        #    - Focus on educational concepts and key facts
        #    - Request coherent, well-structured summary
        # 4. Combine source texts intelligently (don't just concatenate)
        # 5. Generate summary using self.model.generate_content()
        # 6. Handle errors gracefully
        # 
        # RAG TECHNIQUES (Session 2):
        # - Information synthesis: Combine multiple sources effectively
        # - Content summarization: Extract key educational concepts
        # - Context preparation: Format for AI prompt consumption
        # - Quality filtering: Focus on educational relevance
        # 
        # SOURCE DATA STRUCTURE:
        # sources = [
        #     {
        #         'title': 'Source Title',
        #         'snippet': 'Content excerpt...',
        #         'source_type': 'wikipedia'
        #     }, ...
        # ]
        # 
        # PROMPT TECHNIQUES:
        # - Ask for synthesis, not copying
        # - Focus on educational value
        # - Request key facts and concepts
        # - Maintain factual accuracy
        # 
        # EXPECTED OUTPUT:
        # - Coherent summary combining all sources
        # - Key educational concepts preserved
        # - Reduced redundancy
        # - Suitable for AI explanation generation
        
        # TODO: Remove this assertion once you implement the function
        assert False, "❌ EXERCISE 2C NOT IMPLEMENTED: Please implement summarize_sources() function in explanation_service.py"
        
        # TODO: Implement your source summarization solution here
        # Hint: Handle empty sources, create educational synthesis prompt, use self.model
        
        # FALLBACK (for reference):
        if not self.model:
            return ""
        
        # TODO: Your implementation goes here
        return ""
    
    async def generate_explanation_with_sources(self, query: str, source_summary: str, sources: List[Dict]) -> str:
        # TODO: EXERCISE 1A - Implement Explanation Generation (Prompt Engineering Session)
        # INSTRUCTION: Create an AI prompt that generates educational explanations using the Feynman Technique
        # 
        # STEPS TO IMPLEMENT:
        # 1. Handle the case when self.model is None (no API key)
        # 2. Create a comprehensive prompt using techniques from Session 1:
        #    - Persona prompting (assign AI a role as educational expert)
        #    - Clear instructions following Feynman Technique
        #    - Format specification for consistent output
        #    - Integration of source material with citations
        # 3. Include the source_summary in your prompt for RAG functionality
        # 4. Generate content using self.model.generate_content()
        # 5. Return the AI's response
        # 
        # FEYNMAN TECHNIQUE STRUCTURE:
        # 1. Simple explanation in plain language
        # 2. Use analogies and examples
        # 3. Break complex ideas into parts
        # 4. Explain why it matters
        # 
        # PROMPT ENGINEERING TECHNIQUES (Session 1):
        # - Start with persona: "You are an expert educational AI..."
        # - Give clear step-by-step instructions
        # - Specify output format and structure
        # - Include examples if helpful
        # 
        # EXAMPLE PROMPT STRUCTURE:
        # """
        # You are an expert educational AI that explains complex concepts simply.
        # 
        # Explain "{query}" using the Feynman Technique.
        # 
        # Use this verified information: {source_summary}
        # 
        # Structure:
        # 1. What is it? (simple definition)
        # 2. How does it work? (mechanism)
        # 3. Real-world example or analogy
        # 4. Why does it matter?
        # 
        # Guidelines:
        # - Use middle school level language
        # - Include citations [1], [2] when using source facts
        # - Keep explanation clear and engaging
        # """
        if not self.model:
            return "Gemini API not configured"
        prompt = f"""
        You are an expert professor who has been teaching for 100 years. You can explain complex concepts 
        simply using the Feynman Technique.
        
        In a well structured paragraph simply define "{query}" and explain how it works. 
        Make sure to use this verified information: {source_summary} and 
        to include citations [1],[2], when using source facts.
        At the end of the explanation, make sure to include a real-world example or 
        analogy or explain the significance of the concept.

        """
        
        return self.model.generate_content(prompt).text
        
        # TODO: Remove this assertion once you implement the function
        assert False, "❌ EXERCISE 1A NOT IMPLEMENTED: Please implement generate_explanation_with_sources() function in explanation_service.py"
        
        # TODO: Implement your solution here
        
        if not self.model:
            # TODO: Create a better fallback explanation without AI
            return f"Explanation for: {query} (Gemini API not configured)"
            
        # TODO: Create your prompt here using Session 1 techniques
        prompt = f"""
        # Your comprehensive prompt implementation goes here
        # Remember to:
        # - Use persona prompting
        # - Include the source_summary
        # - Apply Feynman Technique structure
        # - Specify citation format
        """
        
        try:
            # TODO: Generate content using self.model.generate_content(prompt)
            # TODO: Return the response text
            pass
        except Exception as e:
            print(f"Error generating explanation with sources: {e}")
            return f"Error generating explanation: {str(e)}"
    
    async def generate_explanation_without_sources(self, query: str) -> str:
        if not self.model:
            return f"Explanation for: {query} (Gemini API not configured)"
            
        prompt = f"""
        Explain this concept using the Feynman Technique: "{query}"
        
        Guidelines:
        1. Start with the core essence - what this really means
        2. Explain in simple terms a middle school student would understand
        3. Use analogies and real-world examples
        4. Break down complex ideas into smaller parts
        
        Structure your explanation with:
        - Brief introduction
        - Core explanation using simple language
        - Real-world example or analogy
        - Why this matters
        
        Note: Explain based on general knowledge without specific citations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return f"Error generating explanation: {str(e)}"