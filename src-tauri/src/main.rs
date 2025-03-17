// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

#[macro_use]
extern crate lazy_static;

mod conf_manager;
use std::path::PathBuf;
use std::sync::Mutex;

lazy_static! {
    static ref CONF_DIR: Mutex<Option<PathBuf>> = Mutex::new(None);
}

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

    *CONF_DIR.lock().unwrap() = conf_dir;

    ssh_client_lib::run()
}
