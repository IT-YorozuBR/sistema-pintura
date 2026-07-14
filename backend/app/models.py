import enum
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AcaoTipo(str, enum.Enum):
    CONFIRMACAO_PRODUCAO = "CONFIRMACAO_PRODUCAO"
    ENVIO_HOLD = "ENVIO_HOLD"
    ENVIO_SCRAP = "ENVIO_SCRAP"
    HOLD_PARA_PRODUCAO = "HOLD_PARA_PRODUCAO"
    HOLD_PARA_SCRAP = "HOLD_PARA_SCRAP"
    CORRECAO = "CORRECAO"


class Etiqueta(Base):
    __tablename__ = "etiquetas"
    __table_args__ = (
        CheckConstraint("quantidade >= 0", name="ck_etiquetas_quantidade"),
        CheckConstraint("qtd_produzida >= 0", name="ck_etiquetas_qtd_produzida"),
        CheckConstraint("qtd_hold >= 0", name="ck_etiquetas_qtd_hold"),
        CheckConstraint("qtd_scrap >= 0", name="ck_etiquetas_qtd_scrap"),
        CheckConstraint("leituras BETWEEN 0 AND 3", name="ck_etiquetas_leituras"),
    )

    chave: Mapped[str] = mapped_column(Text, primary_key=True)
    origem: Mapped[str] = mapped_column(String(3), nullable=False)
    item: Mapped[str] = mapped_column(Text, nullable=False)
    ordem: Mapped[str] = mapped_column(Text, nullable=False)
    sequencia: Mapped[int] = mapped_column(Integer, nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    qtd_produzida: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    qtd_hold: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    qtd_scrap: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    confirmada: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    leituras: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    scrap_motivo: Mapped[str | None] = mapped_column(Text)
    scrap_obs: Mapped[str | None] = mapped_column(Text)
    hold_motivo: Mapped[str | None] = mapped_column(Text)
    hold_responsavel: Mapped[str | None] = mapped_column(Text)
    hold_obs: Mapped[str | None] = mapped_column(Text)
    hold_data_entrada: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    turno: Mapped[str | None] = mapped_column(Text)
    operador: Mapped[str | None] = mapped_column(Text)
    raw_qr_content: Mapped[str | None] = mapped_column(Text)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ultima_mov: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    movimentacoes: Mapped[list["Movimentacao"]] = relationship(
        back_populates="etiqueta", cascade="all, delete-orphan"
    )


class Movimentacao(Base):
    __tablename__ = "movimentacoes"
    __table_args__ = (CheckConstraint("quantidade >= 0", name="ck_movimentacoes_quantidade"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    chave: Mapped[str] = mapped_column(ForeignKey("etiquetas.chave", ondelete="CASCADE"), nullable=False)
    acao: Mapped[AcaoTipo] = mapped_column(
        Enum(AcaoTipo, name="acao_tipo", native_enum=True), nullable=False
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    usuario: Mapped[str] = mapped_column(Text, nullable=False)
    turno: Mapped[str | None] = mapped_column(Text)
    obs: Mapped[str | None] = mapped_column(Text)
    motivo: Mapped[str | None] = mapped_column(Text)
    responsavel: Mapped[str | None] = mapped_column(Text)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    etiqueta: Mapped["Etiqueta"] = relationship(back_populates="movimentacoes")
