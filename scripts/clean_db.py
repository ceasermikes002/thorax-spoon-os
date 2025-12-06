import os
import argparse
import sqlite3


def default_db_path() -> str:
    env_path = os.getenv("AOL_DB_PATH")
    if env_path:
        return env_path
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "aol.db")


def remove_db_file(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
        print(f"Removed DB file: {path}")
    else:
        print(f"DB file not found: {path}")


def drop_tables(path: str) -> None:
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS events")
    cur.execute("DROP TABLE IF EXISTS contracts")
    conn.commit()
    try:
        cur.execute("VACUUM")
        conn.commit()
    except Exception:
        pass
    conn.close()
    print(f"Dropped tables in DB: {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["file", "drop"], default="file")
    parser.add_argument("--db", dest="db_path", default=default_db_path())
    args = parser.parse_args()

    if args.mode == "file":
        remove_db_file(args.db_path)
    else:
        drop_tables(args.db_path)


if __name__ == "__main__":
    main()

