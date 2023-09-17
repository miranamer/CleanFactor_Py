# make it so that only funcs outside a func are checked, not nested: (2 spaces indent)
def FindDirectReferences(referenceTo: str, lines: list) -> list: # enter the func you want to refactor
  refs = []
  for line in lines:
    ptr = 0
    while ptr < len(line):
      stringIndex = 0
      found = True
      if line[ptr] == referenceTo[stringIndex]:
        while ptr < len(line) and stringIndex < len(referenceTo):
          if line[ptr] == referenceTo[stringIndex]:
            stringIndex += 1
          else:
            found = False
            break
          ptr += 1

        if stringIndex == len(referenceTo) and line[ptr] == '(' and line.find('def') == -1 and found:
          refs.append(line)

      ptr += 1
  return refs



def FindSourceFuncFromReference(referenceFunc: str, lines: list) -> list:
  currDef = 0
  allSources = []
  for ind, line in enumerate(lines):
    if len(line) >= 4:
      if line[:4] == 'def ':
        currDef = ind
    if line == referenceFunc:
      #allSources.append(stack[0]) appending actual def func line
      allSources.append(currDef)
  return ["Empty :("] if not allSources else allSources



def ExtractFunctionNameFromSourceLine(sourceLine: str) -> str: # Not Needed
  def_ind = sourceLine.find('def ')
  new_ind = def_ind + 4
  return sourceLine[new_ind:sourceLine.index('(')]




def FindFuncDefFromSourceLineIndex(sourceLineIndex: int, lines: list) -> list:
  ptr = sourceLineIndex + 1
  finalInd = 0
  while ptr < len(lines):
    line = lines[ptr]
    if len(line) >= 4:
      if line[:4] == 'def ':
        finalInd = ptr
        return lines[sourceLineIndex:finalInd]
    ptr += 1
  return lines[sourceLineIndex:]



def GetAllFuncNames(allFuncNames: list, allFuncIndices: list, lines: list) -> None:
  for ind, line in enumerate(lines):
    if len(line) >= 4:
      if line[:4] == 'def ':
        funcDef = line[4:]
        funcRange = funcDef.find('(')
        allFuncNames.add(funcDef[:funcRange+1])
        allFuncIndices.append((funcDef[:funcRange+1], ind))



def FindAnyFuncsUsed(functionCodeBlock: list, allFuncIndices: list) -> list:
  indirectRefs = []
  for func in functionCodeBlock:
    for ind, line in enumerate(func):
      for funcName, funcInd in allFuncIndices:
        if line.find(funcName) != -1:
          indirectRefs.append([funcInd, funcName, line])
  return indirectRefs



def GetType2Dependencies(sourceRef: str, cached: set, allFuncsUsed: list, res: list, lines: list) -> None:
  fRefs = FindDirectReferences(sourceRef, lines)
  if not fRefs:
    return

  for i in fRefs:
    if i not in cached:
      sourceFuncs = FindSourceFuncFromReference(i, lines)
      for source in sourceFuncs:
        res.append(FindFuncDefFromSourceLineIndex(source, lines))
        funcNameUsed = ExtractFunctionNameFromSourceLine(FindFuncDefFromSourceLineIndex(source, lines)[0])
        allFuncsUsed.append(funcNameUsed)
        GetType2Dependencies(funcNameUsed, cached, allFuncsUsed, res, lines)
      cached.add(i)




def GetType1Dependencies(sourceRef: str, allFuncNames: list, allFuncsUsed: list, allFuncIndices: list, res: list, lines: list) -> None:
  #sourceCodeToStr = ''.join(sourceRef)
  for line in sourceRef:
    for func in allFuncNames:
      if line.find(func) != -1 and func[:-1] not in allFuncsUsed:
        allFuncsUsed.append(func[:-1])
        funcDefIndex = [i[1] for i in allFuncIndices if i[0] == func][0]
        funcDef = FindFuncDefFromSourceLineIndex(funcDefIndex, lines)
        res.append(funcDef)