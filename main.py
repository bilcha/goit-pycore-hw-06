from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def is_valid(self):
        return self.value.isdigit() and len(self.value) == 10

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_value):
        phone = Phone(phone_value)
        if phone.is_valid():
            self.phones.append(phone)
        else:
            raise ValueError("Phone number should contain exactly 10 digits.")

    def remove_phone(self, phone_value):
        phone = self.find_phone(phone_value)
        if phone:
            self.phones.remove(phone)
            return f"Phone {phone_value} removed."
        raise ValueError(f"Phone {phone_value} not found.")

    def edit_phone(self, old_phone_value, new_phone_value):
        phone = self.find_phone(old_phone_value)
        if phone:
            if not Phone(new_phone_value).is_valid():
                raise ValueError("New phone number should contain exactly 10 digits.")
            phone.value = new_phone_value
            return f"Phone {old_phone_value} changed to {new_phone_value}."
        raise ValueError(f"Phone {old_phone_value} not found.")

    def find_phone(self, phone_value):
        for phone in self.phones:
            if phone.value == phone_value:
                return phone
        return None

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        if not isinstance(record, Record):
            raise TypeError("Only Record objects can be added.")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        record = self.find(name)
        if record:
            del self.data[name]
            return f"Record for {name} deleted."
        raise ValueError(f"Record for {name} not found.")

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as e:
            print(e)
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, contacts):
    if len(args) < 1:
        raise ValueError("Please provide a name.")
    name = args[0]
    phone = args[1] if len(args) > 1 else None
    if name not in contacts:
        contacts[name] = Record(name)
    if phone:
        contacts[name].add_phone(phone)
    print(f"Contact {'updated' if phone else 'added'}: {name}")

@input_error
def change_contact(args, contacts):
    if len(args) < 3:
        raise ValueError("Please provide a name, the phone number to edit, and the new phone number.")
    name, old_phone, new_phone = args
    if name in contacts:
        print(contacts[name].edit_phone(old_phone, new_phone))
    else:
        raise KeyError(f"Name '{name}' not found in contacts.")

@input_error
def remove_phone(args, contacts):
    if len(args) < 2:
        raise ValueError("Please provide both a name and a phone number to remove.")
    name, phone = args
    if name in contacts:
        print(contacts[name].remove_phone(phone))
    else:
        raise KeyError(f"Name '{name}' not found in contacts.")


def show_all(contacts):
    if contacts:
        print("Contacts list:")
        for name, phone in contacts.items():
            print(f"{name}: {phone}")
    else:
        print("Contact list is empty.")

def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            add_contact(args, contacts)
        elif command == "change":
            change_contact(args, contacts)
        elif command == "remove_phone":
            remove_phone(args, contacts)
        elif command == "all":
            show_all(contacts)
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
