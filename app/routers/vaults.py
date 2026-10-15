from datetime import datetime, UTC
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from app.schemas.vault import VaultCreate, VaultOut

router = APIRouter(prefix="/vaults", tags=["vaults"])

_vaults: dict[UUID, dict] = {}

@router.get("/{vault_id}", response_model=VaultOut)
def get_vault(vault_id: UUID):
    vault = _vaults.get(vault_id)
    if vault is None:
        raise HTTPException(status_code=404, detail="Vault not found")
    return vault

@router.get("/", response_model=list[VaultOut])
def list_vaults():
    return list(_vaults.values())

@router.post("/", response_model=VaultOut, status_code=201)
def create_vault(payload: VaultCreate):
    for existing in _vaults.values():
        if existing["name"] == payload.name:
            raise HTTPException(status_code=409, detail="Vault with this name already exists")

    vault_id = uuid4()
    vault = {"id": vault_id, "name": payload.name, "created_at": datetime.now(UTC)}
    _vaults[vault_id] = vault
    return vault

@router.delete("/{vault_id}", status_code=204)
def delete_vault(vault_id: UUID):
    if vault_id not in _vaults:
        raise HTTPException(status_code=404, detail="Vault not found")
    del _vaults[vault_id]
