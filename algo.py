import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from itertools import groupby

Activity = None

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Gui.ui', self)
        self.setWindowTitle("Personalized Exercise Prescription")
        self.clearButton.clicked.connect(self.clearbutton)
        self.calcButton.clicked.connect(self.design_exercise_plan)
        self.PateintInfo = None

    def clearbutton(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)

    def checkDataFilled(self):
        if self.lineEdit.text() and self.lineEdit_2.text() and self.get_met_value():
            return True
        else:
            return False
        
    def get_met_value(self):
        if self.radioButton.isChecked():
            return 3.5
        elif self.radioButton_2.isChecked():
            return 5
        elif self.radioButton_3.isChecked():
            return 7
        else:
            return None
    
    def calculate_calories_per_minute(self):
        weight_in_kg = int(self.lineEdit.text())
        height_in_meters = int(self.lineEdit_2.text())
        met_value = self.get_met_value()

        if weight_in_kg and height_in_meters and met_value:
            calories_per_minute = met_value * weight_in_kg / 60
            return calories_per_minute
        else: 
            QtWidgets.QMessageBox.information(self, 'Failed', 'Please fill data correctly .')

    def calculate_recommended_weight(self):
        if self.lineEdit and self.lineEdit_2 and self.get_met_value:
            recommended_weight=    24*((float(self.lineEdit_2.text())/100)**2)
            return recommended_weight
        
    def calculate_calories_to_burn(self):
        current_weight = int(self.lineEdit.text())
        recommended_weight = self.calculate_recommended_weight()

        if current_weight and recommended_weight:
            weight_difference =  current_weight-recommended_weight
            calories_to_burn = weight_difference * 7700
            return calories_to_burn
        else:
            QtWidgets.QMessageBox.information(self, 'Failed', 'Please fill data correctly .')

    def design_exercise_plan(self):
        total_calories_to_burn = int(self.calculate_calories_to_burn())
        exercises = self.exercise_dataset()
        # cpm=self.calculate_calories_per_minute()
        max_calories = [0] * (total_calories_to_burn + 1)
        exercise_sequence = [None] * (total_calories_to_burn + 1)

        for i in range(1, total_calories_to_burn + 1):
            for exercise, calories_per_minute in exercises.items():
                if i >= calories_per_minute:
                    if max_calories[i] < max_calories[i - calories_per_minute] + calories_per_minute:
                        max_calories[i] = max_calories[i - calories_per_minute] + calories_per_minute
                        exercise_sequence[i] = exercise
        print(exercise_sequence)
        exercise_plan = []
        # Count repetitions of each exercise in the exercise sequence
        repetitions = {exercise: exercise_sequence.count(exercise) for exercise in set(exercise_sequence)}

        for exercise, count in repetitions.items():
            if count > 0 and exercise is not None:
                exercise_plan.append((exercise, count))

        

        exercise_plan_str = "\n".join([f"{exercise}: {duration} minutes" for exercise, duration in exercise_plan])

        QMessageBox.information(self, "Exercise Plan", exercise_plan_str, QMessageBox.Ok)
        return exercise_plan
    
    def exercise_dataset(self):
        return {
            'Running': 5,  # calories per minute
            'Swimming': 3,
            'Cycling': 2,
            'Walking': 1
        }

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
