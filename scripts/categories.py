from categories.models import Category


def run():
  for c in Category.objects.all():
    path = c.get_children_ids()
    c.path = path
    c.save()
