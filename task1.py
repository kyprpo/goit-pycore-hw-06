from collections import UserDict


class Field:
    """Базовий клас для всіх полів запису."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Поле для імені контакту (обов’язкове)."""
    pass


class Phone(Field):
    """Поле для телефону з валідацією (10 цифр)."""
    def __init__(self, value):
        if not self._is_valid(value):
            raise ValueError("Номер телефону має містити рівно 10 цифр.")
        super().__init__(value)

    @staticmethod
    def _is_valid(value):
        return value.isdigit() and len(value) == 10


class Record:
    """Клас для зберігання контакту: ім’я + список телефонів."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                if not Phone._is_valid(new_number):
                    raise ValueError("Номер телефону має містити рівно 10 цифр.")
                phone.value = new_number
                return
        raise ValueError(f"Телефон {old_number} не знайдено.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    """Книга контактів, що містить записи (Record)."""
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


if __name__ == "__main__":
    # Приклад використання

    # Створення книги контактів
    book = AddressBook()

    # Додавання контактів
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх контактів
    for name, record in book.data.items():
        print(record)

    # Редагування телефону
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

    # Пошук конкретного телефону
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    # Видалення контакту
    book.delete("Jane")

    # Перевірка залишку
    for name, record in book.data.items():
        print(record)
