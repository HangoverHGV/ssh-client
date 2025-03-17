use std::fs;
use std::path::{Path, PathBuf};
use std::env;
use std::io::Write;
use serde_json::json;
use std::sync::Mutex;

extern crate lazy_static;
use lazy_static::lazy_static;

lazy_static! {
    static ref CONF_DIR: Mutex<Option<PathBuf>> = Mutex::new(None);
}

pub fn mkdir(relative_path: &str) -> Result<PathBuf, std::io::Error> {
    let root_path = env::current_dir()?;
    let abs_path = root_path.join(relative_path);

    if !abs_path.exists() {
        fs::create_dir_all(&abs_path)?;
    }

    Ok(abs_path)
}

pub fn create_json(conf_name: &str, data: serde_json::Value) -> std::io::Result<()> {
    let conf_dir = CONF_DIR.lock().unwrap();
    if let Some(ref dir) = *conf_dir {
        let abs_path = dir.join(conf_name);
        let mut file = fs::File::create(abs_path)?;
        file.write_all(json::to_string_pretty(&data).unwrap().as_bytes())?;
    } else {
        eprintln!("Conf directory is not set");
    }

    Ok(())
}