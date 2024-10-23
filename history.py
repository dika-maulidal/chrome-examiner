import os
import sqlite3
import shutil
from datetime import datetime, timedelta

def get_last_5_history():
 db_path = os.path.join(
     os.environ['USERPROFILE'],
     'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History'
 )
 db_copy = os.path.join(os.environ['USERPROFILE'], 'History Copy')
 shutil.copyfile(db_path, db_copy)

 conn = sqlite3.connect(db_copy)
 cursor = conn.cursor()

 cursor.execute("""
     SELECT url, title, visit_count, last_visit_time 
     FROM urls 
     ORDER BY last_visit_time DESC 
     LIMIT 5
 """)
 history_entries = cursor.fetchall()

 formatted_history = []
 for row in history_entries:
     url = row[0]
     title = row[1]
     visit_count = row[2]
     last_visit_time = row[3]

     last_visit_time = datetime(1601, 1, 1) + timedelta(microseconds=last_visit_time)
     formatted_history.append({
         "Title": title,
         "URL": url,
         "Visit Count": visit_count,
         "Last Visited": last_visit_time.strftime('%Y-%m-%d %H:%M:%S')
     })

 cursor.close()
 conn.close()
 os.remove(db_copy)

 if formatted_history:
     print("\nLast 5 Browsing History Entries:")
     print("="*35)
     for i, entry in enumerate(formatted_history, start=1):
         print(f"\nEntry {i}:")
         print(f"Title       : {entry['Title']}")
         print(f"URL         : {entry['URL']}")
         print(f"Visit Count : {entry['Visit Count']}")
         print(f"Last Visited: {entry['Last Visited']}")
 else:
     print("No browsing history found.")

if __name__ == '__main__':
 get_last_5_history()
