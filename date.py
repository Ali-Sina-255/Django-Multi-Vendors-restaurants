from datetime import time
# for h in range(0,24):
#     for m in range(0,30,29):
#         print(time(h,m).strftime('%I :%M %p'))

time = [(time(h,m).strftime('%I :%M %p'),time(h,m).strftime('%I:%M %p')) for h in range(0, 24) for m in range(0,31, 30)]

print(time)