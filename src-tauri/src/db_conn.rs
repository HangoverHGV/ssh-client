use rusqlite::{params, Connection, Result};

pub fn initialize_database() -> Result<()> {
    let conn = Connection::open("db.sqlite")?;
    conn.execute(
        "CREATE TABLE IF NOT EXISTS configs (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            hostname TEXT NOT NULL,
            port TEXT NOT NULL,
            key TEXT
        )",
        params![],
    )?;
    conn.execute(
        "CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            api_key TEXT NOT NULL,
            server TEXT NOT NULL,
            sync BOOLEAN NOT NULL
        )",
        params![],
    )?;
    Ok(())
}

pub fn insert_config(name: &str, hostname: &str, port: &str, key: &str) -> Result<()> {
    let conn = Connection::open("db.sqlite")?;
    conn.execute(
        "INSERT INTO configs (name, hostname, port, key) VALUES (?, ?, ?, ?)",
        params![name, hostname, port, key],
    )?;
    Ok(())
}

pub fn insert_settings(api_key: &str, server: &str, sync: bool) -> Result<()> {
    let conn = Connection::open("db.sqlite")?;
    conn.execute(
        "INSERT INTO settings (api_key, server, sync) VALUES (?, ?, ?)",
        params![api_key, server, sync],
    )?;
    Ok(())
}

pub fn get_configs() -> Result<Vec<(i64, String, String, String, String)>> {
    let conn = Connection::open("db.sqlite")?;
    let mut stmt = conn.prepare("SELECT id, name, hostname, port, key FROM configs")?;
    let rows = stmt.query_map(params![], |row| {
        Ok((
            row.get(0)?,
            row.get(1)?,
            row.get(2)?,
            row.get(3)?,
            row.get(4)?,
        ))
    })?;
    let mut configs = Vec::new();
    for row in rows {
        configs.push(row?);
    }
    Ok(configs)
}

pub fn get_settings() -> Result<(String, String, bool)> {
    let conn = Connection::open("db.sqlite")?;
    let mut stmt = conn.prepare("SELECT api_key, server, sync FROM settings")?;
    let mut rows = stmt.query_map(params![], |row| {
        Ok((
            row.get(0)?,
            row.get(1)?,
            row.get(2)?,
        ))
    })?;
    let row = rows.next().unwrap()?;
    Ok(row)
}
