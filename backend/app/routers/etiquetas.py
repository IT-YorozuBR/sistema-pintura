from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Etiqueta
from app.schemas import EtiquetaCreate, EtiquetaOut, EtiquetaUpdate

router = APIRouter(prefix="/api/etiquetas", tags=["etiquetas"])


@router.get("", response_model=list[EtiquetaOut])
def listar_etiquetas(
    ordem: str | None = None,
    item: str | None = None,
    origem: str | None = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    stmt = select(Etiqueta)
    if ordem:
        stmt = stmt.where(Etiqueta.ordem.ilike(f"%{ordem}%"))
    if item:
        stmt = stmt.where(Etiqueta.item.ilike(f"%{item}%"))
    if origem:
        stmt = stmt.where(Etiqueta.origem.ilike(f"%{origem}%"))
    stmt = stmt.order_by(Etiqueta.criado_em.desc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()


@router.get("/{chave}", response_model=EtiquetaOut)
def obter_etiqueta(chave: str, db: Session = Depends(get_db)):
    etq = db.get(Etiqueta, chave)
    if not etq:
        raise HTTPException(status_code=404, detail="Etiqueta não encontrada.")
    return etq


@router.post("", response_model=EtiquetaOut, status_code=201)
def criar_etiqueta(payload: EtiquetaCreate, db: Session = Depends(get_db)):
    existente = db.get(Etiqueta, payload.chave)
    if existente:
        return existente
    etq = Etiqueta(**payload.model_dump())
    db.add(etq)
    db.commit()
    db.refresh(etq)
    return etq


@router.patch("/{chave}", response_model=EtiquetaOut)
def atualizar_etiqueta(chave: str, payload: EtiquetaUpdate, db: Session = Depends(get_db)):
    etq = db.get(Etiqueta, chave)
    if not etq:
        raise HTTPException(status_code=404, detail="Etiqueta não encontrada.")
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(etq, campo, valor)
    db.commit()
    db.refresh(etq)
    return etq
