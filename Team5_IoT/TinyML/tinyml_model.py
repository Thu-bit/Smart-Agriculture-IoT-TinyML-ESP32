def predict(temperature, humidity, soil):
    if soil <= 24.50:
        if soil <= 23.50:
            if humidity <= 68.50:
                if humidity <= 54.50:
                    return 1
                else:
                    return 1
            else:
                return 1
        else:
            if humidity <= 82.50:
                return 1
            else:
                return 0
    else:
        if humidity <= 49.50:
            if temperature <= 32.50:
                if soil <= 34.50:
                    return 1
                else:
                    return 0
            else:
                if soil <= 26.00:
                    return 1
                else:
                    return 1
        else:
            if soil <= 33.50:
                if temperature <= 32.50:
                    return 0
                else:
                    return 1
            else:
                if soil <= 74.50:
                    return 0
                else:
                    return 0
