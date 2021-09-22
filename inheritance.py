class Person(object):
    def __init__(self, name=None, age=0, sex="F"):
        self.name = name
        self.age = age
        self.sex = sex.upper()
    
    def get_name(self):
        return self.name
        
    def get_age(self):
        return self.age 

    def get_sex(self):
        return self.sex

    def __str__(self):
        if "F" in self.sex:
            s = "Female"
        else:
            s = "Male"
        return "Hello my name is {}.I'm a {} years old {}.".format(self.name, self.age, s)    

class Student(Person):
    def __init__(self, name=None, age=0, sex="F", major=None):        
        Person.__init__(self,name,age,sex)
        self.major = major
    
    def say_major(self):
        return "I'm a {} major".format(self.major)
    
    def with_major(self):
        return  "{} I'm a {} major".format(super(Student,self).__str__(),self.major)  
    

    
class Car(object):
    condition = "new"
    def __init__(self, model, color, mpg):
        self.model = model
        self.color = color
        self.mpg   = mpg

    def display_car(self):
        return "This is a {} {} with {} MPG.".format(self.color, self.model, self.mpg)

    def drive_car(self):
        self.condition = "used"
        
class ElectricCar(Car):
    def __init__(self, model, color, mpg, battery_type):
        super(ElectricCar,self).__init__(model, color, mpg)
        self.battery_type = battery_typeclass 