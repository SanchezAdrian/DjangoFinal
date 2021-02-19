def validateMatricula(matricula):
    print(matricula[:4].isalpha())
    print(matricula[4:7])
    if  matricula[:4].isalpha():
        if matricula[4:7].isnumeric():
            return True
        return False
    return False

print(validateMatricula('MBCV342'))