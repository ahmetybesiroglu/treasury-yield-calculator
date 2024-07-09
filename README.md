
# Treasury Yield Calculator

This project calculates the Treasury yields for specified tickers and dates, fetching data from Yahoo Finance.

## Features

- Fetch Treasury yields for specified tickers and dates.
- Interpolate missing yields for maturities not directly available.

## Prerequisites

Ensure you have Python installed (preferably version 3.6 or higher). You can download it from [python.org](https://www.python.org/).

## Setup

### Clone the Repository

```bash
git clone https://github.com/ahmetybesiroglu/treasury-yield-calculator.git
cd treasury-yield-calculator
```

### Create and Activate a Virtual Environment

It's a good practice to use a virtual environment to manage dependencies. You can create and activate a virtual environment with the following commands:

For Windows:
```bash
python3 -m venv env
env\Scripts\activate
```

For macOS and Linux:
```bash
python3 -m venv env
source env/bin/activate
```

### Install Dependencies

Install the required dependencies using the provided `requirements.txt` file:
```bash
pip3 install -r requirements.txt
```

## Configuration

### JSON Configuration File

Edit the `config/config.json` file to specify the tickers and dates. Here is an example of what the file looks like:

```json
{
  "tickers": {
    "1-year": "^IRX",
    "5-year": "^FVX",
    "10-year": "^TNX"
  },
  "dates": ["1/1/2020", "1/1/2021", "1/1/2022"]
}
```

## Running the Script

Run the script to fetch and interpolate Treasury yields:

```bash
python3 src/treasury_yield_calculator.py
```

## Expected Output

The script will fetch the yields and save the results in a CSV file located in the `output` directory.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## Contact

For further questions, please contact ahmetybesiroglu@gmail.com.
