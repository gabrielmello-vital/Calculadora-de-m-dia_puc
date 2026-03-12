from model.student_model import studentModel
from views.student_view import studentView
from controllers.controller_aluno import controllerALuno

if __name__ == "__main__":
    model = studentModel()
    views = studentView()
    controllers = controllerALuno(model,views)
    controllers.start()