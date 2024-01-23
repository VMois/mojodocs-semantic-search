import logging

from chromadb import HttpClient
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import QueryForm


logger = logging.getLogger(__name__)


def index(request):
    form = QueryForm()
    return render(request, 'index.html', {'form': form})


@require_http_methods(['POST'])
def search(request):
    query = QueryForm(request.POST)
    if query.is_valid():
        results = []
        try:
            client = HttpClient('http://chromadb:8000')

            db = Chroma(
                client=client,
                embedding_function=OpenAIEmbeddings(),
            )

            docs = db.similarity_search(query.cleaned_data['content'])
            results = [{'origin_url': doc.metadata['source_link'], 'matched_content': doc.page_content} for doc in docs[:min(5, len(docs))]]
        except Exception as e:
            logger.error(e)
            return render(request, 'general_error.html', {'message': "Some unexpected error happened. Couldn't perform a search."}, status=HttpResponseServerError.status_code)

        return render(request, 'search_results.html', {'results': results})
    else:
        return render(request, 'form_errors.html', {'form': query}, status=HttpResponseBadRequest.status_code)
