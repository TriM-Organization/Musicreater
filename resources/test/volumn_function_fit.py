import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def q_function1(x, a, a2, c1,):
    return a * np.log( x + a2,)+ c1

def q_function2(x, b, b2, b3, b4, c2):
    return b * ((x + b2) ** b3) + b4 * (x+b2) + c2


x_data = np.array([0, 16, 32, 48, 64, 80, 96, 112, 128])
y_data = np.array([16, 10, 6.75, 4, 2.5, 1.6, 0.8, 0.3, 0])


p_est1, err_est1 = curve_fit(q_function1, x_data[:5], y_data[:5], maxfev=1000000)
p_est2, err_est2 = curve_fit(q_function2, x_data[4:], y_data[4:], maxfev=1000000)


print(q_function1(x_data[:5], *p_est1))
print(q_function2(x_data[4:], *p_est2))

print("参数一：",*p_est1)
print("参数二：",*p_est2)

# 绘制图像
plt.plot(
    np.arange(0, 64.1, 0.1), q_function1(np.arange(0, 64.1, 0.1), *p_est1), label=r"FIT1"
)
plt.plot(
    np.arange(64, 128.1, 0.1), q_function2(np.arange(64, 128.1, 0.1), *p_est2), label=r"FIT2"
)


plt.scatter(x_data, y_data, color="red")  # 标记给定的点
# plt.xlabel('x')
# plt.ylabel('y')
plt.title("Function Fit")
plt.legend()
# plt.grid(True)
plt.show()
