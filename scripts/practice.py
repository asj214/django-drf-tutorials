from users.models import User

def run():
  id = 1
  user = User.objects.get(pk=id)

  print({
    'id': user.id,
    'name': user.name,
    'email': user.email
  })

  # users post list
  posts = user.posts.all()

  for post in posts:
    print({
      'id': post.id,
      'title': post.title,
      'user': post.user,
      'created_at': post.created_at,
      'updated_at': post.updated_at
    })
