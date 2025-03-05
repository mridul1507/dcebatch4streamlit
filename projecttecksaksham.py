import sqlite3
import random

def create_database():
    conn = sqlite3.connect("personal_health_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        steps INTEGER,
                        heart_rate INTEGER,
                        blood_pressure TEXT,
                        sleep_hours FLOAT,
                        oxygen_level FLOAT,
                        medical_report TEXT)''')
    conn.commit()
    return conn, cursor

def generate_sample_data(cursor):
    sample_users = [
        {"name": "Alice", "steps": 8500, "heart_rate": 75, "blood_pressure": "120/80", "sleep_hours": 7.5, "oxygen_level": 98.0},
        {"name": "Bob", "steps": 7000, "heart_rate": 80, "blood_pressure": "130/85", "sleep_hours": 6.5, "oxygen_level": 97.0},
        {"name": "Charlie", "steps": 10000, "heart_rate": 70, "blood_pressure": "110/70", "sleep_hours": 8.0, "oxygen_level": 99.0},
        {"name": "Diana", "steps": 5000, "heart_rate": 85, "blood_pressure": "140/90", "sleep_hours": 5.5, "oxygen_level": 95.0},
        {"name": "Eve", "steps": 9000, "heart_rate": 65, "blood_pressure": "125/85", "sleep_hours": 7.0, "oxygen_level": 98.5}
    ]
    for user in sample_users:
        store_data(cursor, user)

def store_data(cursor, user_data):
    cursor.execute("INSERT INTO users (name, steps, heart_rate, blood_pressure, sleep_hours, oxygen_level, medical_report) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (user_data['name'], user_data['steps'], user_data['heart_rate'], user_data['blood_pressure'], user_data['sleep_hours'], user_data['oxygen_level'], ""))
    cursor.connection.commit()

def generate_medical_report(cursor, user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        steps = user_data[2]
        heart_rate = user_data[3]
        blood_pressure = user_data[4]
        sleep_hours = user_data[5]
        oxygen_level = user_data[6]

        # Generate medical report based on sample data
        report = f"Medical Report for {user_data[1]}:\n"
        report += f"Steps Taken: {steps}\n"
        report += f"Heart Rate: {heart_rate} bpm\n"
        report += f"Blood Pressure: {blood_pressure}\n"
        report += f"Sleep Hours: {sleep_hours} hrs\n"
        report += f"Oxygen Level: {oxygen_level}%\n"

        # Evaluate health based on thresholds (example)
        if heart_rate > 100:
            report += "Warning: High heart rate, consider consulting a doctor.\n"
        if blood_pressure == "140/90":
            report += "Warning: High blood pressure detected, monitor regularly.\n"
        if oxygen_level < 95.0:
            report += "Warning: Low oxygen level, consult a healthcare professional.\n"
        if sleep_hours < 6.0:
            report += "Warning: Insufficient sleep, aim for at least 7-8 hours.\n"

        # Update the medical report in the database
        cursor.execute("UPDATE users SET medical_report = ? WHERE user_id = ?", (report, user_id))
        cursor.connection.commit()
        return report
    else:
        return "User not found!"

def view_data(cursor):
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(user)

def close_connection(conn):
    conn.close()

def main():
    conn, cursor = create_database()
    generate_sample_data(cursor)

    # View stored users data
    print("Stored Data:")
    view_data(cursor)

    # Generate and display medical report for a specific user
    user_id = int(input("\nEnter the user ID to generate a medical report: "))
    report = generate_medical_report(cursor, user_id)
    print("\n" + report)

    close_connection(conn)

if __name__ == "__main__":
    main()