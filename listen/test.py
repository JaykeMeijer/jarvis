hour = 6
minute = 28


if minute > 32:
    hour += 1
hour = hour % 12
if hour == 0:
    hour = 12

minute = (5 * round(minute/5)) % 60
if minute > 30:
    minute_s = 60 - minute
else:
    minute_s = minute

if minute == 0:
    s = f"It is {hour} 'o clock"
elif minute == 45:
    s = f"It is quarter to {hour}"
elif minute == 15:
    s = f"It is quarter past {hour}"
elif minute == 30:
    s = f"It is half past {hour}"
elif minute > 30:
    s = f"It is {minute_s} to {hour}"
else:
    s = f"It is {minute_s} past {hour}"

print(s)