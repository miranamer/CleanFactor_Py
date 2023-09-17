from functions import FindDirectReferences, FindSourceFuncFromReference, FindFuncDefFromSourceLineIndex, ExtractFunctionNameFromSourceLine, GetAllFuncNames, FindAnyFuncsUsed
from functions import GetType2Dependencies, GetType1Dependencies

def main() -> str:
    lines = []

    with open("code.txt") as file:
        for line in file:
            lines.append(line)

    lines[-1] += '\n \n'

    funcNameToRefactor = input('Enter Func Name To Refactor: ')

    fRefs = FindDirectReferences(funcNameToRefactor, lines)
    cached = set()

    allFuncsThatDirectlyRefF = []
    allFuncNamesUsed = [] # currently directly referenced func names

    for i in fRefs:
        if i not in cached:
            sourceFuncs = FindSourceFuncFromReference(i, lines)
            for source in sourceFuncs:
                allFuncsThatDirectlyRefF.append(FindFuncDefFromSourceLineIndex(source, lines))
                funcNameUsed = ExtractFunctionNameFromSourceLine(FindFuncDefFromSourceLineIndex(source, lines)[0])
                allFuncNamesUsed.append(funcNameUsed)
                cached.add(i)

    allFuncNames = set()
    allFuncIndices = []

    GetAllFuncNames(allFuncNames, allFuncIndices, lines)

    valid_name = False
    for i in allFuncNames:
        if i[:-1] == funcNameToRefactor:
            valid_name = True

    if not valid_name:
        print('Invalid Function Name!')
        print('Try One From The Following:')
        for i in allFuncNames:
            print('->', i[:-1])
        return

    FindAnyFuncsUsed(allFuncsThatDirectlyRefF, allFuncIndices)


    accFuncToBeRefactored = FindFuncDefFromSourceLineIndex([i[1] for i in allFuncIndices if i[0] == f'{funcNameToRefactor}('][0], lines)
    res = [accFuncToBeRefactored]
    allFuncsUsed = [funcNameToRefactor]
    cached = set()

    GetType2Dependencies(funcNameToRefactor, cached, allFuncsUsed, res, lines)

    for i in res:
        GetType1Dependencies(i, allFuncNames, allFuncsUsed, allFuncIndices, res, lines)


    new_res = []
    for i in res:
        for j in i:
            new_res.append(j)

    allNecessaryCode = ''.join(new_res)

    file2 = open("sandbox.txt","w")
    file2.truncate(0) #?clear the file
    file2.write(allNecessaryCode)
    file2.close()

    return allNecessaryCode

if __name__ == "__main__":
    main()