# Redirects Relational Map

This project logs URL redirects and visualizes them as a relational map using `networkx` and `matplotlib`.

## Prerequisites

- Python 3.x
- `pip` (Python package installer)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/FinnaCloud/redirects-relational-map.git
    cd redirects-relational-map
    ```

2. Create a virtual environment (optional but recommended):
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the `main.py` script to log URL redirects and save the data to `redirects_map.json`:
    ```sh
    python main.py
    ```

2. Enter the URL to check for redirects when prompted.

3. Run the `view.py` script to visualize the redirects relational map:
    ```sh
    python view.py
    ```

## Project Structure

- `main.py`: Logs URL redirects and saves the data to `redirects_map.json`.
- `view.py`: Visualizes the redirects relational map using `networkx` and `matplotlib`.

## Dependencies

- `requests`: For making HTTP requests.
- `python-whois`: For performing WHOIS lookups.
- `dnspython`: For DNS resolution.
- `networkx`: For creating and manipulating complex networks.
- `matplotlib`: For plotting graphs.

## License

This project is licensed under the MIT License.