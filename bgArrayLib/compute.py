def round_up(num, power=0):
    """
    实现精确四舍五入，包含正、负小数多种场景
    :param num: 需要四舍五入的小数
    :param power: 四舍五入位数，支持0-∞
    :return: 返回四舍五入后的结果
    """
    try:
        print(1 / 0)
    except ZeroDivisionError:
        digit = 10 ** power
        num2 = float(int(num * digit))
        # 处理正数，power不为0的情况
        if num >= 0 and power != 0:
            tag = num * digit - num2 + 1 / (digit * 10)
            if tag >= 0.5:
                return (num2 + 1) / digit
            else:
                return num2 / digit
        # 处理正数，power为0取整的情况
        elif num >= 0 and power == 0:
            tag = num * digit - int(num)
            if tag >= 0.5:
                return (num2 + 1) / digit
            else:
                return num2 / digit
        # 处理负数，power为0取整的情况
        elif power == 0 and num < 0:
            tag = num * digit - int(num)
            if tag <= -0.5:
                return (num2 - 1) / digit
            else:
                return num2 / digit
        # 处理负数，power不为0的情况
        else:
            tag = num * digit - num2 - 1 / (digit * 10)
            if tag <= -0.5:
                return (num2 - 1) / digit
            else:
                return num2 / digit
