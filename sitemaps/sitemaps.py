from django.contrib.sitemaps import Sitemap
from posts.models import Post, Category, SubCategory
from accounts.models import Profile



class PostSitemap(Sitemap):
    changefreg = "daily"
    priority = 0.7
    
    def items(self):
        return Post.objects.all()
    
    def lastmod(self, obj):
        return obj.updatedAt

    

class AccountUserSitemap(Sitemap):
    def items(self):
        return Profile.objects.filter(user__is_active=True).filter(post_author__gte=1).all()
    def lastmod(self, obj):
        return obj.updatedAt


class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()
    
class SubCategorySitemap(Sitemap):
    def items(self):
        return SubCategory.objects.all()
    
    
