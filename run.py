import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app 

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
