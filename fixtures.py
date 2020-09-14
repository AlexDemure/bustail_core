import asyncio
from structlog import get_logger

from accounts.enums import Roles as RolesEnum, Permissions as PermissionsEnum
from accounts.service import RoleService, PermissionService, RolePermissionService
from accounts.schemas import ArmAccountCreate, AuthorizationDataBase, PersonalDataBase
from accounts.settings import ADMIN_LOGIN, ADMIN_PASSWORD
from accounts.logic import CreateArmAccount


async def setup_permissions_and_roles():
    """
    Обновляет права доступа у ролей системы.
    """
    logger = get_logger()

    logger.info(f"Settings up roles")
    for role in RolesEnum.as_choices():  # Устанавливаем роли в системе

        role_id = await RoleService.get(RolesEnum(role[0]))
        if not role_id:
            await RoleService.create(role_type=RolesEnum(role[0]), description=role[1])
            logger.info(f'Role is created', role=role[0], description=role[1])

    for permission in PermissionsEnum.as_choices():  # Устанавливаем роли в системе
        permission_id = await PermissionService.get_by_permission_type(PermissionsEnum(permission[0]))
        if not permission_id:
            await PermissionService.create(permission_type=PermissionsEnum(permission[0]), description=permission[1])
            logger.info(f'Permissions is created', permission_type=permission[0], description=permission[1])

    roles = await RoleService.get_all_roles()
    permissions = await PermissionService.get_all_permissions()

    for role in roles:  # Простоявляем ограничения установленные в permission_list
        if role['name'] == "ADMIN":
            perms_role = [permission.value for permission in PermissionsEnum if permission != PermissionsEnum.public_api_access]
        elif role['name'] == "IDENTIFIER":
            perms_role = [PermissionsEnum.arm_api_access.value]
        elif role['name'] == "CUSTOMER":
            perms_role = [PermissionsEnum.public_api_access.value]
        else:
            perms_role = []

        for permission in permissions:
            if permission['name'] in perms_role:
                role_permission_id = await RolePermissionService.get(role['id'], permission['id'])
                if not role_permission_id:
                    await RolePermissionService.create(role['id'], permission['id'])
                    logger.info(
                        "Permission added to role",
                        role=role['name'],
                        permission=permission['name'],
                    )


async def create_account():
    """Создание аккаунта для АРМ."""
    schema = ArmAccountCreate(
        authorization_data=AuthorizationDataBase(
            login=ADMIN_LOGIN,
            password=ADMIN_PASSWORD,
        ),
        personal_data=PersonalDataBase(
            fullname="Administrator ARM system",
            phone=ADMIN_LOGIN,
            city="Moscow"
        ),
        role=RolesEnum.admin
    )
    await CreateArmAccount(schema).create()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop.create_task(setup_permissions_and_roles()))