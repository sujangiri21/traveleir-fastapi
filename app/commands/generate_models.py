import os
import subprocess
from dotenv import load_dotenv
import pymysql 

def get_matching_tables(host, port, user, password, db_name, pattern):
    """Fetches table names from the DB that match a 'LIKE' pattern."""
    connection = pymysql.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=db_name
    )
    try:
        with connection.cursor() as cursor:
            # SQL 'LIKE' uses % as a wildcard, so 'package%' matches 'package_items', etc.
            cursor.execute(f"SHOW TABLES LIKE '{pattern}'")
            tables = [row[0] for row in cursor.fetchall()]
            return ",".join(tables)
    finally:
        connection.close()

def generate_models():
    load_dotenv()

    # Database Credentials
    db_user = os.getenv("DB_USERNAME")
    db_pass = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_DATABASE")

    # Tunnel Details
    local_host = os.getenv("DB_HOST", "127.0.0.1")
    local_port = os.getenv("LOCAL_DB_PORT", "3307")

    # Tables to sync (Comma separated, no spaces)
    # Update these to match your Laravel table names
    # target_tables = "users,search_logs"
    target_tables = get_matching_tables(local_host, local_port, db_user, db_pass, db_name, "package%")

    if not all([db_user, db_pass, db_name]):
        print("❌ Error: DB credentials missing in .env")
        return

    # Construct the SQLAlchemy URI for the generator
    db_uri = f"mysql+pymysql://{db_user}:{db_pass}@{local_host}:{local_port}/{db_name}"

    # Output file
    output_file = "app/models/packages.py"  # Adjust path to your FastAPI structure

    print(f"📡 Connecting to tunnel at {local_host}:{local_port}...")
    print(f"🛠️  Generating models for: {target_tables}")

    cmd = [
        "sqlacodegen",
        db_uri,
        "--tables", target_tables,
        # "--tables", target_tables,
        "--outfile",
        output_file,
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Success! Models written to {output_file}")
    except subprocess.CalledProcessError:
        print("\n❌ Generation failed.")
        print("💡 Tip: Is your SSH tunnel running? (python tunnel.py)")
    except FileNotFoundError:
        print("❌ Error: 'sqlacodegen' not found. Run 'uv add sqlacodegen'")


if __name__ == "__main__":
    generate_models()
