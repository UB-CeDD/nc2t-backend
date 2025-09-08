from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ("species_management", "0007_alter_speciesherbarium_species"),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                "ALTER TABLE species_management_speciescompound ALTER COLUMN species_id TYPE varchar(22);",
                "ALTER TABLE species_management_speciessite ALTER COLUMN species_id TYPE varchar(22);",
                "ALTER TABLE species_management_speciesherbarium ALTER COLUMN species_id TYPE varchar(22);"
            ],
            reverse_sql=[
                "ALTER TABLE species_management_speciescompound ALTER COLUMN species_id TYPE integer USING species_id::integer;",
                "ALTER TABLE species_management_speciessite ALTER COLUMN species_id TYPE integer USING species_id::integer;",
                "ALTER TABLE species_management_speciesherbarium ALTER COLUMN species_id TYPE integer USING species_id::integer;"
            ]
        )
    ]

