"""
Create classes to track homeworks.

1. Homework - accepts howework text and deadline (datetime.timedelta)
Homework has a method, that tells if deadline has passed.

2. Student - can solve homework with `do_homework` method.
Raises DeadlineError with "You are late" message if deadline has passed

3. Teacher - can create homework with `create_homework`; check homework with `check_homework`.
Any teacher can create or check any homework (even if it was created by one of colleagues).

Homework are cached in dict-like structure named `homework_done`. Key is homework, values are 
solutions. Each student can only have one homework solution.

Teacher can `reset_results` - with argument it will reset results for specific homework, without - 
it clears the cache.

Homework is solved if solution has more than 5 symbols.

-------------------
Check file with tests to see how all these classes are used. You can create any additional classes 
you want.
"""
from datetime import datetime, timedelta


class Homework:
    def __init__(self, hw_description: str, hw_deadline: int):
        self.hw_description = hw_description
        self.hw_deadline = hw_deadline
        self.creation_date = datetime.now()

    def check_deadline(self):
        return self.creation_date + timedelta(days=self.hw_deadline) < datetime.now()


class Student:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def do_homework(self, hw, hw_solution: str):
        if hw.check_deadline():
            raise DeadlineError("You are late")
        else:
            return ResultHomework(hw, self, hw_solution)


class ResultHomework:
    def __init__(self, hw, author, hw_solution):
        self.hw = hw
        self.author = author
        self.hw_solution = hw_solution


class Teacher:
    homework_done = dict()

    def __init__(self, teacher_first_name: str, teacher_last_name: str):
        self.teacher_first_name = teacher_first_name
        self.teacher_last_name = teacher_last_name

    @staticmethod
    def create_homework(hw_description, hw_deadline):
        return Homework(hw_description, hw_deadline)

    @classmethod
    def check_homework(cls, solved_homework):
        if solved_homework.hw in cls.homework_done:
            if solved_homework in cls.homework_done[solved_homework.hw]:
                return True
            elif len(solved_homework.hw_solution) > 5:
                cls.homework_done[solved_homework.hw].append(solved_homework)
                return True
            else:
                return False
        else:
            cls.homework_done[solved_homework.hw] = []
            if len(solved_homework.hw_solution) > 5:
                cls.homework_done[solved_homework.hw].append(solved_homework)
                return True
            else:
                return False

    @classmethod
    def reset_results(cls, hw_description=None):
        if hw_description:
            del cls.homework_done[hw_description]
        else:
            cls.homework_done.clear()


class DeadlineError(Exception):
    """Throw DeadlineError if deadline has passed"""
    pass