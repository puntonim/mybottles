from core.models import Bottle


class BottlesListDomain:
    def get_queryset(self):
        # Always return ordered querysets because they will be paginated
        # later on.
        queryset = Bottle.objects.all().order_by('id')
        return queryset
