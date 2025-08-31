class Article:
    all = []

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self._title = title  # Direct assignment to bypass setter
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            return  # Silently ignore invalid types
        if len(value) < 5 or len(value) > 50:
            return  # Silently ignore invalid lengths
        if hasattr(self, '_title'):
            return  # Silently ignore attempts to change
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            return  # Silently ignore invalid types
        if hasattr(self, '_author') and self._author:
            self._author._articles.remove(self)
        self._author = value
        value._articles.append(self)

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            return  # Silently ignore invalid types
        if hasattr(self, '_magazine') and self._magazine:
            self._magazine._articles.remove(self)
        self._magazine = value
        value._articles.append(self)


class Author:
    def __init__(self, name):
        self._name = None
        self.name = name  # Uses property setter
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            return  # Silently ignore invalid types
        if len(value) == 0:
            return  # Silently ignore empty names
        if hasattr(self, '_name') and self._name is not None:
            return  # Silently ignore attempts to change
        self._name = value

    def articles(self):
        return self._articles

    def magazines(self):
        return list({article.magazine for article in self._articles})

    def add_article(self, magazine, title):
        article = Article(self, magazine, title)
        return article

    def topic_areas(self):
        if not self._articles:
            return None
        return list({magazine.category for magazine in self.magazines()})


class Magazine:
    _all_magazines = []

    def __init__(self, name, category):
        self._name = None
        self._category = None
        self.name = name  # Uses property setter
        self.category = category  # Uses property setter
        self._articles = []
        Magazine._all_magazines.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            return  # Silently ignore invalid types
        if len(value) < 2 or len(value) > 16:
            return  # Silently ignore invalid lengths
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            return  # Silently ignore invalid types
        if len(value) == 0:
            return  # Silently ignore empty categories
        self._category = value

    def articles(self):
        return self._articles

    def contributors(self):
        return list({article.author for article in self._articles})

    def article_titles(self):
        if not self._articles:
            return None
        return [article.title for article in self._articles]

    def contributing_authors(self):
        authors = [article.author for article in self._articles]
        author_counts = {author: authors.count(author) for author in authors}
        result = [author for author, count in author_counts.items() if count > 2]
        return result if result else None

    @classmethod
    def top_publisher(cls):
        if not cls._all_magazines:
            return None
        return max(cls._all_magazines, key=lambda mag: len(mag.articles()))