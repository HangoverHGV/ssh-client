mod conf_manager;
use conf_manager::{CONFIG_FILE, SETTINGS_FILE, INIT_NOTIFY};
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
    println!("Waiting for configuration files to be set...");
    INIT_NOTIFY.notified().await;

    for _ in 0..10 {
        sleep(Duration::from_secs(1)).await;

        let settings_file = SETTINGS_FILE.lock().unwrap().clone();
        let configs_file = CONFIG_FILE.lock().unwrap().clone();

        println!(
            "Settings file: {:?}, Configs file: {:?}",
            settings_file, configs_file
        );
        let set_ptr = &SETTINGS_FILE as *const _;
        println!("{:?}", set_ptr);
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

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![open_terminal, get_config_paths])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
