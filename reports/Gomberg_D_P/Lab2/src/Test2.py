from enum import Enum


# --- Вспомогательные сущности ---
class AssignmentType(Enum):
    PROCEDURE = "Процедура"
    MEDICINE = "Лекарство"
    SURGERY = "Операция"


class Assignment:
    """Класс Назначение (Ассоциация между врачом, типом лечения и исполнителем)"""

    def __init__(self, description, type: AssignmentType):
        self.description = description
        self.type = type
        self.is_completed = False

    def __str__(self):
        status = "✅ Выполнено" if self.is_completed else "⏳ Ожидает"
        return f"[{self.type.value}] {self.description} — {status}"


# --- Модель персонала ---
class Staff:
    def __init__(self, name):
        self.name = name

    def execute_assignment(self, patient, assignment_index):
        """Медсестра или Врач выполняют назначение"""
        if 0 <= assignment_index < len(patient.assignments):
            assignment = patient.assignments[assignment_index]
            assignment.is_completed = True
            print(
                f"Сотрудник {self.name} выполнил: {assignment.description} для {patient.name}"
            )


class Doctor(Staff):
    def prescribe(self, patient, description, type: AssignmentType):
        """Врач делает назначение пациенту"""
        new_assignment = Assignment(description, type)
        patient.assignments.append(new_assignment)
        print(f"Доктор {self.name} назначил {description} пациенту {patient.name}")


class Nurse(Staff):
    pass


# --- Основные сущности системы ---


class Patient:
    def __init__(self, name):
        self.name = name
        self.doctor = None
        self.assignments = []
        self.is_discharged = False
        self.discharge_reason = None

    def __str__(self):
        status = (
            f"Выписан ({self.discharge_reason})" if self.is_discharged else "На лечении"
        )
        return f"Пациент: {self.name} | Статус: {status} | Назначений: {len(self.assignments)}"


class Hospital:
    """Класс Больница"""

    def __init__(self, title):
        self.title = title
        self.patients = []

    def admit_patient(self, patient, doctor):
        patient.doctor = doctor
        self.patients.append(patient)
        print(f"Пациент {patient.name} поступил в '{self.title}' к врачу {doctor.name}")

    def discharge_patient(self, patient, reason="Плановая выписка"):
        if patient in self.patients:
            patient.is_discharged = True
            patient.discharge_reason = reason
            self.patients.remove(patient)
            print(f"Пациент {patient.name} выписан. Причина: {reason}")


hospital = Hospital("Городская клиническая больница №1")
doc_ivanov = Doctor("Иванов И.И.")
nurse_petrova = Nurse("Петрова А.С.")
patient_sidorov = Patient("Сидоров В.Г.")


hospital.admit_patient(patient_sidorov, doc_ivanov)
doc_ivanov.prescribe(patient_sidorov, "Аспирин 500мг", AssignmentType.MEDICINE)
doc_ivanov.prescribe(patient_sidorov, "Промывание", AssignmentType.PROCEDURE)

# 3. Выполнение назначений (Реализация роли исполнителя)
nurse_petrova.execute_assignment(patient_sidorov, 0)
doc_ivanov.execute_assignment(patient_sidorov, 1)

# 4. Проверка статуса
print(patient_sidorov)
for task in patient_sidorov.assignments:
    print(f"  - {task}")

# 5. Выписка по обстоятельствам
hospital.discharge_patient(patient_sidorov, "Нарушение режима")
