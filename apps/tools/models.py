from django.db import models
from django_user_agents.utils import get_user_agent
from django.contrib.gis.geoip2 import GeoIP2Exception, GeoIP2



class Visitor(models.Model):
    visited_url = models.URLField()
    visited_at = models.DateTimeField(auto_now_add=True)
    browser = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        user_agent = get_user_agent(self.request)
        self.browser = user_agent.browser.family

        # Retrieve visitor's location (country and city) based on IP address
        geoip = GeoIP2()
        ip_address = self.request.META.get('REMOTE_ADDR')
        try:
            self.country = geoip.country(ip_address)['country_name']
            self.city = geoip.city(ip_address)['city']
        except GeoIP2Exception:
            pass

        super().save(*args, **kwargs)

    def __str__(self):
        return self.visited_url
