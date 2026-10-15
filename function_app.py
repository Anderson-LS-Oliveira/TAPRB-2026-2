import logging
import azure.functions as func
import os
import pyodbc

app = func.FunctionApp()

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_chamado(myTimer: func.TimerRequest) -> None:

    host = os.getenv("HOST")
    database = os.getenv("DATABASE")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")


    #criar a conexao com o banco de dados
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
        conn = pyoodbc.connect(conn_str)

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
            logging.info(row)

        # Fecha cursor e conexão
        cursor.close()
        conn.close()

        logging.info(f"Total de registros encontrados: {len(rows)}")

    except pyodbc.Error as e:
        logging.error(f"Erro no banco de dados: {e}")
        raise