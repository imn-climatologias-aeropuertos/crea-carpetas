import sqlite3

from typing import Tuple, List, Optional


db_path = "./storage/data/flights.db"


def create():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS arrivals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            icao TEXT NOT NULL UNIQUE,
            alternatives TEXT NOT NULL
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            departure TEXT NOT NULL,
            arrivals TEXT NOT NULL
        );
    """
    )

    conn.commit()
    conn.close()


def insert_into_flights(*elements: str):
    elements = [element.upper() for element in elements]
    elements = tuple(elements)

    results = fetch_by_label(elements[0])

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if len(results) > 0:
        result = results[0]

        if elements[2] in result[3]:
            conn.close()
            return

        arrivals = f"{result[3]} {elements[2]}"
        arrivals = list(set(arrivals.split(" ")))
        arrivals.sort()
        arrivals = " ".join(arrivals)

        cursor.execute(
            f"""
            UPDATE flights
            SET arrivals = '{arrivals}'
            WHERE id = {result[0]}
            """
        )
    else:
        cursor.execute(
            """
            INSERT INTO flights (label, departure, arrivals)
            VALUES (?, ?, ?);
        """,
            elements,
        )
    conn.commit()
    conn.close()


def insert_into_arrivals(*elements: str):
    elements = [element.upper() for element in elements]
    elements = tuple(elements)

    results = fetch_by_icao(elements[0])

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if len(results) > 0:
        result = results[0]

        alternatives = f"{result[2]} {elements[1]}"
        alternatives = list(set(alternatives.split(" ")))
        alternatives.sort()
        alternatives = " ".join(alternatives)

        cursor.execute(
            f"""
            UPDATE arrivals
            SET alternatives = '{alternatives}'
            WHERE id = {result[0]}
            """
        )
    else:
        cursor.execute(
            """
            INSERT INTO arrivals (icao, alternatives)
            VALUES (?, ?);
        """,
            elements,
        )
    conn.commit()
    conn.close()


def insert(
    label: str,
    departure: str,
    arrival: str,
    alternatives: str,
):
    insert_into_arrivals(arrival, alternatives)
    insert_into_flights(label, departure, arrival)


def insert_many(elements: List[Tuple[str]]):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executemany(
        """
        INSERT INTO flights (label, departure, arrivals, alternatives)
        VALUES (?, ?, ?, ?);
    """,
        elements,
    )
    conn.commit()
    conn.close()


def fetch_by_label(label: str) -> List[Tuple]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = f"SELECT * FROM flights WHERE label = '{label.upper()}'"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results


def fetch_flights() -> List[Tuple]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = f"SELECT * FROM flights"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results


def fetch_by_icao(icao: str) -> List[Tuple]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = f"SELECT * FROM arrivals WHERE icao = '{icao.upper()}'"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results


def fetch_by_departure(departure: str) -> List[Tuple]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM flights WHERE departure = ?;
    """,
        (departure,),
    )
    results = cursor.fetchall()
    conn.close()
    return results
