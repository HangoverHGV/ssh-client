// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod conf_manager;
use serde_json::json;
use std::path::PathBuf;
use conf_manager::{CONF_DIR, SETTINGS_FILE, CONFIG_FILE};

fn main() {
    let conf_dir: Option<PathBuf> = match conf_manager::mkdir(".config") {
        Ok(conf_dir) => {
            println!("Conf directory created at: {:?}", conf_dir);
            Some(conf_dir)
        }
        Err(e) => {
            eprintln!("Error creating conf directory: {}", e);
            None
        }
    };

    if let Some(ref dir) = conf_dir {
        *CONF_DIR.lock().unwrap() = Some(dir.clone());

        let settings_path = conf_manager::create_json("settings.json", json!({})).unwrap();
        let configs_path = conf_manager::create_json("config.json", json!([])).unwrap();

        *SETTINGS_FILE.lock().unwrap() = Some(settings_path);
        *CONFIG_FILE.lock().unwrap() = Some(configs_path);

    } else {
        eprintln!("Conf directory was not created.");
    }


    ssh_client_lib::run()
}
