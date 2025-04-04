class Blog(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_blogs',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        related_name='category_blogs',
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tag_blogs',
        blank=True
    )
    likes = models.ManyToManyField(
        User,
        related_name='user_likes',
        blank=True
    )
    title = models.CharField(
        max_length=250
    )
    slug = models.SlugField(null=True, blank=True, max_length=250)  # Increased max_length
    banner = models.ImageField(upload_to='blog_banners')
    description = RichTextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        updating = self.pk is not None
        
        try:
            if updating:
                self.slug = generate_unique_slug(self, self.title, update=True)
            else:
                self.slug = generate_unique_slug(self, self.title)
            
            super().save(*args, **kwargs)
        except Exception as e:
            if 'Data too long for column' in str(e):
                raise ValueError(
                    "The title is too long to generate a unique slug. "
                    "Please shorten the title and try again."
                )
            raise
