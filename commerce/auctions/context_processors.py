from .models import Listing

def categories_processor(request):
    categories = Listing.objects.values_list('category', flat=True).distinct()[:4]
    return {
        'categories': categories
    }
