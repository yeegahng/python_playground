import random
import os
from datetime import datetime


def input_number_count():
    while True:
        numCount = input("게임 숫자 길이를 결정하세요: ")
        if numCount.isdigit() and len(numCount) >= 1:
            return numCount
        else:
            print(numCount, "는 유효한 값이 아닙니다. 재시도 하세요.")


def get_target_numbers(numCount, hide):
    targetDigitList = []
    while len(targetDigitList) < numCount:
        newNum = str(random.randrange(0, 9, 1))
        if targetDigitList.__contains__(newNum) is False:
            targetDigitList += [newNum]
            if hide is False:
                print("새로운 목표숫자: ", str(newNum), ", len = ", str(len(targetDigitList)))
        else:
            if hide is False:
                print(str(newNum), "는 이미 존재하는 숫자입니다. 재선택합니다.")

    if hide is False:
        print("목표 숫자열:", str(targetDigitList))
    return targetDigitList


def input_pitching_numbers(numCount): #한자리씩 입력
    inputDigitList = []
    inputDigit = ''
    while len(inputDigitList) < numCount:
        inputDigit = input(str(len(inputDigitList) + 1) + "번째 숫자를 입력하세요: ")
        quit_game_if_requested(inputDigit)
        if inputDigit.isdecimal() and len(inputDigit) == 1:
            if inputDigitList.__contains__(int(inputDigit)) is False:
                inputDigitList += [int(inputDigit)]
                # print("new input number =", inputDigit, ", len = ", str(inputDigitList.__len__()))
            else:
                print(inputDigit, "는 이미 입력한 숫자입니다. 다시 입력하세요.")
                continue
        else:
            print(inputDigit, "는 한 자리 숫자가 아닙니다. 다시 입력하세요.")
            continue

    # print("입력결과:", str(inputDigitList))
    return inputDigitList


def input_pitching_number_set(numCount): #숫자열로 입력
    #inputDigitList = []
    while True:
        inputNumber = input(str(numCount) + "자리 숫자를 입력하세요: ")
        quit_game_if_requested(inputNumber)
        if len(inputNumber) is not numCount:
            print(inputNumber, "는 " + str(numCount) +"자리 숫자가 아닙니다. 다시 입력하세요.")
            continue
        if inputNumber.isdecimal() is not True:
            print(inputNumber, "는 숫자열이 아닙니다. 다시 입력하세요.")
            continue
        if len(set(inputNumber)) is not numCount:
            print(inputNumber, '에 중복 숫자가 포함되어 있습니다. 다시 입력하세요.')
            continue
        inputDigitList = list(inputNumber)
        break

    return inputDigitList


def score_inning(targetNumbers, pitchNumbers):
    strikes = 0
    balls = 0
    i = 0
    for i in range(0, numCount):
        if targetNumbers[i] == pitchNumbers[i]:
            strikes += 1
        else:
            if targetNumbers.__contains__(pitchNumbers[i]):
                balls += 1
    return strikes, balls


def quit_game_if_requested(key):
    if key is 'q' or key is 'Q':
        print("<게임 종료> 즐거웠길 바랍니다.")
        exit(0)


def playball(numCount, targetNumbers):
    inningRecord = []
    while True:
        inning = len(inningRecord) + 1
        print("<" + str(inning) + "번째 공격>")
        # pitchNumbers = input_pitching_numbers(numCount)
        pitchNumbers = input_pitching_number_set(numCount)
        strikes, balls = score_inning(targetNumbers, pitchNumbers)
        print("<" + str(inning) + "번째 공격 결과>: "
              + str(pitchNumbers) + " --> " + str(strikes) + " strikes, " + str(balls) + " balls")
        inningRecord += [str(inning) + ": " + str(pitchNumbers) + " --> " + str(strikes) + "S " + str(balls) + "B"]
        if strikes == numCount:
            print("성공!! 찾던 숫자는 " + str(pitchNumbers) + " 입니다.")
            return inning
        else:
            for record in inningRecord:
                print(record)
        print("\n")


def get_record_filepath(filename):
    dirPath = os.getcwd() + "/baseballgame/"
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    return dirPath + filename

########
# Game Play Record
########
def update_game_play_record(playerName, inningScore):
    filePath = get_record_filepath("game_play_record.txt")
    gamePlayRecordList = load_file_to_list(filePath)
    gamePlayRecordList.append((str(datetime.now().date())+"-"+str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second), playerName, inningScore))
    save_list_to_file(gamePlayRecordList, filePath)
    print_record(gamePlayRecordList, "번호\t날짜\t이름\t공격횟수")


########
# Top Score Record Management
########
def update_top_score_record(playerName, inningScore):
    filePath = get_record_filepath("top_score_record.txt")
    topScoreRecordList = load_file_to_list(filePath)

    newRank = 0
    if len(topScoreRecordList) == 0:
        topScoreRecordList.insert(0, (playerName, inningScore, (str(datetime.now().date())+"-"+str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second))))
    else:
        for playerRecord, inningRecord, timeRecord in topScoreRecordList:
            if inningScore < int(inningRecord):
                topScoreRecordList.insert(newRank, (playerName, inningScore, (str(datetime.now().date())+"-"+str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second))))
                break
            else:
                newRank += 1
                if newRank == len(topScoreRecordList):
                    topScoreRecordList.insert(newRank, (playerName, inningScore, (str(datetime.now().date())+"-"+str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second))))
                    break

    if newRank <= 10:
        if newRank is 0: #new ranker at top
            print("축하합니다! 신기록입니다!!")
        else:
            print("축하합니다! " + str(newRank) + "위에 올랐습니다!!")
        save_list_to_file(topScoreRecordList, filePath)

    print_record(topScoreRecordList, "순위\t이름\t공격횟수\t기록일")
    return


def load_file_to_list(filename):
    recordList = []
    if not os.path.exists(filename):
        print("<< 첫 게임이시군요. >>")
    else:
        print("<< 기존 기록을 읽어들입니다. >>")
        fp = open(filename, "r")
        if fp is not None:
            for line in fp.readlines():
                recordList.append(line.split())
            if len(recordList) > 0:
                print("<< " + filename + " : Loading " + str(len(recordList)) + " items completed >>")
            else:
                print("<< " + filename + " : No Record >>")
            fp.close()
        else:
            print("<< 파일 읽기 실패: 프로그램 개발자에게 문의하세요. >>")
    return recordList


def save_list_to_file(recordList, filename):
    if not os.path.exists(filename):
        print("<< " + filename + " : 신규 생성 >>")
    else:
        print("<< " + filename + " : 내용 갱신 저장>>")
    fp = open(filename, "w")
    if fp is not None:
        for record in recordList:
            recordString = ""
            for field in record:
                recordString += str(field) + '\t'
            fp.writelines(recordString + '\n')
        fp.close()
    else:
        print("<< 파일 쓰기 실패: 프로그램 개발자에게 문의하세요. >>")


def print_record(recordList, header):
    print("-----------------------------------------")
    print(header)
    print("-----------------------------------------")
    index = 1
    recordLine = ""
    if len(recordList) > 0:
        for record in recordList:
            recordLine += str(index) + '\t'
            for field in record:  # display device info in value field
                recordLine += str(field) + '\t'
            print(recordLine + '\n')
            recordLine = ""
            index += 1
        print('')
    else:
        print("NO RECORD")
    return


########
# Main Routine
########
print("************ 야구 게임을 해봅시다!! ************")
print("(q를 입력하면 언제든 게임 종료됩니다.)\n")
playerName = input("이름을 입력하세요: ")
# numCount = input_number_count()
numCount = 3
hideTarget = True

while True:
    targetNumbers = get_target_numbers(numCount, hideTarget)

    inningScore = playball(numCount, targetNumbers)
    update_game_play_record(playerName, inningScore)
    update_top_score_record(playerName, inningScore)
    playAgain = input("다시 한번 게임 하시겠습니까?(y/n): ")
    if playAgain is 'n' or playAgain is 'N':
        print("아쉽지만 오늘은 이만~!")
        quit_game_if_requested('q')
    else:
        if playAgain is not 'y' and playAgain is not 'Y':
            print("입력이 잘못되었지만 안 한다고 하지 않았으니 다시 하는 걸로 간주하겠습니다. 게임 시작!")
        else:
            print("게임 시작!")


