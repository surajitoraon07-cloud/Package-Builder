PACKAGE BUILDER
===============
Makes a customer quotation from your saved trip-package HTML files.

WHAT YOU NEED
Python 3 (free, from python.org). Nothing else to install.

START
Windows  : double-click start.bat
Mac/Linux: open a terminal in this folder and run:  python3 server.py
The tool opens in your browser at http://127.0.0.1:8000
(To let other computers on your office Wi-Fi use it, run "python server.py lan"
 and open http://<this computer's IP>:8000 from the other computer.)

FIRST-TIME SETUP
1. In "Package library", choose a package HTML file made from your quotation
   template, type the destination name (e.g. Gangtok) and click "Save to library".
   Repeat for every destination. They are saved in the database file
   packages.db (created automatically next to server.py).
   Uploading the same destination again replaces it.
2. In "New quotation", fill in the customer details, tick one or more
   destinations (in travel order) and click "Generate quotation".
3. Check the preview. Use "Edit text" to fix anything by hand, then click
   "Print / Save as PDF" (choose Save as PDF, paper A4, margins None, and
   tick "Background graphics").

WHAT IT CHANGES
Customer name, phone, adults/children, trip type, travel date (optional),
total days / nights, the day-by-day plan (activities are spread over the new
number of days; arrival and departure days stay fixed), and the price if you
enter a total amount (30% advance / 70% balance are recalculated).
Everything else in your saved package stays exactly as it is.

MORE THAN ONE DESTINATION
Set the days for each destination. The first destination's departure day and the
next destination's arrival day become one "transfer" day, so
total days = sum of the destination days minus 1 for each hand-over.
Each destination needs at least 3 days.

GOOD TO KNOW
- Please review days the tool rewrites and the transfer day text.
- For Sharing / Solo / Strangers trips the vehicle wording becomes "Shared Cab";
  edit it in the preview if your wording differs.
- If you open index.html directly (without server.py) it still works, but
  packages are then saved only in that browser.
- Back up the file packages.db to keep your library safe. It is a standard
  SQLite database; you can open it with the free "DB Browser for SQLite".
- If you used the earlier version, your saved packages are imported into the
  database automatically the first time you start this one.
