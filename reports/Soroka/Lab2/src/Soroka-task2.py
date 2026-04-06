from enum import Enum
from typing import List, Optional


class PrescriptionType(Enum):
    MEDICINE = "Лекарство"
    PROCEDURE = "Процедура"
    OPERATION = "Операция"


class DischargeReason(Enum):
    COMPLETED = "Окончание лечения"
    VIOLATION = "Нарушение режима"
    OTHER = "Иные обстоятельства"


class Prescription:
    def __init__(self, title: str, pres_type: PrescriptionType):
        self.title = title
        self.pres_type = pres_type
        self.is_completed = False

    def complete(self):
        self.is_completed = True

    def __str__(self):
        status = "Выполнено" if self.is_completed else "Ожидает"
        return f"[{self.pres_type.value}] '{self.title}' - {status}"


class MedicalStaff:
    def __init__(self, name: str):
        self.name = name

    def perform_prescription(self, prescription: Prescription, patient: "Patient"):
        if not prescription.is_completed:
            prescription.complete()
            role = "Врач" if isinstance(self, Physician) else "Медсестра"
            print(
                f"-> {role} {self.name} выполнил(а) назначение '{prescription.title}' для пациента {patient.name}."
            )
        else:
            print(f"-> Назначение '{prescription.title}' уже было выполнено ранее.")


class Physician(MedicalStaff):
    def prescribe(self, patient: "Patient", title: str, pres_type: PrescriptionType):
        if patient.is_discharged:
            print(
                f"Ошибка: Невозможно сделать назначение. Пациент {patient.name} уже выписан."
            )
            return

        new_prescription = Prescription(title, pres_type)
        patient.prescriptions.append(new_prescription)
        print(
            f"-> Врач {self.name} назначил {pres_type.value.lower()} '{title}' пациенту {patient.name}."
        )


class Nurse(MedicalStaff):
    pass


class Patient:
    def __init__(self, name: str):
        self.name = name
        self.attending_physician: Optional[Physician] = None
        self.prescriptions: List[Prescription] = []
        self.is_discharged = False
        self.discharge_reason: Optional[DischargeReason] = None

    def print_history(self):
        print(f"\n--- Карта пациента: {self.name} ---")
        physician_name = (
            self.attending_physician.name if self.attending_physician else "Не назначен"
        )
        print(f"Лечащий врач: {physician_name}")
        status = (
            f"Выписан ({self.discharge_reason.value if self.discharge_reason else ''})"
            if self.is_discharged
            else "На лечении"
        )
        print(f"Статус: {status}")
        print("Назначения:")
        if not self.prescriptions:
            print("  - Нет назначений")
        for p in self.prescriptions:
            print(f"  - {p}")
        print("----------------------------------\n")


class Hospital:
    def __init__(self, name: str):
        self.name = name
        self.patients: List[Patient] = []
        self.staff: List[MedicalStaff] = []

    def admit_patient(self, patient: Patient):
        self.patients.append(patient)
        print(f" Пациент {patient.name} поступил в больницу '{self.name}'.")

    def hire_staff(self, staff_member: MedicalStaff):
        self.staff.append(staff_member)

    def assign_physician(self, patient: Patient, physician: Physician):
        if patient in self.patients and physician in self.staff:
            patient.attending_physician = physician
            print(f"Пациенту {patient.name} назначен лечащий врач {physician.name}.")

    def discharge_patient(self, patient: Patient, reason: DischargeReason):
        if patient in self.patients:
            if not patient.is_discharged:
                patient.is_discharged = True
                patient.discharge_reason = reason
                print(f"Пациент {patient.name} выписан. Причина: {reason.value}.")
            else:
                print(f"Пациент {patient.name} уже выписан.")


if __name__ == "__main__":
    city_hospital = Hospital("Городская Клиническая Больница №1")

    dr_house = Physician("Грегори Хаус")
    dr_chase = Physician("Роберт Чейз")
    nurse_mary = Nurse("Мария Ивановна")

    city_hospital.hire_staff(dr_house)
    city_hospital.hire_staff(dr_chase)
    city_hospital.hire_staff(nurse_mary)

    patient1 = Patient("Иван Смирнов")
    patient2 = Patient("Петр Васильев")

    city_hospital.admit_patient(patient1)
    city_hospital.admit_patient(patient2)

    city_hospital.assign_physician(patient1, dr_house)
    city_hospital.assign_physician(patient2, dr_chase)

    print("\n--- Процесс лечения ---")

    dr_house.prescribe(patient1, "МРТ Головного мозга", PrescriptionType.PROCEDURE)
    dr_house.prescribe(patient1, "Ибупрофен 400мг", PrescriptionType.MEDICINE)

    dr_chase.prescribe(patient2, "Удаление аппендицита", PrescriptionType.OPERATION)

    nurse_mary.perform_prescription(patient1.prescriptions[1], patient1)

    dr_chase.perform_prescription(patient2.prescriptions[0], patient2)

    dr_chase.perform_prescription(patient1.prescriptions[0], patient1)

    patient1.print_history()

    print("--- Выписка пациентов ---")
    city_hospital.discharge_patient(patient1, DischargeReason.COMPLETED)
    city_hospital.discharge_patient(patient2, DischargeReason.VIOLATION)

    dr_house.prescribe(patient1, "Витамины", PrescriptionType.MEDICINE)

    patient1.print_history()
