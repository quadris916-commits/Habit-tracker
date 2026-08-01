# Habit Tracker

A simple and clean Python Tkinter application for tracking daily habits, logging progress, and archiving completed habits.

## Features

- Add new habits.
- Set a target count and unit.
- Log daily progress.
- View saved logs.
- Archive habits you no longer want to track.
- Data is saved locally in a JSON file.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)

## How to Run

1. Save the code in a file named `habit_tracker.py`
2. Open terminal in the project folder
3. Run:

```bash
python habit_tracker.py
```

## How to Use

1. Enter a habit name.
2. Set the target count and unit.
3. Click **Add Habit**.
4. Select a habit from the dropdown.
5. Enter a date and count.
6. Click **Save Log**.
7. Use **Archive Selected Habit** to hide habits you no longer want.

## Data Storage

The app stores data in:

- `habit_data.json`

This file is created automatically in the same folder as the program.

## Example Habits

- Study for 2 hours
- Drink 8 glasses of water
- Code for 1 hour
- Read 20 pages
- Workout 1 time

## Notes

- Dates should be entered in `YYYY-MM-DD` format.
- Archived habits are hidden from the active list but still kept in the data file.
- If the JSON file gets corrupted, the app will start with a fresh empty dataset.
