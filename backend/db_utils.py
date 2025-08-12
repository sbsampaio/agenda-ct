"""
Funções para inicialização do banco de dados.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models.role import Role

# cria a tabela de roles
def ensure_default_roles(session: Session) -> None:
    admin_role = session.scalar(select(Role).where(Role.name == "admin"))
    user_role = session.scalar(select(Role).where(Role.name == "user"))
    
    roles_to_create = []
    
    if not admin_role:
        admin_role = Role(name="admin")
        session.add(admin_role)
        roles_to_create.append("admin")
    
    if not user_role:
        user_role = Role(name="user")
        session.add(user_role)
        roles_to_create.append("user")
    
    if roles_to_create:
        session.commit()
        print(f"Roles criadas: {', '.join(roles_to_create)}")


def get_admin_role(session: Session) -> Role:
    admin_role = session.scalar(select(Role).where(Role.name == "admin"))
    if not admin_role:
        raise ValueError("Role 'admin' não encontrada. Execute a inicialização das roles primeiro.")
    return admin_role


def get_user_role(session: Session) -> Role:
    user_role = session.scalar(select(Role).where(Role.name == "user"))
    if not user_role:
        raise ValueError("Role 'user' não encontrada. Execute a inicialização das roles primeiro.")
    return user_role


def is_admin(user, session: Session) -> bool:
    from .models.user_role import UserRole
    
    try:
        admin_role = get_admin_role(session)
        user_role = session.scalar(
            select(UserRole).where(
                UserRole.user_id == user.id,
                UserRole.role_id == admin_role.id
            )
        )
        return user_role is not None
    except ValueError:
        return False


def assign_user_role(user_id: int, session: Session) -> None:
    from .models.user_role import UserRole
    
    try:
        user_role = get_user_role(session)
        
        existing = session.scalar(
            select(UserRole).where(
                UserRole.user_id == user_id,
                UserRole.role_id == user_role.id
            )
        )
        
        if not existing:
            user_role_assignment = UserRole(
                user_id=user_id,
                role_id=user_role.id
            )
            session.add(user_role_assignment)
            session.commit()
            
    except ValueError as e:
        print(f"Aviso: Não foi possível atribuir role padrão: {e}")


def promote_to_admin(user_id: int, session: Session) -> bool:
    from .models.user_role import UserRole
    
    try:
        admin_role = get_admin_role(session)
        
        existing = session.scalar(
            select(UserRole).where(
                UserRole.user_id == user_id,
                UserRole.role_id == admin_role.id
            )
        )
        
        if not existing:
            admin_assignment = UserRole(
                user_id=user_id,
                role_id=admin_role.id
            )
            session.add(admin_assignment)
            session.commit()
            return True
        
        return False
        
    except ValueError:
        return False


def remove_admin_role(user_id: int, session: Session) -> bool:
    from .models.user_role import UserRole
    
    try:
        admin_role = get_admin_role(session)
        
        admin_assignment = session.scalar(
            select(UserRole).where(
                UserRole.user_id == user_id,
                UserRole.role_id == admin_role.id
            )
        )
        
        if admin_assignment:
            session.delete(admin_assignment)
            session.commit()
            return True
            
        return False
        
    except ValueError:
        return False
