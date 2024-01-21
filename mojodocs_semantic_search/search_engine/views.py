from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import QueryForm


def index(request):
    form = QueryForm()
    return render(request, 'index.html', {'form': form})


@require_http_methods(['POST'])
def search(request):
    form = QueryForm(request.POST)
    if form.is_valid():
        return render(request, 'search_results.html', {'results': [{'origin_url': 'https://www.example.com', 'matched_content': 'Some content...'}]})
    else:
        return render(request, 'form_errors.html', {'form': form}, status=HttpResponseBadRequest.status_code)
