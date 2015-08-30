import os
import sys

base_dir  = os.path.dirname(os.getcwd())
sys.path.append(base_dir)

from circprimer import app

if __name__ == '__main__':
	app.run(debug=True, port=8888)
