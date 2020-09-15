from accounts.schemas import PersonalDataBase, AccountData


class AccountSerializer:

    @staticmethod
    def prepared_data(**kwargs) -> AccountData:
        personal_data = PersonalDataBase(
            fullname=kwargs['fullname'],
            phone=kwargs['phone'],
            email=kwargs.get('email', None),
            birthday=kwargs.get('birthday', None),
            city=kwargs['city']
        )
        return AccountData(
            id=kwargs['id'],
            registration_date=kwargs['registration_date'],
            personal_data=personal_data
        )
