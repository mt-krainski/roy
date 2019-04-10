from django.contrib.gis.forms import OSMWidget


class BootstrapMapWidget(OSMWidget):
    template_name = 'bistro/map.html'
