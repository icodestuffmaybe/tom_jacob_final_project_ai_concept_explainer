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
        if not self.model:
            # Fallback: use query words + variations
            words = query.split()
            return [query] + words[:2]  # Include full query + first 2 words
            
        prompt = f"""
        Extract 3-5 Wikipedia-searchable keywords from this educational query:
        "{query}"
        
        IMPORTANT:
        - Return keywords that would have Wikipedia articles
        - Include the main topic and related terms
        - Use simple, common terms that Wikipedia would have
        - Prefer single words or common phrases
        - Include the original query if it's a good Wikipedia term
        
        Return only the keywords separated by commas, no explanation.
        
        Examples:
        "What is photosynthesis?" → "photosynthesis, plants, biology, chlorophyll"
        "Explain machine learning" → "machine learning, artificial intelligence, algorithms, computer science"
        """
        
        try:
            response = self.model.generate_content(prompt)
            keywords = [k.strip() for k in response.text.strip().split(',')]
            # Always include the original query as a keyword
            if query not in keywords:
                keywords.insert(0, query)
            return keywords[:5]
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
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # First try: Direct page summary with URL encoding
                import urllib.parse
                encoded_keyword = urllib.parse.quote(keyword.replace(' ', '_'))
                summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_keyword}"
                
                print(f"   📡 Trying direct page: {summary_url}")
                response = await client.get(summary_url)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Direct page found: {data.get('title', 'No title')}")
                    return [{
                        'title': data.get('title', ''),
                        'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                        'snippet': data.get('extract', '')[:300],
                        'source_type': 'wikipedia'
                    }]
                
                # Second try: Search API for broader results
                print(f"   🔍 Trying search API for: {keyword}")
                search_url = "https://en.wikipedia.org/w/api.php"
                search_params = {
                    'action': 'query',
                    'format': 'json',
                    'list': 'search',
                    'srsearch': keyword,
                    'srlimit': 1
                }
                
                search_response = await client.get(search_url, params=search_params)
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    search_results = search_data.get('query', {}).get('search', [])
                    
                    if search_results:
                        result = search_results[0]
                        title = result.get('title', '')
                        print(f"   ✅ Search found: {title}")
                        
                        # Get the summary for the found page
                        clean_title = urllib.parse.quote(title.replace(' ', '_'))
                        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_title}"
                        summary_response = await client.get(summary_url)
                        
                        if summary_response.status_code == 200:
                            summary_data = summary_response.json()
                            return [{
                                'title': summary_data.get('title', title),
                                'url': summary_data.get('content_urls', {}).get('desktop', {}).get('page', f"https://en.wikipedia.org/wiki/{clean_title}"),
                                'snippet': summary_data.get('extract', result.get('snippet', ''))[:300],
                                'source_type': 'wikipedia'
                            }]
                        else:
                            # Fallback to search result snippet
                            return [{
                                'title': title,
                                'url': f"https://en.wikipedia.org/wiki/{clean_title}",
                                'snippet': result.get('snippet', '')[:300],
                                'source_type': 'wikipedia'
                            }]
                    else:
                        print(f"   ❌ No search results for: {keyword}")
                
        except Exception as e:
            print(f"   ❌ Wikipedia search error for '{keyword}': {e}")
        
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
        if not self.model:
            return ""
            
        source_texts = []
        for source in sources:
            source_texts.append(f"Source: {source['title']}\n{source['snippet']}")
        
        prompt = f"""
        Summarize these educational sources into key facts and concepts:
        
        {chr(10).join(source_texts)}
        
        Extract the most important information that would help explain the topic.
        Focus on facts, definitions, and key concepts.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error summarizing sources: {e}")
            return ""
    
    async def generate_explanation_with_sources(self, query: str, source_summary: str, sources: List[Dict]) -> str:
        if not self.model:
            return f"Explanation for: {query} (Gemini API not configured)"
            
        prompt = f"""
        Explain this concept using the Feynman Technique: "{query}"
        
        Use this verified information from credible sources:
        {source_summary}
        
        Guidelines:
        1. Start with the core essence - what this really means
        2. Explain in simple terms a middle school student would understand
        3. Use analogies and real-world examples
        4. Break down complex ideas into smaller parts
        5. Include numbered citations [1], [2], etc. when referencing facts
        
        Structure your explanation with:
        - Brief introduction
        - Core explanation using simple language
        - Real-world example or analogy
        - Why this matters
        
        Keep the explanation concise but complete.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
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