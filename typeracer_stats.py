from datetime import datetime
import requests
import matplotlib.pyplot as plt
import numpy as np


ALL_RACES = -1

class Race:
	def __init__(self, wpm, timestamp):
		self.wpm = wpm;
		self.date = datetime.fromtimestamp(timestamp)


def prompt_username():
	username = ''

	while len(username.strip()) == 0:
		username = input('Username: ')

		if len(username.strip()) == 0:
			print('A non-empty username is required!')

	return username

def prompt_number_of_races():
	n = 20

	answer = input(f'Number of races (default is {n}, \'A\' for all races): ')

	if answer == 'A':
		return ALL_RACES

	try:
		answer_int = int(answer)
		return answer_int
	except:
		return n

def get_races_from_json(races_json):
	return list(map(lambda race : Race(race['wpm'], race['t']), races_json))
	
def plot_races(races):
	# x_vals = np.array(list(map(lambda r: r.date, races)))
	x_vals = np.arange(len(races))
	y_vals = np.array(list(map(lambda r: r.wpm, races)))

	plt.figure('WPM over races')
	plt.title('WPM over races')
	plt.grid(axis='y', color='green', linestyle='--')
	plt.ylabel('WPM')
	plt.xlabel('Race no.')

	plt.plot(x_vals, y_vals)
	plt.show()

def plot_wpm_distribution(races):
	plt.figure('WPM distribution')
	plt.title('WPM distribution')
	plt.hist(list(map(lambda r: r.wpm, races)))
	plt.show()

def get_races(username, number_of_races):
	request_url = f'https://data.typeracer.com/games?playerId=tr:{username}&universe=play'
	if number_of_races == ALL_RACES:
		request_url += f'&startDate={datetime(2000,1,1).timestamp()}'
	else:
		request_url += f'&n={number_of_races}'

	response = requests.get(request_url)

	if response.ok:
		return get_races_from_json(response.json())

	else:
		print(f'Error getting races for {username}')


if __name__ == '__main__':
	username = prompt_username()
	number_of_races = prompt_number_of_races()

	races = get_races(username, number_of_races)
	plot_races(races[::-1])
	plot_wpm_distribution(races)