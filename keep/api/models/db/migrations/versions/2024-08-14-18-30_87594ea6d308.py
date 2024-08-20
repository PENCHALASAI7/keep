"""add rules-related fields to the incident

Revision ID: 87594ea6d308
Revises: 0832e0d9889a
Create Date: 2024-08-14 18:30:09.052273

"""

import sqlalchemy as sa
import sqlalchemy_utils
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "87594ea6d308"
down_revision = "0832e0d9889a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("incident", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "rule_id",
                sqlalchemy_utils.types.uuid.UUIDType(binary=False),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "rule_fingerprint", sqlmodel.sql.sqltypes.AutoString(), nullable=False,
                default="", server_default=""
            )
        )
        batch_op.add_column(
            sa.Column("severity", sa.Integer(), nullable=False, server_default=sa.text("(5)"), default=5)
        )

        batch_op.create_foreign_key(
            "incident_rule_id_fk", "rule", ["rule_id"], ["id"], ondelete="CASCADE"
        )

    with op.batch_alter_table("rule", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "require_approve", sa.Boolean(), nullable=False,
                server_default=sa.text("(FALSE)"),
            )
        )

    op.drop_table("alerttogroup")
    op.drop_table("group")

    with op.batch_alter_table("alerttoincident", schema=None) as batch_op:
        batch_op.add_column(sa.Column("timestamp", sa.DateTime(), nullable=False,
                                      server_default=sa.func.current_timestamp()))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("incident", schema=None) as batch_op:
        batch_op.drop_constraint("incident_rule_id_fk", type_="foreignkey")
        batch_op.drop_column("rule_fingerprint")
        batch_op.drop_column("rule_id")
        batch_op.drop_column("severity")

    with op.batch_alter_table("rule", schema=None) as batch_op:
        batch_op.drop_column("require_approve")

    with op.batch_alter_table("alerttoincident", schema=None) as batch_op:
        batch_op.drop_column("timestamp")

    op.create_table(
        "group",
        sa.Column("rule_id", sa.VARCHAR(length=32), nullable=True),
        sa.Column("id", sa.VARCHAR(length=32), nullable=False),
        sa.Column("tenant_id", sa.VARCHAR(length=32), nullable=False),
        sa.Column("creation_time", sa.DATETIME(), nullable=False),
        sa.Column("group_fingerprint", sa.VARCHAR(length=32), nullable=False),
        sa.ForeignKeyConstraint(["rule_id"], ["rule.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "alerttogroup",
        sa.Column("group_id", sa.CHAR(length=32), nullable=False),
        sa.Column("tenant_id", sa.VARCHAR(length=32), nullable=False),
        sa.Column("timestamp", sa.DATETIME(), nullable=False),
        sa.Column("alert_id", sa.VARCHAR(length=32), nullable=False),
        sa.ForeignKeyConstraint(
            ["alert_id"],
            ["alert.id"],
        ),
        sa.ForeignKeyConstraint(["group_id"], ["group.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("group_id", "alert_id"),
    )