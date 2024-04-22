import sys
import pandas as pd
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QMessageBox

class Patient:

    def __init__(self):
        self.weight = None
        self.height = None
        self.lvlOfActivity = None

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Gui.ui', self)
        self.setWindowTitle("Personalized Exercise Prescription")
        self.clearButton.clicked.connect(self.clearbutton)
        self.calcButton.clicked.connect(self.display_exercise_plan)
        self.PateintInfo = None

    def clearbutton(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)

    def setPatientData(self):
        P = Patient()
        P.weight = float(self.lineEdit.text())
        P.height = float(self.lineEdit_2.text())
        if self.radioButton.isChecked():
            P.lvlOfActivity = 3.5
        elif self.radioButton_2.isChecked():
            P.lvlOfActivity = 5.0
        elif self.radioButton_3.isChecked():
            P.lvlOfActivity = 7.0
        else:
            P.lvlOfActivity = 0  # Default value
        self.PateintInfo = P 
    
    def calculate_calories_per_minute(self):
        if self.PateintInfo is not None:
            return self.PateintInfo.lvlOfActivity * 3.5 * self.PateintInfo.weight / 200
        
    def calculate_recommended_weight(self):
        if self.PateintInfo is not None:
            recommended_weight = 22.5 * (self.PateintInfo.height**2)
            return recommended_weight
        
    def calculate_calories_to_burn(self):
        if self.PateintInfo is not None:
            recommended_weight = self.calculate_recommended_weight()
            calories_to_burn = (self.PateintInfo.weight - recommended_weight) * 7700 
            return calories_to_burn
        
    def exercise_dataset(self):
        return {
            'Running': 10,  # calories per minute
            'Swimming': 8,
            'Cycling': 7,
            'Walking': 5
        }

    def get_exercise_plan(self, exercise_dataset):
        total_calories_to_burn = self.calculate_calories_to_burn()
        calories_burn_rate = self.calculate_calories_per_minute()

        # Initialize DP table
        dp = [0] + [float('inf')] * int(total_calories_to_burn)

        # List to store the exercises for each calorie count
        exercises = [''] + [''] * int(total_calories_to_burn)

        for exercise, calories_per_min in exercise_dataset.items():
            for i in range(calories_per_min, int(total_calories_to_burn) + 1):
                if dp[i - calories_per_min] + 1 < dp[i]:
                    dp[i] = dp[i - calories_per_min] + 1
                    exercises[i] = exercises[i - calories_per_min] + ', ' + exercise if exercises[i - calories_per_min] else exercise

        # Calculate time for each exercise
        exercise_plan = {}
        for exercise in exercises[-1].split(', '):
            if exercise not in exercise_plan:
                exercise_plan[exercise] = 1 / (exercise_dataset[exercise] / calories_burn_rate)
            else:
                exercise_plan[exercise] += 1 / (exercise_dataset[exercise] / calories_burn_rate)

        return exercise_plan
    
    def display_exercise_plan(self):
        self.setPatientData()
        exercise_dataset = self.exercise_dataset()
        exercise_plan = self.get_exercise_plan(exercise_dataset)

        message = "Exercise Plan:\n"
        for exercise, time in exercise_plan.items():
            message += f"{exercise}: {time} minutes\n"

        msg = QMessageBox()
        msg.setWindowTitle("Exercise Plan")
        msg.setText(message)
        msg.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
