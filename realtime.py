import time

from attendance import Attendance

OUTPUT_FILE = '~ehudtami/html/time_series.csv'
HEADER_STR = 'Date,Attendance\n'
MINUTE = 60
WAIT_INTERVAL = 5 * MINUTE

def parse_result(result):
	timestamp = result['timestamp']
	count = sum(1 for member in result['dictionary'] if
					result['dictionary'][member])
	return timestamp, str(count)

def append_to_file(filename, s, header=HEADER_STR):
	with open(filename, 'a') as outfile:
		if outfile.tell() == 0:
			outfile.write(header)
		outfile.write(s)

def main():
	att = Attendance()
	while True:
		result = att.get_attendance()
		timestamp, count = parse_result(result)
		append_to_file(OUTPUT_FILE, ','.join([timestamp, count]) + '\n')
		time.sleep(WAIT_INTERVAL)

if __name__ == '__main__':
	main()