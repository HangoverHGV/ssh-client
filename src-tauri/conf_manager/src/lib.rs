use serde_json;
use std::env;
use std::fs;
use std::io::Write;
use std::path::PathBuf;
use std::sync::{Arc, Mutex};
use tokio::sync::Notify;

extern crate lazy_static;
use lazy_static::lazy_static;

lazy_static! {
    pub static ref CONF_DIR: Arc<Mutex<Option<PathBuf>>> = Arc::new(Mutex::new(None));
    pub static ref SETTINGS_FILE: Arc<Mutex<Option<PathBuf>>> = Arc::new(Mutex::new(None));
    pub static ref CONFIG_FILE: Arc<Mutex<Option<PathBuf>>> = Arc::new(Mutex::new(None));
    pub static ref INIT_NOTIFY: Arc<Notify> = Arc::new(Notify::new());
}

pub fn mkdir(relative_path: &str) -> Result<PathBuf, std::io::Error> {
    let root_path = env::current_dir()?;
    let abs_path = root_path.join(relative_path);

    if !abs_path.exists() {
        fs::create_dir_all(&abs_path)?;
    }

    Ok(abs_path)
}

pub fn create_json(conf_name: &str, data: serde_json::Value) -> std::io::Result<PathBuf> {
    let conf_dir = CONF_DIR.lock().unwrap();
    if let Some(ref dir) = *conf_dir {
        let abs_path = dir.join(conf_name);
        let mut file = fs::File::create(&abs_path)?;
        file.write_all(serde_json::to_string_pretty(&data).unwrap().as_bytes())?;
        Ok(abs_path)
    } else {
        eprintln!("Conf directory is not set");
        Err(std::io::Error::new(
            std::io::ErrorKind::NotFound,
            "Conf directory is not set",
        ))
    }
}
