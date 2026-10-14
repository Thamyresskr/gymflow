
"""
Rotas de gerenciamento de equipamentos.

Responsabilidades:
- Receber requisições relacionadas aos equipamentos.
- Delegar as regras de negócio para a camada de serviços.
- Disponibilizar operações de cadastro, consulta,
  atualização e remoção de equipamentos.
"""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.auth import require_roles
from app.core.dependencies import get_db
from app.models.user import User
from app.schemas.error import ErrorResponse
from app.schemas.equipment import (
    EquipmentCreate,
    EquipmentResponse,
    EquipmentUpdate,
)
from app.services.equipment_service import (
    get_equipment,
    list_equipments,
    register_equipment,
    remove_equipment,
    update_equipment_data,
)

router = APIRouter(
    prefix="/equipments",
    tags=["Equipamentos"],
)


@router.post(
    "/",
    response_model=EquipmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar equipamento",
    response_description="Equipamento cadastrado com sucesso.",
    description="""
Realiza o cadastro de um novo equipamento.

Regras de negócio:

- Apenas usuários ADMIN podem cadastrar equipamentos.
- O patrimônio informado deve ser único.
- O equipamento é criado com status ATIVO por padrão.
""",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Dados inválidos.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Autenticação necessária.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Acesso permitido apenas para administradores.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "Patrimônio já cadastrado.",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Erro de validação.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor.",
        },
    },
)
def criar_equipamento(
    equipamento: EquipmentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> EquipmentResponse:
    """
    Cadastra um novo equipamento.
    """

    return register_equipment(
        db=db,
        equipment_data=equipamento,
    )


@router.get(
    "/",
    response_model=list[EquipmentResponse],
    summary="Listar equipamentos",
    response_description="Lista de equipamentos retornada com sucesso.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Autenticação necessária.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Acesso permitido apenas para administradores.",
        },
    },
)
def listar_equipamentos(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> list[EquipmentResponse]:
    """
    Retorna todos os equipamentos cadastrados.
    """

    return list_equipments(db=db)


@router.get(
    "/{equipment_id}",
    response_model=EquipmentResponse,
    summary="Buscar equipamento",
    response_description="Equipamento localizado com sucesso.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Autenticação necessária.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Acesso permitido apenas para administradores.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Equipamento não encontrado.",
        },
    },
)
def buscar_equipamento(
    equipment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> EquipmentResponse:
    """
    Busca um equipamento pelo identificador.
    """

    return get_equipment(
        db=db,
        equipment_id=equipment_id,
    )


@router.put(
    "/{equipment_id}",
    response_model=EquipmentResponse,
    summary="Atualizar equipamento",
    response_description="Equipamento atualizado com sucesso.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Autenticação necessária.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Acesso permitido apenas para administradores.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Equipamento não encontrado.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "Patrimônio já cadastrado.",
        },
    },
)
def atualizar_equipamento(
    equipment_id: int,
    equipamento: EquipmentUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> EquipmentResponse:
    """
    Atualiza os dados de um equipamento.
    """

    return update_equipment_data(
        db=db,
        equipment_id=equipment_id,
        equipment_data=equipamento,
    )


@router.delete(
    "/{equipment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir equipamento",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Autenticação necessária.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Acesso permitido apenas para administradores.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Equipamento não encontrado.",
        },
    },
)
def excluir_equipamento(
    equipment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> Response:
    """
    Remove um equipamento.
    """

    remove_equipment(
        db=db,
        equipment_id=equipment_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
