from .schemas import (
    PersonalDataBase, AuthorizationDataBase,
    Account
)


class AccountSerializer:

    @staticmethod
    def prepared_data(**kwargs) -> Account:
        personal_data = PersonalDataBase(
            fullname=kwargs['fullname'],
            phone=kwargs['phone'],
            email=kwargs.get('email', None),
            birthday=kwargs.get('birthday', None),
            city=kwargs['city']
        )
        authorization_data = AuthorizationDataBase(
            login=kwargs['login'],
            password=kwargs['password']
        )
        return Account(
            id=kwargs['id'],
            registration_date=kwargs['registration_date'],
            authorization_data=authorization_data,
            personal_data=personal_data
        )
