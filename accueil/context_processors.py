# accueil/context_processors.py
from datetime import datetime

def base_context(request):
    return {
        'current_year': datetime.now().year,
    }
