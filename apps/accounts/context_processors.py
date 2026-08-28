def cineast_context(request):
    """Global context processor for anything... application."""
    return {
        'APP_NAME': 'anything...',
        'PRIMARY_COLOR': '#FF4433',
    }
