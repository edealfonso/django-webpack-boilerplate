from django.db import models

from django_prose_editor.fields import ProseEditorField

# from .choices import *


# Example: rich text (django-prose-editor) + drag & drop ordering in the
# admin (django-admin-sortable2). Uncomment, adapt and run makemigrations.
#
# class Item(models.Model):
#     title = models.CharField(max_length=200)
#     body = ProseEditorField(
#         extensions={
#             "Bold": True,
#             "Italic": True,
#             "Heading": {"levels": [2, 3]},
#             "BulletList": True,
#             "OrderedList": True,
#             "ListItem": True,
#             "Link": True,
#         },
#         sanitize=True,  # server-side HTML cleanup matching the allowed extensions
#         blank=True,
#     )
#     order = models.PositiveIntegerField(default=0, db_index=True)
#
#     class Meta:
#         ordering = ["order"]
#
#     def __str__(self):
#         return self.title
