from time import sleep
import pigpio
import time
import sys

#GPIO???
try:
    pi = pigpio.pi()
    if not pi.connected:
        print("pigpioデーモンに接続できません。")
        print("以下のコマンドでpigpioデーモンを起動してください：")
        print("sudo pigpiod")
        sys.exit(1)
    
    pi.set_mode(17, pigpio.OUTPUT)
    pi.set_mode(22, pigpio.OUTPUT)
    print("pigpioデーモンに正常に接続しました。")
    
except Exception as e:
    print(f"pigpioの初期化でエラーが発生しました: {e}")
    print("pigpioデーモンが起動しているか確認してください：")
    print("sudo pigpiod")
    sys.exit(1)

#PWM?????
pwm_pin1 = 18 #PWM??????
duty = 0 #????????%???
freq = 100 #PWM????Hz???
up_flag = True

#IN1?IN2?????
pi.write(17, 0)
pi.write(22, 1)

#???????
while True:
  
    #???????????
    cnv_dutycycle = int((duty * 1000000 / 100))
    #PWM???
    pi.hardware_PWM(pwm_pin1, freq, cnv_dutycycle)
    #duty???
    if up_flag == True:
        if duty == 100:
            up_flag = False
        else:
            duty += 1
    else:
        if duty == 0:
            up_flag = True
        else:
            duty -=1
    
    time.sleep(0.05)