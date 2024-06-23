# Django-NanoID-Integration

**Django-NanoID-Integration** is a Django library that seamlessly integrates [NanoID](https://github.com/ai/nanoid) - a compact, secure, and URL-friendly unique string ID into your projects.

## Key Features

1. A custom `NanoIDField` for your Django models

2. An `upload_to_nanoid` method for `ImageField` and `FileField`, ensuring unique filenames

3. Predefined character sets for generating safe NanoID strings
   
   

This library draws inspiration from:

- [Ilya Semenov's django-uuid-upload](https://github.com/IlyaSemenov/django-uuid-upload)

- [Gökhan Öztürk's django-nanoid-field](https://github.com/goztrk/django-nanoid-field)

- [Andrew Conti's django-unique-upload](https://github.com/agconti/django-unique-upload)

## Why Use NanoID?

### The Problem with Sequential IDs

Using sequential integers as primary keys in URLs can expose sensitive information, which you likely want to keep confidential. I allows malicious users to easily access your data by modifying the URL. Sequential IDs can reveal information about the size of your database and growth rate, potentially compromising business intelligence.

### The Problem with UUIDs

While using `UUID`s offers mathematically guaranteed uniqueness and is supported by Django without additional libraries, it has the drawbacks of creating unwieldy and unattractive URLs, consuming more storage space (typically 128 bits) and can be slower to index and query in databases.

### The Solution: NanoID

[NanoID](https://github.com/ai/nanoid) is a solution that offers a balance between uniqueness and URL-friendliness. It generates compact, secure, and unique identifiers, making it an excellent choice for primary keys in URLs. NanoID helps:

- Maintain data privacy by avoiding sequential integers in URLs

- Ensure unique, manageable URLs and stable URL structures, even if product names change

- Generate shorter IDs compared to UUIDs (typically 21 characters)

- Offer better performance in databases due to smaller size

- Allow customization of ID length and character set

- Offer language-agnostic implementation with ports available for many programming languages

- Improve user experience with more readable and memorable IDs

## Installation

To install **Django-NanoID-Integration**, use pip:

```sh
pip install django-nanoid-integration
```

Add `django_nanoid_integration` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
...
'django_nanoid_integration',
...
]
```

## Using `NanoIDField`

The `NanoIDField` is a custom Django model field that integrates NanoID functionality directly into your models.

### Adding a `NanoIDField` to Your Model

Here's an example of how to add a `NanoIDField` to your Django model:

```python
from django.db import models
from django_nanoid_integration import NanoIDField

class User(models.Model):
    id = NanoIDField(primary_key=True)
    name = models.CharField(max_length=100)
```

### Customizing the NanoID

You can specify a custom alphabet and size for the NanoID. The following example creates a NanoID like B902_fA1:

```python
from django.db import models
from django_nanoid_integration import NanoIDField

class User(models.Model):
    id = NanoIDField(primary_key=True, alphabet='_-0123456789ABCdef', size=8)
    name = models.CharField(max_length=100)
```

### Using Predefined Alphabets

You can also use predefined alphabets for generating NanoIDs. The available choices are:

- **safe**: Contains characters that are easily distinguishable and avoid confusion, such as excluding similar-looking characters like '1' and 'I' or '0' and 'O'. This set combines safe uppercase and lowercase letters along with safe numbers. It is also the default choice when using `NanoIDField()`

- **unsafe**: A broader set that includes both safe and potentially confusing characters, such as similar-looking letters and numbers

- **numbers**: Only numeric characters (0-9)

- **safe_letters**: A combination of safe uppercase and lowercase letters

- **safe_letters_uppercase**: Only safe uppercase letters

- **safe_letters_lowercase**: Only safe lowercase letters

- **safe_letters_uppercase_and_numbers**: Safe uppercase letters combined with safe numbers

- **safe_letters_lowercase_and_numbers**: Safe lowercase letters combined with safe numbers

Here’s an example using the predefined `numbers` alphabet, which will create a NanoID like `40349`:

```python
from django.db import models
from django_nanoid_integration import NanoIDField

class User(models.Model):
    id = NanoIDField(primary_key=True, alphabet_predefined='numbers', size=5)
    name = models.CharField(max_length=100)
```

### Ensuring Unique NanoIDs

When generating NanoIDs, there is a small chance that two identical IDs might be created, especially if they are very short. This is known as a "collision." You can use the [Nano ID Collision Calculator](https://alex7kom.github.io/nano-nanoid-cc) to check the likelihood of collisions for different ID lengths and character sets.

To ensure uniqueness, use the `UniqueNanoIDMixin` and set `unique=True` for the field. Primary Keys are set `unique=True` by default. You can also specify the number of attempts to generate a unique ID with `nanoid_max_attempts` (default is 10).

Here's an example of how to use the `UniqueNanoIDMixin` in your Django models:

```python
from django.db import models
from django_nanoid_integration import NanoIDField, UniqueNanoIDMixin

class User(UniqueNanoIDMixin, models.Model):
    id = NanoIDField(primary_key=True)
    another_unique_nanoid = NanoIDField(alphabet_predefined='numbers', size=5, unique=True)
    name = models.CharField(max_length=100)

nanoid_max_attempts = 10
```

### Regenerating NanoIDs

You can regenerate a NanoID for a specified field, useful for updating non-primary key fields. Use `force=True` to bypass safety confirmations, but be cautious with foreign key relations. They are not supported yet.

Here's an example of how to use `regenerate_nanoid`:

```python
user = User.objects.get(email='email@example.com')
user.regenerate_nanoid('unique_nanoid_field', force=True)
```

## Using `upload_to_nanoid` Function

The `upload_to_nanoid` function in `ImageField` or `FileField` generates unique filenames, enhancing security and uniqueness.

### Settings adjustment

Add `MEDIA_URL` and `MEDIA_ROOT` to your `settings.py` if not yet done. This step is crucial for handling media files in Django.

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Also:

- Ensure `BASE_DIR` is correctly defined

- Ensure `urlpatterns` in `urls.py` are set to serve Media Files during Development

- Ensure your custom storage backend is configured properly (if you use it)

### Adding `upload_to_nanoid` to Your Model

```python
from django.db import models
from django_nanoid_integration import upload_to_nanoid

class UserProfile(models.Model):
    picture = models.ImageField(upload_to=upload_to_nanoid('pictures'))
    anyfile = models.FileField(upload_to=upload_to_nanoid('files'))
```

### Key Parameters for `upload_to_nanoid`

#### `preserve_original_filename`

The `preserve_original_filename` parameter controls whether to keep the original filenames when uploading files. By default, it is set to `False`.

- If `False`, files are uploaded with a unique identifier like `/media/pictures/{nanoid}.jpg`

- If `True`, files retain their original filenames within a directory formatted as `/media/pictures/{nanoid}/original.jpg`

```python
from django.db import models
from django_nanoid_integration import upload_to_nanoid

class UserProfile(models.Model):
    ...
    picture = models.ImageField(upload_to=upload_to_nanoid('pictures', preserve_original_filename=True))
    ...
```

#### `remove_query_strings`

The `remove_query_strings` parameter determines whether to remove query strings from the filenames of uploaded files, ensuring a clean and consistent file name. By default, it is set to `True`.

```python
from django.db import models
from django_nanoid_integration import upload_to_nanoid

class UserProfile(models.Model):
    ...
    picture = models.ImageField(upload_to=upload_to_nanoid('pictures', remove_query_strings=True))
    ...
```

#### `alphabet`, `size`

The `alphabet` and `size` parameters allow you to specify a custom alphabet and length for the NanoID, exactly as in the `NanoIDField`. This example creates a filepath like `/media/pictures/B902_fA1.jpg`:

```python
from django.db import models
from django_nanoid_integration import upload_to_nanoid

class UserProfile(models.Model):
    ...
    picture = models.ImageField(upload_to=upload_to_nanoid('pictures', alphabet='_-0123456789ABCdef', size=8))
    ...
```

#### `alphabet_predefined`

You can also use predefined alphabets for generating NanoIDs, similar to the `NanoIDField`. The available choices are also the same as in `NanoIDField`.

```python
from django.db import models
from django_nanoid_integration import upload_to_nanoid

class UserProfile(models.Model):
    ...
    picture = models.ImageField(upload_to=upload_to_nanoid('pictures', alphabet_predefined='numbers', size=1))
    ...
```

## Global Configuration in `settings.py`

You can set global options for the NanoID generator in your `settings.py`. If both `NANOID_ALPHABET` and `NANOID_ALPHABET_PREDEFINED` are set, `NANOID_ALPHABET` takes precedence.

```python
NANOID_ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-'
NANOID_ALPHABET_PREDEFINED = 'safe'
NANOID_SIZE = 10
```

## Database Migration Instructions

After making changes to your models, update your database schema. Additionally, if you change `NANOID_ALPHABET`, `NANOID_ALPHABET_PREDEFINED`, or `NANOID_SIZE` in `settings.py`, run these commands:

```sh
python manage.py makemigrations
python manage.py migrate
```

## Contributing

Your contributions are welcome and appreciated! This project is actively maintained, and I am eager to hear your feature requests and suggestions. Follow these steps to get started:

1. **Fork the repository**: Click the "Fork" button on the repository's GitHub page to create a copy of the repository under your own GitHub account

2. **Clone your fork**: Clone your forked repository to your local machine (git clone https://github.com/spechtx/django-nanoid-integration)

3. **Create a new branch**: Create a new branch for your feature or bug fix (git checkout -b feature-branch)

4. **Make your changes**: Implement your changes or new features

5. **Commit your changes**: Commit your changes with a descriptive commit message (git commit -m 'Add new feature')

6. **Push your branch**: Push your branch to your forked repository on GitHub (git push origin feature-branch)

7. **Open a Pull Request**: Navigate to the original repository on GitHub and click the "New Pull Request" button. Compare your feature branch with the original repository's branch (main) and submit the pull request.

I look forward to your contributions!

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Roadmap

- **Update Foreign Key Relations**: Ensure that foreign key relations are correctly updated when regenerating NanoIDs

- **Write Tests**: Develop comprehensive tests to ensure the reliability and stability of the NanoID integration.

## Acknowledgements

This library draws inspiration from:

- [Ilya Semenov's django-uuid-upload](https://github.com/IlyaSemenov/django-uuid-upload)

- [Gökhan Öztürk's django-nanoid-field](https://github.com/goztrk/django-nanoid-field)

- [Andrew Conti's django-unique-upload](https://github.com/agconti/django-unique-upload)

Enjoy using Django-NanoID-Integration? Give us a ⭐ on GitHub and share your experience!
