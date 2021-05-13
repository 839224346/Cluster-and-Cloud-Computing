import time


current_time = time.localtime()

today = time.strftime('%Y-%-m-%-d', current_time)

file_name = today +str(current_time) + ".txt"

output = open(file_name, "w")

output.write(str(today))

print("OK DONE!")

