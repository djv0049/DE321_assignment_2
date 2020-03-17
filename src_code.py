# python program one


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.eye_color = "red"
        self.height = 1

    def change_name(self, new_name):
        self.previous_name = self.name
        self.name = new_name

    def grow(self):
        print("hi")


p1 = Person("John", 36)

print(type(p1.name))
print(p1.age)
