import os
import re
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from .models import Reference
from .serializers import ReferenceSerializer
from ncct_backend.species_management.serializers import SpeciesSerializer
from ncct_backend.species_management.models import Species
from django.db.models import Q
from dotenv import load_dotenv

load_dotenv()

CROSSREF_API = os.getenv("CROSSREF_API")
SEMANTIC_SCHOLAR_API = os.getenv("SEMANTIC_SCHOLAR_API")
BING_SEARCH_API = os.getenv("BING_SEARCH_API")
BING_API_KEY = os.getenv("BING_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

def extract_text_from_pdf(pdf_file):
    """Extract full text from PDF using PyMuPDF."""
    text = ""
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in pdf_document:
        text += page.get_text()
    return text

def google_search(query):
        """Search using Google Custom Search API."""
        if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
            return []

        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CSE_ID,
            "q": query,
            "num": 10
        }

        res = requests.get(search_url, params=params)
        # Check if the request was successful
        if res.status_code != 200:
            return []

        results = []
        for item in res.json().get("items", []):
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet", "")
            })
        return results

def web_search(query):
    """Try Bing API first, fallback to Google if no key."""
    print(f"Web search query: {query}")
    if BING_API_KEY:
        headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
        bing_res = requests.get(BING_SEARCH_API, headers=headers, params={"q": query, "count": 5})
        print(f"Bing API response status code: {bing_res.status_code}")
        print(f"Bing API response JSON: {bing_res.json()}")
        if bing_res.status_code == 200:
            return bing_res.json().get("webPages", {}).get("value", [])
    else:
        google_results = google_search(query)
        print(f"Google Search results: {google_results}")
        return google_results

def search_publication_internet(text):
    results = {
        "doi": None,
        "metadata": None,
        "semantic_scholar": None,
        "web_matches": None
    }

    # 1️⃣ Try extracting DOI
    doi_match = re.search(r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+', text, re.I)
    if doi_match:
        doi = doi_match.group(0)
        results["doi"] = doi

        # CrossRef metadata
        crossref_res = requests.get(f"{CROSSREF_API}/{doi}")
        if crossref_res.status_code == 200:
            results["metadata"] = crossref_res.json().get("message", {})

        # Semantic Scholar
        ss_params = {"query": doi, "limit": 1, "fields": "title,authors,url,abstract"}
        ss_res = requests.get(SEMANTIC_SCHOLAR_API, params=ss_params)
        if ss_res.status_code == 200:
            results["semantic_scholar"] = ss_res.json()

        # Web search by DOI
        results["web_matches"] = web_search(doi)
        return results

    # 2️⃣ If no DOI → try title
    title_match = re.search(r'(?<=\n)[A-Z][^\n]{20,200}(?=\n)', text)
    if title_match:
        title = title_match.group(0).strip()

        # CrossRef search
        cr_params = {"query.title": title, "rows": 1}
        cr_res = requests.get(CROSSREF_API, params=cr_params)
        if cr_res.status_code == 200:
            items = cr_res.json().get("message", {}).get("items", [])
            if items:
                results["metadata"] = items[0]

        # Semantic Scholar
        ss_params = {"query": title, "limit": 1, "fields": "title,authors,url,abstract"}
        ss_res = requests.get(SEMANTIC_SCHOLAR_API, params=ss_params)
        if ss_res.status_code == 200:
            results["semantic_scholar"] = ss_res.json()

        # Web search
        results["web_matches"] = web_search(f'"{title}"')
        return results

    return {"error": "No DOI or title found"}

@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_and_search_pdf(request):
    """
    Upload a PDF, extract metadata from the internet (CrossRef, Semantic Scholar, Web Search).
    """
    pdf_file = request.FILES.get("file")
    if not pdf_file:
        return Response({"error": "No file uploaded"}, status=400)

    # Step 1: Extract text
    text = extract_text_from_pdf(pdf_file)

    # Step 2: Search internet
    results = search_publication_internet(text)

    return Response(results)

class ReferenceListCreateView(ListCreateAPIView):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [IsAuthenticated]

class ReferenceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [IsAuthenticated]

class ReferenceSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_term = request.query_params.get('q', None)
        if not search_term:
            return Response({"error": "A search term ('q' parameter) is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Find references where the search term matches any field
        references = Reference.objects.filter(
            Q(type__icontains=search_term) |
            Q(title__icontains=search_term) |
            Q(author__icontains=search_term) |
            Q(doi__icontains=search_term) |
            Q(thesis_level__icontains=search_term)
        )

        species_with_refs = Species.objects.none()
        if references.exists():
            # Get all species linked to these references
            species_with_refs = Species.objects.filter(references__in=references).distinct()

        if species_with_refs.exists():
            serializer = SpeciesSerializer(species_with_refs, many=True)
            formatted_data = []
            reference_map = {ref.id: ref for ref in references}
            for obj in serializer.data:
                # Get all reference IDs for this species
                species_references = obj.get("references", [])
                # Get the first matching reference from the filtered references, if any
                ref = None
                for ref_id in species_references:
                    if ref_id in reference_map:
                        ref = reference_map[ref_id]
                        break
                formatted_data.append({
                    "title": obj.get("name"),
                    "author": ref.author if ref else None,
                    "doi": ref.doi if ref else None,
                    "brief_text": obj.get("trad_uses")[:100] if obj.get("trad_uses") else "",
                    "link": None,  # You can add a link if available in your model/serializer
                    "reference_id": ref.id if ref else None,
                    "reference_title": ref.title if ref else None,
                })
            return Response({
                "message": "Results found in the database",
                "results": formatted_data
            })
        else:
            search_query = f"{search_term}"
            print(f"Initiating web search for query: {search_query}")
            web_results = web_search(search_query)
            print(f"Raw web search results: {web_results}")
            # Always return web search results as an array
            formatted_results = []
            for result in web_results:
                link = result.get("link") or result.get("url")
                if not link:
                    print(f"Skipping result due to no link: {result}")
                    continue

                doi = None
                print(f"Attempting to fetch content from link: {link}")
                try:
                    page_res = requests.get(link, timeout=10)
                    print(f"Page content fetch status for {link}: {page_res.status_code}")
                    if page_res.status_code == 200:
                        soup = BeautifulSoup(page_res.content, 'html.parser')
                        text = soup.get_text()
                        doi_match = re.search(r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b', text, re.IGNORECASE)
                        if doi_match:
                            doi = doi_match.group(0)
                            print(f"DOI found for {link}: {doi}")
                        else:
                            print(f"No DOI found on page: {link}")
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching page {link}: {e}")
                    pass

                formatted_results.append({
                    "title": result.get("title") or result.get("name"),
                    "author": None,
                    "doi": doi,
                    "brief_text": result.get("snippet")[:100],
                    "link": link
                })
            print(f"Formatted web search results: {formatted_results}")
            return Response({
                "message": "No results found in the database. Showing web search results.",
                "results": formatted_results
            })