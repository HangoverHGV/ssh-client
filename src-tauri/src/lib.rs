use std::path::PathBuf;
use conf_manager;
use serde_json::json;
use std::process::Command;
use tokio::time::{sleep, Duration};

#[tauri::command]
fn open_terminal(server: &str, port: &str, key: &str) {
    println!(
        "Opening terminal for server: {} on port: {} with key: {}",
        server, port, key
    );
    let mut command: String = String::from("ssh ") + server + " -p " + port;
    if !key.is_empty() {
        command += &(" -i ".to_owned() + key);
    }

    if cfg!(target_os = "windows") {
        Command::new("cmd")
            .args(&["/C", "start", "cmd", "/K", command.as_str()])
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
async fn get_config_paths() -> serde_json::Value {

    for _ in 0..10 {
        sleep(Duration::from_secs(1)).await;

        let settings_file = conf_manager::SETTINGS_FILE.lock().unwrap().clone();
        let configs_file = conf_manager::CONFIG_FILE.lock().unwrap().clone();

        if let (Some(settings_path), Some(configs_path)) =
            (settings_file.as_ref(), configs_file.as_ref())
        {
            return json!({
                "settings_file": settings_path.to_str().unwrap(),
                "configs_file": configs_path.to_str().unwrap()
            });
        }
    }

    json!({
        "error": "Configuration files are not set"
    })
}

#[tauri::command]
async fn get_json_configs(config_type: &str) -> Result<serde_json::Value, String> {
    println!("{}", config_type);

    if config_type != "settings" && config_type != "configs" {
        return Err("Invalid configuration type".to_string());
    }
    let file_path = if config_type == "settings" {
        conf_manager::SETTINGS_FILE.lock().unwrap().clone()
    } else {
        conf_manager::CONFIG_FILE.lock().unwrap().clone()
    };

    let file_content = match file_path {
        Some(file) => {
            let content = std::fs::read_to_string(file).map_err(|e| e.to_string())?;
            serde_json::from_str(&content).map_err(|e| e.to_string())?
        }
        None => {
            return Err("Config file is not set".to_string());
        }
    };
    Ok(file_content)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![open_terminal, get_config_paths, get_json_configs])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
