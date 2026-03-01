from abc import ABC, abstractmethod

class Person:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"

class MedicalStaff(Person):
    pass

class Doctor(MedicalStaff):
    def prescribe(self, patient, description: str):
        prescription = Prescription(description, self, patient)
        patient.add_prescription(prescription)
        return prescription

class Nurse(MedicalStaff):
    pass

class Patient(Person):
    def __init__(self, name: str):
        super().__init__(name)
        self.prescriptions = []
        self.is_discharged = False
        self.discharge_reason = None

    def add_prescription(self, prescription):
        self.prescriptions.append(prescription)

    def discharge(self, reason: str):
        self.is_discharged = True
        self.discharge_reason = reason

    def __str__(self):
        status = "Выписан" if self.is_discharged else "На лечении"
        return f"Пациент: {self.name}, статус: {status}"

class Executable(ABC):
    @abstractmethod
    def execute(self, performer):
        pass

class Prescription(Executable):
    def __init__(self, description: str, doctor: Doctor, patient: Patient):
        self.description = description
        self.doctor = doctor
        self.patient = patient
        self.is_executed = False

    def execute(self, performer):
        if not isinstance(performer, MedicalStaff):
            raise ValueError("Исполнитель должен быть медицинским персоналом")
        self.is_executed = True
        print(f"{performer.name} выполнил назначение: {self.description}")

    def __str__(self):
        status = "Выполнено" if self.is_executed else "Не выполнено"
        return f"Назначение: {self.description} ({status})"

class Hospital:
    def __init__(self, name: str):
        self.name = name
        self.patients = []
        self.staff = []

    def add_patient(self, patient: Patient):
        self.patients.append(patient)

    def add_staff(self, staff_member: MedicalStaff):
        self.staff.append(staff_member)

    def __str__(self):
        return f"Больница: {self.name}, пациентов: {len(self.patients)}, персонала: {len(self.staff)}"

if __name__ == "__main__":
    hospital = Hospital("Городская больница")

    doctor = Doctor("Иванов")
    nurse = Nurse("Петрова")
    patient = Patient("Сидоров")

    hospital.add_staff(doctor)
    hospital.add_staff(nurse)
    hospital.add_patient(patient)

    print(hospital)

    # Врач назначает лечение
    prescription = doctor.prescribe(patient, "Приём антибиотиков")

    print(prescription)

    # Медсестра выполняет назначение
    prescription.execute(nurse)

    print(prescription)

    # Выписка пациента
    patient.discharge("Окончание лечения")

    print(patient)
