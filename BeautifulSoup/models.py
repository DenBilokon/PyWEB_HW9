from mongoengine import connect, Document, StringField, ListField, CASCADE, ReferenceField

connect(host='mongodb+srv://userweb10:567234@pyweb.e9uvnnc.mongodb.net/?retryWrites=true&w=majority')


class Author(Document):
    fullname = StringField(required=True)
    date_born = StringField()
    born_location = StringField()
    bio = StringField()


class Quotes(Document):
    author = ReferenceField(Author)
    tags = ListField(StringField())
    quote = StringField(required=True)

