from django.contrib import admin
from django.db.models import QuerySet
from .models import Author, Publication, Comment


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("username", "last_name", "first_name", "birthday", "phone", "is_active", "is_staff",
                    "created", "edited")
    list_filter = ("is_active",)
    list_display_links = ("username", "first_name", "last_name", "phone", "is_active")

    fieldsets = (
        (None, {
            "fields": ("username", "last_name", "first_name", "birthday", "phone", "password")
        }),
        ("Дополнительные сведения", {
            "fields": ("is_active", "is_staff")
        }),
    )

    actions = ("change_false_status", "change_true_status")

    @admin.action(description='Изменить статус: Неактивный')
    def change_false_status(self, request, queryset: QuerySet):
        """
        Экшн изменения статуса читателя на Неактивного
        """
        queryset.update(is_active=False)
        self.message_user(request, f'Статус читателя изменен на "Неактивный"')

    @admin.action(description='Изменить статус: Активный')
    def change_true_status(self, request, queryset: QuerySet):
        """
        Экшн изменения статуса читателя на Активного
        """
        queryset.update(is_active=True)
        self.message_user(request, f'Статус читателя изменен на "Активный"')


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("heading", "author_link",  "created", "edited")
    list_display_links = ("heading", )
    list_filter = ("author",)
    search_fields = ("pdescription", "author")

    fieldsets = (
        (None, {
            "fields": ("heading", "pdescription",)
        }),
        ("Укажите автора/ов", {
            "fields": ("author", )
        }),
        ("Добавить изображение", {
            "fields": ("img",)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("cdescription", "author_link",  "created", "edited")
    list_display_links = ("cdescription",)
    list_filter = ("author",)
    search_fields = ("author",)

    fieldsets = (
        (None, {
            "fields": ("cdescription", )
        }),
        ("Укажите автора/ов", {
            "fields": ("author",)
        }),
    )
