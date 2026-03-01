# test_hospital.py
from hospital import Hospital, Doctor, Nurse, Patient, Prescription, MedicalStaff


def test_hospital_system():
    print("=== Тест 1: создание больницы ===")
    hospital = Hospital("Городская больница")
    print(hospital)

    print("\n=== Тест 2: добавление персонала ===")
    doctor = Doctor("Иванов")
    nurse = Nurse("Петрова")
    patient = Patient("Сидоров")

    hospital.add_staff(doctor)
    hospital.add_staff(nurse)
    hospital.add_patient(patient)

    print(hospital)

    print("\n=== Тест 3: назначение лечения ===")
    prescription = doctor.prescribe(patient, "Приём антибиотиков")
    print(prescription)
    print("Количество назначений у пациента:", len(patient.prescriptions))

    print("\n=== Тест 4: выполнение назначения ===")
    prescription.execute(nurse)
    print(prescription)

    print("\n=== Тест 5: выписка пациента ===")
    patient.discharge("Окончание лечения")
    print(patient)

    print("\n=== Тест 6: проверка строковых представлений ===")
    print(str(doctor))
    print(str(nurse))
    print(str(patient))

    print("\n=== Тест 7: проверка ошибки (не медперсонал) ===")
    try:
        prescription.execute(patient)  # пациент не может выполнять
    except ValueError as e:
        print("Ошибка (ожидаемо):", e)


if __name__ == "__main__":
    test_hospital_system()
