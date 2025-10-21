from time import sleep
import RPi.GPIO as GPIO
import time
import sys

#GPIO???
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    print("GPIOが正常に初期化されました。")
    
except Exception as e:
    print(f"GPIOの初期化でエラーが発生しました: {e}")
    sys.exit(1)

#PWM?????
pwm_pin1 = 18 #PWM??????
duty = 0 #????????%???
freq = 100 #PWM????Hz???
up_flag = True

#IN1?IN2?????
GPIO.output(17, GPIO.LOW)
GPIO.output(22, GPIO.HIGH)

#PWM???
pwm = GPIO.PWM(pwm_pin1, freq)
pwm.start(duty)

#???????
try:
    while True:
        #PWM???
        pwm.ChangeDutyCycle(duty)
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

except KeyboardInterrupt:
    print("\nプログラムを終了します...")
    pwm.stop()
    GPIO.cleanup()