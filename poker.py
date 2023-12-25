import random


def poker():
    result = ''
    for i in range(5):
        dice = random.randint(1, 6)
        match dice:
            case 1:
                result += "1️⃣"
            case 2:
                result += "2️⃣"
            case 3:
                result += "3️⃣"
            case 4:
                result += "4️⃣"
            case 5:
                result += "5️⃣"
            case 6:
                result += "6️⃣"
    return result
