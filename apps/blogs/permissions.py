from authority import permissions
from blogs.models import Post


class BlogPermission(permissions.BasePermission):
    label = 'blog_permission'
    checks = ('blog_edit', )

    def blog_edit(self):
        print "12121"
        return True

authority.register(Post, BlogPermission)
