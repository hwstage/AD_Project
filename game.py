from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from randomLogic import *
from scoreDB import *

class ArithmeticGame(QWidget):
    
    def __init__(self): # GUI 생성
        super().__init__()
        self.problemWindow = QTextEdit()
        self.problemWindow.setReadOnly(True)
        self.problemWindow.setAlignment(Qt.AlignCenter)
        font = self.problemWindow.font()
        font.setPointSize(17)
        self.problemWindow.setFont(font)
        self.problemWindow.setText("Welcome to Arithemetic game")
        self.problemWindow.setMinimumWidth(300)
        
        problemLayout = QGridLayout()
        problemLayout.addWidget(self.problemWindow, 0, 0)

        first_btn = QPushButton("1")
        second_btn = QPushButton("2")
        third_btn = QPushButton("3")

        first_btn.setMinimumHeight(80)
        second_btn.setMinimumHeight(80)
        third_btn.setMinimumHeight(80)
        first_btn.setMaximumWidth(80)
        second_btn.setMaximumWidth(80)
        third_btn.setMaximumWidth(80)

        first_btn.clicked.connect(self.buttonclicked) # buttonclicked 함수에 버튼을 연결
        second_btn.clicked.connect(self.buttonclicked)
        third_btn.clicked.connect(self.buttonclicked)
        
        buttonLayout = QGridLayout()
        buttonLayout.addWidget(first_btn, 0, 0)
        buttonLayout.addWidget(second_btn, 0, 1)
        buttonLayout.addWidget(third_btn , 0, 2)

        self.nameEdit = QLineEdit("Guest")
        self.difficultyBox = QComboBox()
        self.modeBox = QComboBox()
        self.roundEdit = QLineEdit("5")
        startButton = QPushButton("Game Start")
        scoreButton = QPushButton("Show Score")
        
        startButton.setMinimumHeight(120)
        scoreButton.setMinimumHeight(120)

        self.difficultyBox.addItem("Easy Mode")
        self.difficultyBox.addItem("Normal Mode")
        self.difficultyBox.addItem("Hard Mode")

        self.modeBox.addItem("+")
        self.modeBox.addItem("-")
        self.modeBox.addItem("*")
        self.modeBox.addItem("/")

        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("이름"))
        hbox1.addWidget(self.nameEdit)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("난이도 "))
        hbox2.addWidget(self.difficultyBox)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(QLabel("연산 모드"))
        hbox3.addWidget(self.modeBox)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(QLabel("라운드 수"))
        hbox4.addWidget(self.roundEdit)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addWidget(startButton)
        vbox.addWidget(scoreButton)


        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(problemLayout, 0, 0)
        mainLayout.addLayout(buttonLayout, 1, 0)
        mainLayout.addLayout(vbox, 0, 1, 2, 3)
        
        startButton.clicked.connect(self.startGame) # 각 버튼을 맞는 함수에 연결
        scoreButton.clicked.connect(self.showScore)
        
        self.setLayout(mainLayout)
        self.show()
        self.setWindowTitle("ArithmeticGame")
        
    def startGame(self): # 게임 시작 버튼이 눌리면 실행
        self.name = self.nameEdit.text()
        self.operator = self.modeBox.currentText()
        self.setDifficulty() # 난이도는 따로 함수를 구현
        self.record = [] # 문제 풀이 결과를 기록하는 리스트
        try:
            self.round = int(self.roundEdit.text()) # 게임을 총 몇 판 진행할 것인지 설정
        except:
            self.problemWindow.setText("진행할 라운드를 정수로 입력하세요.")
            return
        self.playGame() # 본격적인 게임 시작
        
    def playGame(self):
        self.round -= 1 # 라운드 변수를 줄여가며 0이 될때까지 게임을 반복
        self.correctAnswer = self.calculation() # 문제의 정답을 변수에 저장
        
                    
    def calculation(self):
        first_num = random.randrange(1, 10*self.coefficient)
        if (self.operator == "+" or self.operator =="-"): # 덧셈과 뺄셈은 첫번째 수, 두번째 수 모두 자릿수가 같음
            second_num = random.randrange(1, 10*self.coefficient) # 난이도의 결과로 얻어지는 계수를 곱해 난수를 생성
        else:                                             # 곱셈과 나눗셈은 두번재 수의 자릿수가 더 낮음
            second_num = random.randrange(1, 10 if (self.difficulty == "Easy Mode" or self.difficulty == "Normal Mode")else 100)
        correct_answer = eval(f'{first_num} {self.operator} {second_num}') # eval()을 이용해 정답을 계산
        choiceList = ruleSelect(correct_answer) # 선지를 제시하는 로직을 따로 구현하여 호출
        random.shuffle(choiceList) # 로직을 선택하여 선지를 뽑아내고, 다시 한 번 섞어서 보여줌
        self.problemWindow.setText(f"{first_num} {self.operator} {second_num} = ?\n(1) : {choiceList[0]}\n(2) : {choiceList[1]}\n(3) : {choiceList[2]}")
        return choiceList.index(correct_answer) + 1 # 정답과 맞는 번호를 리턴
        
    def setDifficulty(self): # 난이도에 따라 계수를 결정하고, caculation 함수에서 사용한다.
        self.difficulty = self.difficultyBox.currentText()
        if self.difficulty == "Easy Mode":
            self.coefficient = 1 # 첫번째 수와 두번째 수의 자릿수를 계수를 곱해서 결정한다.
        elif self.difficulty == "Normal Mode":
            self.coefficient = 10
        else:
            self.coefficient = 100

    def buttonclicked(self):
        try:
            if self.round == -1: # 정한 라운드 수만큼 게임을 진행하면 더이상 진행되지 않는다.
                return
            sender = self.sender()
            userChoice = int(sender.text())
            if self.correctAnswer == userChoice: # 정답과 사용자의 선택이 일치할 때
                self.record.append(True) # 결과를 기록
            else:
                self.record.append(False)
            if self.round != 0: # 라운드 수가 남아있다면 게임을 계속 진행한다.
                self.playGame()
            else:
                self.round = -1 # 라운드 수가 남아있지 않다면 남은 라운드를 -1로 고정한다.
                result = "" # 결과를 출력할 문자열 선언
                o = "O"
                x = "X"
                for i in range(len(self.record)):
                    result += f"{i + 1} : {o if self.record[i] else x} " # 기록을 토대로 점수를 출력
                self.problemWindow.setText(result)
                if self.name != "Guest": # default user인 Guest면 점수를 기록하지 않는다.
                    scdb = readScoreDB() # 나머지 user들은 scoreDB에 기록을 저장한다. 점수는 산술평균을 이용한다.
                    recordScoreDB(scdb, self.name, round((sum(self.record)/int(self.roundEdit.text()))*100, 1), self.difficulty, self.operator)
                    writeScoreDB(scdb)
        except:
            pass
        
    def showScore(self): # 사용자의 채점 기록을 보여준다.
        self.name = self.nameEdit.text()
        self.mode = self.modeBox.currentText()
        self.difficulty = self.difficultyBox.currentText()
        result = "" # 결과를 출력할 문자열 선언
        scdb = readScoreDB() # dictionary 형태의 score database를 불러온다.
        try:
            if self.name == "Guest": # default user인 Guest면 점수를 보여주지 않는다.
                self.problemWindow.setText("Guest is not available.")
                return
            if self.name not in scdb:
                self.problemWindow.setText("Unregistered name.")
                return
            if self.mode not in scdb[self.name]:
                self.problemWindow.setText("You've never played this mode.")
                return
            if self.difficulty not in scdb[self.name][self.mode]:
                self.problemWindow.setText("You've never played this difficulty.")
                return
            scdb = scdb[self.name][self.mode][self.difficulty] # database에서 선택한 이름, 모드, 난이도의 점수를 불러온다.
            if len(scdb) > 10: # 기록이 10개가 넘는다면 최근 10개를 불러온다.
                scdb = scdb[len(scdb) - 10 :]
            for i in range(len(scdb)):
                result += f"{i + 1} : {scdb[i]}  " # 결과 출력
                if ((i + 1) % 3) == 0:
                    result +="\n"
            self.problemWindow.setText(result)
        except:
            pass



if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    game = ArithmeticGame()
    game.show()
    sys.exit(app.exec_())