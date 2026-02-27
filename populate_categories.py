from events.models import Category

categories = ['Music', 'Technology', 'Sports', 'Art', 'Food', 'Business', 'Health', 'Education']
existing_count = Category.objects.count()

if existing_count == 0:
    print("No categories found. Creating default categories...")
    for name in categories:
        Category.objects.create(name=name)
        print(f"Created category: {name}")
    print("Done.")
else:
    print(f"Categories already exist. Count: {existing_count}")
