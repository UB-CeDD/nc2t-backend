from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ("species_management", "0008_alter_species_id_to_varchar"),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE species_management_species_references ALTER COLUMN species_id TYPE varchar(22);",
            reverse_sql="ALTER TABLE species_management_species_references ALTER COLUMN species_id TYPE integer USING species_id::integer;"
        )
    ]

