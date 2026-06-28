from core.models import Chapter

c = Chapter(
    number=1,
    title="Introducción",
    text="Hola mundo"
)

print(c)

print(c.words)

print(c.characters)
