from datetime import date, datetime, time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AcaoTipo, Etiqueta, Movimentacao
from app.schemas import MovimentacaoCreate, MovimentacaoOut

router = APIRouter(prefix="/api/movimentacoes", tags=["movimentacoes"])


@router.get("", response_model=list[MovimentacaoOut])
def listar_movimentacoes(
    data_ini: date | None = None,
    data_fim: date | None = None,
    turno: str | None = None,
    acao: AcaoTipo | None = None,
    item: str | None = None,
    ordem: str | None = None,
    origem: str | None = None,
    usuario: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    stmt = select(Movimentacao)
    precisa_join = any([item, ordem, origem])
    if precisa_join:
        stmt = stmt.join(Etiqueta, Movimentacao.chave == Etiqueta.chave)
        if item:
            stmt = stmt.where(Etiqueta.item.ilike(f"%{item}%"))
        if ordem:
            stmt = stmt.where(Etiqueta.ordem.ilike(f"%{ordem}%"))
        if origem:
            stmt = stmt.where(Etiqueta.origem.ilike(f"%{origem}%"))
    if data_ini:
        stmt = stmt.where(Movimentacao.ts >= datetime.combine(data_ini, time.min))
    if data_fim:
        stmt = stmt.where(Movimentacao.ts <= datetime.combine(data_fim, time.max))
    if turno:
        stmt = stmt.where(Movimentacao.turno == turno)
    if acao:
        stmt = stmt.where(Movimentacao.acao == acao)
    if usuario:
        stmt = stmt.where(Movimentacao.usuario.ilike(f"%{usuario}%"))
    stmt = stmt.order_by(Movimentacao.ts.desc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()


@router.post("", response_model=MovimentacaoOut, status_code=201)
def criar_movimentacao(payload: MovimentacaoCreate, db: Session = Depends(get_db)):
    etq = db.get(Etiqueta, payload.chave)
    if not etq:
        raise HTTPException(status_code=404, detail="Etiqueta referenciada não encontrada.")
    mov = Movimentacao(**payload.model_dump())
    db.add(mov)
    db.commit()
    db.refresh(mov)
    return mov
