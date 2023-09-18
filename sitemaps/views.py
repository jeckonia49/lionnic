from .sitemaps import PostSitemap, AccountUserSitemap, CategorySitemap, SubCategorySitemap


site_sitemaps = {
    "posts":PostSitemap,
    "writers": AccountUserSitemap,
    "categories": CategorySitemap,
    "sub_categories": SubCategorySitemap
}
