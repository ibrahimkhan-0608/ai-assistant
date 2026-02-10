"""
🤖 PERSONAL PRODUCTIVITY ASSISTANT
Version 1.0 - Complete System
"""
import datetime
import json
import os
import sys

class ProductivityAssistant:
    def __init__(self, name="PyAssistant"):
        self.name = name
        self.user_name = ""
        self.tasks = []
        self.notes = []
        self.data_file = "assistant_data.json"
        self.load_data()
    
    def load_data(self):
        """Load saved data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.notes = data.get('notes', [])
                    self.user_name = data.get('user', "")
        except Exception as e:
            print(f"⚠️ Could not load data: {e}")
            self.tasks = []
            self.notes = []
    
    def save_data(self):
        """Save all data to file"""
        try:
            data = {
                'tasks': self.tasks,
                'notes': self.notes,
                'user': self.user_name,
                'last_saved': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except:
            return False
    
    def greet(self):
        """Welcome message with time-based greeting"""
        hour = datetime.datetime.now().hour
        
        if hour < 12:
            greeting = "🌅 Good morning"
        elif hour < 18:
            greeting = "☀️ Good afternoon"
        else:
            greeting = "🌙 Good evening"
        
        if not self.user_name:
            self.user_name = input(f"{greeting}! What's your name? ").strip()
            if self.user_name:
                self.save_data()
        
        return f"{greeting}, {self.user_name}! I'm {self.name}, your personal productivity assistant."
    
    def show_menu(self):
        """Display main menu with ASCII art"""
        menu = f"""
        ╔══════════════════════════════════════╗
        ║      🤖 PRODUCTIVITY ASSISTANT      ║
        ╠══════════════════════════════════════╣
        ║  1. 📝 Add Task                     ║
        ║  2. ✅ View/Complete Tasks          ║
        ║  3. 📒 Add Note                     ║
        ║  4. 📖 View Notes                   ║
        ║  5. 🧮 Calculator                   ║
        ║  6. 📅 Date & Time                  ║
        ║  7. ⚙️ Settings                     ║
        ║  8. 💾 Save & Exit                  ║
        ╚══════════════════════════════════════╝
        
        👤 User: {self.user_name}
        📊 Tasks: {len(self.tasks)} | Notes: {len(self.notes)}
        """
        return menu
    
    def add_task(self):
        """Add a new task with priority"""
        print("\n" + "="*40)
        print("📝 ADD NEW TASK")
        print("="*40)
        
        task = input("Task description: ").strip()
        if not task:
            print("❌ Task cannot be empty!")
            return False
        
        print("\nPriority levels:")
        print("1. 🔴 High (Urgent)")
        print("2. 🟡 Medium (Important)")
        print("3. 🟢 Low (Whenever)")
        
        priority_map = {1: "High 🔴", 2: "Medium 🟡", 3: "Low 🟢"}
        try:
            priority_choice = int(input("\nSelect priority (1-3): "))
            priority = priority_map.get(priority_choice, "Medium 🟡")
        except:
            priority = "Medium 🟡"
        
        new_task = {
            'id': len(self.tasks) + 1,
            'task': task,
            'priority': priority,
            'created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'completed': False
        }
        
        self.tasks.append(new_task)
        print(f"\n✅ Task added successfully!")
        print(f"   ID: {new_task['id']} | Priority: {priority}")
        return True
    
    def view_tasks(self, show_completed=False):
        """Display all tasks with options"""
        if not self.tasks:
            print("\n📭 No tasks found!")
            return
        
        print("\n" + "="*50)
        print("📋 YOUR TASKS")
        print("="*50)
        
        pending = [t for t in self.tasks if not t['completed']]
        completed = [t for t in self.tasks if t['completed']]
        
        if pending:
            print("\n⏳ PENDING TASKS:")
            for task in pending:
                status = "○"
                print(f"\n{task['id']}. [{status}] {task['task']}")
                print(f"   Priority: {task['priority']}")
                print(f"   Created: {task['created']}")
        
        if completed and show_completed:
            print("\n✅ COMPLETED TASKS:")
            for task in completed:
                status = "✓"
                print(f"\n{task['id']}. [{status}] {task['task']}")
                print(f"   Created: {task['created']}")
        
        print("\n" + "="*50)
        print(f"📊 Summary: {len(pending)} pending, {len(completed)} completed")
        
        return len(pending)
    
    def manage_tasks(self):
        """Complete or delete tasks"""
        pending_count = self.view_tasks()
        
        if pending_count == 0:
            return
        
        print("\n" + "="*40)
        print("✅ TASK MANAGEMENT")
        print("="*40)
        print("1. Mark task as completed")
        print("2. Delete task")
        print("3. Back to menu")
        
        try:
            action = input("\nSelect action (1-3): ").strip()
            
            if action == '1':
                task_id = int(input("Enter task ID to complete: "))
                for task in self.tasks:
                    if task['id'] == task_id and not task['completed']:
                        task['completed'] = True
                        task['completed_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        print(f"\n✅ Task {task_id} marked as completed!")
                        return
                print("❌ Task not found or already completed!")
            
            elif action == '2':
                task_id = int(input("Enter task ID to delete: "))
                for i, task in enumerate(self.tasks):
                    if task['id'] == task_id:
                        deleted_task = self.tasks.pop(i)
                        print(f"\n🗑️ Task deleted: '{deleted_task['task']}'")
                        # Re-number remaining tasks
                        for j, t in enumerate(self.tasks[i:], start=i):
                            t['id'] = j + 1
                        return
                print("❌ Task not found!")
        
        except ValueError:
            print("❌ Please enter valid numbers!")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def add_note(self):
        """Add a new note"""
        print("\n" + "="*40)
        print("📒 ADD NEW NOTE")
        print("="*40)
        
        note = input("Enter your note: ").strip()
        if not note:
            print("❌ Note cannot be empty!")
            return False
        
        category = input("Category (Work/Personal/Ideas/etc): ").strip()
        if not category:
            category = "General"
        
        new_note = {
            'id': len(self.notes) + 1,
            'note': note,
            'category': category,
            'created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.notes.append(new_note)
        print(f"\n📝 Note saved successfully!")
        print(f"   ID: {new_note['id']} | Category: {category}")
        return True
    
    def view_notes(self):
        """Display all notes by category"""
        if not self.notes:
            print("\n📭 No notes found!")
            return
        
        print("\n" + "="*50)
        print("📖 YOUR NOTES")
        print("="*50)
        
        # Group notes by category
        categories = {}
        for note in self.notes:
            cat = note['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(note)
        
        for category, notes_list in categories.items():
            print(f"\n📁 {category.upper()} ({len(notes_list)} notes):")
            print("-" * 40)
            for note in notes_list:
                print(f"\n{note['id']}. {note['note']}")
                print(f"   📅 {note['created']}")
        
        print("\n" + "="*50)
        print(f"📊 Total notes: {len(self.notes)}")
    
    def calculator(self):
        """Enhanced calculator with history"""
        print("\n" + "="*40)
        print("🧮 ENHANCED CALCULATOR")
        print("="*40)
        
        history = []
        
        while True:
            print("\nOptions:")
            print("1. ➕ Addition")
            print("2. ➖ Subtraction")
            print("3. ✖️ Multiplication")
            print("4. ➗ Division")
            print("5. 📜 View History")
            print("6. ↩️ Back to Menu")
            
            try:
                choice = input("\nSelect operation (1-6): ").strip()
                
                if choice == '6':
                    break
                
                elif choice == '5':
                    if not history:
                        print("\nNo calculations yet!")
                    else:
                        print("\n📜 CALCULATION HISTORY:")
                        for i, calc in enumerate(history, 1):
                            print(f"{i}. {calc}")
                    continue
                
                if choice in ['1', '2', '3', '4']:
                    try:
                        num1 = float(input("Enter first number: "))
                        num2 = float(input("Enter second number: "))
                        
                        operations = {
                            '1': ('➕', '+', lambda a, b: a + b),
                            '2': ('➖', '-', lambda a, b: a - b),
                            '3': ('✖️', '×', lambda a, b: a * b),
                            '4': ('➗', '÷', lambda a, b: a / b if b != 0 else "Undefined (division by zero)")
                        }
                        
                        emoji, symbol, operation = operations[choice]
                        
                        if choice == '4' and num2 == 0:
                            result = "Undefined (division by zero)"
                        else:
                            result = operation(num1, num2)
                        
                        calculation = f"{num1} {symbol} {num2} = {result}"
                        history.append(calculation)
                        
                        print(f"\n{emoji} RESULT: {calculation}")
                        
                    except ValueError:
                        print("❌ Please enter valid numbers!")
                    except ZeroDivisionError:
                        print("❌ Cannot divide by zero!")
                
                else:
                    print("❌ Invalid choice!")
            
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_datetime(self):
        """Show current date and time with calendar"""
        now = datetime.datetime.now()
        
        print("\n" + "="*40)
        print("📅 DATE & TIME INFORMATION")
        print("="*40)
        
        print(f"\n📆 Date: {now.strftime('%A, %B %d, %Y')}")
        print(f"🕒 Time: {now.strftime('%I:%M:%S %p')}")
        print(f"📅 ISO Format: {now.strftime('%Y-%m-%d')}")
        
        # Week information
        week_num = now.isocalendar()[1]
        print(f"📅 Week Number: {week_num}")
        
        # Days until next month
        next_month = now.replace(day=28) + datetime.timedelta(days=4)
        days_next_month = (next_month.replace(day=1) - now).days
        print(f"📅 Days until next month: {days_next_month}")
        
        print("\n" + "="*40)
    
    def settings(self):
        """Assistant settings"""
        print("\n" + "="*40)
        print("⚙️ ASSISTANT SETTINGS")
        print("="*40)
        
        print(f"\nCurrent settings:")
        print(f"👤 User: {self.user_name}")
        print(f"🤖 Assistant name: {self.name}")
        print(f"💾 Data file: {self.data_file}")
        print(f"📊 Data: {len(self.tasks)} tasks, {len(self.notes)} notes")
        
        print("\nOptions:")
        print("1. Change assistant name")
        print("2. Change username")
        print("3. Clear all data")
        print("4. View system info")
        print("5. Back to menu")
        
        try:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                new_name = input("Enter new assistant name: ").strip()
                if new_name:
                    self.name = new_name
                    print(f"✅ Assistant name changed to: {new_name}")
            
            elif choice == '2':
                new_user = input("Enter new username: ").strip()
                if new_user:
                    self.user_name = new_user
                    print(f"✅ Username changed to: {new_user}")
            
            elif choice == '3':
                confirm = input("⚠️ WARNING: This will delete ALL tasks and notes! Type 'DELETE' to confirm: ")
                if confirm == "DELETE":
                    self.tasks = []
                    self.notes = []
                    if os.path.exists(self.data_file):
                        os.remove(self.data_file)
                    print("✅ All data cleared!")
                else:
                    print("❌ Cancelled. Data preserved.")
            
            elif choice == '4':
                print("\n🖥️ SYSTEM INFORMATION:")
                print(f"Python: {sys.version}")
                print(f"Platform: {sys.platform}")
                print(f"Current directory: {os.getcwd()}")
                print(f"Data file size: {os.path.getsize(self.data_file) if os.path.exists(self.data_file) else 0} bytes")
            
            elif choice == '5':
                return
            
            else:
                print("❌ Invalid option!")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def exit_program(self):
        """Save and exit gracefully"""
        print("\n" + "="*40)
        print("💾 SAVING DATA...")
        print("="*40)
        
        if self.save_data():
            print(f"✅ Data saved to '{self.data_file}'")
            print(f"📊 Saved: {len(self.tasks)} tasks, {len(self.notes)} notes")
        else:
            print("❌ Could not save data!")
        
        print("\n" + "="*40)
        print("👋 Goodbye! See you next time!")
        print("="*40)

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Main program loop"""
    assistant = ProductivityAssistant()
    
    # Clear screen and show welcome
    clear_screen()
    print("\n" + "="*60)
    print(" " * 20 + "🤖 PRODUCTIVITY ASSISTANT")
    print(" " * 15 + "Version 1.0 | By Python Learner")
    print("="*60)
    
    print(assistant.greet())
    
    while True:
        try:
            # Show menu and get choice
            print(assistant.show_menu())
            choice = input("\n👉 Enter your choice (1-8): ").strip()
            
            if choice == '1':
                assistant.add_task()
            elif choice == '2':
                assistant.manage_tasks()
            elif choice == '3':
                assistant.add_note()
            elif choice == '4':
                assistant.view_notes()
            elif choice == '5':
                assistant.calculator()
            elif choice == '6':
                assistant.show_datetime()
            elif choice == '7':
                assistant.settings()
            elif choice == '8':
                assistant.exit_program()
                break
            else:
                print("\n❌ Invalid choice! Please enter 1-8")
            
            # Pause before showing menu again
            input("\n↵ Press Enter to continue...")
            clear_screen()
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Program interrupted!")
            save = input("Save data before exiting? (y/n): ").lower()
            if save == 'y':
                assistant.save_data()
                print("✅ Data saved!")
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            input("\n↵ Press Enter to continue...")
            clear_screen()

if __name__ == "__main__":
    main()