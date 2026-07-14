"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-07-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ACAO_VALUES = (
    "CONFIRMACAO_PRODUCAO",
    "ENVIO_HOLD",
    "ENVIO_SCRAP",
    "HOLD_PARA_PRODUCAO",
    "HOLD_PARA_SCRAP",
    "CORRECAO",
)


def upgrade() -> None:
    acao_tipo = sa.Enum(*ACAO_VALUES, name="acao_tipo")

    op.create_table(
        "etiquetas",
        sa.Column("chave", sa.Text(), nullable=False),
        sa.Column("origem", sa.String(length=3), nullable=False),
        sa.Column("item", sa.Text(), nullable=False),
        sa.Column("ordem", sa.Text(), nullable=False),
        sa.Column("sequencia", sa.Integer(), nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column("qtd_produzida", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("qtd_hold", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("qtd_scrap", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("confirmada", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("leituras", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("scrap_motivo", sa.Text(), nullable=True),
        sa.Column("scrap_obs", sa.Text(), nullable=True),
        sa.Column("hold_motivo", sa.Text(), nullable=True),
        sa.Column("hold_responsavel", sa.Text(), nullable=True),
        sa.Column("hold_obs", sa.Text(), nullable=True),
        sa.Column("hold_data_entrada", sa.DateTime(timezone=True), nullable=True),
        sa.Column("turno", sa.Text(), nullable=True),
        sa.Column("operador", sa.Text(), nullable=True),
        sa.Column("raw_qr_content", sa.Text(), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("ultima_mov", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("chave"),
        sa.CheckConstraint("quantidade >= 0", name="ck_etiquetas_quantidade"),
        sa.CheckConstraint("qtd_produzida >= 0", name="ck_etiquetas_qtd_produzida"),
        sa.CheckConstraint("qtd_hold >= 0", name="ck_etiquetas_qtd_hold"),
        sa.CheckConstraint("qtd_scrap >= 0", name="ck_etiquetas_qtd_scrap"),
        sa.CheckConstraint("leituras BETWEEN 0 AND 3", name="ck_etiquetas_leituras"),
    )
    op.create_index("ix_etiquetas_ordem", "etiquetas", ["ordem"])
    op.create_index("ix_etiquetas_item", "etiquetas", ["item"])
    op.create_index("ix_etiquetas_origem", "etiquetas", ["origem"])

    op.create_table(
        "movimentacoes",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("chave", sa.Text(), nullable=False),
        sa.Column("acao", acao_tipo, nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column("usuario", sa.Text(), nullable=False),
        sa.Column("turno", sa.Text(), nullable=True),
        sa.Column("obs", sa.Text(), nullable=True),
        sa.Column("motivo", sa.Text(), nullable=True),
        sa.Column("responsavel", sa.Text(), nullable=True),
        sa.Column("ts", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["chave"], ["etiquetas.chave"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("quantidade >= 0", name="ck_movimentacoes_quantidade"),
    )
    op.create_index("ix_mov_chave", "movimentacoes", ["chave"])
    op.create_index("ix_mov_ts", "movimentacoes", ["ts"])
    op.create_index("ix_mov_acao", "movimentacoes", ["acao"])
    op.create_index("ix_mov_turno", "movimentacoes", ["turno"])
    op.create_index("ix_mov_usuario", "movimentacoes", ["usuario"])


def downgrade() -> None:
    op.drop_index("ix_mov_usuario", table_name="movimentacoes")
    op.drop_index("ix_mov_turno", table_name="movimentacoes")
    op.drop_index("ix_mov_acao", table_name="movimentacoes")
    op.drop_index("ix_mov_ts", table_name="movimentacoes")
    op.drop_index("ix_mov_chave", table_name="movimentacoes")
    op.drop_table("movimentacoes")

    op.drop_index("ix_etiquetas_origem", table_name="etiquetas")
    op.drop_index("ix_etiquetas_item", table_name="etiquetas")
    op.drop_index("ix_etiquetas_ordem", table_name="etiquetas")
    op.drop_table("etiquetas")
