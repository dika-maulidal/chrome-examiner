## About
Windows Chrome Browser Forensics is a tool for extracting and analyzing browsing data from the Google Chrome browser on Windows. It provides access to user information such as saved passwords, search history, and frequently visited sites to assist in digital forensics.

## Features
- Extract saved passwords and emails from Chrome. 
- Retrieve top searched keywords and browsing history.
- Present data in a user-friendly format.

## Usage Instructions
```bash
$ git clone https://github.com/dika-maulidal/chrome-examiner.git
$ cd chrome-examiner
$ pip install -r requirements.txt
$ python main.py
```

## Screenshot
![chrom-examiner](https://github.com/user-attachments/assets/c3957709-7ab2-4541-9148-98f23074de74)

## Example of extracted data interface
![bookmark](https://github.com/user-attachments/assets/f282aae6-18a5-4ef4-97a9-c0848a528492)

## Data Sources
To access the relevant data for analysis, navigate to the following paths on your Windows machine:

| Content         | Path                                             |
| -------------- | ------------------------------------------------------- |
| Saved Password  | C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Default\Login Data |
| Bookmarks | C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Default\Bookmarks |
| History | C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Default\History |
| Top Sites  | C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Default\Top Sites |
| Keyword | C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Default\History |
| Top Keyword	 | C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Default\History |
| Emails   | C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Default\Login data & Preferences |
| Favicon   | C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Default\Favicons |
| Google Account   | C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Default\Preferences |
