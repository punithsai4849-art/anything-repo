import ipaddress
import socket
import urllib.parse
import urllib.request
import mimetypes
import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.conf import settings
from apps.reviews.models import Review
from apps.entities.models import Entity

def is_safe_remote_url(url_str):
    """
    Validate that the URL uses http/https and does not resolve to private/loopback/link-local IP addresses.
    (SSRF prevention per security guidelines)
    """
    try:
        parsed = urllib.parse.urlparse(url_str)
        if parsed.scheme not in ('http', 'https'):
            return False
        hostname = parsed.hostname
        if not hostname:
            return False
            
        addr_info = socket.getaddrinfo(hostname, None)
        for _, _, _, _, sockaddr in addr_info:
            ip = ipaddress.ip_address(sockaddr[0])
            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
                or ip.is_multicast
            ):
                return False
        return True
    except Exception:
        return False

def entity_image_proxy_view(request, slug):
    """
    Serves entity artwork as a same-origin image for canvas export without CORS tainting.
    Handles local uploaded files and SSRF-validated remote URLs.
    """
    entity = get_object_or_404(Entity, slug=slug)
    img_url = entity.image_display_url
    if not img_url:
        raise Http404("Entity has no image")

    # 1. Local media file (/media/...)
    if img_url.startswith('/media/'):
        rel_path = img_url[len('/media/'):]
        full_path = os.path.join(settings.MEDIA_ROOT, rel_path)
        if os.path.exists(full_path):
            content_type, _ = mimetypes.guess_type(full_path)
            content_type = content_type or 'image/jpeg'
            with open(full_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type=content_type)
                response['Cache-Control'] = 'public, max-age=86400'
                response['Access-Control-Allow-Origin'] = '*'
                return response
        raise Http404("Media file not found")

    # 2. Local ImageField
    if entity.primary_image:
        try:
            content_type, _ = mimetypes.guess_type(entity.primary_image.name)
            content_type = content_type or 'image/jpeg'
            with entity.primary_image.open('rb') as f:
                response = HttpResponse(f.read(), content_type=content_type)
                response['Cache-Control'] = 'public, max-age=86400'
                response['Access-Control-Allow-Origin'] = '*'
                return response
        except Exception:
            pass

    # 3. Remote URL (e.g. Unsplash, TMDB)
    if img_url.startswith('http://') or img_url.startswith('https://'):
        if not is_safe_remote_url(img_url):
            return HttpResponseBadRequest("Invalid or unsafe image URL")

        try:
            req = urllib.request.Request(
                img_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            with urllib.request.urlopen(req, timeout=5) as remote_res:
                content_type = remote_res.headers.get_content_type()
                if not content_type or not content_type.startswith('image/'):
                    content_type = 'image/jpeg'
                
                # Cap response at 5MB
                img_bytes = remote_res.read(5 * 1024 * 1024)
                response = HttpResponse(img_bytes, content_type=content_type)
                response['Cache-Control'] = 'public, max-age=86400'
                response['Access-Control-Allow-Origin'] = '*'
                return response
        except Exception:
            raise Http404("Failed to fetch remote image")

    raise Http404("Unsupported image source")

def share_card_view(request, review_id):
    review = get_object_or_404(
        Review.objects.select_related('user__profile', 'entity__category', 'rating'),
        id=review_id
    )
    metadata = review.entity.metadata or {}
    year = metadata.get('release_year') or metadata.get('year') or ''
    creator = metadata.get('director') or metadata.get('artist') or metadata.get('author') or metadata.get('brand') or ''

    context = {
        'review': review,
        'entity': review.entity,
        'category': review.entity.category,
        'rating': review.rating,
        'author': review.user,
        'year': str(year) if year else '',
        'creator': str(creator) if creator else '',
    }
    return render(request, 'sharing/share_card.html', context)

def share_entity_card_view(request, slug):
    entity = get_object_or_404(
        Entity.objects.select_related('category'),
        slug=slug
    )
    
    # Try to find a featured/user review if available
    review = None
    if request.user.is_authenticated:
        review = entity.reviews.filter(user=request.user).select_related('user__profile', 'rating').first()
    if not review:
        review = entity.reviews.select_related('user__profile', 'rating').order_by('-created_at').first()

    metadata = entity.metadata or {}
    year = metadata.get('release_year') or metadata.get('year') or ''
    creator = metadata.get('director') or metadata.get('artist') or metadata.get('author') or metadata.get('brand') or ''

    context = {
        'review': review,
        'entity': entity,
        'category': entity.category,
        'rating': review.rating if review else None,
        'author': review.user if review else None,
        'year': str(year) if year else '',
        'creator': str(creator) if creator else '',
        'is_entity_share': True,
    }
    return render(request, 'sharing/share_card.html', context)

