// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
mod conf_manager;
use conf_manager::{SETTINGS_FILE, CONFIG_FILE};
use serde_json::json;
use std::process::Command;

#[tauri::command]
fn open_terminal(server: &str, port: &str, key: &str) {
    println!("Opening terminal for server: {} on port: {} with key: {}", server, port, key);
    let mut command: String = String::from("ssh ") + server + " -p " + port;
    if !key.is_empty() {
        command += &(" -i ".to_owned() + key);
    }

    if cfg!(target_os = "windows") {
        Command::new("cmd")
            .args(&[
                "/C",
                "start",
                "cmd",
                "/K",
                command.as_str(),
            ])
            .spawn()
            .expect("failed to execute process");
    } else if cfg!(target_os = "macos") {
        Command::new("open")
            .arg("-a")
            .arg("Terminal")
            .spawn()
            .expect("failed to execute process");
        Command::new("sh")
            .arg("-c")
            .arg(command.as_str())
            .spawn()
            .expect("failed to execute process");
    } else if cfg!(target_os = "linux") {
        Command::new("x-terminal-emulator")
            .arg("-e")
            .arg(format!("sh -c '{}'; exec bash", command))
            .spawn()
            .expect("failed to execute process");
    }
}

#[tauri::command]
fn get_config_paths() -> serde_json::Value {
    let settings_file = SETTINGS_FILE.lock().unwrap().as_ref().unwrap().to_str().unwrap().to_string();
    let configs_file = CONFIG_FILE.lock().unwrap().as_ref().unwrap().to_str().unwrap().to_string();

    json!({
        "settings_file": settings_file,
        "configs_file": configs_file
    })
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![open_terminal])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
