with open('War and Peace_Book One.txt', mode='r') as reader:
        lineCounter = 0
        letter = ['a','b','c','d','e','f','g']

        for line in reader:
            if 'CHAPTER ' in line:
                lineCounter += 1
            print(int(lineCounter/10))
            with open('./CHAPTERS/Charpter ' +letter[int(lineCounter/10)]+str(lineCounter)+ '.txt', encoding='utf-8', mode='a') as writer:
                writer.write(line)

