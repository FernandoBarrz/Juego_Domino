
# Revisa si este patron de fichas es valido para ganar
def patron_win(func_snake):
    if func_snake[0][0] == func_snake[-1][-1] and sum(x.count(func_snake[0][0]) for x in func_snake) == 8:
        return True