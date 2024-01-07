import matplotlib.pyplot as plt
import numpy as np

# 定义对数函数
def q_function1(vol):
    # return -23.65060754864053*((x+508.2130392724084)**0.8433764630986903) + 7.257078620637543 * (x+407.86870598508153) + 1585.6201108739122
    # return -58.863374003875954 *((x+12.41481943150274 )**0.9973316187745871 ) +57.92341268595151 * (x+ 13.391132186222036) +  -32.92986286030519
    return  -8.081720684086314 * np.log( vol + 14.579508825070013,)+ 37.65806375944386 
    
    
def q_function2(vol):
    return 0.2721359356095803 * ((vol + 2592.272889454798) ** 1.358571233418649) + -6.313841334963396 * (vol + 2592.272889454798) + 4558.496367823575

# 生成 x 值
x_values = np.linspace(0, 128, 1000)


x_data = np.array([0,16,32,48,64,80,96,112,128])
y_data = np.array([16, 10, 6.75, 4, 2.5, 1.6, 0.8, 0.3, 0])


print(q_function1(x_data))
print(q_function2(x_data))

# 绘制图像
plt.plot(x_values, q_function1(x_values,),label = "fit1")
plt.plot(x_values, q_function2(x_values,),label = "fit2")
plt.scatter(x_data, y_data, color='red')  # 标记给定的点
# plt.scatter(x_data, y_data2, color='green')  # 标记给定的点
# plt.scatter(x_data, y_data3, color='blue')  # 标记给定的点
plt.xlabel('x')
plt.ylabel('y')
plt.title('Function')
plt.legend()
plt.grid(True)
plt.show()
