import json


def main():
	with open('grades.json') as f:
		grades = json.load(f)
		for grade in grades:
			if grade["class_id"] == 28:
				print (grade["scores"])

if __name__ == "__main__":
	main()
