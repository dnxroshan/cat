
from table_question_bank import TableQuestionBank
from table_tests import TableTests
from constants import Difficulty, Options

class TestEngine:

    def __init__(self, state):
        self.question_bank = TableQuestionBank()
        self.tests = TableTests()
        self.state = state

    def __save_state(self):
        self.state['test_id'] = self.test_id
        self.state['question_id'] = self.question_id
        self.state['question_no'] = self.question_no
        self.state['score'] = self.score
        self.state['difficulty'] = self.difficulty

    def __get_state(self):
        self.test_id = self.state['test_id']
        self.question_id = self.state['question_id']
        self.question_no = self.state['question_no']
        self.score = self.state['score']
        self.difficulty = self.state['difficulty']

    def start(self, test_id):
        self.test_id = test_id
        self.question_id = 0
        self.question_no = 0
        self.score = 0
        self.difficulty = Difficulty.Medium

        self.__save_state()

    def question(self):
        self.__get_state()

        self.question_no = self.question_no + 1
        new_question = self.question_bank.get_random_question(self.test_id, self.difficulty)
        self.question_id = new_question[0]

        self.__save_state()

        return new_question


    def update(self, answer):
        
        self.__get_state()

        result = answer == self.question_bank.get_answer(self.question_id)
        self.__update_score(result)
        self.__update_difficulty(result)

        self.__save_state()

        score_threshold = self.tests.get_threshold_score(self.test_id)

        if self.score < score_threshold:
            return 1
        else:
             return 0



    def __update_difficulty(self, result):

        if result and self.difficulty == Difficulty.Easy:
            new_difficulty = Difficulty.Medium
        elif not result and self.difficulty == Difficulty.Easy:
            new_difficulty = Difficulty.Easy
        elif result and self.difficulty == Difficulty.Medium:
            new_difficulty = Difficulty.Hard
        elif not result and self.difficulty == Difficulty.Medium:
            new_difficulty = Difficulty.Easy
        elif result and self.difficulty == Difficulty.Hard:
            new_difficulty = Difficulty.Hard
        elif not result and self.difficulty == Difficulty.Hard:
            new_difficulty = Difficulty.Medium

        self.difficulty = new_difficulty

    def __update_score(self, result):
        increment = 0

        scores = self.tests.get_scores(self.test_id)

        if result:
            if self.difficulty == Difficulty.Easy: 
                increment = scores['score_easy']
            elif self.difficulty == Difficulty.Medium: 
                increment = scores['score_medium']
            elif self.difficulty == Difficulty.Hard: 
                increment = scores['score_hard']

        self.score = self.score + increment

