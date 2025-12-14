"""
gradebook.py
Author:Yugal kishore      
Date: 23-11-2025           
Title: GradeBook Analyzer CLI
"""

import csv
import sys
from typing import Dict, List, Tuple

# ---------- Task 3: Statistical functions ----------
def calculate_average(marks: Dict[str, float]) -> float:
    if not marks:
        return 0.0
    total = sum(marks.values())
    return total / len(marks)

def calculate_median(marks: Dict[str, float]) -> float:
    if not marks:
        return 0.0
    vals = sorted(marks.values())
    n = len(vals)
    mid = n // 2
    if n % 2 == 1:
        return float(vals[mid])
    else:
        return (vals[mid - 1] + vals[mid]) / 2.0

def find_max_score(marks: Dict[str, float]) -> Tuple[str, float]:
    if not marks:
        return ("", 0.0)
    name = max(marks, key=lambda k: marks[k])
    return (name, marks[name])

def find_min_score(marks: Dict[str, float]) -> Tuple[str, float]:
    if not marks:
        return ("", 0.0)
    name = min(marks, key=lambda k: marks[k])
    return (name, marks[name])

# ---------- Task 4: Grade assignment ----------
def assign_grade(score: float) -> str:
    # A: 90+, B: 80–89, C: 70–79, D: 60–69, F: <60
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def build_grades_dict(marks: Dict[str, float]) -> Dict[str, str]:
    return {name: assign_grade(score) for name, score in marks.items()}

def grade_distribution(grades: Dict[str, str]) -> Dict[str, int]:
    dist = {"A":0, "B":0, "C":0, "D":0, "F":0}
    for g in grades.values():
        if g in dist:
            dist[g] += 1
        else:
            dist[g] = 1
    return dist

# ---------- Task 2: Input methods ----------
def load_csv(filepath: str) -> Dict[str, float]:
    marks = {}
    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row.get("Name") or row.get("name") or row.get("Student") or ""
                score = row.get("Marks") or row.get("marks") or row.get("Score") or ""
                name = name.strip()
                try:
                    score_val = float(score)
                except ValueError:
                    print(f"Warning: skipping {name} because marks '{score}' is not a number.")
                    continue
                marks[name] = score_val
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return marks

def manual_entry() -> Dict[str, float]:
    print("Enter student name and marks. Type ENTER on name to stop.")
    marks = {}
    while True:
        name = input("Student name (or press ENTER to finish): ").strip()
        if name == "":
            break
        raw = input(f"Marks for {name}: ").strip()
        try:
            score = float(raw)
            marks[name] = score
        except ValueError:
            print("Invalid marks. Please enter a number.")
    return marks

# ---------- Task 5: Pass/Fail filter ----------
def pass_fail_lists(marks: Dict[str, float], pass_mark: float = 40.0) -> Tuple[List[str], List[str]]:
    passed = [name for name, score in marks.items() if score >= pass_mark]
    failed = [name for name, score in marks.items() if score < pass_mark]
    return passed, failed

# ---------- Task 6: Output table ----------
def print_results_table(marks: Dict[str, float], grades: Dict[str, str]) -> None:
    print("\nName".ljust(20) + "Marks".ljust(10) + "Grade")
    print("-" * 40)
    for name, score in marks.items():
        grade = grades.get(name, "")
        print(f"{name.ljust(20)}{str(score).ljust(10)}{grade}")
    print("-" * 40)

def export_to_csv(marks: Dict[str, float], grades: Dict[str, str], filepath: str) -> None:
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Marks", "Grade"])
            for name, score in marks.items():
                writer.writerow([name, score, grades.get(name, "")])
        print(f"Results exported to {filepath}")
    except Exception as e:
        print(f"Failed to export CSV: {e}")

# ---------- Orchestration / CLI Loop ----------
def analyze_marks(marks: Dict[str, float]) -> None:
    if not marks:
        print("No student data to analyze.")
        return

    avg = calculate_average(marks)
    med = calculate_median(marks)
    mx_name, mx_val = find_max_score(marks)
    mn_name, mn_val = find_min_score(marks)

    grades = build_grades_dict(marks)
    dist = grade_distribution(grades)
    passed, failed = pass_fail_lists(marks, pass_mark=40.0)

    # Print summary
    print("\n=== Analysis Summary ===")
    print(f"Total students: {len(marks)}")
    print(f"Average (mean): {avg:.2f}")
    print(f"Median: {med:.2f}")
    print(f"Highest: {mx_name} -> {mx_val}")
    print(f"Lowest:  {mn_name} -> {mn_val}")
    print("\nGrade distribution:")
    for g in ["A","B","C","D","F"]:
        print(f"  {g}: {dist.get(g,0)}")
    print(f"\nPassed ({len(passed)}): {', '.join(passed) if passed else 'None'}")
    print(f"Failed ({len(failed)}): {', '.join(failed) if failed else 'None'}")

    # Results table
    print_results_table(marks, grades)

    # Offer CSV export
    choice = input("Export results table to CSV? (y/N): ").strip().lower()
    if choice == 'y':
        path = input("Enter file name (e.g. final_grades.csv): ").strip()
        if path == "":
            path = "final_grades.csv"
        export_to_csv(marks, grades, path)

def main_menu():
    marks_data = {}
    while True:
        print("\n=== GradeBook Analyzer ===")
        print("1. Manual entry of students")
        print("2. Load students from CSV")
        print("3. Show current data")
        print("4. Run analysis on current data")
        print("5. Clear current data")
        print("6. Exit")
        sel = input("Choose an option (1-6): ").strip()

        if sel == '1':
            new = manual_entry()
            marks_data.update(new)
            print(f"Added {len(new)} student(s). Total now: {len(marks_data)}")
        elif sel == '2':
            path = input("Enter CSV path (default: students.csv): ").strip()
            if path == "":
                path = "students.csv"
            loaded = load_csv(path)
            if loaded:
                marks_data.update(loaded)
                print(f"Loaded {len(loaded)} students. Total now: {len(marks_data)}")
            else:
                print("No data loaded from CSV.")
        elif sel == '3':
            if not marks_data:
                print("No data loaded yet.")
            else:
                print_results_table(marks_data, build_grades_dict(marks_data))
        elif sel == '4':
            analyze_marks(marks_data)
        elif sel == '5':
            marks_data.clear()
            print("Cleared current data.")
        elif sel == '6':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    print("Welcome to GradeBook Analyzer CLI")
    print("Choose manual entry or CSV to start.")
    main_menu()