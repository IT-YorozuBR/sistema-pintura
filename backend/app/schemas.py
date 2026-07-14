from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import AcaoTipo


class EtiquetaCreate(BaseModel):
    chave: str
    origem: str
    item: str
    ordem: str
    sequencia: int
    quantidade: int
    turno: str | None = None
    operador: str | None = None
    raw_qr_content: str | None = None


class EtiquetaUpdate(BaseModel):
    qtd_produzida: int | None = None
    qtd_hold: int | None = None
    qtd_scrap: int | None = None
    confirmada: bool | None = None
    leituras: int | None = None
    scrap_motivo: str | None = None
    scrap_obs: str | None = None
    hold_motivo: str | None = None
    hold_responsavel: str | None = None
    hold_obs: str | None = None
    hold_data_entrada: datetime | None = None
    turno: str | None = None
    operador: str | None = None


class EtiquetaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chave: str
    origem: str
    item: str
    ordem: str
    sequencia: int
    quantidade: int
    qtd_produzida: int
    qtd_hold: int
    qtd_scrap: int
    confirmada: bool
    leituras: int
    scrap_motivo: str | None
    scrap_obs: str | None
    hold_motivo: str | None
    hold_responsavel: str | None
    hold_obs: str | None
    hold_data_entrada: datetime | None
    turno: str | None
    operador: str | None
    raw_qr_content: str | None
    criado_em: datetime
    ultima_mov: datetime


class MovimentacaoCreate(BaseModel):
    chave: str
    acao: AcaoTipo
    quantidade: int
    usuario: str
    turno: str | None = None
    obs: str | None = None
    motivo: str | None = None
    responsavel: str | None = None


class MovimentacaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chave: str
    acao: AcaoTipo
    quantidade: int
    usuario: str
    turno: str | None
    obs: str | None
    motivo: str | None
    responsavel: str | None
    ts: datetime
