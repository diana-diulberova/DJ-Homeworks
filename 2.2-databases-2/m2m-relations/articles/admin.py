from django.contrib import admin
from .models import Article, Tags, TagsArticle
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            if form.cleaned_data:
                if form.cleaned_data['is_main'] == True:
                    count += 1
        if count == 1:
            return super().clean()  # вызываем базовый код переопределяемого метода
        else:
            if count == 0:
                raise ValidationError('Укажите основной раздел')
            else:
                raise ValidationError('Основным может быть только один раздел')


class RelationshipInline(admin.TabularInline):
    model = TagsArticle
    formset = RelationshipInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass


@admin.register(TagsArticle)
class TagsArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'tag', 'is_main']
