import logging
import os

import azure.functions as func
import pyodbc

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 * * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def extract_chamado(myTimer: func.TimerRequest) -> None:
    host = os.getenv("HOST")
    database = os.getenv("DATABASE")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")

    # Criar a conexão com o banco de dados
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={host};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        # Estabelece a conexão
        conn = pyodbc.connect(conn_str)

        logging.info("Conexão com o banco estabelecida com sucesso.")

        # Cria o cursor
        cursor = conn.cursor()

        # Executa o SELECT
        query = """
            SELECT TOP 10 *
            FROM itsm.chamado
        """

        cursor.execute(query)

        # Recupera os registros
        rows = cursor.fetchall()

        # Exibe os resultados no log
        for row in rows:
            logging.info("%s", row)

        # Fecha cursor e conexão
        cursor.close()
        conn.close()

        logging.info("Total de registros encontrados: %s", len(rows))

    except pyodbc.Error:
        logging.exception("Erro no banco de dados.")
        raise