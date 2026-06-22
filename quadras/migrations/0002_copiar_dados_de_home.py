from django.db import migrations


def copiar_quadras(apps, schema_editor):
    """
    Copia as quadras que já existiam na tabela antiga (app home)
    para a nova tabela do app quadras, preservando o id original.
    """
    QuadraAntiga = apps.get_model('home', 'Quadra')
    QuadraNova = apps.get_model('quadras', 'Quadra')

    # 'home.Quadra' já não existe mais como model Python depois que
    # removemos a classe, mas a tabela 'home_quadra' ainda existe no
    # banco neste ponto da migração (o DeleteModel só roda depois).
    # Por isso acessamos via SQL direto, que é mais seguro aqui.
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, tipo, preco_hora, disponivel FROM home_quadra")
        linhas = cursor.fetchall()

    for id_antigo, nome, tipo, preco_hora, disponivel in linhas:
        QuadraNova.objects.using(schema_editor.connection.alias).create(
            id=id_antigo,
            nome=nome,
            tipo=tipo,
            preco_hora=preco_hora,
            disponivel=bool(disponivel),
        )


def reverter(apps, schema_editor):
    QuadraNova = apps.get_model('quadras', 'Quadra')
    QuadraNova.objects.using(schema_editor.connection.alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('quadras', '0001_initial'),
        ('home', '0003_alter_quadra_id_alter_usuarios_id'),
    ]

    operations = [
        migrations.RunPython(copiar_quadras, reverter),
    ]
