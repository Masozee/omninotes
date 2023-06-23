from django.utils.deprecation import MiddlewareMixin
from django_user_agents.utils import get_user_agent
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import GeoIP2Exception
from .models import Visitor

class VisitorMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = get_user_agent(request)
        visited_url = request.path

        visitor = Visitor()
        visitor.visited_url = visited_url
        visitor.browser = user_agent.browser.family

        # Get and save visitor's location
        geoip = GeoIP2()
        ip_address = request.META.get('REMOTE_ADDR')
        try:
            visitor.country = geoip.country(ip_address)['country_name']
            visitor.city = geoip.city(ip_address)['city']
        except GeoIP2Exception:
            pass

        visitor.save()

        # Attach visitor instance to the request for further use if needed
        request.visitor = visitor
