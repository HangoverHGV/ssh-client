// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
mod db_conn;

fn main() {
    db_conn::initialize_database().expect("Failed to initialize database");
    ssh_client_lib::run()
}
