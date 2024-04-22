import sys
import pandas as pd
from PyQt5 import QtWidgets, uic, QtGui

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
        
    def max_calories_exercise(self):
        if self.PateintInfo is not None:
            total_calories_to_burn = int(self.calculate_calories_to_burn())
            calories_per_minute = self.calculate_calories_per_minute()
            exercises = [
                {"name": "Walking", "calories_per_minute": 5}, # 5 calories per minute
                {"name": "Jogging", "calories_per_minute": 10}, # 10 calories per minute
                {"name": "Cycling", "calories_per_minute": 8},  # 8 calories per minute
                {"name": "Swimming", "calories_per_minute": 12} # 12 calories per minute
            ]

            # Initialize a list to store the maximum calories for each total calories to burn
            max_calories = [0] * (total_calories_to_burn + 1)
            exercise_sequence = [[] for _ in range(total_calories_to_burn + 1)]

            # Iterate through each total calories to burn
            for i in range(1, total_calories_to_burn + 1):
                # Initialize the maximum calories for this total calories to burn as calories_per_minute
                max_calories[i] = calories_per_minute

                # Check if splitting the total calories to burn and using the maximum calories from previous durations is more beneficial
                for j in range(1, i):
                    if max_calories[i] < max_calories[j] + max_calories[i - j]:
                        max_calories[i] = max_calories[j] + max_calories[i - j]
                        exercise_sequence[i] = exercise_sequence[j] + exercise_sequence[i - j]

                exercise_sequence[i].append(calories_per_minute)

            # Return the exercise sequence needed to burn the total calories
            return exercise_sequence[total_calories_to_burn]



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
